"""Import modules"""
import re
import telebot
import requests


TOKEN = '1222076034:AAGb6JnhqymBqoRu2r4tFAY7IqJUgl75SYo'
bot = telebot.TeleBot(TOKEN)


def getWeather(city):
    if bool(re.search('[а-яА-Я]', city)):
        return 'Бот не может прочесть Ваше сообщение потому что оно написано не на латинице'
    else:
        url = 'https://api.openweathermap.org/data/2.5/weather?q='+city + \
            '&units=metric&lang=ru&appid=e26fbcf1d6e728a5a2bd51c9a23b2dcd'
        res = requests.get(url)
        data = res.json()
        if data['cod'] == 200:
            weather = 'Погода в '+city+': ' + \
                data['weather'][0]['description'].capitalize()+'.'
            weather += ' Температура: ' + \
                str(data['main']['temp'])+'C. Ощущается как: ' + \
                str(data['main']['feels_like'])+'C.'
            weather += ' Скорость ветра: '+str(data['wind']['speed'])+' м/с.'
            weather += ' Давление: '+str(data['main']['pressure'])+'HPa.'
            weather += ' Видимость: '+str(data['visibility'])+'м.'
            weather += ' Влажность: '+str(data['main']['humidity'])+'%'
            return weather
        else:
            return 'Погода в этом городе не найдена'


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.chat.id, text='Введите город для поиска погоды')


@bot.message_handler(content_types=["text"])
def start(message):
    if len(message.text) > 0:
        bot.send_message(message.chat.id, text=getWeather(message.text))
        bot.send_message(
            message.chat.id, text='Введите город для поиска погоды')
    else:
        bot.send_message(message.chat.id, text='Извините, я Вас не понял.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
