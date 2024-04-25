import datetime

import telebot
from telebot.types import ReplyKeyboardRemove

from dbmanager import DB
from gpt import ask_gpt
from keyboards import start_butt, rank_butt, director_keyboard, menti_keyboard, mentor_keyboard, manager_keyboard, \
    profile_inline, direction_keyboard, update_keyboard, tasks_keyboard, answer_inline

bot = telebot.TeleBot('6041193122:AAFCuyJnpGt4CYVdBYeVJlnMkbrOhdfyPgU')
temp = {}

db = DB()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет.', reply_markup=start_butt)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Зарегистрироваться':
        if db.get_user(message.chat.id):
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы.')
            return

        bot.send_message(message.chat.id, 'Отправьте ФИО.')
        bot.register_next_step_handler(message, fio)

    if message.text == 'Меню':
        user = db.get_user(message.chat.id)
        if not user:
            bot.send_message(message.chat.id, 'Необходима регистрация.')
            return

        if user['position'] == 'director':
            bot.send_message(message.chat.id, 'Меню', reply_markup=director_keyboard)

        if user['position'] == 'Manager':
            bot.send_message(message.chat.id, 'Меню', reply_markup=manager_keyboard)

        if user['position'] == 'Mentor':
            bot.send_message(message.chat.id, 'Меню', reply_markup=mentor_keyboard)

        if user['position'] == 'Menti':
            bot.send_message(message.chat.id, 'Меню', reply_markup=menti_keyboard)

    if message.text == 'Профиль':
        user = db.get_user(message.chat.id)
        bot.send_message(message.chat.id, str(user), reply_markup=profile_inline)

    if message.text == 'Рандомный совет':
        ask_gpt(message, 'Напиши короткий совет для менторов', bot)

    if message.text == 'Часто задаваемые вопросы':
        bot.send_message(message.chat.id, 'Калай укочон')

    if message.text == 'Выбор нового менти':
        free_mentis = db.get_free_mentis()
        mentis = ''
        for menti in free_mentis:
            mentis += f"`{menti['id']}` / {menti['fio']} / {menti['age']} / {menti['direction']}\n"

        bot.send_message(message.chat.id, mentis + '\nВведите айди менти котого хотите выбрать',
                         reply_markup=ReplyKeyboardRemove(), parse_mode='markdown')
        bot.register_next_step_handler(message, get_new_menti)

    if message.text == 'Формирование пар':
        wanting_mentis = db.get_wantings()
        wantings = ''
        for mentor in wanting_mentis:
            wantings += f"[{mentor} / {db.get_user(mentor)['fio']}] хочет нанять "
            for user_id in wanting_mentis[mentor]:
                user = db.get_user(user_id)
                wantings += f"& [{user_id} / {user['fio']}]"
            wantings += '\n'

        bot.send_message(message.chat.id, wantings + '\nВведите айди ментора и менти через пробел')
        bot.register_next_step_handler(message, add_pair)

    if message.text == 'Оформить заказ':
        bot.send_message(message.chat.id, 'Напишите текст заказа')
        bot.register_next_step_handler(message, make_order)

    if message.text == 'Заказы':
        orders = db.get_orders()
        ords = ''
        for idx, order in enumerate(orders, start=1):
            ords += f'[{idx}] {order}\n'

        bot.send_message(message.chat.id, f'Заказы:\n{ords}')

    if message.text == 'Обновить':
        bot.send_message(message.chat.id, 'Выберети действие', reply_markup=update_keyboard)

    if message.text == 'Читать предложения':
        reviews = db.get_reviews()
        if not reviews:
            bot.send_message(message.chat.id, 'Нету предложений')
            return
        bot.send_message(message.chat.id, '\n\n'.join(reviews))

    if message.text == 'Назначить встречу':
        bot.send_message(message.chat.id,
                         'Напишите встречу в таком формате\n\nТема\n\nДата и время (в формате dd.mm.YY)')
        bot.register_next_step_handler(message, make_meeting)

    if message.text == 'Назначить совещание':
        bot.send_message(message.chat.id,
                         'Напишите совещание в таком формате\n\nТема\n\nДата и время (в формате dd.mm.YY)')
        bot.register_next_step_handler(message, make_session)

    if message.text == 'Назначить задачу':
        bot.send_message(message.chat.id, 'Напишите задачу для своего менти')
        bot.register_next_step_handler(message, make_task)

    if message.text == 'Назначенные встречи':
        meetings = db.get_meetings(message.chat.id)
        bot.send_message(message.chat.id, 'Назначенные встречи:\n\n' + '\n'.join(meetings))

    if message.text == 'Назначенные задачи':
        tasks = db.get_tasks(message.chat.id)
        tasks_text = ''
        for task in tasks:
            tasks_text += f'{task[0]} {task[1]}\n\n'
        bot.send_message(message.chat.id, 'Назначенные задачи:\n\n' + tasks_text, reply_markup=tasks_keyboard)

    if message.text == 'Отслеживать выполнение плана':
        statics = db.get_statics()
        bot.send_message(message.chat.id, statics)

    if message.text == 'Написать ментору':
        bot.send_message(message.chat.id, 'Напишите сообщение которое хотите написать вашему ментору')
        bot.register_next_step_handler(message, write_to_mentor)


