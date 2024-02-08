import openpyxl
import psycopg2
from telebot import *
import db_connect
import kaz
import rus
import userClass
import commands_historyClass
import common_file
import file
import user_infoClass


bot = telebot.TeleBot(db_connect.TOKEN, parse_mode="HTML")
admin_id = ['484489968', '760906879', '187663574', '577247261', '204504707', '531622371']
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]

API_KEY = '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'


def check_id(categories, input_id):
    for category, details in categories.items():
        if details.get("id") == input_id:
            return True
    return False


def check_is_command(text_):
    if text_ == "/menu" or text_ == "/start" or text_ == "/help" or text_ == "/language":
        return False
    return True


def check_register(message, func):
    markup = rus.get_markup(message)
    arr = [markup, rus, "Изменения сохранены", "Оставить обращение"]
    language = userClass.get_language(message)
    if language == "kaz":
        markup = kaz.get_markup(message)
        arr = [markup, kaz, "Өзгерістер сақталды", "Өтінішті қалдыру"]
    if func == "profile":
        bot.send_message(message.chat.id, arr[2], reply_markup=arr[0])
        return 1
    elif func == "end":
        arr[1].appeal(bot, message, arr[3])
        return 1
    return 0


@bot.message_handler(commands=['delete_me'])
def delete_me(message):
    userClass.delete_user(message)
    bot.send_message(message.chat.id, "Изменения сохранены")


@bot.message_handler(commands=['insert_into_performers'])
def insert_into_performers(message):
    db_connect.create_db()
    db_connect.insert_into_performers()
    bot.send_message(message.chat.id, "Изменения сохранены")


@bot.message_handler(commands=['insert_into_performers_right'])
def insert_into_performers(message):
    db_connect.create_db()
    db_connect.insert_into_performers_right()
    bot.send_message(message.chat.id, "Изменения сохранены")


@bot.message_handler(commands=['delete_performers'])
def delete_performers(message):
    db_connect.delete_performers()
    bot.send_message(message.chat.id, "Изменения сохранены")


@bot.message_handler(commands=['register_start'])
def register(message, func="menu"):
    commands_historyClass.cm_sv_db(message, '/start_register')
    language = userClass.get_language(message)
    arr = ["Приветствую, друг!🫡 \nМеня зовут ktbot, \nТвой личный помощник в компании АО'Казахтелеком'.",
           "Перед началом пользования,\nДавай пройдем регистрацию и познакомимся😊",
           "Выберите филиал из списка"]
    if language == "kaz":
        arr = ["Сәлем досым!🫡 \nМенің атым ktbot\n'Қазақтелеком' АҚ-дағы сіздің жеке көмекшіңізбін",
               "Пайдалануды бастамас бұрын,\nТіркеуден өтіп танысайық😊", "Тізімнен филиалды таңдаңыз"]
    if func == "start":
        bot.send_message(message.chat.id, arr[0])
        time.sleep(0.75)
        bot.send_message(message.chat.id, arr[1])
        time.sleep(0.75)
    markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_b = common_file.generate_buttons(branches, markup_b)
    msg = bot.send_message(message.chat.id, arr[2], reply_markup=markup_b)
    bot.register_next_step_handler(msg, change_branch, func)
    # msg = bot.send_message(message.chat.id, arr[2])
    # bot.register_next_step_handler(msg, change_firstname, func)


def change_firstname(message, func):
    language = userClass.get_language(message)
    if not check_is_command(message.text):
        if language == "kaz":
            msg = bot.send_message(message.chat.id, "Командаларды пайдалану үшін атауды енгізу керек")
        else:
            msg = bot.send_message(message.chat.id, "Для использования команд необходимо ввести имя")
        bot.register_next_step_handler(msg, change_firstname, func)
        return
    userClass.set_firstname(message, message.text)
    if check_register(message, func) != 0:
        return
    if language == 'kaz':
        msg = bot.send_message(message.chat.id, "Тегіңізді енгізіңіз")
    else:
        msg = bot.send_message(message.chat.id, "Введите фамилию")
    bot.register_next_step_handler(msg, change_lastname, func)


