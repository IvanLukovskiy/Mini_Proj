import sqlite3 as sq
from create_bot import dp, bot

def sql_start(): # Создаём базу данных/ подключаемся к существкющей
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)') # TEXT в img, т.к. мы изначально сохраняем при внесении фотки админом именно ID фотографии, а не само фото
    base.commit() # сохраняем изменения

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall(): # метод "fetchall()" - выгружает всё в виде списка
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


