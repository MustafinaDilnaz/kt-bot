from datetime import timedelta

import requests
from telebot import *
import db_connect

# categories = {
#     'Learning.telecom.kz | Техническая поддержка': 'info.ktcu@telecom.kz',
#     'Обучение | Корпоративный Университет': 'info.ktcu@telecom.kz',
#     'Служба поддержки “Нысана"': 'nysana@cscc.kz',
#     'Обратиться в службу комплаенс': 'tlek.issakov@telecom.kz',
# }
categories = {
    'Learning.telecom.kz | Техническая поддержка': {
        "id": "187663574",
        "name": "Оспанов Тамирлан",
        "phone_num": "87777777777",
        "email": "info.ktcu@telecom.kz",
        "telegram": "@tamirlan"
    },
    'Обучение | Корпоративный Университет': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "info.ktcu@telecom.kz",
        "telegram": "@dilnaz.mustafina"
    },
    'Служба поддержки "Нысана"': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "nysana@cscc.kz",
        "telegram": "@dilnaz.mustafina"
    },
    'Обратиться в службу комплаенс': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "tlek.issakov@telecom.kz",
        "telegram": "@dilnaz.mustafina"
    },
}
faq_field = ["Часто задаваемые вопросы", "Демеу", "Вопросы к HR", "Вопросы по займам"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["👷Заполнить карточку БиОТ", "Опасный фактор/условие", "Поведение при выполнении работ", "Предложения/Идеи"]
kb_field = ["🗃️База знаний", "База инструкций", "Глоссарий", "Полезные ссылки", "Сервис и Продажи"]
kb_field_all = ["Логотипы и Брендбук", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus | Инструкции",
                "CheckPoint VPN | Удаленная работа", "Командировка | Порядок оформления",
                "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП",
                "Данные по серверам филиалов", "Инструкция по установке Lotus", "Установочный файл Lotus",
                "АО 'Казахтелеком'", 'Как посмотреть подключенные услуги', 'Как оплатить услугу',
                'Как посмотреть о деталях оплаты', "Раздел 'Мои Услуги'",
                "Корпоративный университет", "ADSL модем", "IDTV приставки",
                "ONT модемы", "Router 4G and Router Ethernet", "Инструкция по установке CheckPoint",
                "Установочный файл CheckPoint", ]
instr_field = ["Брендбук и логотипы", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus & CheckPoint"]
adapt_field = ["Welcome курс | Адаптация"]
portal_bts = ["Что такое портал 'Бірлік'?", "Как войти на портал?", "Оставить обращение на портал", "Бірлік Гид"]
portal_ = ["Мобильная версия", "ПК или ноутбук", "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП",
           "iOS", "Android", "Есть checkpoint", "Нет checkpoint"]
portal_guide = ["Куда обратиться для обратной связи - комментарии и предложения?",
                "Где на портале можно ознакомиться со стратегией компании?",
                "Как создать сообщество?", "Как запланировать отпуск в экосистеме?",
                "Как поблагодарить коллегу?", "Как создать опрос в экосистеме?",
                "Как купить товар со скидкой в Казахтелеком магазине?", "Как купить мерч Казахтелеком?",
                "Где увидеть скидки и акции для работников Компании?"]

faq_1 = {
    'Ha кого направлена программа “Демеу” в AO “Казахтелеком”?':
        'Социальная поддержка Программы «Демеу» AO «Казахтелеком»:  (далее - Программа) направлена работникам по статусу: \
  \n1) многодетная семья - семья, имеющая в своем составе четырех и более совместно проживающих несовершеннолетних детей, в том числе детей, обучающихся по очной форме обучения в организациях среднего, \
  технического и профессионального, послесреднего, высшего и (или) послевузовского образования после достижения ими совершеннолетия до времени окончания образования (но не более чем до достижения \
  двадцатитрехлетнего возраста); '
        '\n2) семья c детьми-инвалидами - семья, имеющая в своем составе ребенка (детей) до восемнадцати лет, имеющего(-их) нарушение здоровья co стойким расстройством функций организма,\
  обусловленное заболеваниями, увечьями (ранениями, травмами, контузиями), их последствиями, дефектами, которые приводят к ограничению жизнедеятельности и необходимости ero (их) социальной защиты; \
  \n3) семья, усыновившая/удочерившая более 2-x детей - семья, имеющая в своем составе более 2-x несовершеннолетних усыновленных/удочеренных детей, которые состоят на диспансерном учете по состоянию здоровья, и единственного кормильца. \
  \n4) Работникам грейда A8-B4 устанавливается социальная поддержка по оплате выпускного курса обучения (без учета расходов на проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем учебном заведении (далее - BYZ). \
  \nBce виды социальной поддержки оказываются работникам Общества, имеющим на момент предоставления социальной поддержки стаж непрерывной работы в Обществе не менее 3-x лет.\
  \n*Обращения физических лиц ob оказании социальной поддержки/помощи, не состоящих в трудовых отношениях c AO «Казахтелеком», к рассмотрению не принимаются.',
    'Виды социальной поддержки для работников': '1) возмещение расходов, связанных c приобретением путевок в детские оздоровительные лагеря; \
  \n2) возмещение расходов, связанных c приобретением путевок в детские оздоровительные санатории (для детей-инвалидов); \
  \n3) материальная помощь на приобретение лекарственных средств для детей; \
  \n4) материальная помощь на питание учащихся школ; \n5) материальная помощь к началу учебного года; \
  \n6) возмещение средств за медицинскую реабилитацию/индивидуальную программу реабилитации ребенка (для детей-инвалидов); \
  \n7) возмещение средств за специальные образовательные программы (для детей-инвалидов); \
  \n8) возмещение средств за посещение специальных коррекционных организаций (для детей-инвалидов); \
  \n9) материальная помощь выпускникам школ, не достигшим на дату окончания школы совершеннолетия и окончившим учебу на отлично; \
  \n10) возмещение (работникам грейда A8-B4) расходов по оплате выпускного курса обучения (без учета расходов на '
                                                'проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем учебном заведении '
                                                '(далее - BYZ).',
    'Процесс подачи заявления в социальную комиссию':
        'Основанием для рассмотрения вопроса об оказании социальной поддержки является заявление работника \n'
        'ЦА/филиала, поданное в Социальную комиссию ЦА/филиала с приложением подтверждающих документов.',
    'Где оформлять заявление?': 'Заявление оформляете в своей рабочей базе(БРД). Специальных баз нет.',
    'Председатель социальной комиссии': 'Председатель Социальной комиссии в филиалах - Генеральный директор филиала. '
                                        'В ЦА – Главный директор по операционной эффективности',
}
faq_2 = {
    'Как получить справку c места работы?': 'Заявку на получение спpaвки c места работы необходимо оформить в Базе «Заявки ОЦО HR». \nСоздать новый – выбрать наименование Вашего филиала – заявка на выдачу справки с места работы – заполнить ФИО сотрудника, вид справки и необходимые критерии (язык, стаж, должностной оклад, средняя заработная плата) – сохранить заявку – Отправить в ОЦО В Заявке автоматически будет указан Исполнитель Вашей заявки.',
    'Как создать учетную запись Lotus и доступ к ИС и БРД?': 'Для создания учетной записи Lotus Notes необходимо обратиться к Вашему курирующему руководителю/наставнику/делопроизводителю структурного подразделения для оформления заявки в Базе ЕСУД (Единая система управления доступом). \nПо мере готовности учетной записи (файл с логином и паролем),'
                                                             ' необходимо оформить заявку в Help Desk по номеру: +7 727 2587304 После установления учетной записи Lotus Notes, необходимо самостоятельно создать заявку в Базе ЕСУД с указанием необходимого для Вас доступа к ИС и БД.',
    'Куда обратиться если забыл пароль или сбой в Lotus?': 'Оставить заявку HelpDesk +77272587304 по возникшим вопросам.',
    'Как оплачиваются листы временной нетрудоспособности?': 'Листы временной нетрудоспособности для работников (членов профсоюзной организации и присоединившихся к Коллективному договору) оплачиваются в зависимости от непрерывного стажа работы в компании: \n- до 2-х лет включительно - в соответствии с законодательством Республики Казахстан; \n- до 5 лет - 40% средней заработной платы; \n- свыше 5 лет - 70% средней заработной платы за дни временной нетрудоспособности.',
    'Кто заполняет больничный лист?': 'Больничный лист заполняет табельщик/делопроизводитель структурного подразделения. B больничном листе отражаете  наименование филиала "Дивизион по розничному бизнесу - филиал AO "Казахтелеком" и свою должность.',
    'Кому сдавать лист временной нетрудоспособности (больничный лист)?': 'Прежде чем сдать лист временной нетрудоспособности, его необходимо заполнить и подписать  y своего непосредственного руководителя. \nВ случае, если в Вашем офисе отсутствует работник фронт-офиса ОЦО HR - отсканировать с двух сторон БЛ и оформить заявкой в Базе Заявки ОЦО HR; в противном случае – сдать заполненный оригинал БЛ работнику фронт-офиса ОЦО HR.',
    'Как вступить в Профсоюз?': 'Для вступления в Локальный профсоюз, необходимо оформить заявление о вступлении в Профсоюз Вашего филиала (шаблон о вступлении в Профсоюз можно получить у работника фронт-офиса ОЦО HR) и оформить заявку в Базе Заявки в ОЦО ЗП об удержании профсоюзных взносов. Процент удержания составляет – 1 %.',
    'Страховка по ДМС (добровольное медицинское страхование)': 'Страховка по ДМС (добровольное медицинское страхование) осуществляется  работникам имеющих стаж работы в Обществе более 3-x  лет, при условии возможности страхового покрытия',
    'Где найти телефон коллег?': 'Телефон коллеги Вы можете найти базе "Телефонный справочник Общества" - номера телефонов по Фамилии, поиск сотрудников по подразделению',
    'Обходной лист. Когда ero оформлять?': '1) При оформление заявления на увольнение, автоматически сформирован в третьем листе обходной лист и указаны подписанты.\n2) При переводе/одностороннем порядке/ в филиал обходной лист оформляем в своих рабочих базах',
}
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("😊Welcome курс | Адаптация")
# button2 = types.KeyboardButton("Обращения")
button3 = types.KeyboardButton("🗃️База знаний")
button4 = types.KeyboardButton("👷Заполнить карточку БиОТ")
button5 = types.KeyboardButton("📄У меня есть вопрос")
button6 = types.KeyboardButton("🧐Мой профиль")
button7 = types.KeyboardButton("🖥Портал 'Бірлік'")
markup.add(button, button3, button7, button5, button4, button6)


def send_welcome_message(bot, message):
    welcome_message = f'Привет, {db_connect.get_firstname(message)} 👋'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    with open("images/menu.jpg", 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "B моем сценарии есть несколько команд:\
        \n/menu — вернуться в главное меню (ты можешь сделать это в любой момент прохождения демо!)\
        \n/help — связаться c разработчиками (используй эту команду, если столкнешься c трудностями "
                                      "или y тебя есть предложения для улучшения)\
    \n/start — Перезапустить бота \
    \n/language - Сменить язык бота\
    \n\nKoмaнды ты можешь найти во вкладке «Меню» в строке сообщений (слева внизу) или просто пришли название команды, "
                                      "только значок «/» не забывай!")


def send_error(bot, message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


def adaption(bot, message):
    if message.text == "Welcome курс | Адаптация😊":
        db_connect.cm_sv_db(message, 'Welcome курс | Адаптация')
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton("Рассказывай!", callback_data="Рассказывай!")
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, f'Добро пожаловать в AO “Казахтелеком”🥳')
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Только для начала расскажу тебе, как мной пользоваться 🫡",
                         reply_markup=markup_adapt)


def performer_text(appeal_info):
    text = f"Обращения <b>ID</b> {appeal_info[0]}\n\n" \
           f" Статус: {str(appeal_info[2])}\n" \
           f" Дата создания: {str(appeal_info[5])}\n" \
           f" Категория: {str(appeal_info[3])}\n" \
           f" Текст обращения: {str(appeal_info[4])}\n" \
           f" Дата последнего изменения статуса: {str(appeal_info[6])}\n\n" \
           f"Исполнитель\n" \
           f" ФИО: {categories.get(str(appeal_info[3]), {}).get('name', None)}\n" \
           f" Номер телефона: {categories.get(str(appeal_info[3]), {}).get('phone_num', None)}\n" \
           f" Email: {categories.get(str(appeal_info[3]), {}).get('email', None)}\n" \
           f" Telegram: {categories.get(str(appeal_info[3]), {}).get('telegram', None)}\n\n" \
           f" Комментарий: {str(appeal_info[8])}"
    return text


def call_back(bot, call):
    if call.data == 'Рассказывай!':
        db_connect.cm_sv_db(call.message, 'Рассказывай!')
        bot.send_photo(call.message.chat.id, photo=open('images/picture.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно", callback_data="Понятно")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "У меня есть клавиатура⌨️, пользуясь которой ты можешь переходить по "
                                               "разделам и получать нужную для тебя информацию",
                         reply_markup=markup_callback)
    elif call.data == "Понятно":
        bot.send_photo(call.message.chat.id, photo=open('images/hello.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Поехали!", callback_data="Поехали!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Жми на кнопку ниже👇🏻 и мы продолжаем.", reply_markup=markup_callback)
    elif call.data == "Поехали!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "AO 'Казахтелеком' - это крупнейшая телекоммуникационная компания "
                                               "Казахстана,  образованная в соответствии c постановлением Кабинета "
                                               "Министров Республики\Казахстан от 17 июня 1994 года.\n\n📌У нас есть "
                                               "краткая история o компании, которую мы подготовили специально для тебя."
                                               "Просто открой файлы ниже и ознакомься c ней.")
        bot.send_document(call.message.chat.id, open('images/PDF-1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/PDF-2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, давай!", callback_data="Да, давай!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Если все понятно, то продолжаем?", reply_markup=markup_callback)
    elif call.data == "Да, давай!":
        bot.send_message(call.message.chat.id, "У тебя уже есть Бадди?😁")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Если еще нет, не расстраивайся, он найдет тебя в ближайшее время!")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, хочу узнать больше!", callback_data="Да, хочу узнать больше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Ты спросишь, a кто это и для чего он мне нужен? Отвечаю)",
                         reply_markup=markup_callback)
    elif call.data == "Да, хочу узнать больше!":
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Так что, проверь свой корпоративный e-мэйл, возможно тебе уже пришло "
                                               "сообщение от Твоего Бадди c предложением встретиться, познакомиться и "
                                               "рассказать o программе адаптации в нашей Компании.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Принято!", callback_data="Принято!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-3.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Принято!":
        bot.send_message(call.message.chat.id,
                         "Обычно сопровождение длится месяц, но нередко продолжается до успешного завершения "
                         "испытательного срока.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Кстати, участником программы Бадди может стать сотрудник любого отдела, и это здорово - "
                         "расширяются горизонтальные и вертикальные связи.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Круто, продолжаем дальше!",
                                                     callback_data="Круто, продолжаем дальше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Позже и Ты тоже можешь стать Бадди и помогать будущим новичкам адаптироваться! 😊",
                         reply_markup=markup_callback)
    elif call.data == "Круто, продолжаем дальше!":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-1")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-1":
        bot.send_message(call.message.chat.id, "Наша компания состоит из 9 филиалов "
                                               "аббревиатуры которых ты точно будешь слышать в работе каждый день.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Поэтому давай познакомимся co структурой компании.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "A на случай если ты столкнешься c незнакомыми для тебя\
                                             терминами или аббревиатурами, то мы подготовили для тебя глоссарий в базе знаний.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Базу знаний ты всегда можешь найти в главном меню.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-3")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-3":
        bot.send_message(call.message.chat.id, 'B компании AO "Казахтелеком" есть продукты по разным направлениям:\
                                             \n🌍Интepнeт\n📞Teлeфoния\n📹Bидeoнabлюдeниe\n🖥️TV+\n🛍️Maraзин shop.telecom.kz')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-4")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Актуальную информацию по продуктам и их тарифам ты всегда сможешь найти на сайте telecom.kz",
                         reply_markup=markup_callback)
    elif call.data == "Далее-4":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-5")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-5":
        bot.send_message(call.message.chat.id, "☎️B AO 'Казахтелеком' интегрирована горячая линия «Нысана», "
                                               "куда каждый работник сможет обратиться посредством QR-кода "
                                               "или по контактам ниже в картинке")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-6":
        bot.send_message(call.message.chat.id, "Отлично! \nMы c тобой познакомились c основной информацией o компании.\
                                             \n\nTы всегда можешь воспользоваться базой знаний или разделом часто задаваемых вопросов в главном меню бота.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно!", callback_data="Понятно!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/picture.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Понятно!":
        db_connect.cm_sv_db(call.message, 'Welcome курс | Адаптация end')
        bot.send_message(call.message.chat.id, "Поздравляю!\nTы прошел Welcome курс.\n\nДoбpo пожаловать в компанию!.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду /menu")
    elif call.data == "checkPoint":
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton("iOS", callback_data="iOS")
        button_p2 = types.InlineKeyboardButton("Android", callback_data="Android")
        markup_p.add(button_p1, button_p2)
        bot.send_message(str(call.message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif call.data == portal_[5]:
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton(text="Ссылка на App Store",
                                               url="https://apps.apple.com/ru/app/check-point-capsule-connect/id506669652")
        markup_p.add(button_p1)
        bot.send_message(str(call.message.chat.id), "Ссылка на видео инструкцию checkpoint на iOS\nhttps://youtu.be/giK26_GgVgE ", reply_markup=markup_p)
    elif call.data == portal_[6]:
        markup_p = types.InlineKeyboardMarkup()
        button_p2 = types.InlineKeyboardButton(text="Ссылка на PlayMarket",
                                               url="https://play.google.com/store/apps/details?id=com.checkpoint.VPN&hl=en&gl=US&pli=1")
        markup_p.add(button_p2)
        bot.send_message(str(call.message.chat.id), "Ссылка на видео инструкцию checkpoint на Android\nhttps://youtu.be/KjL9tpunb4U", reply_markup=markup_p)
    elif str(call.data).isdigit():
        appeal_id = str(call.data)
        appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
        image_data = db_connect.get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        text = performer_text(appeal_info)
        bot.send_message(call.message.chat.id, text)
    # elif db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)admin$') is not None:
    #     appeal_id = db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)admin$')
    #     appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
    #     callback_d = f"{appeal_id}statusdecided"
    #     btn_text = "Изменить статус на Решено"
    #     if appeal_info[9]:
    #         text = f"ID обращения {appeal_id}\n\n" \
    #                f" Статус: {str(appeal_info[2])}\n" \
    #                f" Дата создания: {str(appeal_info[5])}\n" \
    #                f" Категория: {str(appeal_info[3])}\n" \
    #                f" Текст обращения: {str(appeal_info[4])}\n" \
    #                f" Дата последнего изменения статуса: {str(appeal_info[6])}\n" \
    #                f" Комментарий: {str(appeal_info[8])}\n\n"
    #         if str(appeal_info[2]) == "Обращение принято":
    #             callback_d = f"{appeal_id}statusinprocess"
    #             btn_text = "Изменить статус на 'В процессе'"
    #     else:
    #         appeal_info = db_connect.get_appeal_by_id_inner_join_users(appeal_id)[0]
    #         text = f"ID обращения {appeal_id}\n\n" \
    #                f" Статус: {str(appeal_info[1])}\n" \
    #                f" Дата создания: {str(appeal_info[4])}\n" \
    #                f" Категория: {str(appeal_info[2])}\n" \
    #                f" Текст обращения: {str(appeal_info[3])}\n" \
    #                f" Дата последнего изменения статуса: {str(appeal_info[5])}\n" \
    #                f" Комментарий: {str(appeal_info[6])}\n\n" \
    #                f"Пользователь\n" \
    #                f" ФИО: {str(appeal_info[9])} {str(appeal_info[8])}\n" \
    #                f" Номер телефона: {str(appeal_info[11])}\n" \
    #                f" Email: {str(appeal_info[12])}\n" \
    #                f" Telegram: {str(appeal_info[7])}\n" \
    #                f" Филиал: {str(appeal_info[13])}"
    #         if str(appeal_info[1]) == "Обращение принято":
    #             callback_d = f"{appeal_id}statusinprocess"
    #             btn_text = "Изменить статус на 'В процессе'"
    #     markup_a = types.InlineKeyboardMarkup(row_width=1)
    #     button_a = types.InlineKeyboardButton(btn_text, callback_data=callback_d)
    #     callback_d = f"{appeal_id}addcomment"
    #     button_a1 = types.InlineKeyboardButton("Добавить комментарий", callback_data=callback_d)
    #     markup_a.add(button_a, button_a1)
    #     bot.send_message(call.message.chat.id, text, reply_markup=markup_a)
    elif db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)statusinprocess') is not None \
            or db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)statusdecided$') is not None:
        appeal_id = db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)statusinprocess')
        if appeal_id is None:
            appeal_id = db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)statusdecided$')
            db_connect.set_status(appeal_id, "Решено")
        else:
            db_connect.set_status(appeal_id, "В процессе")
        now = datetime.now() + timedelta(hours=6)
        now_updated = db_connect.remove_milliseconds(now)
        db_connect.set_date_status(appeal_id, str(now_updated))
        bot.send_message(call.message.chat.id, "Статус изменен")
        db_connect.admin_appeal_callback(call, bot, add_comment)
        appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
        text = performer_text(appeal_info)
        bot.send_message(appeal_info[1], "Статус вашего обращения изменен")
        image_data = db_connect.get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        bot.send_message(appeal_info[1], text)
        if db_connect.get_status(appeal_id)[0][0] == "Решено":
            markup_callback = types.InlineKeyboardMarkup(row_width=5)
            for i in range(1, 6):
                callback_d = str(i) + "evaluation" + str(appeal_info[0])
                button_callback = types.InlineKeyboardButton(i, callback_data=callback_d)
                markup_callback.add(button_callback)
            bot.send_message(appeal_info[1], "Оцените решенное обращение от 1 до 5\n\nГде 1 - очень плохо, "
                                             "5 - замечательно", reply_markup=markup_callback)
    # elif db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)addcomment') is not None:
    #     appeal_id = db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)addcomment')
    #     msg = bot.send_message(call.message.chat.id, 'Введите комментарий')
    #     bot.register_next_step_handler(msg, add_comment, bot, appeal_id)
    elif db_connect.extract_numbers_from_status_change_decided(str(call.data)) is not None:
        evaluation, appeal_id = db_connect.extract_numbers_from_status_change_decided(str(call.data))
        db_connect.set_evaluation(appeal_id, evaluation)
        bot.edit_message_text("Спасибо за Ваш отзыв и за то\nВы помогаете нам стать лучше", call.message.chat.id,
                              call.message.message_id)
        bot.answer_callback_query(call.id)
    else:
        db_connect.admin_appeal_callback(call, bot, add_comment)


def add_comment(message, bot, appeal_id):
    comment = message.text + " \n" + str(db_connect.get_comment(appeal_id)[0][0])
    db_connect.set_comment(appeal_id, comment)
    appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
    image_data = db_connect.get_image_data(appeal_id)
    text = performer_text(appeal_info)
    bot.send_message(appeal_info[1], "Добавлен комментарий к вашему обращению")
    try:
        bot.send_photo(appeal_info[1], image_data)
    except:
        print("error")
    bot.send_message(appeal_info[1], text)
    bot.send_message(message.chat.id, "Комментарий добавлен")


def appeal(bot, message, message_text):
    db_connect.set_appeal_field(message, True)
    # if message_text == "Обращения":
    #     db_connect.cm_sv_db(message, 'Обращения')
    #     markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1_ap = types.KeyboardButton("Мои обращения")
    #     button2_ap = types.KeyboardButton("Оставить обращение")
    #     if db_connect.check_id(categories, str(message.chat.id)):
    #         markup_ap.add(types.KeyboardButton("Админ панель для обращений"))
    #     markup_ap.add(button1_ap, button2_ap)
    #     bot.send_message(message.chat.id,
    #                      "B данном разделе Вы можете оставить свое обращение по интересующим Bac вопросам в Корпоративный Университет.",
    #                      reply_markup=markup_ap)
    #     time.sleep(0.75)
    #     bot.send_message(message.chat.id,
    #                      "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
    if message_text == "Мои обращения":
        db_connect.cm_sv_db(message, 'Мои обращения')
        markup_a = db_connect.appealInlineMarkup(message)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Здесь вы можете отслеживать статусы ваших обращений",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Тут пока пусто, "
                                              "\nно Вы можете оставить обращение и оно будет отображаться здесь")
    elif message_text == "Оставить обращение" or message_text == portal_bts[2]:
        db_connect.cm_sv_db(message, 'Оставить обращение')
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Да")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Информация верна?", reply_markup=markup_ap)
    elif message_text == "Да":
        if db_connect.get_category_users_info(message) == "portal":
            appeal(bot, message, "portal")
            return
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap = db_connect.generate_buttons(categories, markup_ap)
        bot.send_message(message.chat.id, "Выберите категорию обращения", reply_markup=markup_ap)
    # elif message_text == "Анонимно":
    #     db_connect.cm_sv_db(message, 'Анонимно')
    #     db_connect.set_is_appeal_anon_users_info(message.chat.id, True)
    #     markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    #     markup_ap = generate_buttons(categories, markup_ap)
    #     bot.send_message(message.chat.id,
    #                      "Выберите категорию обращения",
    #                      reply_markup=markup_ap)
    elif message_text == "portal":
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')
    elif message_text in categories.keys():
        db_connect.cm_sv_db(message, message_text)
        db_connect.set_category(message, message.text)
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:\nВы также можете скинуть фотографию')
    elif db_connect.get_appeal_field(message) and db_connect.get_category_users_info(message) != ' ':
        now = datetime.now() + timedelta(hours=6)
        now_updated = db_connect.remove_milliseconds(now)
        category = db_connect.get_category_users_info(message)
        if category == "portal":
            user_info = f"Имя Фамилия: {db_connect.get_firstname(message)} {db_connect.get_lastname(message)}\n" \
                        f"Табельный номер: {db_connect.get_table_number(message)}\n" \
                        f"Номер телефона: {db_connect.get_phone_number(message)}\n" \
                        f"Email: {db_connect.get_email(message)}\n" \
                        f"Филиал: {db_connect.get_branch(message.chat.id)}"
            new_message = f'{user_info} \n {message.text}'
            db_connect.send_gmails(new_message, "Портал 'Бірлік'")
            bot.send_message(str(message.chat.id), "Ваше обращение успешно отправлено")
            return
        performer_id = categories.get(category, {}).get('id', None)
        if db_connect.get_is_appeal_anon_users_info(message.chat.id):
            appeal_id = db_connect.add_appeal(message.chat.id, "Обращение принято", category, message.text,
                                              now_updated, now_updated, performer_id, ' ', True)
            text = f"ID Обращения {appeal_id}\n" \
                   f"Статус: {db_connect.get_status(appeal_id)[0][0]}\n" \
                   f"Категория: {db_connect.get_category_users_info(message)}\n" \
                   f"Обращение: {message.text}\n" \
                   f"Дата создания: {now_updated}"
        else:
            appeal_id = db_connect.add_appeal(message.chat.id, "Обращение принято", category, message.text,
                                              now_updated, now_updated, performer_id, ' ', False)
            text = f"ID Обращения {appeal_id}\n\n" \
                   f"Статус: {db_connect.get_status(appeal_id)[0][0]}\n" \
                   f"Имя Фамилия: {db_connect.get_firstname(message)} {db_connect.get_lastname(message)}\n" \
                   f"Табельный номер: {db_connect.get_table_number(message)}\n" \
                   f"Номер телефона: {db_connect.get_phone_number(message)}\n" \
                   f"Почта: {db_connect.get_email(message)}\n" \
                   f"Категория: {db_connect.get_category_users_info(message)}\n" \
                   f"Обращение: {db_connect.get_appeal_text(appeal_id)}\n" \
                   f"Дата создания: {now_updated}"
        bot.send_message(message.chat.id, "Ваше обращения принято")
        bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню "
                                          "команд слева от строки ввода.")
        if message.photo:
            file_info: object = bot.get_file(message.photo[-1].file_id)
            file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(db_connect.TOKEN, file_info.file_path))
            db_connect.set_image_data(appeal_id, file)
            image_data = db_connect.get_image_data(appeal_id)
            bot.send_photo(performer_id, image_data)
            db_connect.set_appeal_text(appeal_id, message.caption)
        markup_a1 = types.InlineKeyboardMarkup()
        callback_d = f"{appeal_id}statusinprocess"
        button_a = types.InlineKeyboardButton("Обращение просмотрено", callback_data=callback_d)
        markup_a1.add(button_a)
        bot.send_message(performer_id, text, reply_markup=markup_a1)
        db_connect.clear_appeals(message)
    else:
        db_connect.admin_appeal(bot, message, message_text, categories)
    # elif message_text == "Админ панель для обращений":
    #     markup_a = types.ReplyKeyboardMarkup()
    #     button1_a = types.KeyboardButton("Текущие Обращения")
    #     button2_a = types.KeyboardButton("Решенные Обращения")
    #     markup_a.add(button1_a, button2_a)
    #     bot.send_message(message.chat.id, "Выберите следующий шаг", reply_markup=markup_a)
    # elif db_connect.check_id(categories, str(message.chat.id)) and message_text == "Текущие Обращения":
    #     db_connect.admin_appeal(bot, message)
    # elif db_connect.check_id(categories, str(message.chat.id)) and message_text == "Решенные Обращения":
    #     get_excel_admin1(bot, message, "Решено")
    # else:
    #     db_connect.admin_appeal(bot, message)


