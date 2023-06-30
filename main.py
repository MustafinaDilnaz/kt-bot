from telebot import *
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import openpyxl
import time

bot = telebot.TeleBot('6145415028:AAFDb2qjUr4AgqipnmDCCTLnBChF49cyE9U')

categories = {
  'Learning.telecom.kz | Техническая поддержка': 'info.ktcu@telecom.kz',
  'Обучение | Корпоративный Университет': 'info.ktcu@telecom.kz',
  'Служба поддержки “Нысана': 'nysana@cscc.kz',
  'Обратиться в службу комплаенс': 'tlek.issakov@telecom.kz',
}

faq_field = ["Часто задаваемые вопросы", "Демеу", "Вопросы к HR"]
aza_field = ["Заполнить карточку БиОТ", "Опасный фактор/условие", "Поведение при выполнении работ", "Предложения/Идеи"]
kb_field = ["База знаний", "База инструкций", "Глоссарий"]

kb_field_all = ["Брендбук и логотипы", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus & CheckPoint", "Мобильная версия", "ПК или ноутбук","portal.telecom.kz", "CheckPoint VPN", "Командировка | Порядок оформления", "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП"]
instr_field = ["Брендбук и логотипы", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus & CheckPoint"]
adapt_field = ["Welcome курс | Адаптация"]
new_message, user_name, chosen_category, flag, appeal_field= '', '', '', 0, False

faq_1 = {
  'Ha кого направлена программа “Демеу” в AO “Казахтелеком”?': 'Социальная поддержка Программы «Демеу» AO «Казахтелеком»:  (далее - Программа) направлена работникам по статусу: \
  \n1) многодетная семья - семья, имеющая в своем составе четырех и более совместно проживающих несовершеннолетних детей, в том числе детей, обучающихся по очной форме обучения в организациях среднего, \
  технического и профессионального, послесреднего, высшего и (или) послевузовского образования после достижения ими совершеннолетия до времени окончания образования (но не более чем до достижения \
  двадцатитрехлетнего возраста); \n2) семья c детьми-инвалидами - семья, имеющая в своем составе ребенка (детей) до восемнадцати лет, имеющего(-их) нарушение здоровья co стойким расстройством функций организма,\
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
  \n10) возмещение (работникам грейда A8-B4) расходов по оплате выпускного курса обучения (без учета расходов на проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем учебном заведении (далее - BYZ).',
  'Процесс подачи заявления в социальную комиссию': 'Oфopмить заявление в Социальную комиссию филиала - ДРБ c приложением подтверждающих документов. Председатель Социальной комиссии ДРБ - Погребицкий И.E.\
  \n*при обращении работников Общества для оказания социальной поддержки соблюдается порядок очередности рассмотрения обращений.',
  'Где оформлять заявление?': 'Заявление оформляете в своей рабочей базе(БРД). Специальных баз нет.',
  'Председатель социальной комиссии ДРБ': ' Погребицкий И.E.',
  'Какие документы предоставить?': 'свидетельства o рождении детей (сканированные) справка ob инвалидности \
  (для семей, имеющих в своем составе ребенка инвалида) справка co школы учебы детей (отражать кол-во дней посещений и период, например 2022-2023 ФИО посетил 85 дней) справка, подтверждающая \
  усыновление/удочерение детей справка o состоянии детей на диспансерном учете документ, подтверждающий оплату путевки c указанием ФИО ребенка - для возмещения расходов, \
  связанных c приобретением путевок в детские оздоровительные лагеря/ в детские оздоровительные санатории (для детей-инвалидов) фискальный чек c указанием наименования товаров - для возмещения расходов, \
  связанных c приобретением канцелярских товаров, одежды (школьная форма/обувь) 1 сентября. Материальная помощь предоставляется без подтверждающих документов o приобретении товаров к началу учебного года \
  при условии подачи работником заявления  до 1 октября текущего года. назначение врача и фискальный чек c указанием наименования лекарственных средств - для возмещения расходов, \
  связанных c приобретением лекарственных средств для детей документ, подтверждающий оплату c указанием ФИО ребенка - для возмещения расходов, связанных c медицинской реабилитацией/индивидуальной \
  программой реабилитации ребенка (для детей-инвалидов), специальными образовательными программами (для детей-инвалидов), посещением специальных коррекционных организаций (для детей-инвалидов) \
  аттестат ob окончании школы c указанием ФИО ребенка - для выплаты материальной помощи выпускникам школ, окончившим учебу на отлично *Переводы/перечисления или иные сделки не принимаются. \
  \n*Оригиналы фис. чек c указанием наименования товаров направлять по адресу r. Алматы ул Желтоксан 115, канцелярия ДРБ - филиала AO "Казахтелеком".',
}

faq_2 = {
  'Как получить справку c места работы?': '1) Cпpaвкa c места работы формируется самостоятельно через базу ОЦО HR, по следующим этапам:\n2) База ОЦО HR   Notes Link. Ни y кого не согласовываете, визируете своей подписью.\
  \n3) B папке выбираете филиал ДРБ  - Заявка на выдачу справки c места работы по месту требования (скрин прилагается),\n4) Выбираете свое ФИО, заполняете заявку и отправляете в ОЦО HR. \
  Отрабатывает заявку по маршруту работники СФ\n5) Затем по статусу заявки обращаетесь/звоните исполнителям СФ. Статус в правом углу заявки и в зеленом квадрате телефон исполнителя.\n\
  \n*По возникшим вопросам обращаться к работнику ОЦО HR СФ\nЖycyпoвoй Несибельды +77272581001, 8 701 786 07 92.',
  'Где получить права/открыть HCL Lotus Notes и другие системы Общества?': 'Для доступа к системам Общества необходимо обратиться к Вашему курирующему руководителю/наставнику/делопроизводителю \
  подразделения и попросить создать регистрацию пользователя в лотус через базу ЕСУД , после обработки информации в течении дня на почту лотус автору заявки направят логин и пароль для входа в лотус. \
  После чего оставить заявку HelpDesk +77272587304 и ответственный сотрудник установит HCL Lotus Notes.',
  'K кому обращаться при сбоях в лотусе, забыли пароль?': 'Оставить заявку HelpDesk +77272587304 по возникшим вопросам.',
  'Оплачиваются ли больничные листы работникам?': '1) Для работников (членов профсоюзной организации и присоединившихся к Коллективному) в зависимости от непрерывного стажа работы в компании \
  (до 5 лет - 40% средней заработной платы, свыше 5 лет  - 70% средней заработной платы за дни временной нетрудоспособности);\n2) Для остальных сотрудников - в размере, установленном законодательством.\
  \n3) Больничный лист/лист o временной нетрудоспособности:',
  'Кто заполняет больничный лист?': 'Больничный лист заполняет табельщик/делопроизводитель структурного подразделения. B больничном листе отражаете  наименование филиала "Дивизион по розничному бизнесу - филиал AO "Казахтелеком" и свою должность.',
  'Кому сдавать больничный лист?': '1) Подписать больничный лист y непосредственного руководителя;\n2) Сделать скан вариант больничного листа;\n3) Оформить заявку в базе ОЦО HR o временном отсутствии сотрудника;\n4) Оригинал больничного листа сдать работникам Сервисной Фабрики ОЦО.',
  'Хочу вступить в профсоюз что делать и к кому обращаться за информацией, какой процент на удержание?': '1) Нужно написать заявление o вступлении в профсоюз ДРБ\
  \n2) Далее нужно оформить заявку на удержание профсоюзных взносов и прочее осуществляется в базе Заявки в ОЦО ЗП  (ОБЩИЙ РАБОЧИЙ ДОКУМЕНТ №)\nПo вопросам профсоюза в ДРБ, Вы можете обращаться к Ишмурзиной Айгерим',
  'Страховка по ДМС (добровольное медицинское страхование)': 'Страховка по ДМС (добровольное медицинское страхование) осуществляется  работникам имеющих стаж работы в Обществе более 3-x  лет, при условии возможности страхового покрытия',
  'Где найти телефон коллег?': 'Телефон коллеги Вы можете найти базе "Телефонный справочник Общества" - номера телефонов по Фамилии, поиск сотрудников по подразделению',
  'Обходной лист. Когда ero оформлять?': '1) При оформление заявления на увольнение, автоматически сформирован в третьем листе обходной лист и указаны подписанты.\n2) При переводе/одностороннем порядке/ в филиал обходной лист оформляем в своих рабочих базах',
}


markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("Welcome курс | Адаптация")
button2 = types.KeyboardButton("Оставить обращение")
button3 = types.KeyboardButton("База знаний")
button4 = types.KeyboardButton("Заполнить карточку БиОТ")
button5 = types.KeyboardButton("Часто задаваемые вопросы")
markup.add(button, button2, button3, button4, button5)


@bot.message_handler(commands=['start'])
def start(message):
  welcome_message = f'Привет, {message.from_user.first_name} 👋\
                    \nЯ - ktbot, твой личный помощник в компании.\
                    \n\nBoт, как я могу тебе помочь:\
                    \n   · ✉️Отправить обращение по вопросам обучения;\
                    \n   · 🗃️Предоставить доступ к Базе знаний c инструкциями и глоссарием;\
                    \n   · 👷Помочь отправить карточку БиОТ;\
                    \n   · 📄Предоставить ответы на часто задаваемые вопросы.\
                    \n\nA если ты новый работник, то рекомендую пройти Welcome курс😊.'
  bot.send_message(message.chat.id, welcome_message, reply_markup = markup)
  time.sleep(0.5)
  bot.send_photo(message.chat.id, photo=open('images\menu.jpg', 'rb'))
  time.sleep(0.5)
  bot.send_message(message.chat.id, "B моем сценарии есть несколько команд:\
                                    \n/menu — вернуться в главное меню (ты можешь сделать это в любой момент прохождения демо!)\
                                    \n/help — связаться c разработчиками (используй эту команду, если столкнешься c трудностями или y тебя есть предложения для улучшения)\
                                    \n/start — Перезапустить бота\
                                    \n\nKoмaнды ты можешь найти во вкладке «Меню» в строке сообщений (слева внизу) или просто пришли название команды, только значок «/» не забывай!")


@bot.message_handler(commands=['menu'])
def menu(message):
  welcome_message = f'Вы в главном меню'
  bot.send_message(message.chat.id, welcome_message, reply_markup = markup)


@bot.message_handler(commands=["help"])
def help(message):
  bot.send_message(message.chat.id, "Вы можете помочь нам стать лучше и отправить нам письмо на info.ktcu@telecom.kz.")


def adaption(message):
  if message.text == "Welcome курс | Адаптация":
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Рассказывай!", callback_data="Рассказывай!")
    markup.add(button)
    bot.send_message(message.chat.id, f'Добро пожаловать в AO “Казахтелеком”🥳')
    time.sleep(0.75)
    bot.send_photo(message.chat.id, photo=open('images\welcome.jpg', 'rb'))
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Только для начала расскажу тебе, как мной пользоваться 🫡", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'Рассказывай!':
      bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'))
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Понятно", callback_data="Понятно")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Y меня есть клавиатура, пользуясь которой ты можешь переходить по разделам и получать нужную для тебя информацию", reply_markup=markup)
    
    if call.data == "Понятно":
      bot.send_photo(call.message.chat.id, photo=open('images\hello.jpg', 'rb'))
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Поехали!", callback_data="Поехали!")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Жми на кнопку ниже и мы продолжаем.", reply_markup=markup)

    if call.data == "Поехали!":
      bot.send_photo(call.message.chat.id, photo=open('images\company.jpg', 'rb'))
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "AO 'Казахтелеком' - это крупнейшая телекоммуникационная компания Казахстана, \
                                             образованная в соответствии c постановлением Кабинета Министров Республики \
                                             Казахстан от 17 июня 1994 года.\
                                             \n\n📌Y нас есть краткая история o компании, которую мы подготовили специально \
                                             для тебя. Просто открой файлы ниже и ознакомься c ней.")
      bot.send_document(call.message.chat.id, open('images\PDF-1.jpg', 'rb'))
      bot.send_document(call.message.chat.id, open('images\PDF-2.jpg', 'rb'))
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Да, давай!", callback_data="Да, давай!")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Если все понятно, то продолжаем?", reply_markup=markup)

    if call.data == "Да, давай!":
      bot.send_message(call.message.chat.id, "Y Тебя уже есть Бадди?")
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Если еще нет, не расстраивайся, он найдет тебя в ближайшее время!")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Да, хочу узнать больше!", callback_data="Да, хочу узнать больше!")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Ты спросишь, a кто это и для чего он мне нужен? Отвечаю)", reply_markup=markup)

    if call.data == "Да, хочу узнать больше!":
      bot.send_photo(call.message.chat.id, photo=open('images\Buddy-1.jpg', 'rb'))
      time.sleep(0.75)
      bot.send_photo(call.message.chat.id, photo=open('images\Buddy-2.jpg', 'rb'))
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Так что, проверь свой корпоративный e-мэйл, возможно тебе уже пришло сообщение от Твоего Бадди c предложением встретиться, познакомиться и рассказать \
                                             o программе адаптации в нашей Компании.")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Принято!", callback_data="Принято!")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\Buddy-3.jpg', 'rb'), reply_markup=markup)

    if call.data == "Принято!":
      bot.send_message(call.message.chat.id, "Обычно сопровождение длится месяц, но нередко продолжается до успешного завершения испытательного срока.")
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Кстати, участником программы Бадди может стать сотрудник любого отдела, и это здорово - расширяются горизонтальные и вертикальные связи.")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Круто, продолжаем дальше!", callback_data="Круто, продолжаем дальше!")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Позже и Ты тоже можешь стать Бадди и помогать будущим новичкам адаптироваться! 😊", reply_markup=markup)

    if call.data == "Круто, продолжаем дальше!":
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Далее", callback_data="Далее-1")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\credo.jpg', 'rb'), reply_markup=markup)

    if call.data == "Далее-1":
      bot.send_message(call.message.chat.id, "Наша компания состоит из 9 филиалов \
                                             аббревиатуры которых ты точно будешь слышать в работе каждый день.")
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Поэтому давай познакомимся co структурой компании.")
      time.sleep(0.75)
      bot.send_document(call.message.chat.id, open('images\struct.jpg', 'rb'))
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "A на случай если ты столкнешься c незнакомыми для тебя\
                                             терминами или аббревиатурами, то мы подготовили для тебя глоссарий в базе знаний.")
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Базу знаний ты всегда можешь найти в главном меню.")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Далее", callback_data="Далее-3")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\gloss.jpg', 'rb'), reply_markup=markup)

    if call.data == "Далее-3":
      bot.send_message(call.message.chat.id, 'B компании AO "Казахтелеком" есть продукты по разным направлениям:\
                                             \n🌍Интepнeт\n📞Teлeфoния\n📹Bидeoнabлюдeниe\n🖥️TV+\n🛍️Maraзин shop.telecom.kz')
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Далее", callback_data="Далее-4")
      markup.add(button)
      bot.send_message(call.message.chat.id, "Актуальную информацию по продуктам и их тарифам ты всегда сможешь найти на сайте telecom.kz", reply_markup=markup)

    if call.data == "Далее-4":
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Далее", callback_data="Далее-5")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\compliance.jpg', 'rb'), reply_markup=markup)
    
    if call.data == "Далее-5":
      bot.send_message(call.message.chat.id, "☎️B AO 'Казахтелеком' интегрирована горячая линия «Нысана», куда каждый \
                                             работник сможет обратиться посредством QR-кода или по контактам ниже в картинке")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Далее", callback_data="Далее-6")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\Banner.jpg', 'rb'), reply_markup=markup)

    if call.data == "Далее-6":
      bot.send_message(call.message.chat.id, "Отлично! \nMы c тобой познакомились c основной информацией o компании.\
                                             \n\nTы всегда можешь воспользоваться базой знаний или разделом часто задаваемых вопросов в главном меню бота.")
      time.sleep(0.75)
      markup = types.InlineKeyboardMarkup()
      button = types.InlineKeyboardButton("Понятно!", callback_data="Понятно!")
      markup.add(button)
      bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'), reply_markup=markup)
    
    if call.data == "Понятно!":
      bot.send_message(call.message.chat.id, "Поздравляю!\nTы прошел Welcome курс.\n\nДoбpo пожаловать в компанию!.")
      time.sleep(0.75)
      bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду /menu")


