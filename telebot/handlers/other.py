from aiogram import types, Dispatcher
from create_bot import dp
import json
import string

# @dp.message_handler()  # Пустой Хэндлер долэен быть внизу, если бот ОДНОфайловый!!!! либо примет в себя любую команду и просто не пропустит дальше +++декоратор - обозначает событие, когда в наш чат кто-то что-то пишет
async def echo_send(message: types.Message):  # (Параметр : Аннотация) ассинхронная ф-ция, позволяющая выполнять что-то ещё во время работы других ф-ций (в промежутках паузных)
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))):
        await message.reply('Ты чего? Маты запрещены!')
        await message.delete()          # получаем множество очищенных от маскировки ''pure'' слов и проверяем (перекрестная проверка) со множеством в файле ценза на наличие совпадений

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)

    # await message.answer('Приветсвтую! Как дела? Что кушал?')  # этот Метод (.answer()) текстом, указанным внутри метода
    # await message.reply(message.text) # то же, но ответом на сообщение (подтягивает сообщение пользователя, на которое отвечает)
    # await bot.send_message(message.from_user.id, message.text) # отправляет сообщение в личку, НО если ранее пользователь написал боту лично (Бот не может написать пользователю Первым)

