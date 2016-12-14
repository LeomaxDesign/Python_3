import pyowm

import datetime

# инициализация библиотеки API ключом
owm = pyowm.OWM('fff85453964a1692a3628cdef0492d7c')

# функция, которая возвращает все данные о погоде
def weather_now(text):

    # определяем город
    if text[7:13:1] == 'ростов':
        city = 'Rostov-on-Don, RU'
    if text[7:12:1] == 'москв':
        city = 'Moscow, RU'
    if text[7:12:1] == 'санкт':
        city = 'Saint Petersburg, RU'
    if text[7:13:1] == 'ереван':
        city = 'Yerevan, AM'
    if text[7:11:1] == 'киев':
        city = 'Kiev, UA'

    try:
        observation = owm.weather_at_place(city)
    except:
        return 'Данный город не поддерживается.'

    # погодные данные
    weather = observation.get_weather()

    # данные местоположения
    location = observation.get_location()

    #  словарь для перевода названия городов
    translate_city = {'Rostov-na-Donu': 'Ростов-на-Дону', 'Moscow': 'Москва', 'Saint Petersburg': 'Санкт-Петербург',
                       'Yerevan': 'Ереван', 'Kiev': 'Киев'}

    # функция которая определяет температуру днём и ночью
    def temperature(string):
        f_observation = owm.daily_forecast(city)
        f_weather = f_observation.get_weather_at(
            datetime.datetime(datetime.date.today().year, datetime.date.today().month,
                              datetime.date.today().day, 12, 00, 00))
        return str(round(f_weather.get_temperature('celsius')[string]))

    # функция, которая определяет направление ветра
    def direction_wind():
        try:
            deg = weather.get_wind()['deg']
        except:
            return ''
        if deg > 337.5:
            return 'северный, '

        if deg <= 22.5:
            return 'северный, '

        if 22.5 < deg <= 67.5:
            return 'северо-восточный, '

        if 67.5 < deg <= 112.5:
            return 'восточный, '

        if 112.5 < deg <= 157.5:
            return 'юго-восточный, '

        if 157.5 < deg <= 202.5:
            return 'южный, '

        if 202.5 < deg <= 247.5:
            return 'юго-западный, '

        if 247.5 < deg <= 292.5:
            return 'западный, '

        if 292.5 < deg <= 337.5:
            return 'северо-западный, '

    # функция, которая возвращает погодные явления
    def status():
        icon = weather.get_weather_icon_name()

        if icon == '01d' or icon == '01n':
            return 'ясно'
        if icon == '02d' or icon == '02n':
            return 'малооблачно'
        if icon == '03d' or icon == '03n':
            return 'облачно'
        if icon == '04d' or icon == '04n':
            return 'пасмурно'
        if icon == '09d' or icon == '09n':
            return 'небольной дождь'
        if icon == '10d' or icon == '10n':
            return 'дождь'
        if icon == '11d' or icon == '11n':
            return 'гроза'
        if icon == '13d' or icon == '13n':
            return 'снег'
        if icon == '50d' or icon == '50n':
            return 'туман'
    try:
        return str('Погода в городе ' + translate_city[location.get_name()] + ' на сегодня:' +
            '\n' + '\nСейчас: ' + status() +
            '\nТемпература: ' + str(round(weather.get_temperature('celsius')['temp'])) + '°C' +
            '\nВетер: ' + direction_wind() + str(round(weather.get_wind()['speed'], 1)) + ' м/c ' +
            '\nДавление: ' + str(round(weather.get_pressure()['press'] * 0.750062)) + ' мм рт. ст.' +
            '\nВлажность: ' + str(weather.get_humidity()) + ' %' +
            '\n' +
            '\nТемпература днём: ' + temperature('day') + '°C' +
            '\nТемпература ночью: ' + temperature('night') + '°C')
    except:
        return 'Прогноз погоды в данное время недоступен.'