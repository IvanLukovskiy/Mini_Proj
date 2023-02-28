from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # класс "MemoryStorage" позволяет хранить данные в оперативной памяти (для Машины Состояний). Он самый простой, т.к. если бот уйдет в Оффлайн, то и данные сразу пропадут из памяти. Поэтому подходит для тех данных, которые сразу попадают в обработку (наш случай)

storage = MemoryStorage()

bot = Bot(token=os.getenv('Token'))  # создаем Экземпляры бота
dp = Dispatcher(bot, storage=storage)  # создаем Экземпляры бота
