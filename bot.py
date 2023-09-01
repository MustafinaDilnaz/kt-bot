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
    arr = [rus.markup, rus, "Изменения сохранены", "Оставить обращение"]
    language = db_connect.get_language(message)
    if language == "kaz":
        arr = [kaz.markup, kaz, "Өзгерістер сақталды", "Өтінішті қалдыру"]
    if func == "profile":
        bot.send_message(message.chat.id, arr[2], reply_markup=arr[0])
        return 1
    elif func == "end":
        arr[1].appeal(bot, message, arr[3])
        return 1
    return 0


@bot.message_handler(commands=['delete_me'])
def delete_me(message):
    db_connect.delete_user(message)


def register(message, func="menu"):
    db_connect.cm_sv_db(message, '/start_register')
    language = db_connect.get_language(message)
    arr = ["Приветствую, друг!🫡 \nМеня зовут ktbot, \nТвой личный помощник в компании АО'Казахтелеком'.",
           "Перед началом пользования,\nДавай пройдем регистрацию и познакомимся😊",
           "Введите свое имя"]
    if language == "kaz":
        arr = ["Сәлем досым!🫡 \nМенің атым ktbot\n'Қазақтелеком' АҚ компаниясындағы сіздің жеке көмекшіңіз.",
               "Пайдалануды бастамас бұрын,\nТіркеуден өтіп танысайық😊", "Атыңызды енгізіңіз"]
    if func == "start":
        bot.send_message(message.chat.id, arr[0])
        time.sleep(0.75)
        bot.send_message(message.chat.id, arr[1])
        time.sleep(0.75)
    msg = bot.send_message(message.chat.id, arr[2])
    bot.register_next_step_handler(msg, change_firstname, func)


def change_firstname(message, func):
    db_connect.set_firstname(message, message.text)
    if check_register(message, func) != 0:
        return
    language = db_connect.get_language(message)
    if language == 'kaz':
        msg = bot.send_message(message.chat.id, "Фамилияңызды енгізіңіз")
    else:
        msg = bot.send_message(message.chat.id, "Введите фамилию")
    bot.register_next_step_handler(msg, change_lastname, func)


def change_lastname(message, func):
    db_connect.set_lastname(message, message.text)
    if check_register(message, func) != 0:
        return
    language = db_connect.get_language(message)
    if language == 'kaz':
        msg = bot.send_message(message.chat.id, "Енді табель нөміріңізді енгізіңіз\n\n"
                                                "P.s.: қойынды. сіз өзіңіздің HR генералистіңізден білетін нөміріңіз")
    else:
        msg = bot.send_message(message.chat.id, "А теперь введите Ваш табельный номер \n\n"
                                                "P.s.: Таб. номер Вы узнать у Вашего HR дженералиста")
    bot.register_next_step_handler(msg, change_table_num, func)


def change_table_num(message, func):
    language = db_connect.get_language(message)
    arr = ["Вы ввели некорректные данные, введите в таком шаблоне:\n123456",
           "Введите Ваш номер телефона\n\nНапример: +7 777 777 7777 "]
    if language == "kaz":
        arr = ["Сіз қате деректерді енгіздіңіз, осы үлгіге енгізіңіз:\n123456",
               "Телефон нөміріңізді енгізіңіз\n\nМысалы: +7 777 777 7777"]
    try:
        int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_table_num, func)
        return
    if len(message.text) > 10:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_table_num, func)
    else:
        db_connect.set_table_number(message, message.text)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, arr[1])
        bot.register_next_step_handler(msg, change_phone_num, func)


def change_phone_num(message, func):
    phone_num = message.text
    pattern = r'^(\+?7|8)(\d{10})$'
    language = db_connect.get_language(message)
    arr = ["Вы ввели некорректные данные, введите в таком шаблоне +77001112233",
           "Введите Ваш корпоративный E-mail\n\n(временно можете указать и Ваш личный)"]
    if language == "kaz":
        arr = ["Сіз қате деректерді енгіздіңіз, осындай үлгіге +77001112233 енгізіңіз",
               "Корпоративтік e-mail енгізіңіз\n\n(сіз өзіңіздің жеке басыңызды уақытша көрсете аласыз)"]
    if not re.match(pattern, phone_num):
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_phone_num, func)
    elif len(phone_num) > 12 or len(phone_num) < 11:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_phone_num, func)
    else:
        db_connect.set_phone_number(message, phone_num)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, arr[1])
        bot.register_next_step_handler(msg, change_email, func)


