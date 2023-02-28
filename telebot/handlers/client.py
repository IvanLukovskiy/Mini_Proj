from aiogram import types, Dispatcher # для Аннтоаций типов
from create_bot import dp, bot
from keybords import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sql_db

# @dp.message_handler(commands=['start', 'help']) # Декораторы нужны в случае написания ОДНОфайлового бота!!!
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await messae.reply("Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Pitska_BobBot")

# @dp.message_handler(commands=['Режим_работы']) # Декораторы нужны в случае написания ОДНОфайлового бота!!!
async def pizza_rej_rab_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')

# @dp.message_handler(commands=['Адрес']) # Декораторы нужны в случае написания ОДНОфайлового бота!!!
async def pizza_adress_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'ул. Заводская 25', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message : types.Message):
    await sql_db.sql_read(message)

def register_handlers_client(dp : Dispatcher): # регистрируем наши Хэндлеры
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_rej_rab_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_adress_command, commands=['Адрес'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])