from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #, ReplyKeyboardRemove - ситуативна. например, для исчезновения клавиатуры полностью после первого нажатия на неё пользователем

b1 = KeyboardButton('/Режим_Работы') # переменные - кнопки
b2 = KeyboardButton('/Адрес') # переменные - кнопки
b3 = KeyboardButton('/Меню') # переменные - кнопки
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Отправить где я', request_location=True)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True) # замещает обычную клавиатуру на ту, которую мы задаем

kb_client.add(b1).add(b2).add(b3).row(b4, b5)

#kb_client.row(b1, b2, b3) # метод "row()" размещает Все перечисленные в нем кнопки в строку
#kb_client.add(b1).add(b2).insert(b3) # метод "insert()" размещает несколько кнопок на одной строке
#kb_client.add(b1).add(b2).add(b3) # добавляем кнопкт через метод "add()" - добавляет каждую кнопку с новой строки в указанном порядке