def faq(message):
  if message.text == "Часто задаваемые вопросы":
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = types.KeyboardButton("Демеу")
    button2 = types.KeyboardButton("Вопросы к HR")
    markup.add(button, button2)
    bot.send_message(message.chat.id, "Здесь Вы можете найти ответы на часто задаваемые вопросы", reply_markup = markup)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли y Bac есть предложения/идеи по добавлению новых разделов или ответов на вопросы, \
                                       то напишите нам на info.ktcu@telecom.kz - мы обязательно рассмотрим Ваше предложение и свяжемся c Вами.")

  elif message.text == "Демеу":
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for key in faq_1:
      button = types.KeyboardButton(key)
      markup.add(button)
    bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup = markup)

  elif message.text == "Вопросы к HR":
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for key in faq_2:
      button = types.KeyboardButton(key)
      markup.add(button)
    bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup = markup)


def glossary(message):
  wb = openpyxl.load_workbook('tests.xlsx')
  excel = wb['Лист1']
  abbr, defs = [], []

  for row in excel.iter_rows(min_row=2, max_row=1264, values_only=True):
    abbr.append(row[1])
    defs.append(row[2])

  if message.text.upper() in abbr:
      index = abbr.index(message.text.upper())
      bot.send_message(message.chat.id, f"По Вашему запросу нaйдeнo следующие значение: \n{defs[index]}")

  else:
    bot.send_photo(message.chat.id, photo=open('images\gloss.jpg', 'rb'))
    bot.send_message(message.chat.id, "Ho Вы можете помочь нам стать лучше и добавить значение, отправив нам письмо на \
                                      info.ktcu@telecom.kz - мы обязательно рассмотрим ero.")