def faq(bot, message):
    if message.text == "Часто задаваемые вопросы":
        db_connect.cm_sv_db(message, 'Часто задаваемые вопросы')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("Вопросы к HR")
        button_1 = types.KeyboardButton("Вопросы по займам")
        markup_faq.add(button_d, button_hr, button_1)
        bot.send_message(message.chat.id, "Здесь Вы можете найти ответы на часто задаваемые вопросы",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Ecли y Bac есть предложения/идеи по добавлению новых разделов или ответов "
                                          "на вопросы, то напишите нам на info.ktcu@telecom.kz - мы обязательно "
                                          "рассмотрим Ваше предложение и свяжемся c Вами.")
    elif message.text == "Демеу":
        db_connect.cm_sv_db(message, 'Демеу')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    elif message.text == "Вопросы к HR":
        db_connect.cm_sv_db(message, 'Вопросы к HR')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    elif message.text == "Вопросы по займам":
        db_connect.cm_sv_db(message, 'Вопросы по займам')
        branch = db_connect.get_branch(message.chat.id)
        if branch == "Центральный Аппарат":
            markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            markup_faq = db_connect.generate_buttons(branches[1:], markup_faq)
            bot.send_message(message.chat.id, "Выберите филиал", reply_markup=markup_faq)
        elif branch in branches[1:]:
            bot.send_message(message.chat.id, f"Филиал {branch}\n\n"
                                              "Все вопросы по займам Вы можете адресовать по следующим контактам:")
            func_branch(bot, message, branch)
    else:
        func_branch(bot, message, message.text)


