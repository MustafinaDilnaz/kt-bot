import openpyxl
import pandas as pd
import psycopg2
from telebot import *
import kaz
import rus
import db_connect

bot = telebot.TeleBot('6220689869:AAH6luRPM4E1HW7ZfUeZvT-VlssMzClvXuI')
admin_id = ['484489968', '760906879', '187663574', '577247261', '204504707', '531622371']
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Рознечному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]


def check_id(categories, input_id):
    for category, details in categories.items():
        if details.get("id") == input_id:
            return True
    return False


def check_register(message, func):
    if func == "profile":
        bot.send_message(message.chat.id, "Изменения сохранены")
        return 1
    elif func == "end":
        language = db_connect.get_language(message)
        if language[0][0] == 'rus':
            rus.appeal(bot, message, 'Оставить обращение')
        elif language[0][0] == 'kaz':
            kaz.appeal(bot, message, 'Өтінішті қалдыру')
        return 1
    return 0


def register(message, func="menu"):
    db_connect.cm_sv_db(message, '/start_register')
    if func == "start":
        bot.send_message(message.chat.id, "Приветствую, друг!🫡 \n"
                                          "Меня зовут ktbot, \nТвой личный помощник в компании АО'Казахтелеком'.")
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Перед началом пользования, \nДавай пройдем регистрацию и познакомимся😊")
        time.sleep(0.75)
    msg = bot.send_message(message.chat.id, "Введите свое имя")
    bot.register_next_step_handler(msg, change_firstname, func)


def change_firstname(message, func):
    db_connect.set_firstname(message, message.text)
    if check_register(message, func) != 0:
        return
    msg = bot.send_message(message.chat.id, "Введите свою фамилию")
    bot.register_next_step_handler(msg, change_lastname, func)


def change_lastname(message, func):
    db_connect.set_lastname(message, message.text)
    if check_register(message, func) != 0:
        return
    msg = bot.send_message(message.chat.id, "А теперь введите Ваш табельный номер \n\n"
                                            "P.s.: Таб. номер Вы узнать у Вашего HR дженералиста")
    bot.register_next_step_handler(msg, change_table_num, func)


def change_table_num(message, func):
    try:
        int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Вы ввели некоректные данные, введите в таком шаблоне:\n123456")
        bot.register_next_step_handler(msg, change_table_num, func)
        return
    if len(message.text) > 7:
        msg = bot.send_message(message.chat.id, "Вы ввели некоректные данные, введите в таком шаблоне:\n123456")
        bot.register_next_step_handler(msg, change_table_num, func)
    else:
        db_connect.set_table_number(message, message.text)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, "Введите Ваш номер телефона\n\nНапример: +7 777 777 7777 ")
        bot.register_next_step_handler(msg, change_phone_num, func)


def change_phone_num(message, func):
    phone_num = message.text
    pattern = r'^(\+?7|8)(\d{10})$'
    if not re.match(pattern, phone_num):
        msg = bot.send_message(message.chat.id, "Вы ввели некоректные данные, введите в таком шаблоне +77001112233")
        bot.register_next_step_handler(msg, change_phone_num, func)
    elif len(phone_num) > 12 or len(phone_num) < 11:
        msg = bot.send_message(message.chat.id, "Вы ввели некоректные данные, введите в таком шаблоне +77001112233")
        bot.register_next_step_handler(msg, change_phone_num, func)
    else:
        db_connect.set_phone_number(message, phone_num)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, "Введите Ваш корпоративный E-mail\n\n"
                                                "(временно можете указать и Ваш личный)")
        bot.register_next_step_handler(msg, change_email, func)


def change_email(message, func):
    email = message.text
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        db_connect.set_email(message, email)
        if check_register(message, func) != 0:
            return
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = db_connect.generate_buttons(branches, markup_b)
        msg = bot.send_message(message.chat.id, "И завершающий этап\n"
                                                "Выберите Ваш филиал из списка", reply_markup=markup_b)
        bot.register_next_step_handler(msg, change_branch, func)
    else:
        msg = bot.send_message(message.chat.id,
                               "Вы ввели некоректные данные, введите в таком шаблоне dilnaz@telecom.kz")
        bot.register_next_step_handler(msg, change_email, func)