def change_lastname(message, func):
    language = userClass.get_language(message)
    if not check_is_command(message.text):
        if language == "kaz":
            msg = bot.send_message(message.chat.id, "Командаларды пайдалану үшін фамилияны енгізу керек")
        else:
            msg = bot.send_message(message.chat.id, "Для использования команд необходимо ввести фамилию")
        bot.register_next_step_handler(msg, change_lastname, func)
        return
    userClass.set_lastname(message, message.text)
    if check_register(message, func) != 0:
        return
    if language == 'kaz':
        msg = bot.send_message(message.chat.id, "Телефон нөміріңізді енгізіңіз\n\nМысалы: +77001112233")
    else:
        msg = bot.send_message(message.chat.id, "Введите Ваш номер телефона\n\nНапример: +77001112233")
    bot.register_next_step_handler(msg, change_phone_num, func)


def change_table_num(message, func):
    language = userClass.get_language(message)
    arr = ["Вы ввели некорректные данные, введите в таком шаблоне:\n123456",
           "Подтвердите ваши данные: ", "Введите Ваше имя",
           "Введенный табельный номер не найден, хотите еще раз ввести табельный номер?", "Это я", "Это не я"]
    if language == "kaz":
        arr = ["Сіз деректерді қате енгіздіңіз, осы үлгіде енгізіңіз:\n123456",
               "Деректеріңізді растаңыз: ", "Атыңызды енгізіңіз",
               "Енгізілген табель нөмірі табылмады, табель нөмірін қайтадан енгізгіңіз келе ме?", "Бұл мен",
               "Бұл мен емес"]
    try:
        table_num = int(message.text)
        if userClass.get_branch(message.chat.id) == branches[2]:
            wb = openpyxl.load_workbook('ДРБ Табельные номера.xlsx')
            excel = wb['ШР на 01.10.2023']
            tab_nums, full_names = [], []
            for row in excel.iter_rows(min_row=2, max_row=3510, values_only=True):
                tab_nums.append(row[1])
                full_names.append(row[2])
            if table_num in tab_nums:
                index = tab_nums.index(table_num)
                full_name = full_names[index]
                full_name_arr = full_name.split(' ')
                userClass.set_table_number(message, table_num)
                userClass.set_firstname(message, full_name_arr[1])
                userClass.set_lastname(message, full_name_arr[0])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(arr[4])
                button2 = types.KeyboardButton(arr[5])
                markup.add(button1, button2)
                msg = bot.send_message(message.chat.id, arr[1] + str(full_name), reply_markup=markup)
                bot.register_next_step_handler(msg, is_it_you, func)
                return
            else:
                func_1(message, func)
                return
        else:
            userClass.set_table_number(message, message.text)
            if check_register(message, func) != 0:
                return
            msg = bot.send_message(message.chat.id, arr[2])
            bot.register_next_step_handler(msg, change_firstname, func)
    except ValueError:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_table_num, func)
        return
    if len(message.text) > 10:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_table_num, func)
    else:
        userClass.set_table_number(message, message.text)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, arr[2])
        bot.register_next_step_handler(msg, change_firstname, func)


def func_1(message, func):
    language = userClass.get_language(message)
    arr = ["Введенный табельный номер не найден, хотите еще раз ввести табельный номер?"]
    if language == "kaz":
        arr = ["Енгізілген табель нөмірі табылмады, табель нөмірін қайтадан енгізгіңіз келе ме?"]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    button1 = types.KeyboardButton("Да")
    button2 = types.KeyboardButton("Нет")
    markup.add(button1, button2)
    msg = bot.send_message(message.chat.id, arr[0], reply_markup=markup)
    bot.register_next_step_handler(msg, yes_no, func)


def is_it_you(message, func):
    language = userClass.get_language(message)
    arr = ["Введите Ваш номер телефона\n\nНапример: +77001112233", "Войти по табельному номеру", "Это я"]
    if language == "kaz":
        arr = ["Телефон нөміріңізді енгізіңіз\n\nМысалы: +77001112233", "Табель нөмірі бойынша кіру", "Бұл мен"]
    if message.text == arr[2]:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_phone_num, func)
    else:
        in_table(message, func, arr[1])