def func_branch(bot, message, message_text):
    if message_text == "Корпоративный Университет":
        db_connect.cm_sv_db(message, 'Займы КУ')
        bot.send_message(message.chat.id, "Таспаева Гульшат Сериккалиевна\nФинансовый блок\nГлавный бухгалтер\n"
                                          "мобильный +7-701-780-64-34")
    elif message_text == "Дивизион Информационных Технологий":
        db_connect.cm_sv_db(message, 'Займы ДИТ')
        bot.send_message(message.chat.id, "Рысбеков Нуркен Алтынбаевич\nДепартамент финансового анализа и планирования"
                                          "\nВедущий экономист\nрабочий +7-727-398-91-53, мобильный +7-702-345-6292"
                                          "\n\nДусалиева Жанна Хабидуллаевна\nДепартамент финансового анализа и "
                                          "планирования\nВедущий специалист\nрабочий +7-727-398-91-49, "
                                          "мобильный +7-777-181-8919")
    elif message_text == "Дивизион по Корпоративному Бизнесу":
        db_connect.cm_sv_db(message, 'Займы ДКБ')
        bot.send_message(message.chat.id, "Уразбаев Ануар Талғатұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nВедущий экономист\n"
                                          "рабочий +7-727-244-70-54 мобильный +7-747-106-37-63\n\n"
                                          "Зинелов Әділет Маратұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nЭкономист\nрабочий +7-727-272-04-11 "
                                          "мобильный +7-707-315-55-59")
    elif message_text == "Дирекция Управления Проектами":
        db_connect.cm_sv_db(message, 'Займы ДУП')
        bot.send_message(message.chat.id, "Шекенова Нургуль Жантасовна\nEX сектор\nEX operations\nрабочий "
                                          "+7-717-224-97-46 мобильный +7-747-403-82-92)")
    elif message_text == "Дирекция Телеком Комплект":
        db_connect.cm_sv_db(message, 'Займы ДТК')
        bot.send_message(message.chat.id, "Рамазанқызы Айнұр\nОтдел экономики и финансов\nВедущий специалистn\n"
                                          "мобильный +7-777-241-2936")
    elif message_text == "Сервисная Фабрика":
        db_connect.cm_sv_db(message, 'Займы СФ')
        bot.send_message(message.chat.id, "Тезекбаев Максат Темирбековичn\nОтдел бюджетирования, экономики и финансов\n"
                                          "Ведущий экономист\nмобильный +7-708-694-75-40")
    elif message_text == "Дивизион по Розничному Бизнесу":
        db_connect.cm_sv_db(message, 'Займы ДРБ')
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = db_connect.generate_buttons(drb_regions, markup_r)
        bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_r)
    elif message_text == 'Обьединение Дивизион "Сеть"':
        db_connect.cm_sv_db(message, 'Займы ОДС')
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = db_connect.generate_buttons(ods_regions, markup_r)
        bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_r)