def change_branch(message, func):
    branch = message.text
    if branch in branches:
        db_connect.set_branch(message.chat.id, branch)
        if func == "start" or func == "menu":
            bot.send_message(message.chat.id, f"Регистрация пройдена!\n\n{db_connect.get_firstname(message)}, "
                                              f"\nПриятно познакомиться!😇")
            time.sleep(0.75)
            bot.send_message(message.chat.id, "Чтобы изменить информацию, введите команду "
                                              "/register или найдите её в меню команд")
            time.sleep(0.75)
        if check_register(message, func) != 0:
                return
        db_connect.cm_sv_db(message, '/end_register')
        if func == "menu":
            menu(message)
        elif func == 'start':
            start(message)
    else:
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = db_connect.generate_buttons(branches, markup_b)

        msg = bot.send_message(message.chat.id,
                               "Вы ввели некоректные данные, выберете филиал из списка", reply_markup=markup_b)
        bot.register_next_step_handler(msg, change_branch, func)


@bot.message_handler(commands=['alter_table_users'])
def alter_table(message):
    db_connect.alter_table_users()
    bot.send_message(message.chat.id, "Изменение прошло успешно")


@bot.message_handler(commands=['start'])
def start(message):
    # bot.send_sticker(message.chat.id, sticker_file)
    db_connect.create_db()
    db_connect.addIfNotExistUser(message)
    db_connect.cm_sv_db(message, '/start')
    db_connect.clear_appeals(message)

    if str(message.chat.id)[0] == '-':
        return
    language = db_connect.get_language(message)
    if db_connect.get_branch(str(message.chat.id)) == ' ':
        register(message, 'start')
        return
    if language[0][0] == 'rus':
        rus.send_welcome_message(bot, message)
    elif language[0][0] == 'kaz':
        kaz.send_welcome_message(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['language'])
def lang(message):
    if str(message.chat.id)[0] == '-':
        return
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='🇷🇺 Русский язык', callback_data='rus')
    button2 = types.InlineKeyboardButton(text='🇰🇿 Қазақ тілі', callback_data='kaz')
    markup.add(button2, button1)
    bot.send_message(text='Тілді таңдаңыз | Выберите язык', chat_id=message.chat.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'rus')
def handle_button_rus(call):
    db_connect.change_language(call.message, 'rus')
    start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'kaz')
def handle_button_kaz(call):
    db_connect.change_language(call.message, 'kaz')
    start(call.message)


@bot.message_handler(commands=['menu'])
def menu(message):
    db_connect.create_db()
    db_connect.addIfNotExistUser(message)
    db_connect.cm_sv_db(message, 'menu')
    if str(message.chat.id)[0] == '-':
        return
    language = db_connect.get_language(message)[0][0]
    if language == 'rus':
        rus.menu(bot, message)
    elif language == 'kaz':
        kaz.menu(bot, message)
    else:
        lang(message)
    db_connect.clear_appeals(message)


@bot.message_handler(commands=["help"])
def help(message):
    db_connect.cm_sv_db(message, '/help')
    language = db_connect.get_language(message)[0][0]
    if str(message.chat.id)[0] == '-':
        return
    if language == 'rus':
        bot.send_message(message.chat.id,
                         "Вы можете помочь нам стать лучше и отправить нам письмо на info.ktcu@telecom.kz.")
    elif language == 'kaz':
        bot.send_message(message.chat.id,
                         "Сіз бізге жақсы адам болуға көмектесе аласыз және бізге хат жібере аласыз "
                         "info.ktcu@telecom.kz.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "Изменить Имя":
        msg = bot.send_message(call.message.chat.id, "Введите Имя")
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_firstname, "end")
        else:
            bot.register_next_step_handler(msg, change_firstname, "profile")
    elif call.data == "Изменить Фамилию":
        msg = bot.send_message(call.message.chat.id, "Введите Фамилию")
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_lastname, "end")
        else:
            bot.register_next_step_handler(msg, change_lastname, "profile")
    elif call.data == "Изменить номер телефона":
        msg = bot.send_message(call.message.chat.id, "Введите номер телефона")
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_phone_num, "end")
        else:
            bot.register_next_step_handler(msg, change_phone_num, "profile")
    elif call.data == "Изменить email":
        msg = bot.send_message(call.message.chat.id, "Введите email")
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_email, "end")
        else:
            bot.register_next_step_handler(msg, change_email, "profile")
    elif call.data == "Изменить табельный номер":
        msg = bot.send_message(call.message.chat.id, "Введите табельный номер")
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_table_num, "end")
        else:
            bot.register_next_step_handler(msg, change_table_num, "profile")
    elif call.data == "Изменить филиал":
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = db_connect.generate_buttons(branches, markup_b)
        msg = bot.send_message(call.message.chat.id, "Выберите Ваш филиал из списка", reply_markup=markup_b)
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_branch, "end")
        else:
            bot.register_next_step_handler(msg, change_branch, "profile")
    else:
        language = db_connect.get_language(call.message)[0][0]
        if language == 'rus':
            rus.call_back(bot, call)
        elif language == 'kaz':
            kaz.call_back(bot, call)