def fio(message):
    temp[message.chat.id] = [message.text]
    bot.send_message(message.chat.id, 'Отправьте ваш возраст.')
    bot.register_next_step_handler(message, age)


def age(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Отправьте ваш возраст в цифрах.')
        return bot.register_next_step_handler(message, age)

    temp[message.chat.id] += [message.text]
    bot.send_message(message.chat.id, 'Отправьте ваше звание сотрудника', reply_markup=rank_butt)
    bot.register_next_step_handler(message, rank)


def rank(message):
    if message.text in ['Директор', 'Управляющий']:
        temp[message.chat.id] += [message.text]
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, password_verify)
        return

    if message.text == 'Менти':
        bot.send_message(message.chat.id, 'Введите направление подготовки:', reply_markup=direction_keyboard)
        bot.register_next_step_handler(message, direction_input)
        return

    if message.text not in ['Ментор']:
        bot.send_message(message.chat.id, 'Отправьте ваше звание сотрудника по кнопке')
        bot.register_next_step_handler(message, rank)
        return

    db.add_user(
        {
            'id': message.chat.id,
            'fio': temp[message.chat.id][0],
            'age': temp[message.chat.id][1],
            'position': 'Mentor',
            'direction': None
        }
    )

    bot.send_message(message.chat.id, 'Вы были успешно зарегистрированы.', reply_markup=start_butt)


def password_verify(message):
    if message.text == 'hse_kunte':
        db.add_user(
            {
                'id': message.chat.id,
                'fio': temp[message.chat.id][0],
                'age': temp[message.chat.id][1],
                'position': {'Директор': 'Director', 'Управляющий': 'Manager'}[temp[message.chat.id][2]],
                'direction': None
            }
        )
        bot.send_message(
            message.chat.id,
            'Регистрация завершена',
            reply_markup=manager_keyboard if temp[message.chat.id][2] == 'Управляющий' else director_keyboard
        )

    else:
        bot.send_message(message.chat.id, 'Неправильный пароль, вы кунти.', reply_markup=start_butt)
        return


def direction_input(message):
    db.add_user(
        {
            'id': message.chat.id,
            'fio': temp[message.chat.id][0],
            'age': temp[message.chat.id][1],
            'position': 'Menti',
            'direction': message.text
        }
    )
    bot.send_message(message.chat.id, 'Регистрация завершена', reply_markup=start_butt)


def get_new_menti(message):
    mentis = db.get_free_mentis()
    for menti in mentis:
        if menti['id'] == int(message.text):
            db.add_wanting(message.chat.id, int(message.text))
            bot.send_message(message.chat.id, f"[{menti['fio']}] Был выбран вашим желаемым менти",
                             reply_markup=mentor_keyboard)
            return

    bot.send_message(message.chat.id, 'Выберите айди из списка')
    bot.register_next_step_handler(message, get_new_menti)
    return


def add_pair(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Отменено', reply_markup=start_butt)
        return
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, 'Введите айди ментора и менти через пробел')
        bot.register_next_step_handler(message, add_pair)
        return

    mentor_id, menti_id = map(int, message.text.split())
    db.add_job(mentor_id, menti_id)
    bot.send_message(message.chat.id, 'Готово', reply_markup=manager_keyboard)

    mentor = db.get_user(mentor_id)
    menti = db.get_user(menti_id)

    bot.send_message(mentor_id, f"Вам назначен новый менти {menti['fio']}")
    bot.send_message(menti_id, f"Вам назначен новый ментор {mentor['fio']}")


def make_order(message):
    db.add_order(message.text)
    bot.send_message(message.chat.id, 'Заказ успешно добавлен')