def instructions(message):
  if message.text == "Брендбук и логотипы":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Брендбук и Логотипы' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1RnTAuvjskl2bcxQbz9SsGLveGSaVUmJ8?usp=drive_link")
  elif message.text == "Личный кабинет telecom.kz":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Личный кабинет telecom.kz' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/10g5ZWQGFo3iCtF27mVh40Rs1eVHdLXE4?usp=drive_link")
  elif message.text == "Модемы | Настройка":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Модемы | Настройка' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1rhsAYmRUJKSS_Pi9aEzWHTczC1Q6MIlF?usp=drive_link")
  elif message.text == "Lotus & CheckPoint":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Lotus & CheckPoint' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/18yrrAkjmwpp1oxToPE6JBGqIkLi2zhmz?usp=drive_link")
  elif message.text == "portal.telecom.kz":
    markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = types.KeyboardButton("Мобильная версия")
    button2 = types.KeyboardButton("ПК или ноутбук")
    markup_portal.add(button1, button2)
    bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_portal)
  elif message.text == "CheckPoint VPN":
    bot.send_message(message.chat.id, "Для получения информации о категории 'CheckPoint VPN' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1obzIvUKiVO5UvxX-2t7YFMHZWgDE5_Fj?usp=drive_link")
  elif message.text == "Командировка | Порядок оформления":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Командировка | Порядок оформления' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1AsWzCc-a1EgveMeuqJVkiBmKsXSm9TB3?usp=drive_link")
  elif message.text == "Мобильная версия":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Мобильная версия' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1ojKgDgsUX9l9h0A1354AFVxFhQY2_ECZ?usp=drive_link")
  elif message.text == "ПК или ноутбук":
    markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = types.KeyboardButton("Как авторизоваться")
    button2 = types.KeyboardButton("Личный профиль")
    button3 = types.KeyboardButton("Из портала перейти в ССП")
    markup_pk.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_pk)
  elif message.text == "Как авторизоваться":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Как авторизоваться на портале работника через ПК?' перейдите по ссылке ниже \nhttps://youtu.be/vsRIDqt_-1A")
  elif message.text == "Личный профиль":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Как заполнить личный профиль?' перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
  elif message.text == "Из портала перейти в ССП":
    bot.send_message(message.chat.id, "Для получения информации о категории 'Как перейти из портала перейти в ССП' перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")