@bot.message_handler(commands=['get_excel'])
def get_excel(message):
    sql_query = "SELECT users.id, firstname, lastname, commands_name, commands_history.date FROM commands_history " \
                "full outer join users on commands_history.id = users.id"
    db_connect.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_users'])
def get_excel(message):
    sql_query = "SELECT * from users"
    db_connect.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_users_info'])
def get_excel(message):
    sql_query = "SELECT * from users_info"
    db_connect.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_appeals'])
def get_excel(message):
    sql_query = "SELECT * from appeals"
    db_connect.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


def send_error(message):
    language = db_connect.get_language(message)
    if language == 'rus':
        rus.send_error(bot, message)
    elif language == 'kaz':
        kaz.send_error(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['broadcast'])
def info_broadcast(message):
    if str(message.chat.id) not in admin_id:
        return
    msg = bot.reply_to(message, 'Введите текст')
    bot.register_next_step_handler(msg, text_check)


def text_check(message):
    markup_text_check = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_yes = types.KeyboardButton("Да")
    button_no = types.KeyboardButton("Нет")
    markup_text_check.add(button_yes, button_no)
    msg = bot.reply_to(message, "Вы уверены что хотите отправить это сообщение?", reply_markup=markup_text_check)
    bot.register_next_step_handler(msg, message_sender, message)


def message_sender(message, broadcast_message):
    if message.text.upper() == "ДА":
        # conn = psycopg2.connect(user="postgres", password="j7hPC180")
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute('SELECT id FROM users')
        users_id = cur.fetchall()
        cur.close()
        conn.close()
        for id in users_id:
            if broadcast_message.photo:
                photo_id = broadcast_message.photo[-1].file_id
                bot.send_photo(id[0], photo_id, broadcast_message.caption)

            if broadcast_message.audio:
                audio_id = broadcast_message.audio.file_id
                bot.send_video(id[0], audio_id, broadcast_message.caption)

            if broadcast_message.video:
                video_id = broadcast_message.video.file_id
                bot.send_video(id[0], video_id, broadcast_message.caption)

            if broadcast_message.voice:
                voice_id = broadcast_message.voice.file_id
                bot.send_voice(id[0], voice_id, broadcast_message.caption)

            if broadcast_message.text:
                bot.send_message(id[0], broadcast_message.text)
    elif message.text.upper() == "НЕТ":
        bot.send_message(message.chat.id, "Вызовите функцию /broadcast чтобы вызвать комманду рассылки еще раз")
    else:
        rus.send_error(bot, message)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message = message.text
    # try:
    if str(message.chat.id)[0] == '-':
        return
    language = db_connect.get_language(message)[0][0]
    if language == 'rus':
        text(message, get_message, rus)
    elif language == 'kaz':
        text(message, get_message, kaz)
    else:
        lang(message)
    # except:
    #     lang(message)


def text(message, get_message, lang_py):
    if get_message in lang_py.faq_field or get_message in branches:
        lang_py.faq(bot, message)
    elif get_message in drb_regions or get_message in ods_regions:
        lang_py.func_region(bot, message)
    elif get_message == "Мой профиль" or get_message == "Менің профилім":
        db_connect.profile(bot, message)
    elif get_message in lang_py.faq_1.keys():
        bot.send_message(message.chat.id, lang_py.faq_1[message.text])
    elif get_message in lang_py.faq_2.keys():
        bot.send_message(message.chat.id, lang_py.faq_2[message.text])
    elif get_message in lang_py.biot_field:
        lang_py.biot(bot, message)
    elif get_message in lang_py.kb_field:
        lang_py.kb(bot, message)
    elif get_message in lang_py.adapt_field:
        lang_py.adaption(bot, message)
    elif get_message == "Оставить обращение" or get_message == "Өтінішті қалдыру" \
            or db_connect.get_appeal_field(message):
        lang_py.appeal(bot, message, message.text)
    elif str(message.chat.id) in db_connect.get_users_id():
        if db_connect.get_glossar(message):
            lang_py.glossary(bot, message)
        elif db_connect.get_instr(message) and message.text in lang_py.kb_field_all:
            lang_py.instructions(bot, message)
        else:
            lang_py.send_error(bot, message)
    else:
        lang_py.send_error(bot, message)


bot.polling(none_stop=True)
