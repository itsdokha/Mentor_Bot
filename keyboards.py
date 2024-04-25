from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_butt = ReplyKeyboardMarkup(resize_keyboard=True)
start_butt.add(
    KeyboardButton('Зарегистрироваться'),
    KeyboardButton('Меню'),
    KeyboardButton('Рандомный совет')
)

rank_butt = ReplyKeyboardMarkup(resize_keyboard=True)
rank_butt.add(
    KeyboardButton('Директор'),
    KeyboardButton('Управляющий'),
    KeyboardButton('Ментор'),
    KeyboardButton('Менти')
)

direction_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
direction_keyboard.add(
    KeyboardButton('Лектор'),
    KeyboardButton('Семинарист'),
    KeyboardButton('Ассистент')
)

director_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
director_keyboard.add(
    KeyboardButton('Читать предложения'),
    KeyboardButton('Заказы'),
    KeyboardButton('Отслеживать выполнение плана')
)

manager_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
manager_keyboard.add(
    KeyboardButton('Оформить заказ'),
    KeyboardButton('Отслеживать выполнение плана'),
    KeyboardButton('Формирование пар'),
    KeyboardButton('Назначить совещание'),
    KeyboardButton('Читать предложения')
)

mentor_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
mentor_keyboard.add(
    KeyboardButton('Обновить'),
    KeyboardButton('Выбор нового менти'),
    KeyboardButton('Назначить задачу'),
    KeyboardButton('Назначить встречу'),
    KeyboardButton('Расписание'),
    KeyboardButton('Отслеживать менти'),
    KeyboardButton('Профиль')
)

menti_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menti_keyboard.add(
    KeyboardButton('Обновить'),
    KeyboardButton('Назначенные задачи'),
    KeyboardButton('Назначенные встречи'),
    KeyboardButton('Написать ментору'),
    KeyboardButton('Профиль'),
    KeyboardButton('Часто задаваемые вопросы'),
    KeyboardButton('Рандомный совет')
)

orders_keyboard = InlineKeyboardMarkup()
orders_keyboard.add(
    InlineKeyboardButton('Вернуться', callback_data='back'),
    InlineKeyboardButton('Вернуться', callback_data='delete_order')
)

update_keyboard = InlineKeyboardMarkup()
update_keyboard.add(
    InlineKeyboardButton('Вернуться', callback_data='back'),
    InlineKeyboardButton('Написать предложение', callback_data='write_review'),
    InlineKeyboardButton('Завершить сеанс 👨🏿‍🤝‍👨🏿', callback_data='delete_account')
)

tasks_keyboard = InlineKeyboardMarkup()
tasks_keyboard.add(
    InlineKeyboardButton('Вернуться', callback_data='back'),
    InlineKeyboardButton('Завершить задачу', callback_data='make_task')
)

profile_inline = InlineKeyboardMarkup()
profile_inline.add(
    InlineKeyboardButton('Вернуться', callback_data='back'),
    InlineKeyboardButton('Изменить данные', callback_data='edit_profile')
)

answer_inline = InlineKeyboardMarkup()
answer_inline.add(
    InlineKeyboardButton('Ответить ментичучоку', callback_data='answer_menti')
)