def yes_no(message, func):
    language = userClass.get_language(message)
    arr = ["Регистрация", "Войти по табельному номеру"]
    if language == "kaz":
        arr = ["Тіркеу", "Табель нөмірі бойынша кіру"]
    if message.text == "Да":
        in_table(message, func, arr[1])
    else:
        in_table(message, func, arr[0])


def change_phone_num(message, func):
    phone_num = message.text
    pattern = r'^(\+?7|8)(\d{10})$'
    language = userClass.get_language(message)
    arr = ["Вы ввели некорректные данные, введите в таком шаблоне +77001112233",
           "Введите Ваш корпоративный E-mail\n\n(временно можете указать и Ваш личный)"]
    if language == "kaz":
        arr = ["Сіз деректерді қате енгіздіңіз, осы үлгіде +77001112233 енгізіңіз",
               "Корпоративтік e-mail енгізіңіз\n\n(уақытша өзіңіздің жеке поштаңызды көрсете аласыз)"]
    if not re.match(pattern, phone_num):
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_phone_num, func)
    elif len(phone_num) > 12 or len(phone_num) < 11:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_phone_num, func)
    else:
        userClass.set_phone_number(message, phone_num)
        if check_register(message, func) != 0:
            return
        msg = bot.send_message(message.chat.id, arr[1])
        bot.register_next_step_handler(msg, change_email, func)


def change_email(message, func):
    email = message.text
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    language = userClass.get_language(message)
    arr = ["Регистрация пройдена!\n\nПриятно познакомиться!😇",
           "Вы ввели некорректные данные, введите в таком шаблоне dilnaz@telecom.kz",
           "Для использования команд необходимо ввести email",
           "Если вы хотите изменить информацию то перейдите во вкладку Мой профиль"]
    if language == "kaz":
        arr = ["Тіркеуден өттіңіз!\n\nТанысқаныма қуаныштымын!😇",
               "Сіз деректерді қате енгіздіңіз, осы үлгіде енгізіңіз dilnaz@telecom.kz",
               "Пәрмендерді пайдалану үшін email енгізу керек",
               "Сіз ақпаратты өзгерткіңіз келсе, онда Менің профилім қосымшасына өтіңіз"]
    if not check_is_command(message.text):
        msg = bot.send_message(message.chat.id, arr[2])
        bot.register_next_step_handler(msg, change_email, func)
        return
    elif re.fullmatch(regex, email):
        userClass.set_email(message, email)
        if check_register(message, func) != 0:
            return
        bot.send_message(message.chat.id, arr[0])
        bot.send_message(message.chat.id, arr[3])
        commands_historyClass.cm_sv_db(message, '/end_register')
        if func == "menu":
            menu(message)
        elif func == 'start':
            start(message)
    else:
        msg = bot.send_message(message.chat.id, arr[1])
        bot.register_next_step_handler(msg, change_email, func)


def change_branch(message, func):
    branch = message.text
    language = userClass.get_language(message)
    arr = ["Введите табельный номер", "Вы ввели некорректные данные, выберите филиал из списка", "Введите имя",
           "Выберите способ входа", "Регистрация", "Войти по табельному номеру"]
    if language == "kaz":
        arr = ["Табель нөмірін енгізіңіз", "Сіз қате деректерді енгіздіңіз, тізімнен филиалды таңдаңыз",
               "Атыңызды енгізіңіз", "Кіру әдісін таңдаңыз", "Тіркеу", "Табель нөмірі бойынша кіру"]
    if branch in branches:
        userClass.set_branch(message.chat.id, branch)
        if check_register(message, func) != 0:
            return
        if branch == branches[2]:
            markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            button1_b = types.KeyboardButton(arr[4])
            button2_b = types.KeyboardButton(arr[5])
            markup_b.add(button1_b, button2_b)
            msg = bot.send_message(message.chat.id, arr[3], reply_markup=markup_b)
            bot.register_next_step_handler(msg, in_table, func)
        else:
            msg = bot.send_message(message.chat.id, arr[2])
            bot.register_next_step_handler(msg, change_firstname, func)
    else:
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = common_file.generate_buttons(branches, markup_b)
        msg = bot.send_message(message.chat.id, arr[1], reply_markup=markup_b)
        bot.register_next_step_handler(msg, change_branch, func)