def func_region(bot, message):
    if message.text == "Алматинский регион, г.Алматы":
        bot.send_message(message.chat.id, "Бекен Назгуль Нурмахановна\nДРБ/Отдел учета расходов\nВедущий специалист\n"
                                          "мобильный +7-707-701-6110")
    elif message.text == "Западный, Центральный регион":
        bot.send_message(message.chat.id,
                         "Жумабейсова Гульшара Касимкуловна\nДРБ/Отдел ввода оплаты\nВедущий специалист"
                         "\nрабочий +7-713-254-50-45, мобильный +7-775 751-1269")
    elif message.text == "Северный, Южный, Восточный регионы":
        bot.send_message(message.chat.id,
                         "Суханбердиева Малика Дауреновна\nДРБ/Отдел ввода оплаты\nВедущий специалист\n"
                         "мобильный +7-708-566-6834")
    elif message.text == "ДЭСД 'Алматытелеком'":
        bot.send_message(message.chat.id, "Мусрепбекова Маржан Жексенбайқызы\nФЭБ\nВедущий экономист\n+77021737933, "
                                          "+77272975716")
    elif message.text == "Южно-Казахстанский ДЭСД":
        bot.send_message(message.chat.id, "Есенбекова Сауле Рахимжановна\nФЭБ\nЛогистик\n+77017605836, +77252530225")
    elif message.text == "Кызылординский ДЭСД":
        bot.send_message(message.chat.id, "Уракбаева Акканыш Утегуловна\nФЭБ\nВедущий экономист\n+77002151447, "
                                          "+77242264333")
    elif message.text == "Костанайский ДЭСД":
        bot.send_message(message.chat.id, "Жунусова Динара Тимурхановна\nФЭБ\nЭкономист 1 категории\n+77052153323, "
                                          "+77142573004")
    elif message.text == "Восточно-Казахстанский ДЭСД":
        bot.send_message(message.chat.id, "Беркимбаев Жаслан Жакауович\nФЭБ\nВедущий экономист\n+77142393364, "
                                          "+77142573373")
    elif message.text == "Атырауский ДЭСД":
        bot.send_message(message.chat.id, "Кенжетаева Гульнара  Сагиндыковна\nФЭБ\nВедущий экономист\n+77017987499, "
                                          "+77172577588")
    elif message.text == "Актюбинский ДЭСД":
        bot.send_message(message.chat.id, "Дуйсенов Бауыржан Рысбаевич\nФЭБ\nВедущий логистик\n+77053444748, "
                                          "+77292301077")
    elif message.text == "ДЭСД 'Астана'":
        bot.send_message(message.chat.id, "Уатаева Камшат Мейрхановна\nФЭБ\nВедущий экономист\n+77779939323, "
                                          "+77232200318")
    elif message.text == "ТУСМ-1":
        bot.send_message(message.chat.id, "Кан Людмила Трофимовна\nТБ\nИнженер электросвязи 1 категории\n+77012262288, "
                                          "+77273844921")
    elif message.text == "ТУСМ-6":
        bot.send_message(message.chat.id, "Жук Светлана Ивановна\nТБ\nИнженер электросвязи 1 категории\n+77771517171, "
                                          "+77222642713")
    elif message.text == "ТУСМ-8":
        bot.send_message(message.chat.id, "Клюшина Ирина Александровна\nТБ\nИнженер электросвязи 1 категории\n"
                                          "+77771472072, +77143192751")
    elif message.text == "ТУСМ-10":
        bot.send_message(message.chat.id, "Кенжебаев Самат Оспанұлы\nТБ\nИнженер электросвязи 2 категории\n"
                                          "+77075652955, +77172594103")
    elif message.text == "ТУСМ-11":
        bot.send_message(message.chat.id, "Усенова Балжан Тузеловна\nТБ\nИнженер электросвязи 1 категории\n"
                                          "+77056846921, +77252449534")
    elif message.text == "ТУСМ-13":
        bot.send_message(message.chat.id, "Туржигитова Венера Амангельдиновна\nТБ\nТехник линейных сооружений связи и "
                                          "абонентских устройств 1 категории\n+77473021977, +77122366397")
    elif message.text == "ТУСМ-14":
        bot.send_message(message.chat.id, "Арыстанова Нургуль Аманжуловна\nТБ\nТехник линейных сооружений связи и "
                                          "абонентских устройств 1 категории\n+77711863815, +77132530638")
    elif message.text == "ГА":
        bot.send_message(message.chat.id, "Арефьева Марина Александровна\nФЭБ\nЭкономист 1 категории\n+77053882043, "
                                          "+77273312070")