def delete_order(message):
    db.delete_order(int(message.text))
    bot.send_message(message.chat.id, 'Готово', reply_markup=director_keyboard)


def write_review(message):
    db.add_review(message.text)
    bot.send_message(message.chat.id, 'Ваше ревью записано.')


def make_meeting(message):
    menti_id = db.get_mentors_menti_id(message.chat.id)
    db.add_meeting(message.chat.id, message.text)
    bot.send_message(menti_id, f'Вам назначена встреча\n\n{message.text}')
    bot.send_message(message.chat.id, 'Готово')


def make_session(message):
    mentors = db.get_users_by_role('Mentor')
    db.add_session(message.text)
    for mentor in mentors:
        bot.send_message(mentor['id'], f'Вам назначена конференция\n\n{message.text}')
    bot.send_message(message.chat.id, 'Готово')


def make_task(message):
    temp[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Напишите дедлайн задачи в формате dd.mm.YY')
    bot.register_next_step_handler(message, make_task_date)


def make_task_date(message):
    task_text = temp[message.chat.id]
    menti_id = db.get_mentors_menti_id(message.chat.id)
    try:
        task_deadline = datetime.datetime.strptime(message.text, '%d.%m.%Y')

    except ValueError:
        bot.send_message(message.chat.id, 'Напишите в правильном формате dd.mm.YY (например 01.02.2003)')
        bot.register_next_step_handler(message, make_task_date)
        return

    db.add_task(message.chat.id, task_text, task_deadline)
    bot.send_message(menti_id, f'Вам назначена новая задача\n\n{task_text}\n\nДедлайн: {message.text}')
    bot.send_message(message.chat.id, 'Готово')


def get_task_id(message):
    temp[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Отправьте ваше выполнение этой задачи следующим сообщением')
    bot.register_next_step_handler(message, get_task)


def get_task(message):
    mentor_id = db.get_mentis_mentor_id(message.chat.id)
    task_id = temp[message.chat.id]
    db.delete_task(mentor_id, int(task_id))
    bot.send_message(mentor_id, f'Ваш менти отправил выполнение {task_id} задачи:')
    bot.forward_message(mentor_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Готово.')


def write_to_mentor(message):
    mentor_id = db.get_mentis_mentor_id(message.chat.id)
    bot.send_message(mentor_id, 'Ваш ментичучок написал вам сообщение:', reply_markup=answer_inline)
    bot.forward_message(mentor_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Готово.')


def write_to_menti(message):
    menti_id = db.get_mentors_menti_id(message.chat.id)
    bot.send_message(menti_id, 'Ваш ментор написал вам сообщение:')
    bot.forward_message(menti_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Готово.')


@bot.callback_query_handler(lambda call: call.data == 'back')
def process_callback(call):
    bot.send_message(call.message.chat.id, 'Меню', reply_markup=start_butt)


@bot.callback_query_handler(lambda call: call.data == 'edit_profile')
def process_callback(call):
    db.delete_user(call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Отправьте ФИО.')
    bot.register_next_step_handler(call.message, fio)


@bot.callback_query_handler(lambda call: call.data == 'delete_order')
def process_callback(call):
    bot.send_message(call.message.chat.id, 'Введите номер заказа:')
    bot.register_next_step_handler(call.message, delete_order)


@bot.callback_query_handler(lambda call: call.data == 'write_review')
def process_callback(call):
    bot.send_message(call.message.chat.id, 'Напишите ваше предложение:')
    bot.register_next_step_handler(call.message, write_review)


@bot.callback_query_handler(lambda call: call.data == 'make_task')
def process_callback(call):
    tasks = db.get_tasks(call.message.chat.id)
    tasks_text = ''
    for idx, task in enumerate(tasks, start=1):
        tasks_text += f'[{idx}] {task[0]}\n'

    bot.send_message(call.message.chat.id, f'{tasks_text}\nВыберите номер задачи которую хотите выполнить')
    bot.register_next_step_handler(call.message, get_task_id)


@bot.callback_query_handler(lambda call: call.data == 'delete_account')
def process_callback(call):
    db.delete_user(call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Ваш аккаунт был успешно удалён из системы.', reply_markup=start_butt)


@bot.callback_query_handler(lambda call: call.data == 'answer_menti')
def process_callback(call):
    bot.send_message(call.message.chat.id, 'Напишите сообщение которое хотите отправить вашему ментичучоку')
    bot.register_next_step_handler(call.message, write_to_menti)


bot.polling()
