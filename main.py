import telebot
from telebot import types

from API import getExchangeValue, saveImg

bot = telebot.TeleBot('6245867896:AAEpE3fdvmkbnBtz5cbg8PsZIDZv6GQPLr8')
flag_reverse = False
flag_value = "USD"
flag_language = "ru"


def introduction(user, key):
    dict = {"ru": ["Юань-Рубль", "Доллар-Рубль", "Чугун-Рубль", "Сталь-Рубль"],
            "en": ["Yuan-Ruble", "Dollar-Ruble", "Chugun-Ruble", "Steel-Ruble"]}
    markup = types.ReplyKeyboardMarkup(row_width=3)
    btn_yuan = types.KeyboardButton(dict[key][0])
    btn_dollar = types.KeyboardButton(dict[key][1])
    btn_metal1 = types.KeyboardButton(dict[key][2])
    btn_metal2 = types.KeyboardButton(dict[key][3])

    markup.add(btn_yuan, btn_dollar, btn_metal1, btn_metal2)
    setstring = {"ru": """
               Добрый день, в сами бот для работы с самой свежей информацией по курсам валют.
Выберите интересующий вас курс:

Юань - Рубль
Доллар - Рубль
Чугун - Рубль
Сталь - Рубль
               """,
                 "en": """
                Good afternoon, the bot itself is working with the latest information on exchange rates.
Select the rate you are interested in:

Yuan - Ruble 
Dollar - Ruble
Chugun - Ruble
Steel - Ruble
                     """}
    bot.send_message(user.from_user.id, setstring[key], reply_markup=markup)


def result_reverse() -> str:
    if flag_language == "en":
        return f"1 {flag_value} now coast - " + str(getExchangeValue(flag_value)) + " rub."
    else:
        return f"1 {flag_value} сейчас стоит - " + str(getExchangeValue(flag_value)) + " руб."


def to_float(text):
    try:
        return float(text)
    except:
        return str(text)


def to_reverse(key):
    pass


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_en = types.KeyboardButton("en")
    btn_ru = types.KeyboardButton("ru")
    markup.add(btn_ru)
    markup.add(btn_en)
    bot.send_message(message.from_user.id, "Chose your language / Выберите свой язык ", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == 'photo')
def get_user_photo(message):
    bot.send_photo(message.chat.id, open("foto.png", "rb"))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    key = to_float(message.text)
    global flag_language
    if isinstance(key, str):
        dict = {"ru": ["Юань-Рубль", "Доллар-Рубль", "Металлы-Рубль", "Чугун-Рубль", "Сталь-Рубль"],
                "en": ["Yuan-Ruble", "Dollar-Ruble", "Chugun-Ruble", "Steel-Ruble"]}
        dict_value = {"Юань-Рубль": "CNY", "Yuan-Ruble": "CNY", "Доллар-Рубль": "USD", "Dollar-Ruble": "USD",
                      "Чугун-Рубль": "CGN", "Chugun-Ruble": "CGN", "Сталь-Рубль": "STL", "Steel-Ruble": "STL"}
        if key in dict[flag_language]:
            global flag_value
            flag_value = dict_value[key]
            bot.send_message(message.from_user.id, result_reverse())
            saveImg(flag_value, "foto")
            bot.send_photo(message.chat.id, open("foto.png", "rb"))
        elif key == "en" or key == "ru":
            flag_language = key
            introduction(message, key)

    elif isinstance(key, float) and flag_reverse:
        to_reverse(key)
    else:
        bot.send_message(message.from_user.id,
                         message.text + "Я сожалею, но такой операции на данный момент не существует" +
                         " Вы можете написать сообщение на почту levshin01bk.ru ")


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)
    pass