def biot(bot, message):
    if message.text == "👷Заполнить карточку БиОТ":
        db_connect.cm_sv_db(message, 'Заполнить карточку БиОТ')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Опасный фактор/условие")
        button2 = types.KeyboardButton("Поведение при выполнении работ")
        button3 = types.KeyboardButton("Предложения/Идеи")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id,
                         "Вы заметили опасный фактор, небезопасное поведение или y Bac есть предложения/идеи по улучшению безопасности и охраны труда на рабочем месте?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Bыбepитe необходимую классификацию события и заполните карточку БиОТ.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
    elif message.text == "Опасный фактор/условие":
        db_connect.cm_sv_db(message, 'Опасный фактор/условие')
        bot.send_message(message.chat.id, "Если Вы заметили опасный фактор или условие в процессе работы, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
    elif message.text == "Поведение при выполнении работ":
        db_connect.cm_sv_db(message, 'Поведение при выполнении работ')
        bot.send_message(message.chat.id, "Если Вы заметили риски в поведении при выполнении работ, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
    elif message.text == "Предложения/Идеи":
        db_connect.cm_sv_db(message, 'Предложения/Идеи')
        bot.send_message(message.chat.id, "Если y Bac есть предложения или идеи, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")


def instructions(bot, message):
    if message.text == "Логотипы и Брендбук":
        db_connect.cm_sv_db(message, 'Логотипы и Брендбук')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("АО 'Казахтелеком'")
        button2_i = types.KeyboardButton("Корпоративный университет")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    elif message.text == "Модемы | Настройка":
        db_connect.cm_sv_db(message, 'Модемы | Настройка')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("ADSL модем")
        button2_i = types.KeyboardButton("IDTV приставки")
        button3_i = types.KeyboardButton("ONT модемы")
        button4_i = types.KeyboardButton("Router 4G and Router Ethernet")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    elif message.text == "Lotus | Инструкции":
        db_connect.cm_sv_db(message, 'Lotus | Инструкции')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Данные по серверам филиалов")
        button2_i = types.KeyboardButton("Инструкция по установке Lotus")
        button3_i = types.KeyboardButton("Установочный файл Lotus")
        markup_instr.add(button1_i, button2_i, button3_i)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    # elif message.text == "portal.telecom.kz | Инструкции":
    #     db_connect.cm_sv_db(message, 'portal.telecom.kz | Инструкции')
    #     markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1 = types.KeyboardButton("Мобильная версия")
    #     button2 = types.KeyboardButton("ПК или ноутбук")
    #     markup_portal.add(button1, button2)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_portal)
    elif message.text == "CheckPoint VPN | Удаленная работа":
        db_connect.cm_sv_db(message, 'CheckPoint VPN | Удаленная работа')
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton("iOS", callback_data="iOS")
        button_p2 = types.InlineKeyboardButton("Android", callback_data="Android")
        markup_p.add(button_p1, button_p2)
        bot.send_message(str(message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif message.text == "Личный кабинет telecom.kz":
        db_connect.cm_sv_db(message, 'Личный кабинет telecom.kz')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Как оплатить услугу")
        button2_i = types.KeyboardButton("Как посмотреть о деталях оплаты")
        button3_i = types.KeyboardButton("Как посмотреть подключенные услуги")
        button4_i = types.KeyboardButton("Раздел 'Мои Услуги'")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    elif message.text == "Командировка | Порядок оформления":
        db_connect.cm_sv_db(message, 'Командировка | Порядок оформления')
        bot.send_message(message.chat.id, "Для получения информации о категории 'Командировка | Порядок оформления' "
                                          "перейдите по ссылке ниже "
                                          "\nhttps://wiki.telecom.kz/ru/instructionsopl/kommandiroviporyadok")
    # elif message.text == "Мобильная версия":
    #     bot.send_document(message.chat.id, document=open("images/инструкция VPN IOS.jpg", 'rb'))
    #     bot.send_document(message.chat.id, document=open("images/инструкция VPN Android.jpg", 'rb'))
    #
    # elif message.text == "ПК или ноутбук":
    #     markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1 = types.KeyboardButton("Как авторизоваться")
    #     button2 = types.KeyboardButton("Личный профиль")
    #     button3 = types.KeyboardButton("Из портала перейти в ССП")
    #     markup_pk.add(button1, button2, button3)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_pk)
    # elif message.text == "Как авторизоваться":
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как авторизоваться на портале "
    #                                       "работника через ПК?' перейдите по ссылке ниже "
    #                                       "\nhttps://youtu.be/vsRIDqt_-1A")
    # elif message.text == "Личный профиль":
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как заполнить личный профиль?' "
    #                                       "перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    # elif message.text == "Из портала перейти в ССП":
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как перейти из портала перейти в ССП'"
    #                                       " перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")
    elif message.text == "Данные по серверам филиалов":
        bot.send_document(message.chat.id, document=open("files/Данные по всем lotus серверам.xlsx", 'rb'))
    elif message.text == "Инструкция по установке Lotus":
        bot.send_document(message.chat.id, document=open("files/Инструкция по Lotus Notes на домашнем пк_.docx", 'rb'))
    elif message.text == "Установочный файл Lotus":
        bot.send_message(message.chat.id, "Установочный файл Lotus Notes: "
                                          "\nhttps://drive.google.com/drive/folders/1MrpjeXavmRnUMvYUiTcylhxAIEA6dvBb?usp=drive_link")
    elif message.text == "Инструкция по установке CheckPoint":
        bot.send_document(message.chat.id, document=open("files/Инструкция по установке CheckPoint.pdf", 'rb'))
    elif message.text == "Установочный файл CheckPoint":
        bot.send_document(message.chat.id, document=open("files/E85.40_CheckPointVPN.msi", 'rb'))
    elif message.text == "АО 'Казахтелеком'":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративный университет":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
    elif message.text == "Как оплатить услугу":
        bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
    elif message.text == "Как посмотреть о деталях оплаты":
        bot.send_document(message.chat.id,
                          document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
    elif message.text == "Как посмотреть подключенные услуги":
        bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
    elif message.text == "Раздел 'Мои Услуги'":
        bot.send_document(message.chat.id, document=open("files/раздел «МОИ УСЛУГИ».pdf", 'rb'))
    elif message.text == "ADSL модем":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'ADSL модем' перейдите по ссылке\nhttps://drive.google.com/drive/folders/1ZMcd4cVuX8_JUJ8OoN0rYx5d5DjwlEbz?usp=drive_link")
    elif message.text == "IDTV приставки":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'IDTV приставки' перейдите по ссылке\nhttps://drive.google.com/drive/folders/1ZFbUrKi9QITBLkJQ93I45dxhINSsgv7H?usp=drive_link")
    elif message.text == "ONT модемы":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'ONT модемы' перейдите по ссылке\nhttps://drive.google.com/drive/folders/1IiLJ14dKF3wQhoLYb18jJMLD6BNz3K7x?usp=drive_link")
    elif message.text == "Router 4G and Router Ethernet":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Router 4G and Router Ethernet' перейдите по ссылке\nhttps://drive.google.com/drive/folders/1EkzERKwa-DTnMW86-qJGbc_YAU2k6A74?usp=drive_link")


def kb(bot, message):
    if message.text == "🗃️База знаний":
        db_connect.cm_sv_db(message, 'База знаний')
        db_connect.set_bool(message, False, False)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button = types.KeyboardButton("База инструкций")
        button2 = types.KeyboardButton("Глоссарий")
        button3 = types.KeyboardButton("Полезные ссылки")
        markup.add(button2, button, button3)
        bot.send_message(message.chat.id, "Добро пожаловать в мобильную базу знаний!", reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Здесь Вы можете найти для себя нужную для Bac инструкцию или воспользоваться "
                         "поисковиком глоссарий по ключевым терминам, которые мы используем в нашей "
                         "компании каждый день.")
    elif message.text == "База инструкций":
        db_connect.cm_sv_db(message, 'База инструкций')
        db_connect.set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1 = types.KeyboardButton("Логотипы и Брендбук")
        button2 = types.KeyboardButton("Личный кабинет telecom.kz")
        button3 = types.KeyboardButton("Модемы | Настройка")
        button4 = types.KeyboardButton("Lotus | Инструкции")
        button6 = types.KeyboardButton("CheckPoint VPN | Удаленная работа")
        button7 = types.KeyboardButton("Командировка | Порядок оформления")
        markup_instr.add(button4, button6, button1, button7, button2, button3)
        bot.send_message(message.chat.id, "Здесь Вы можете найти полезную для Bac инструкцию.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Для выбора инструкции выберите категория, a затем саму инструкцию в меню-клавиатуре⌨️.")
    elif message.text == "Глоссарий":
        db_connect.cm_sv_db(message, 'Глоссарий')
        db_connect.set_bool(message, False, True)
        bot.send_message(message.chat.id, "Глоссарий терминов и аббревиатур в компании AO Казахтелеком.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Для того, чтобы получить расшифровку аббревиатуры или описание термина- "
                                          "начните вводить слово и отправьте для получения информации.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Важно!\n\n- Вводите слово без ошибок и лишних символов.\n - Аббревиатуры важно вводить c "
                         "верхним регистром. Например: ЕППК, ОДС, ДИТ.")
    # elif message.text == "Сервис и Продажи":
    #     db_connect.cm_sv_db(message, 'Сервис и Продажи')
    #     markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1_i = types.KeyboardButton("Личный кабинет telecom.kz")
    #     button2_i = types.KeyboardButton("Акции")
    #     button3_i = types.KeyboardButton("НРД")
    #     button4_i = types.KeyboardButton("Скрипты")
    #     button5_i = types.KeyboardButton("Тарифы")
    #     markup_instr.add(button1_i, button2_i, button3_i, button4_i, button5_i)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    elif message.text == "Полезные ссылки":
        db_connect.cm_sv_db(message, 'Полезные ссылки')
        db_connect.set_bool(message, False, False)
        time.sleep(0.5)
        markup = db_connect.useful_links()
        bot.send_message(message.chat.id, "Полезные ссылки", reply_markup=markup)


# def kb_service(bot, message):
#     if message.text == "Личный кабинет telecom.kz":
#         db_connect.cm_sv_db(message, 'Личный кабинет telecom.kz')
#         markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_i = types.KeyboardButton("Как оплатить услугу")
#         button2_i = types.KeyboardButton("Как посмотреть о деталях оплаты")
#         button3_i = types.KeyboardButton("Как посмотреть подключенные услуги")
#         button4_i = types.KeyboardButton("Раздел 'Мои Услуги'")
#         markup_instr.add(button1_i, button2_i, button3_i, button4_i)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
#     elif message.text == "Акции":
#         db_connect.cm_sv_db(message, 'Акции')
#         bot.send_document(message.chat.id, open("files/Скрипт по акции Почувствуй разницу!.docx", 'rb'))
#     elif message.text == "Скрипты":
#         db_connect.cm_sv_db(message, 'Скрипты')
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("НЛТ-2022")
#         button2_s = types.KeyboardButton("Текст SMS уведомления")
#         button3_s = types.KeyboardButton("Повышение Тарифов, Скрипт")
#         button4_s = types.KeyboardButton("Скрипт замена оборудования")
#         button5_s = types.KeyboardButton("Скрипт замена оборудования ПСС, УП")
#         button6_s = types.KeyboardButton("Скрипт с КАТВ на ТВ+")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "НЛТ-2022":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("2022 НЛТ_Bereket A для ЦРК")
#         button2_s = types.KeyboardButton("2022 НЛТ_Bereket А для ЦАП")
#         button3_s = types.KeyboardButton("2022 НЛТ_Керемет TV для ЦАП")
#         button4_s = types.KeyboardButton("2022 НЛТ_Керемет TV для ЦРК")
#         button5_s = types.KeyboardButton("2022 НЛТ_Керемет Моbile для ЦАП")
#         button6_s = types.KeyboardButton("2022 НЛТ_Керемет Моbile для ЦРК")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Тарифы":
#         db_connect.cm_sv_db(message, 'Тарифы')
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Save Desk - Тарифы для удержания")
#         button2_s = types.KeyboardButton("Раздаточный материал, Приказ 210")
#         button3_s = types.KeyboardButton("Действующие пакеты 2022")
#         button4_s = types.KeyboardButton("Дополнительные виды услуг и сервисов")
#         button5_s = types.KeyboardButton("Тарифы на организацию доступа к услугам")
#         button6_s = types.KeyboardButton("Тарифы на Интернет")
#         button7_s = types.KeyboardButton("Тарифы на услуги мобильной связи")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s, button7_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "НРД":
#         db_connect.cm_sv_db(message, 'НРД')
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Стандарты СО")
#         button2_s = types.KeyboardButton("Публичный договор")
#         button3_s = types.KeyboardButton("Правила класификации лицевых счетов")
#         markup_s.add(button1_s, button2_s, button3_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Save Desk - Тарифы для удержания":
#         bot.send_document(message.chat.id, open("files/Save Desk-Тарифы для удержания.pdf", 'rb'))
#     elif message.text == "Раздаточный материал, Приказ 210":
#         bot.send_document(message.chat.id,
#                           open("files/Раздаточный материал, с 01.08.2023, Приказ 210 от 28.07.2023.xlsx", 'rb'))
#     elif message.text == "Действующие пакеты 2022":
#         bot.send_document(message.chat.id, open("files/Каз-12 Действующие пакеты 2022.pdf", 'rb'))
#     elif message.text == "Дополнительные виды услуг и сервисов":
#         bot.send_document(message.chat.id, open("files/Каз-8-Дополнительные виды услуг и сервисов.pdf", 'rb'))
#     elif message.text == "Тарифы на организацию доступа к услугам":
#         bot.send_document(message.chat.id, open("files/Каз-4-Тарифы на организацию доступа к услугам.pdf", 'rb'))
#     elif message.text == "Тарифы на Интернет":
#         bot.send_document(message.chat.id, open("files/Каз 7-Тарифы на Интернет.pdf", 'rb'))
#     elif message.text == "Тарифы на услуги мобильной связи":
#         bot.send_document(message.chat.id, open("files/Каз 3-Тарифы на услуги мобильной связи.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Bereket A для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Bereket A для ЦРК.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Bereket А для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Bereket А для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет TV для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет TV для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет TV для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет TV  для ЦРК.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет Моbile для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет Моbile для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет Моbile для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет Моbile  для ЦРК.pdf", 'rb'))
#     elif message.text == "Текст SMS уведомления":
#         bot.send_document(message.chat.id, open("files/Текст SMS увед, каз и рус.pdf", 'rb'))
#     elif message.text == "Повышение Тарифов, Скрипт":
#         bot.send_document(message.chat.id, open("files/Повышение тарифов, Скрипт - с 1 августа 2023.pdf", 'rb'))
#     elif message.text == "Скрипт замена оборудования":
#         bot.send_document(message.chat.id, open("files/П_Скрипт замена оборудования.pdf", 'rb'))
#     elif message.text == "Скрипт замена оборудования ПСС, УП":
#         bot.send_document(message.chat.id, open("files/П_Скрипт замена оборудования ПСС, УП.pdf", 'rb'))
#     elif message.text == "Скрипт с КАТВ на ТВ+":
#         bot.send_document(message.chat.id, open("files/К_Скрипт с КАТВ на ТВ+.pdf", 'rb'))
#     elif message.text == "Стандарты СО":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Внутренний клиент, Стандарты СО")
#         button2_s = types.KeyboardButton("Внешний клиент, Стандарты СО")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Внутренний клиент, Стандарты СО":
#         bot.send_document(message.chat.id, open("files/Внутренний клиент, Стандарты СО.pdf", 'rb'))
#     elif message.text == "Внешний клиент, Стандарты СО":
#         bot.send_document(message.chat.id, open("files/Внешний клиент, Стандарты СО.pdf", 'rb'))
#     elif message.text == "Публичный договор":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Публичный договор рус")
#         button2_s = types.KeyboardButton("Публичный договор каз")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Публичный договор рус":
#         bot.send_document(message.chat.id, open("files/Публичный договор рус.pdf", 'rb'))
#     elif message.text == "Публичный договор каз":
#         bot.send_document(message.chat.id, open("files/Публичный договор каз.pdf", 'rb'))
#     elif message.text == "Правила классификации лицевых счетов рус":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Публичный договор рус")
#         button2_s = types.KeyboardButton("Публичный договор каз")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Правила классификации лицевых счетов рус":
#         bot.send_document(message.chat.id, open("files/Правила классификации лицевых счетов рус.pdf", 'rb'))
#     elif message.text == "Правила классификации лицевых счетов каз":
#         bot.send_document(message.chat.id, open("files/Правила классификации лицевых счетов каз.pdf", 'rb'))
#     elif message.text == "Как оплатить услугу":
#         bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
#     elif message.text == "Как посмотреть о деталях оплаты":
#         bot.send_document(message.chat.id,
#                           document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
#     elif message.text == "Как посмотреть подключенные услуги":
#         bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
#     elif message.text == "Раздел 'Мои Услуги'":
#         bot.send_document(message.chat.id, document=open("files/РАЗДЕЛ «МОИ УСЛУГИ» (1).pdf", 'rb'))


def menu(bot, message):
    db_connect.set_bool(message, False, False)
    bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=markup)


def glossary(bot, message):
    text1 = f"По Вашему запросу нaйдeнo следующие значение:"
    text2 = "Ho Вы можете помочь нам стать лучше и добавить значение, отправив нам письмо на \
                                      info.ktcu@telecom.kz - мы обязательно рассмотрим ero."
    db_connect.glossary(bot, message, text1, text2)


def profile(bot, message):
    db_connect.cm_sv_db(message, "🧐Мой профиль")
    markup_ap = types.InlineKeyboardMarkup(row_width=1)
    button1_ap = types.InlineKeyboardButton("Изменить Имя", callback_data="Изменить Имя")
    button2_ap = types.InlineKeyboardButton("Изменить Фамилию", callback_data="Изменить Фамилию")
    button3_ap = types.InlineKeyboardButton("Изменить номер телефона", callback_data="Изменить номер телефона")
    button4_ap = types.InlineKeyboardButton("Изменить email", callback_data="Изменить email")
    button5_ap = types.InlineKeyboardButton("Изменить табельный номер", callback_data="Изменить табельный номер")
    button6_ap = types.InlineKeyboardButton("Изменить филиал", callback_data="Изменить филиал")
    markup_ap.add(button1_ap, button2_ap, button3_ap, button4_ap, button5_ap, button6_ap)
    bot.send_message(message.chat.id, f"Сохраненная информация\n\n"
                                      f"Имя: {db_connect.get_firstname(message)}\n"
                                      f"Фамилия: {db_connect.get_lastname(message)}\n"
                                      f"Номер телефона: {db_connect.get_phone_number(message)}\n"
                                      f"Email: {db_connect.get_email(message)}\n"
                                      f"Табельный номер: {db_connect.get_table_number(message)}\n"
                                      f"Филиал: {db_connect.get_branch(message.chat.id)}",
                     reply_markup=markup_ap)


def questions(bot, message):
    button_q = types.KeyboardButton("Мои обращения")
    button_q1 = types.KeyboardButton("Оставить обращение")
    button_q2 = types.KeyboardButton("Часто задаваемые вопросы")
    markup_q = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_q.add(button_q2, button_q1, button_q)
    if db_connect.check_id(categories, str(message.chat.id)):
        markup_q.add(types.KeyboardButton("Админ панель для обращений"))
    bot.send_message(str(message.chat.id), "B данном разделе Вы можете оставить свое обращение или "
                                           "посмотреть ответы на часто задаваемые вопросы", reply_markup=markup_q)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu "
                                      "в меню команд слева от строки ввода.")


def portal(bot, message):
    message_text = message.text
    if message_text == "🖥Портал 'Бірлік'":
        db_connect.cm_sv_db(message, "Портал 'Бірлік'")
        markup_p = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, )
        markup_p = db_connect.generate_buttons(portal_bts, markup_p)
        bot.send_message(str(message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif message_text == portal_bts[0]:
        bot.send_message(str(message.chat.id), "Что такое портал - файл")
    # elif message_text == portal_bts[1]:
    #     db_connect.cm_sv_db(message, portal_bts[1])
    #     markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1 = types.KeyboardButton(portal_[0])
    #     button2 = types.KeyboardButton(portal_[1])
    #     markup_portal.add(button1, button2)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_portal)
    elif message_text == portal_[0]:
        markup_p = types.InlineKeyboardMarkup()
        button_p = types.InlineKeyboardButton("Нужен checkpoint?", callback_data="checkPoint")
        markup_p.add(button_p)
        bot.send_message(str(message.chat.id), "Как авторизоваться на портале работника на IOS и Android | portal.telecom.kz\nhttps://youtu.be/WJdS1aIBe1I", reply_markup=markup_p)
    # elif message_text == portal_[1]:
    #     markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1_p = types.KeyboardButton("Как авторизоваться")
    #     button2_p = types.KeyboardButton("Личный профиль")
    #     button3_p = types.KeyboardButton("Из портала перейти в ССП")
    #     markup_pk.add(button1_p, button2_p, button3_p)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_pk)
    # elif message_text == portal_[2]:
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как авторизоваться на портале "
    #                                       "работника через ПК?' перейдите по ссылке ниже "
    #                                       "\nhttps://youtu.be/vsRIDqt_-1A")
    # elif message_text == portal_[3]:
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как заполнить личный профиль?' "
    #                                       "перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    # elif message_text == portal_[4]:
    #     bot.send_message(message.chat.id, "Для получения информации о категории 'Как перейти из портала перейти в ССП'"
    #                                       " перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")
    elif message_text == portal_bts[3]:
        markup_p = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, )
        markup_p = db_connect.generate_buttons(portal_guide, markup_p)
        bot.send_message(str(message.chat.id), "Выберите вопрос", reply_markup=markup_p)
    elif message_text == portal_bts[2]:
            db_connect.set_category(message, "portal")
            appeal(bot, message, message_text)
    else:
        if checkpoint(bot, message):
            return
        db_connect.check_portal_guide(bot, message, message_text, portal_guide)


def checkpoint(bot, message):
    message_text = message.text
    if message_text == portal_bts[1]:
        db_connect.cm_sv_db(message, portal_bts[1])
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(portal_[0])
        button2 = types.KeyboardButton(portal_[1])
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_portal)
    elif message_text == portal_[1]:
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_p = types.KeyboardButton("Как авторизоваться")
        button2_p = types.KeyboardButton("Личный профиль")
        button3_p = types.KeyboardButton("Из портала перейти в ССП")
        markup_pk.add(button1_p, button2_p, button3_p)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_pk)
    elif message_text == portal_[2]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как авторизоваться на портале "
                                          "работника через ПК?' перейдите по ссылке ниже "
                                          "\nhttps://youtu.be/vsRIDqt_-1A")
    elif message_text == portal_[3]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как заполнить личный профиль?' "
                                          "перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    elif message_text == portal_[4]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как перейти из портала перейти в ССП'"
                                          " перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")
    else:
        return False
    return True