def in_table(message, func, message_text=None):
    if message_text is None:
        message_text = message.text
    language = userClass.get_language(message)
    arr = ["Введите табельный номер", "Введите имя", "Регистрация", "Войти по табельному номеру",
           "Выберите способ входа"]
    if language == "kaz":
        arr = ["Табель нөмірін енгізіңіз", "Атыңызды енгізіңіз", "Тіркеу", "Табель нөмірі бойынша кіру",
               "Кіру әдісін таңдаңыз"]
    if message_text == arr[2]:
        msg = bot.send_message(message.chat.id, arr[1])
        bot.register_next_step_handler(msg, change_firstname, func)
    elif message_text == arr[3]:
        msg = bot.send_message(message.chat.id, arr[0])
        bot.register_next_step_handler(msg, change_table_num, func)
    else:
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_b = types.KeyboardButton(arr[2])
        button2_b = types.KeyboardButton(arr[3])
        markup_b.add(button1_b, button2_b)
        msg = bot.send_message(message.chat.id, arr[4], reply_markup=markup_b)
        bot.register_next_step_handler(msg, in_table, func)


@bot.message_handler(commands=['alter_table_users'])
def alter_table(message):
    db_connect.alter_table_users()
    bot.send_message(message.chat.id, "Изменение прошло успешно")


@bot.message_handler(commands=['start'])
def start(message):
    # bot.send_sticker(message.chat.id, sticker_file)
    db_connect.create_db()
    db_connect.addIfNotExistUser(message)
    commands_historyClass.cm_sv_db(message, '/start')
    user_infoClass.clear_appeals(message)
    if str(message.chat.id)[0] == '-':
        return
    language = userClass.get_language(message)
    if language == 'rus':
        if userClass.get_email(message) == ' ':
            register(message, 'start')
            return
        rus.send_welcome_message(bot, message)
    elif language == 'kaz':
        if userClass.get_email(message) == ' ':
            register(message, 'start')
            return
        kaz.send_welcome_message(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['language'])
def lang(message):
    if str(message.chat.id)[0] == '-':
        return
    if userClass.get_branch(str(message.chat.id)) == ' ':
        bot.send_sticker(message.chat.id, open('images/AnimatedStickerHi.tgs', 'rb'))
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='🇷🇺 Русский язык', callback_data='rus')
    button2 = types.InlineKeyboardButton(text='🇰🇿 Қазақ тілі', callback_data='kaz')
    markup.add(button2, button1)
    bot.send_message(text='Тілді таңдаңыз | Выберите язык', chat_id=message.chat.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'rus')
def handle_button_rus(call):
    userClass.change_language(call.message, 'rus')
    start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'kaz')
def handle_button_kaz(call):
    userClass.change_language(call.message, 'kaz')
    start(call.message)


@bot.message_handler(commands=['menu'])
def menu(message):
    db_connect.create_db()
    db_connect.addIfNotExistUser(message)
    commands_historyClass.cm_sv_db(message, 'menu')
    if str(message.chat.id)[0] == '-':
        return
    language = userClass.get_language(message)
    if language == 'rus':
        if userClass.get_email(message) == ' ':
            register(message, 'start')
            return
        rus.menu(bot, message)
    elif language == 'kaz':
        if userClass.get_email(message) == ' ':
            register(message, 'start')
            return
        kaz.menu(bot, message)
    else:
        lang(message)
    user_infoClass.clear_appeals(message)