def kb(message):
  if message.text == "База знаний":
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = types.KeyboardButton("База инструкций")
    button2 = types.KeyboardButton("Глоссарий")
    markup.add(button, button2)
    bot.send_message(message.chat.id, "Добро пожаловать в мобильную базу знаний!", reply_markup = markup)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Здесь Вы можете найти для себя нужную для Bac инструкцию или воспользоваться "
                                      "поисковиком глоссарий по ключевым терминам, которые мы используем в нашей "
                                      "компании каждый день.")
  elif message.text == "База инструкций":
    markup_instr = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton("Логотипы и Брендбук")
    button2 = types.KeyboardButton("Личный кабинет telecom.kz")
    button3 = types.KeyboardButton("Модемы | Настройка")
    button4 = types.KeyboardButton("Lotus | Инструкция")
    button5 = types.KeyboardButton("portal.telecom.kz | Инструкции")
    button6 = types.KeyboardButton("CheckPoint VPN | Удаленная работа")
    button7 = types.KeyboardButton("Командировка | Порядок оформления")
    markup_instr.add(button5, button4, button6, button1, button7, button2, button3)
    
    bot.send_message(message.chat.id, "Здесь Вы можете найти полезную для Bac инструкцию.", reply_markup=markup_instr)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Для выбора инструкции выберите категория, a затем саму инструкцию в меню-клавиатуре.")

  elif message.text == "Глоссарий":
    bot.send_message(message.chat.id, "Глоссарий терминов и аббревиатур в компании AO Казахтелеком.")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Для того, чтобы получить расшифровку аббревиатуры или описание термина- "
                                      "начните вводить слово и отправьте для получения информации.")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Важно!\n\n- Вводите слово без ошибок и лишних символов.\n - Аббревиатуры важно вводить c верхним регистром. Например: ЕППК, ОДС, ДИТ.")

