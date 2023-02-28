from aiogram.dispatcher.filters import Text
import equals as equals
from aiogram.dispatcher import FSMContext # для аннотации типов в хэндлерах
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sql_db
from keybords import admin_kb

ID = None

class FSMAdmin(StatesGroup):
    photo = State() # класс "State()" нужен для переходов между этими 4-мя состояниями. Сам переход пропишем в Хэндлере
    name = State()
    description = State()
    price = State()

# Получаем ID текущего модератора. Писать нужно именно в ЧАТ, а не боту!!!!!!
# @dp.message_handler(commands=['moderator']), is_chat_admin=True) #Проверка на модератора, при вводе данной команды
async def make_changes_command(message : types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Слушаю Вас', reply_markup=admin_kb.button_case_admin) # + добавляем кнопки из файла "admin_kb"
    await message.delete() #Удаляем сообщение из группового чата

# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID: # Диалог начнется только при совпадении ID с админским
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

#Выход из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*") # параметр "ignore_case", чтобы не зависело от написания
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state() # "state.get_state()" - получаем состояние бота
        if current_state is None: # т.е. если бот НЕ в Машинном состоянии - ничего не вернется = не сработает
            return
        await state.finish()
        await message.reply('ОК')


# Ловим первый ответ и пишем в Словарь машины
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id # в Словарь указанному ключу присваеваем НЕ фото, а файл ID. Т.е пользователю потом будет отправлено фото посредством IDшника этой фотки
        await FSMAdmin.next() #  бот ждет следующего ответа на "name = State()" сверху
        await message.reply('Теперь введи название')

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text # ключу "Name" присвоится введенный пользователем текст
        await FSMAdmin.next()
        await message.reply('Введи описание')

# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text # ключу "description" присвоится введенный пользователем текст
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')

# Ловим четвертый (Последний) ответ
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text) # ключу "description" присвоится введенный пользователем текст

        await sql_db.sql_add_command(state) # ф-ция из файла "sql_db"
        await state.finish() # после этой команды бот Выйдет из машины состояний и очистит весь словарь, Поэтому обработку данных нужно произвести ДО этой команды




def register_handlers_admin(dp : Dispatcher): # регистрируем наши Хэндлеры (в ТОЙ же последовательности, что и в коде), т.к. перед ф-циями они нам не нужны, т.к. мы их будет сообщать в другой файл
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands='moderator', is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')