@bot.message_handler(commands=["help"])
def help_command(message):
    commands_historyClass.cm_sv_db(message, '/help')
    language = userClass.get_language(message)
    if str(message.chat.id)[0] == '-':
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    if language == 'rus':
        button = types.InlineKeyboardButton("Написать сообщение", callback_data="send_m")
        markup.add(button)
        bot.send_message(message.chat.id,
                         "Помогите нам стать лучше! Ждем вашего мнения и предложений. Вы можете отправить письмо "
                         "на info.ktcu@telecom.kz или воспользоваться ботом, нажав на экранную кнопку и написав нам "
                         "сообщение.", reply_markup=markup)
    elif language == 'kaz':
        button = types.InlineKeyboardButton("Хабарлама жазу", callback_data="send_m")
        markup.add(button)
        bot.send_message(message.chat.id,
                         "Бізге жақсы адам болуға көмектесіңіз! Біз сіздің пікіріңіз бен ұсыныстарыңызды күтеміз. "
                         "Сіз хат жібере аласыз info.ktcu@telecom.kz немесе экрандағы түймені басып, бізге хабарлама "
                         "жазу арқылы ботты пайдаланыңыз.", reply_markup=markup)


def get_help_message(message):
    language = userClass.get_language(message)
    help_message = message.text + "\n\n" + file.get_user_info(message.chat.id)
    if language == 'rus':
        bot.send_message(message.chat.id, "Ваше сообщение успешно сохранено")
    else:
        bot.send_message(message.chat.id, "Сіздің хабарламаңыз сәтті сақталды")
    bot.send_message('187663574', help_message)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    commands_historyClass.cm_sv_db(call.message, str(call.data))
    language = userClass.get_language(call.message)
    arr = ["Введите имя", "Введите Фамилию", "Введите номер телефона",
           "Введите Ваш корпоративный E-mail\n\n(временно можете указать и Ваш личный)", "Введите табельный номер",
           "Выберите Ваш филиал из списка"]
    if language == "kaz":
        arr = ["Атыңызды енгізіңіз", "Тегіңізді енгізіңіз", "Телефон нөміріңізді енгізіңіз",
               "Корпоративтік e-mail енгізіңіз\n\n(сіз өзіңіздің жеке басыңызды уақытша көрсете аласыз)",
               "Табель нөмірін енгізіңіз", "Тізімнен филиалды таңдаңыз"]
    if call.data == "Изменить Имя":
        msg = bot.send_message(call.message.chat.id, arr[0])
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_firstname, "end")
        else:
            bot.register_next_step_handler(msg, change_firstname, "profile")
    elif call.data == "Изменить Фамилию":
        msg = bot.send_message(call.message.chat.id, arr[1])
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_lastname, "end")
        else:
            bot.register_next_step_handler(msg, change_lastname, "profile")
    elif call.data == "Изменить номер телефона":
        msg = bot.send_message(call.message.chat.id, arr[2])
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_phone_num, "end")
        else:
            bot.register_next_step_handler(msg, change_phone_num, "profile")
    elif call.data == "Изменить email":
        msg = bot.send_message(call.message.chat.id, arr[3])
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_email, "end")
        else:
            bot.register_next_step_handler(msg, change_email, "profile")
    elif call.data == "Изменить табельный номер":
        msg = bot.send_message(call.message.chat.id, arr[4])
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_table_num, "end")
        else:
            bot.register_next_step_handler(msg, change_table_num, "profile")
    elif call.data == "Изменить филиал":
        markup_b = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_b = common_file.generate_buttons(branches, markup_b)
        msg = bot.send_message(call.message.chat.id, arr[5], reply_markup=markup_b)
        if user_infoClass.get_appeal_field(call.message):
            bot.register_next_step_handler(msg, change_branch, "end")
        else:
            bot.register_next_step_handler(msg, change_branch, "profile")
    elif call.data == "send_m":
        if language == 'rus':
            msg = bot.send_message(call.message.chat.id, "Отправьте ваше сообщение")
            bot.register_next_step_handler(msg, get_help_message)
        elif language == 'kaz':
            msg = bot.send_message(call.message.chat.id, "Хабарламаңызды жіберіңіз")
            bot.register_next_step_handler(msg, get_help_message)
    else:
        if language == 'rus':
            rus.call_back(bot, call)
        elif language == 'kaz':
            kaz.call_back(bot, call)