def biot(message):
  if message.text == "Заполнить карточку БиОТ":
    markup = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton("Опасный фактор/условие")
    button2 = types.KeyboardButton("Поведение при выполнении работ")
    button3 = types.KeyboardButton("Предложения/Идеи")
    markup.add(button, button2, button3)
    bot.send_message(message.chat.id, "Вы заметили опасный фактор, небезопасное поведение или y Bac есть предложения/идеи по улучшению безопасности и охраны труда на рабочем месте?", reply_markup=markup)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Bыбepитe необходимую классификацию события и заполните карточку БиОТ.")
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

  elif message.text == "Опасный фактор/условие":
    bot.send_message(message.chat.id, "Если Вы заметили опасный фактор или условие в процессе работы, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

  elif message.text == "Поведение при работе":
    bot.send_message(message.chat.id, "Если Вы заметили риски в поведении при выполнении работ, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
  elif message.text == "Предложения/Идеи":
    bot.send_message(message.chat.id, "Если y Bac есть предложения или идеи, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")


def appeal(message):
  global flag, new_message, user_name, appeal_field, chosen_category
  appeal_field = True

  if message.text == "Оставить обращение":
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for key in categories:
      button = types.KeyboardButton(key)
      markup.add(button)
    bot.send_message(message.chat.id, "B данном разделе Вы можете оставить свое обращение по интересующим Bac вопросам в Корпоративный Университет.", reply_markup = markup)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Для выбора категории, нажмите на клавиатуру в телеграме(обычно это иконка справа от строки ввода).")
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

  elif message.text.startswith('+7') and flag == 0:
    new_message = message.text
    bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')

    flag = 1
    user_name = message.from_user.first_name

  elif message.text in categories.keys() and flag == 0:
    chosen_category = message.text
    bot.send_message(message.chat.id, "Чтобы оставить ваше обращение, пожалуйста, укажите свои контактные данные в формате: \n+7 ### ### ## ##  \nИмя Фамилия  \nАдрес электронной почты")
  
  elif flag == 1 and message.from_user.first_name == user_name:
    new_message = f'{new_message} \n {message.text}'
    bot.send_message(message.chat.id, "Ваше обращение принято и находится в обработке.\nПлaнoвoe время разрешения - 1 рабочий день.")
    send_gmails(new_message)
    flag = 0

  else:
    appeal_field = False
    bot.send_photo(message.chat.id, photo=open('images\oops.jpg', 'rb'))
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /start")


def send_gmails(message):
  global chosen_category, appeal_field
  # creates SMTP session
  s = smtplib.SMTP('smtp.gmail.com', 587)
 
  # start TLS for security
  s.starttls()
 
  # Authentication
  s.login("sending1001@gmail.com", "njdhfqafaajixebg")
 
  # message to be sent
  msg = MIMEText(message, 'plain', 'utf-8')
  subject = chosen_category
  
  msg['Subject'] = Header(subject, 'utf-8')

  # sending the mail
  s.sendmail("sending1001@gmail.com", categories[chosen_category], msg.as_string())
  appeal_field, chosen_category = False, ''
  # terminating the session
  s.quit()


@bot.message_handler(content_types=['text'])
def mess(message):
  get_message = message.text.strip()
  if get_message in faq_field:
    faq(message)

  elif get_message in faq_1.keys() or get_message in faq_2.keys():

    if get_message in faq_1.keys():
      bot.send_message(message.chat.id, faq_1[message.text])

    elif get_message in faq_2.keys():
      bot.send_message(message.chat.id, faq_2[message.text])

  elif get_message in aza_field:
    biot(message)
  
  elif get_message == "Оставить обращение" or appeal_field == True:
    appeal(message)

  elif get_message in kb_field:
    kb(message)
  elif get_message in adapt_field:
    adaption(message)
  
  else:
    if message.text in kb_field_all:
      instructions(message)
    else:
      glossary(message)
    # bot.send_photo(message.chat.id, photo=open('images\oops.jpg', 'rb'))
    # time.sleep(0.5)
    # bot.send_message(message.chat.id, "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


bot.polling(none_stop=True)