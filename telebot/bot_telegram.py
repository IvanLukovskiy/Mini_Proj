from aiogram.utils import executor
from create_bot import dp # импортируем диспетчер
from handlers import client, admin, other
from data_base import sql_db


async def on_startup(_):
    print('Бот вышел в онлайн')
    sql_db.sql_start() # запускаем одноименную ф-цию из указанного файла

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp) # Соблюдать такую последовательность, т.к. у нас там пустой Хэндлер, кот. нужно регистр-ть Последним!


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # чтобы бот не отвечал на сообщение, полученные в НЕонлайне статусе