def change_email(message, func):
    email = message.text
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    language = db_connect.get_language(message)
    arr = ["И завершающий этап\nВыберите Ваш филиал из списка",
           "Вы ввели некорректные данные, введите в таком шаблоне dilnaz@telecom.kz"]
    if language == "kaz":
        arr = ["Және соңғы кезең\nТізімнен филиалды таңдаңыз",
               "Сіз қате деректерді енгіздіңіз, осы үлгіге енгізіңіз dilnaz@telecom.kz"]
    if re.fullmatch(regex, email):
        db_connect.set_email(message, email)
        if check_register(message, func) != 0:
            return
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = db_connect.generate_buttons(branches, markup_b)
        msg = bot.send_message(message.chat.id, arr[0], reply_markup=markup_b)
        bot.register_next_step_handler(msg, change_branch, func)
    else:
        msg = bot.send_message(message.chat.id,arr[1])
        bot.register_next_step_handler(msg, change_email, func)


def change_branch(message, func):
    branch = message.text
    language = db_connect.get_language(message)
    arr = ["Регистрация пройдена!\n\nПриятно познакомиться!😇",
           "Если вы хотите изменить информацию то перейдите во вкладку Мой профиль",
           "Вы ввели некорректные данные, выберите филиал из списка"]
    if language == "kaz":
        arr = ["Тіркеу өтті!\n\nТанысқаныма қуаныштымын!😇",
               "Егер сіз ақпаратты өзгерткіңіз келсе онда Менің профилім қойындысына өтіңіз",
               "Сіз қате деректерді енгіздіңіз, тізімнен филиалды таңдаңыз"]
    if branch in branches:
        db_connect.set_branch(message.chat.id, branch)
        if func == "start" or func == "menu":
            bot.send_message(message.chat.id, arr[0])
            time.sleep(0.75)
            bot.send_message(message.chat.id, arr[1])
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

        msg = bot.send_message(message.chat.id, arr[2], reply_markup=markup_b)
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
    if language == 'rus':
        if db_connect.get_branch(str(message.chat.id)) == ' ':
            register(message, 'start')
            return
        rus.send_welcome_message(bot, message)
    elif language == 'kaz':
        if db_connect.get_branch(str(message.chat.id)) == ' ':
            register(message, 'start')
            return
        kaz.send_welcome_message(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['language'])
def lang(message):
    if str(message.chat.id)[0] == '-':
        return
    if db_connect.get_branch(str(message.chat.id)) == ' ':
        bot.send_sticker(message.chat.id, open('images/AnimatedStickerHi.tgs', 'rb'))
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
    language = db_connect.get_language(message)
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
    language = db_connect.get_language(message)
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
    language = db_connect.get_language(call.message)
    arr = ["Введите Имя", "Введите Фамилию", "Введите номер телефона",
           "Введите Ваш корпоративный E-mail\n\n(временно можете указать и Ваш личный)", "Введите табельный номер",
           "Выберите Ваш филиал из списка"]
    if language == "kaz":
        arr = ["Атыңызды енгізіңіз", "Фамилияны Енгізіңіз", "Телефон нөміріңізді енгізіңіз",
               "Корпоративтік e-mail енгізіңіз\n\n(сіз өзіңіздің жеке басыңызды уақытша көрсете аласыз)",
               "Табель нөмірін енгізіңіз", "Тізімнен филиалды таңдаңыз"]
    if call.data == "Изменить Имя":
        msg = bot.send_message(call.message.chat.id, arr[0])
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_firstname, "end")
        else:
            bot.register_next_step_handler(msg, change_firstname, "profile")
    elif call.data == "Изменить Фамилию":
        msg = bot.send_message(call.message.chat.id, arr[1])
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_lastname, "end")
        else:
            bot.register_next_step_handler(msg, change_lastname, "profile")
    elif call.data == "Изменить номер телефона":
        msg = bot.send_message(call.message.chat.id, arr[2])
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_phone_num, "end")
        else:
            bot.register_next_step_handler(msg, change_phone_num, "profile")
    elif call.data == "Изменить email":
        msg = bot.send_message(call.message.chat.id, arr[3])
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_email, "end")
        else:
            bot.register_next_step_handler(msg, change_email, "profile")
    elif call.data == "Изменить табельный номер":
        msg = bot.send_message(call.message.chat.id, arr[4])
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_table_num, "end")
        else:
            bot.register_next_step_handler(msg, change_table_num, "profile")
    elif call.data == "Изменить филиал":
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = db_connect.generate_buttons(branches, markup_b)
        msg = bot.send_message(call.message.chat.id, arr[5], reply_markup=markup_b)
        if db_connect.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_branch, "end")
        else:
            bot.register_next_step_handler(msg, change_branch, "profile")
    else:
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
        bot.send_message(message.chat.id, str(users_id))
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
    language = db_connect.get_language(message)
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
        lang_py.profile(bot, message)
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