@bot.message_handler(commands=['get_excel'])
def get_excel(message):
    sql_query = "SELECT users.id, firstname, lastname, commands_name, commands_history.date FROM commands_history " \
                "full outer join users on commands_history.id = users.id"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_users'])
def get_excel(message):
    sql_query = "SELECT * from users"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_users_info'])
def get_excel(message):
    sql_query = "SELECT * from users_info"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_appeals'])
def get_excel(message):
    sql_query = """
        SELECT
            appeals.id AS "ID",
            users.firstname AS "Имя работника",
            users.lastname AS "Фамилия работника",
            table_number AS "Табельный номер",
            users.phone_number AS "Номер телефона работника",
            users.email AS "Почта",
            branch AS "Филиал",
            status AS "Статус",
            appeals.category AS "Категория",
            appeal_text AS "Текст заявки",
            date AS "Дата создания",
            date_status AS "Дата последнего изменения статуса",
            comment AS "Комментарий",
            evaluation AS "Оценка",
            image_data AS "Фото",
            performers.firstname AS "Имя исполнителя",
            performers.lastname AS "Фамилия исполнителя",
            performers.email AS "Почта исполнителя",
            performers.telegram AS "Телеграм исполнителя"
        FROM appeals
        LEFT OUTER JOIN users ON appeals.user_id = users.id
        LEFT OUTER JOIN performers ON performers.category = appeals.category
        order by appeals.id 
    """
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_appeals_'])
def get_excel(message):
    sql_query = "SELECT * from appeals"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_performers'])
def get_excel(message):
    sql_query = "SELECT * from performers"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_internal_sale'])
def get_excel(message):
    sql_query = "SELECT * from internal_sale"
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


@bot.message_handler(commands=['get_sales'])
def get_excel(message):
    sql_query = """
       SELECT
            appeals.id AS "ID",
            users.firstname AS "Имя работника",
            users.lastname AS "Фамилия работника",
            table_number AS "Табельный номер",
            users.phone_number AS "Номер телефона работника",
            users.email AS "Почта",
            branch AS "Филиал",
            status AS "Статус",
            appeals.category AS "Категория",
            appeal_text AS "Текст заявки",
            date AS "Дата создания",
            date_status AS "Дата последнего изменения статуса",
            comment AS "Комментарий",
            evaluation AS "Оценка",
            image_data AS "Фото",
            performers.firstname AS "Имя исполнителя",
            performers.lastname AS "Фамилия исполнителя",
            performers.email AS "Почта исполнителя",
            performers.telegram AS "Телеграм исполнителя"
        FROM appeals
        LEFT OUTER JOIN users ON appeals.user_id = users.id
        LEFT OUTER JOIN performers ON performers.category = appeals.category 
        RIGHT OUTER JOIN internal_sale ON appeals.lte_id = internal_sale.id
        order by appeals.id 
    """
    common_file.get_excel(bot, message, admin_id, 'output_file.xlsx', sql_query)


def send_error(message):
    language = userClass.get_language(message)
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
    global broadcast_count
    if message.text.upper() == "ДА":
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute('SELECT id FROM users')
        users_id = cur.fetchall()
        cur.close()
        conn.close()
        for user_id in users_id:
            try:
                if broadcast_message.photo:
                    photo_id = broadcast_message.photo[-1].file_id
                    bot.send_photo(user_id[0], photo_id, broadcast_message.caption)
                if broadcast_message.audio:
                    audio_id = broadcast_message.audio.file_id
                    bot.send_video(user_id[0], audio_id, broadcast_message.caption)
                if broadcast_message.video:
                    video_id = broadcast_message.video.file_id
                    bot.send_video(user_id[0], video_id, broadcast_message.caption)
                if broadcast_message.voice:
                    voice_id = broadcast_message.voice.file_id
                    bot.send_voice(user_id[0], voice_id, broadcast_message.caption)
                if broadcast_message.text:
                    bot.send_message(user_id[0], broadcast_message.text)
            except:
                continue
        bot.send_message(message.chat.id, "Рассылка отправлена")
    elif message.text.upper() == "НЕТ":
        bot.send_message(message.chat.id, "Вызовите функцию /broadcast чтобы вызвать комманду рассылки еще раз")
    else:
        rus.send_error(bot, message)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message = message.text
    commands_historyClass.cm_sv_db(message, get_message)
    if str(message.chat.id)[0] == '-':
        return
    language = userClass.get_language(message)
    if language == 'rus':
        text(message, get_message, rus)
    elif language == 'kaz':
        text(message, get_message, kaz)
    else:
        lang(message)
    # except Exception as ex:
    #     send_error(message)
    #     bot.send_message(message.chat.id, str(ex.args))
        # register(message)


