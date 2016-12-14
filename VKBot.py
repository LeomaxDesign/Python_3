import datetime
import vk
import weather
import time

# Авторезация сессии с помощью access token
session = vk.Session('b71d75339c5d0afe759c39d58521c6d431cd617e525f230a77880d699e9202b3beb5ff37ab3f21ec0e757')

# Объект api
api = vk.API(session)

while (True):
    try:
        # Список последнх сообщения
        messages = api.messages.get()
    except:
        continue
    # Перебор каждого сообщение
    for m in messages[1:]:
        # Если сообщение не прочитано
        if m['read_state'] == 0:

            # id сообщения
            uid = m['uid']

            # Имя пользователя
            user_name = api.users.get(user_ids=uid)[0]['first_name']
            try:
                # id чата
                chat_id = m['chat_id']
            except:
                chat_id = 0
            if chat_id > 0:
                uid = 0

            # Форматированный текст сообщения
            text = m['body']
            text = text.lower()
            text = text.replace(' ', '')

            # Строка с датой и временем
            date_time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

            # Команды
            # Приветствие
            if text == 'привет':
                api.messages.send(uid=uid, chat_id=chat_id, message=date_time + '\n\nЗдравствуй, ' + user_name + '!✋')
            # Погода
            if text[0:7:1] == "погода в":
                api.messages.send(uid=uid, chat_id=chat_id, message=str(date_time + '\n\nЗдравствуй,' + weather.weather_now(text)))
            # Отмечает сообщение как прочитанное
            api.messages.markAsRead(message_ids=m['mid'])
    # Время ожидания 3 секунды
    time.sleep(3)