def text(message, get_message, lang_py):
    if get_message == "🧐Мой профиль" or get_message == "🧐Менің профилім":
        user_infoClass.clear_appeals(message)
        lang_py.profile(bot, message)
    elif get_message in lang_py.faq_1.keys():
        user_infoClass.clear_appeals(message)
        bot.send_message(message.chat.id, lang_py.faq_1[message.text])
    elif get_message in lang_py.faq_2.keys():
        user_infoClass.clear_appeals(message)
        bot.send_message(message.chat.id, lang_py.faq_2[message.text])
    elif get_message in lang_py.faq_procurement_portal.keys():
        user_infoClass.clear_appeals(message)
        bot.send_message(message.chat.id, lang_py.faq_procurement_portal[message.text])
    elif get_message in lang_py.faq_procurement_activities.keys():
        user_infoClass.clear_appeals(message)
        bot.send_message(message.chat.id, lang_py.faq_procurement_activities[message.text])
    elif get_message in lang_py.biot_field:
        user_infoClass.clear_appeals(message)
        lang_py.biot(bot, message)
    elif get_message in lang_py.kb_field:
        user_infoClass.clear_appeals(message)
        lang_py.kb(bot, message)
    elif get_message in lang_py.adapt_field:
        user_infoClass.clear_appeals(message)
        lang_py.adaption(bot, message)
    elif get_message == "📄У меня есть вопрос" or get_message == "📄Менің сұрағым бар":
        lang_py.questions(bot, message)
    elif get_message == "Мои обращения" or get_message == "Менің өтініштерім" \
            or get_message == "Оставить обращение" or get_message == "Өтінішті қалдыру" \
            or get_message == "Админ панель" \
            or user_infoClass.get_appeal_field(message):
        lang_py.appeal(bot, message, message.text)
    elif get_message == '🖥Портал "Бірлік"' or get_message in lang_py.portal_bts or get_message in lang_py.portal_ \
            or get_message in lang_py.portal_guide:
        user_infoClass.clear_appeals(message)
        lang_py.portal(bot, message)
    elif get_message in lang_py.lte_ or get_message in lang_py.lte_files:
        lang_py.lte(message, bot)
    elif str(message.chat.id) in userClass.get_users_id():
        if user_infoClass.get_glossary(message):
            lang_py.glossary(bot, message)
        elif user_infoClass.get_instr(message) and message.text in lang_py.kb_field_all:
            lang_py.instructions(bot, message)
        else:
            user_infoClass.clear_appeals(message)
            lang_py.send_error(bot, message)
    elif get_message in lang_py.faq_field or get_message in branches:
        user_infoClass.clear_appeals(message)
        lang_py.faq(bot, message)
    elif get_message in drb_regions or get_message in ods_regions:
        user_infoClass.clear_appeals(message)
        lang_py.func_region(bot, message)
    else:
        user_infoClass.clear_appeals(message)
        lang_py.send_error(bot, message)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    language = userClass.get_language(message)
    if user_infoClass.get_appeal_field(message):
        if language == 'rus':
            rus.appeal(bot, message, message.text)
        elif language == 'kaz':
            kaz.appeal(bot, message, message.text)
    else:
        send_error(message)


try:
    bot.polling(none_stop=True)
except (ConnectionError, TimeoutError) as ex:
    print(str(ex.args))

