from datetime import timedelta

import requests
from telebot import *
import db_connect
import rus

categories = {
    'Learning.telecom.kz | Техникалық қолдау': {
        "id": "187663574",
        "name": "Оспанов Тамирлан",
        "phone_num": "87777777777",
        "email": "info.ktcu@telecom.kz",
        "telegram": "@tamirlan"
    },
    'Оқыту | Корпоративтік Университет': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "info.ktcu@telecom.kz",
        "telegram": "@dilnaz.mustafina"
    },
    '"Нысана" қолдау қызметі': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "nysana@cscc.kz",
        "telegram": "@dilnaz.mustafina"
    },
    'Комплаенс қызметіне хабарласыңыз': {
        "id": "760906879",
        "name": "Мустафина Дильназ",
        "phone_num": "87089081808",
        "email": "tlek.issakov@telecom.kz",
        "telegram": "@dilnaz.mustafina"
    },
}

faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары", "Қарыздар бойынша сұрақтар"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["👷ҚТ ж ЕҚ кәртішкесін толтыру", "Қауіпті фактор | шарт", "Жұмысты орындау тәртібі", "Ұсыныстар | Идеялар"]
kb_field = ["🗃️Білім базасы", "Нұсқаулық базасы", "Глоссарий", "Пайдалы сілтемелер"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар",
                "Checkpoint VPN | Қашықтан жұмыс", "Iссапар | Рәсімдеу тәртібі",
                "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту", "Филиал серверлері бойынша деректер",
                "Lotus Орнату нұсқаулары", "Lotus орнату файлы", "Қазақтелеком АҚ",
                "Корпоративтік Университет", "Қызметті қалай төлеуге болады", "Төлем туралы мәліметтерді қалай көруге болады",
                "Қосылған қызметтерді қалай көруге болады", "'Менің Қызметтерім' Бөлімі", "ADSL модемі",
                "IDTV консолі", "ONT модемдері", "Router 4G and Router Ethernet", "CheckPoint Орнату нұсқаулығы",
                "Checkpoint орнату файлы"]
instr_field = ["Брендбук және логотиптер", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар"]
adapt_field = ["😊Welcome курс | Бейімделу"]
portal_bts = ["'Бірлік' порталы дегеніміз не?", "Порталға қалай кіруге болады?", "Порталға өтініш қалдыру", "Бірлік Гид"]
portal_ = ["Мобильді нұсқа", "ДК немесе ноутбук", "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту",
           "iOS", "Android", "Есть checkpoint", "Нет checkpoint"]
portal_guide = ["Кері байланыс үшін қайда жүгіну керек-пікірлер мен ұсыныстар?",
                "Порталда компанияның стратегиясымен қайдан танысуға болады?",
                "Қауымдастықты қалай құруға болады?", "Экожүйеде демалысты қалай жоспарлауға болады?",
                "Әріптесіңізге қалай алғыс айтамын?", "Экожүйеде сауалнаманы қалай құруға болады?",
                "Қазақтелеком дүкенінен жеңілдікпен тауарды қалай сатып алуға болады?",
                "Қазақтелеком саудасын қалай сатып алуға болады?",
                "Компания қызметкерлеріне жеңілдіктер мен акцияларды қайдан көруге болады?"]

faq_1 = {
    'Қазақтелеком "АҚ-да "Демеу" бағдарламасы кімге бағытталған?':
        'Қазақтелеком" АҚ "Демеу" бағдарламасын әлеуметтік қолдау: (бұдан әрі-Бағдарлама) жұмыскерлерге мәртебесі бойынша жіберілді: \
\n1) Көп балалы отбасы-өз құрамында төрт және одан да көп бірге тұратын кәмелетке толмаған балалары, оның ішінде кәмелетке толғаннан кейін орта, техникалық және кәсіптік, орта білімнен кейінгі, жоғары және (немесе) жоғары оқу орнынан кейінгі білім беру ұйымдарында күндізгі оқу нысаны бойынша білім алатын балалары бар отбасы  \
отбасы (бірақ білім алуды аяқтағанға дейін) жиырма үш жасқа толған жетістіктер);  \
\n2) Мүгедек балалары бар отбасы-өз құрамында он сегіз жасқа дейінгі баласы (балалары) бар, бар, тұрмыс-тіршілігінің шектелуіне және оны әлеуметтік қорғау қажеттігіне әкеп соқтыратын, ауруларға, мертігулерге (жаралануға, жарақаттарға, контузияларға), олардың зардаптарына, кемістіктерге байланысты ағзаның қызметінде тұрақты бұзылуы бар отбасын (оларды) әлеуметтік қорғау; \
\n3) 2-ден астам бала асырап алған/асырап алған отбасы - құрамында 2-ден астам кәмелетке толмаған асырап алған/асырап алынған балалары бар, денсаулық жағдайы бойынша диспансерлік есепте тұрған және жалғыз асыраушысы бар отбасы.\
\n4) A8-B4 грейдінің жұмыскерлеріне балаларының орта арнаулы оқу орнында (бұдан әрі - CYZ) жоғары оқу орнында (бұдан әрі - BYZ) түлектердің оқу курсына (тұруға және тамақтануға арналған шығыстарды есептемегенде) ақы төлеу бойынша әлеуметтік қолдау белгіленеді. Барлық әлеуметтік қолдау түрлері әлеуметтік қолдау көрсету мерзімінде Қоғамда кемінде 3 жыл үздіксіз жұмыс өтілі бар Қоғам жұмыскерлеріне көрсетіледі.',
    'Жұмыскерлерге әлеуметтік қолдау түрлері':
        '1) балалардың сауықтыру лагерьлеріне жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n2) Балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін) жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n3) Балаларға арналған дәрілік заттарды сатып алуға материалдық көмек; \
\n4) Мектеп оқушыларының тамақтануына материалдық көмек; \
\n5) Оқу жылының басына материалдық көмек; \
\n6) Медициналық оңалту/баланы оңалтудың жеке бағдарламасы үшін қаражатты өтеу (мүгедек балалар үшін); \
\n7) Арнайы білім беру бағдарламалары үшін қаражатты өтеу (мүгедек балалар үшін); \
\n8) Арнайы түзету ұйымдарына барғаны үшін қаражатты өтеу (мүгедек балалар үшін); \
\n9) Мектеп бітірген күні кәмелетке толмаған және оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек; \
\n10) Орта арнаулы оқу орнында (бұдан әрі-CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) балаларының бітіруші оқу курсын (тұруға және тамақтануға арналған шығыстарды есептемегенде) төлеу жөніндегі шығыстарды (A8 - B4 грейд қызметкерлеріне) өтеу.',
    'Әлеуметтік комиссияға өтініш беру үдерісі':
        'Филиалдың әлеуметтік комиссиясына өтінішті ресімдеу - др. ДРБ әлеуметтік комиссиясының төрағасы-Погребицкий И. Е. әлеуметтік қолдау көрсету үшін қоғам қызметкерлері жүгінген кезде өтініштерді қараудың кезектілік тәртібі сақталады.',
    'Өтінішті қайда рәсімдеу керек?':
        'Сіз өзіңіздің жұмыс базаңызда(BRD) өтініш жасайсыз. Арнайы базалар жоқ.',
    'Әлеуметтік комиссияның төрағасы': 'Филиалдардағы әлеуметтік комиссияның төрағасы-филиалдың бас директоры. ОА-операциялық тиімділік жөніндегі Бас директор',
}
faq_2 = {
    'Жұмыс орнынан анықтаманы қалай алуға болады?': 'Жұмыс орнынан анықтама алуға өтінімді "HR ОҚО өтінімдері" базасында ресімдеу қажет. Жаңасын жасаңыз-филиалыңыздың атауын таңдаңыз - жұмыс орнынан анықтама беруге өтінім – жұмыскердің аты – жөнін, анықтама түрін және қажетті өлшемдерді толтырыңыз (тілі, өтілі, лауазымдық жалақысы, орташа жалақысы) – өтінімді сақтаңыз-өтінімді ОҚО-ға жіберіңіз өтінімде сіздің өтініміңіздің орындаушысы автоматты түрде көрсетіледі.',
    'Lotus Notes есептік жазбасын құру және ИС  және ЖҚБ-ға кіруге болады?': 'Lotus Notes есептік жазбасын құру үшін  өзіңіздің жетекшілік ететін құрылымдық бөлімшенің басшысына/тәлімгеріне/іс жүргізушісіне ҚББЖ  (қатынауды басқарудың бірыңғай жүйесі) өтінімді ресімдеу үшін жүгінуіңіз керек. \nПо есептік жазбаның дайындығына қарай (логині мен паролі бар файл) Help Desk-ке келесі нөмір бойынша өтінім беру қажет: +7 727 2587304 Lotus Notes есептік жазбасын орнатқаннан кейін, сіз үшін АЖ және ДҚ-ға қажетті қол жетімділікті көрсете отырып, ҚББЖ базасында өтінімді өз бетіңізше жасау қажет.',
    'Егер сіз Lotus паролін немесе ақауын ұмытып қалсаңыз, қайда барасыз?': 'Туындаған мәселелер бойынша Help Desk +77272587304 өтінімін қалдырыңыз.',
    'Аурухана парақтары жұмысшыларға төлене ме?': '1) компаниядағы үздіксіз жұмыс өтіліне байланысты қызметкерлер (кәсіподақ ұйымының мүшелері және ұжымдық ұйымға қосылған) үшін (5 жасқа дейін - орташа жалақының 40%, 5 жылдан астам - еңбекке уақытша жарамсыздық күндері үшін орташа жалақының 70%);\n2) қалған қызметкерлер үшін - заңнамада белгіленген мөлшерде.\n3) Еңбекке уақытша жарамсыздық парағы / o парағы',
    'Еңбекке жарамсыздық парағын кім толтырады?': 'Еңбекке жарамсыздық парағын құрылымдық бөлімшенің  табельшісі/іс жүргізушісі толтырады. Еңбекке жарамсыздық парағында "Қазақтелеком" АҚ филиалы - "Бөлшек бизнес жөніндегі дивизион" -  филиалының атауы және өз лауазымы көрсетіледі.',
    'Еңбекке уақытша жарамсыздық парағын кімге тапсыру керек (аурухана парағы)': 'Еңбекке уақытша жарамсыздық парағын тапсырар алдында оны толтырып, оның тікелей жетекшісі қол қою керек, егер сіздің кеңсеңізде OҚO HR фронт-офисінің жұмыскері болмаса - BL екі жағынан сканерлеп, OҚO HR өтінім базасында өтінім ресімдеңіз; әйтпесе-толтырылған BL түпнұсқасын OҚO HR фронт-офисінің жұмыскеріне тапсырыңыз.',
    'Әріптестердің телефонын қайдан табуға болады?': 'Әріптестің телефонын  Қоғамның "Телефон анықтамалығы" базасынан таба аласыз-телефон нөмірлері, жұмыскерлерді бөлім бойынша іздеу',
    'Айналып өту парағы. Ол қашан ресімделеді?': '1) Жұмыстан босату туралы өтінішті ресімдегенде, үшінші парақта автоматты түрде кету парағы жасалады және қол қоюшылар көрсетіледі.\n2) филиалға/біржақты тәртіппен/ ауыстыру кезінде кету парағын өз жұмыс базаларында ресімделеді,'
}
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']



markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("😊Welcome курс | Бейімделу")
# button2 = types.KeyboardButton("Өтініштер")
button3 = types.KeyboardButton("🗃️Білім базасы")
button4 = types.KeyboardButton("👷ҚТ ж ЕҚ кәртішкесін толтыру")
button5 = types.KeyboardButton("📄Менің сұрағым бар")
button6 = types.KeyboardButton("🧐Менің профилім")
button7 = types.KeyboardButton("🖥Портал 'Бірлік'")
markup.add(button, button3, button7, button5, button4, button6)


def send_welcome_message(bot, message):
    welcome_message = f'Сәлем {db_connect.get_firstname(message)}👋'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    with open("images/menu.jpg", 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Менің сценарийімде бірнеше пәрмендер бар:\
        \n/menu — негізгі мәзірге оралу (сіз мұны демонстрация кезінде кез келген уақытта жасай аласыз!)\
        \n/help - әзірлеушілермен байланысыңыз (егер қиындықтарға тап болсаңыз немесе сізде жақсарту үшін ұсыныстар "
                                      "болса, осы пәрменді қолданыңыз) \
        \n/start — ботты қайта іске қосыңыз\
        \n/language - боттың тілін өзгерту\
        \n\n Пәрмендерді /menu бөлігіндегі хабарламалар жолағынан таба аласыз (төменгі сол жақта) "
                                      "немесе жай ғана пәрменнің атауына, '/' ұмытпаңыз! белгісіне келіңіз.")


def send_error(bot, message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error kaz.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Ой, бірдеңе дұрыс болмады... /menu түймесін басу арқылы ботты қайта іске қосып көріңіз")


def adaption(bot, message):
    if message.text == '😊Welcome курс | Бейімделу':
        db_connect.cm_sv_db(message, 'Welcome курс | Бейімделу')
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton('Айтыңызшы!', callback_data='Айтыңызшы!')
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue_kaz.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, 'Бастау үшін сізге мені қалай пайдалану керектігін айтамын 🫡',
                         reply_markup=markup_adapt)


def performer_text(appeal_info, message):
    status = kaz_get_status(message, appeal_info[0])
    categories_ = categories
    if categories_.get(str(appeal_info[3]), {}).get('name', None) is None:
        categories_ = rus.categories
    category = db_connect.rename_category_to_kaz(rus.categories, categories, appeal_info[3])
    text = f"Өтініш <b>ID</b> {appeal_info[0]}\n\n" \
           f" Мәртебесі: {status}\n" \
           f" Құрылған күні: {str(appeal_info[5])}\n" \
           f" Санат: {category}\n" \
           f" Өтініш мәтіні: {str(appeal_info[4])}\n" \
           f" Соңғы мәртебе өзгерген күн: {str(appeal_info[6])}\n\n" \
           f"Орындаушы\n" \
           f" ТАӘ: {categories_.get(str(appeal_info[3]), {}).get('name', None)}\n" \
           f" Телефон нөмірі: {categories_.get(str(appeal_info[3]), {}).get('phone_num', None)}\n" \
           f" Email: {categories_.get(str(appeal_info[3]), {}).get('email', None)}\n" \
           f" Telegram: {categories_.get(str(appeal_info[3]), {}).get('telegram', None)}\n\n" \
           f" Пікір: {str(appeal_info[8])}"
    return text


def kaz_get_status(message, appeal_id):
    language = db_connect.get_language(message)
    status = db_connect.get_status(appeal_id)[0][0]
    if language == "kaz":
        if status == "Решено":
            return "Шешілді"
        elif status == "В процессе":
            return "Процесінде"
        return "Өтініш қабылданды"
    return status


def call_back(bot, call):
    if call.data == 'Айтыңызшы!':
        db_connect.cm_sv_db(call.message, 'Айтыңызшы!')
        bot.send_photo(call.message.chat.id, photo=open('images/picture kaz.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Менде пернетақта бар⌨️, оның көмегімен сіз бөлімдерге өтіп, өзіңізге "
                                               "қажетті ақпаратты ала аласыз",
                         reply_markup=markup_callback)
    elif call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images/hello kaz.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Төмендегі түймешікті басыңыз👇🏻, жалғастырамыз.", reply_markup=markup_callback)
    elif call.data == "Кеттік!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo_kaz.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "'Қазақтелеком' АҚ - Қазақстан Республикасы Министрлер Кабинетінің "
                                               "1994 жылғы 17 маусымдағы қаулысына сәйкес құрылған, Қазақстанның ірі "
                                               "телекоммуникациялық компаниясы.📌Бізде сізге арнайы дайындалған "
                                               "Компанияның қысқаша тарихы бар. Төмендегі файлдарды ашып, онымен танысыңыз.")
        bot.send_document(call.message.chat.id, open('images/Наша история 1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/Наша история 2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Ал, Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Егер бәрі түсінікті болса, біз жалғастырамыз ба?", reply_markup=markup_callback)
    elif call.data == "Ал, Кеттік!":
        bot.send_message(call.message.chat.id, "Сізде Бадди бар ма?😁")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Егер жоқ болса, көңіліңізді түсірмеңіз, ол сізді жақын арада табады!")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Ия, көбірек білгім келеді!", callback_data="Ия, көбірек білгім келеді!")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Сізде бұл кім және маған не үшін қажет деген сұрақ туындаса, мен жауап беремін",
                         reply_markup=markup)
    elif call.data == "Ия, көбірек білгім келеді!":
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сонымен, корпоративтік e-mail-ді тексеріңіз, сізге Баддиден біздің Компаниядағы бейімделу "
                         "бағдарламасымен танысу туралы хабарлама келген шығар. ")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Қабылданды!", callback_data="Қабылданды!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 3.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Қабылданды!":
        bot.send_message(call.message.chat.id,
                         "Әдетте қолдау бір айға созылып, көбіне сынақ мерзімі сәтті аяқталғанға дейін жалғасады.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Айтпақшы, кез-келген бөлімнің жұмыскері Бадди бағдарламасына қатыса алады және бұл өте "
                         "жақсы-көлденең және тік байланыстар кеңейеді.")
        time.sleep(0.75)
        markup_1 = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton("Керемет, әрі қарай жалғастырамыз!",
                                              callback_data="Керемет, әрі қарай жалғастырамыз!")
        markup_1.add(button_1)
        bot.send_message(call.message.chat.id,
                         text="Болашақта жаңадан келгендерге бейімделуге көмектесіп, сіз де Бадди бола аласыз!  😊",
                         reply_markup=markup_1)
    elif call.data == "Керемет, әрі қарай жалғастырамыз!":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-1")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1_kaz.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-1":
        bot.send_message(call.message.chat.id,
                         "Біздің компания 9 филиалдан тұрады және олардың аббревиатураларын күн сайын жұмыста міндетті"
                         " түрде естисіз.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сол себепті Компанияның құрылымымен танысайық.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сізге бейтаныс терминдер немесе аббревиатуралар кездессе, онда біз сізге білім қорында "
                         "глоссарий дайындадық.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сіз әрқашан негізгі мәзірден білім қорын таба аласыз.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-3")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-3":
        bot.send_message(call.message.chat.id, '"Қазақтелеком" АҚ-да түрлі бағыттар бойынша өнімдер бар:\
                                             \n🌍Ғаламтор \n📞Телефон\n📹Бейнебақылау\n🖥️TV+ \n🛍️Дүкен shop.telecom.kz')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-4")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Өнімдер мен олардың тарифтері туралы өзекті ақпаратты сіз әрқашан сайттан таба аласыз "
                         "telecom.kz",
                         reply_markup=markup_callback)
    elif call.data == "Келесі-4":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-5")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users_kaz.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-5":
        bot.send_message(call.message.chat.id,
                         '☎️" Қазақтелеком " АҚ-да "Нысана" жедел желісі біріктірілген, онда әр жұмыскер QR-код арқылы '
                         'немесе төмендегі суретте көрсетілген байланыс нөміріне хабарласа алады. ')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center_kaz.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-6":
        bot.send_message(call.message.chat.id,
                         "Керемет! \nКомпания туралы негізгі ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі "
                         "білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.Компания туралы негізгі "
                         "ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын "
                         "сұрақтар бөлімін пайдалана аласыз.")
        time.sleep(0.75)
        markup_welcome = types.InlineKeyboardMarkup()
        button_ = types.InlineKeyboardButton("Түсінікті!", callback_data="Түсінікті!")
        markup_welcome.add(button_)
        bot.send_photo(call.message.chat.id, photo=open('images/picture kaz.jpg', 'rb'), reply_markup=markup_welcome)
    elif call.data == "Түсінікті!":
        db_connect.cm_sv_db(call.message, 'Welcome курс | Бейімделу end')
        bot.send_message(call.message.chat.id,
                         "Құттықтаймыз!\nСіз Welcome курсынан өттіңіз. \n\nКомпанияға қош келдіңіз!")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Негізгі мәзірге өту үшін /menu пәрменін теріңіз немесе басыңыз")
    elif call.data == "checkPoint":
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton("iOS", callback_data="iOS")
        button_p2 = types.InlineKeyboardButton("Android", callback_data="Android")
        markup_p.add(button_p1, button_p2)
        bot.send_message(str(call.message.chat.id), "Санатты таңдаңыз", reply_markup=markup_p)
    elif call.data == portal_[5]:
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton(text="App Store сілтемесі",
                                               url="https://apps.apple.com/ru/app/check-point-capsule-connect/id506669652")
        markup_p.add(button_p1)
        bot.send_message(str(call.message.chat.id), "iOS жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/giK26_GgVgE ", reply_markup=markup_p)
    elif call.data == portal_[6]:
        markup_p = types.InlineKeyboardMarkup()
        button_p2 = types.InlineKeyboardButton(text="PlayMarket сілтемесі",
                                               url="https://play.google.com/store/apps/details?id=com.checkpoint.VPN&hl=en&gl=US&pli=1")
        markup_p.add(button_p2)
        bot.send_message(str(call.message.chat.id), "Android жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/KjL9tpunb4U", reply_markup=markup_p)
    elif str(call.data).isdigit():
        appeal_id = str(call.data)
        appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
        image_data = db_connect.get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        text = performer_text(appeal_info, message=call.message)
        bot.send_message(call.message.chat.id, text)
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
        text = performer_text(appeal_info, message=call.message)
        bot.send_message(appeal_info[1], "Сіздің өтінішіңіздің мәртебесі өзгертілді")
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
            bot.send_message(appeal_info[1], "Шешілген үндеуді 1-ден 5-ке дейін бағалаңыз\n\nҚайда 1-өте нашар, "
                                             "5-керемет", reply_markup=markup_callback)
    # elif db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)addcomment') is not None:
    #     appeal_id = db_connect.extract_number_from_status_change(str(call.data), r'^(\d+)addcomment')
    #     msg = bot.send_message(call.message.chat.id, 'Введите комментарий')
    #     bot.register_next_step_handler(msg, add_comment, bot, appeal_id)
    elif db_connect.extract_numbers_from_status_change_decided(str(call.data)) is not None:
        evaluation, appeal_id = db_connect.extract_numbers_from_status_change_decided(str(call.data))
        db_connect.set_evaluation(appeal_id, evaluation)
        bot.edit_message_text("Пікіріңіз үшін және жақсы адам болуға көмектескеніңіз үшін рахмет", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    else:
        db_connect.admin_appeal_callback(call, bot, add_comment)


def add_comment(message, bot, appeal_id):
    comment = message.text + " \n" + str(db_connect.get_comment(appeal_id)[0][0])
    db_connect.set_comment(appeal_id, comment)
    appeal_info = db_connect.get_appeal_by_id(appeal_id)[0]
    bot.send_message(appeal_info[1], "Сіздің үндеуіңізге түсініктеме қосылды")
    image_data = db_connect.get_image_data(appeal_id)
    try:
        bot.send_photo(appeal_info[1], image_data)
    except:
        print("error")
    text = performer_text(appeal_info, message)
    bot.send_message(appeal_info[1], text)
    bot.send_message(message.chat.id, "Комментарий добавлен")


def appeal(bot, message, message_text):
    db_connect.set_appeal_field(message, True)
    # if message_text == "Өтініштер":
    #     db_connect.cm_sv_db(message, 'Өтініштер')
    #     markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1_ap = types.KeyboardButton("Менің өтініштерім")
    #     button2_ap = types.KeyboardButton("Өтінішті қалдыру")
    #     markup_ap.add(button1_ap, button2_ap)
    #     bot.send_message(message.chat.id,
    #                      "B осы бөлімде Сіз өзіңізді қызықтыратын мәселелер бойынша өтінішіңізді корпоративтік университетке қалдыра аласыз.",
    #                      reply_markup=markup_ap)
    #     time.sleep(0.75)
    #     bot.send_message(message.chat.id,
    #                      "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")
    if message_text == "Менің өтініштерім":
        db_connect.cm_sv_db(message, 'Менің өтініштерім')
        markup_a = db_connect.appealInlineMarkup(message, "kaz", rus.categories, categories)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Мұнда сіз өтініштеріңіздің күйін бақылай аласыз",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Бұл жерде әлі бос,\nбірақ сіз апелляцияны қалдыра аласыз және ол осы жерде көрсетіледі")
    elif message_text == "Өтінішті қалдыру" or message_text == portal_bts[2]:
        db_connect.cm_sv_db(message, 'Өтінішті қалдыру')
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Иә")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Ақпарат дұрыс па?", reply_markup=markup_ap)
    elif message_text == "Иә":
        if db_connect.get_category_users_info(message) == "portal":
            appeal(bot, message, "portal")
            return
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap = db_connect.generate_buttons(categories, markup_ap)
        bot.send_message(message.chat.id, "Өтініш санатын таңдаңыз", reply_markup=markup_ap)
    elif message_text == "portal":
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text in categories.keys():
        db_connect.cm_sv_db(message, message_text)
        category = db_connect.rename_category_to_rus(rus.categories, categories, message.text)
        db_connect.set_category(message, category)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:\nСіз сондай-ақ фотосуретті тастай аласыз')
    elif db_connect.get_appeal_field(message) and db_connect.get_category_users_info(message) != ' ':
        now = datetime.now() + timedelta(hours=6)
        now_updated = db_connect.remove_milliseconds(now)
        category = db_connect.get_category_users_info(message)
        if category == "portal":
            user_info = f"Аты Тегі: {db_connect.get_firstname(message)} {db_connect.get_lastname(message)}\n" \
                        f"Табель нөмірі: {db_connect.get_table_number(message)}\n" \
                        f"Телефон нөмірі: {db_connect.get_phone_number(message)}\n" \
                        f"Email: {db_connect.get_email(message)}\n" \
                        f"Филиалы: {db_connect.get_branch(message.chat.id)}"
            new_message = f'{user_info} \n {message.text}'
            db_connect.send_gmails(new_message, "Портал 'Бірлік'")
            bot.send_message(str(message.chat.id), "Сіздің өтінішіңіз сәтті жіберілді")
            return
        categories_ = categories
        if categories_.get(str(category), {}).get('name', None) is None:
            categories_ = rus.categories
        performer_id = categories_.get(category, {}).get('id', None)
        category_ = db_connect.rename_category_to_kaz(rus.categories, categories, db_connect.get_category_users_info(message))

        # if db_connect.get_is_appeal_anon_users_info(message.chat.id):
        #     appeal_id = db_connect.add_appeal(message.chat.id, "Өтініш қабылданды", category, message.text,
        #                                       now_updated, now_updated, performer_id, ' ', True)
        #     status = kaz_get_status(message, appeal_id)
        #     text = f"Өтініш ID {appeal_id}\n" \
        #            f"Мәртебесі: {status}\n" \
        #            f"Санат: {db_connect.get_category_users_info(message)}\n" \
        #            f"Өтініш: {message.text}\n" \
        #            f"Құрылған күні: {now_updated}"
        # else:
        appeal_id = db_connect.add_appeal(message.chat.id, "Обращение принято", category, message.text,
                                          now_updated, now_updated, performer_id, ' ', False)
        status = kaz_get_status(message, appeal_id)
        bot.send_message(message.chat.id, "Сіздің өтініштеріңіз қабылданды")
        bot.send_message(message.chat.id, "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының "
                                          "сол жағында")
        if message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(db_connect.TOKEN, file_info.file_path))
            db_connect.set_image_data(appeal_id, file)
            image_data = db_connect.get_image_data(appeal_id)
            bot.send_photo(performer_id, image_data)
            db_connect.set_appeal_text(appeal_id, message.caption)
        text = f"Өтініш ID {appeal_id}\n\n" \
               f"Мәртебесі: {status}\n" \
               f"Аты Тегі: {db_connect.get_firstname(message)} {db_connect.get_lastname(message)}\n" \
               f"Табель нөмірі: {db_connect.get_table_number(message)}\n" \
               f"Телефон нөмірі: {db_connect.get_phone_number(message)}\n" \
               f"Email: {db_connect.get_email(message)}\n" \
               f"Санат: {category_}\n" \
               f"Өтініш: {message.text}\n" \
               f"Құрылған күні: {now_updated}"
        markup_a1 = types.InlineKeyboardMarkup()
        callback_d = f"{appeal_id}statusinprocess"
        button_a = types.InlineKeyboardButton("Обращение просмотрено", callback_data=callback_d)
        markup_a1.add(button_a)
        bot.send_message(performer_id, text, reply_markup=markup_a1)
        db_connect.clear_appeals(message)
    else:
        db_connect.admin_appeal(bot, message, message_text, categories)


def faq(bot, message):
    if message.text == "Жиі қойылатын сұрақтар":
        db_connect.cm_sv_db(message, 'Жиі қойылатын сұрақтар')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("HR сұрақтары")
        button_1 = types.KeyboardButton("Қарыздар бойынша сұрақтар")
        markup_faq.add(button_d, button_hr, button_1)
        bot.send_message(message.chat.id, "Мұнда сіз жиі қойылатын сұрақтарға жауап таба аласыз",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Егер жаңа бөлім немесе сұрақтарға жауап қосу бойынша ұсыныстар/идеялар болса, бізге жазыңыз "
                         "info.ktcu@telecom.kz - Біз сіздің ұсынысыңызды міндетті түрде қарастырамыз және "
                         "сізбен байланысамыз.")
    elif message.text == "Демеу":
        db_connect.cm_sv_db(message, 'Демеу')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "HR сұрақтары":
        db_connect.cm_sv_db(message, 'HR сұрақтары')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "Қарыздар бойынша сұрақтар":
        db_connect.cm_sv_db(message, 'Қарыздар бойынша сұрақтар')
        branch = db_connect.get_branch(message.chat.id)
        if branch == "Центральный Аппарат":
            markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            markup_faq = db_connect.generate_buttons(branches[1:], markup_faq)
            bot.send_message(message.chat.id, "Филиалды таңдаңыз", reply_markup=markup_faq)
        elif branch in branches[1:]:
            bot.send_message(message.chat.id, f"Филиал {branch}\n\n"
                                              "Қарыздар бойынша сұрақтарды келесі байланыс нөміріне жіберуге болады")
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
    if message.text == "👷ҚТ ж ЕҚ кәртішкесін толтыру":
        db_connect.cm_sv_db(message, 'ҚТ ж ЕҚ кәртішкесін толтыру')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Қауіпті фактор | шарт")
        button2 = types.KeyboardButton("Жұмысты орындау тәртібі")
        button3 = types.KeyboardButton("Ұсыныстар | Идеялар")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id, "Сіз қауіпті факторды, қауіпті мінез-құлықты байқадыңыз ба немесе жұмыс "
                                          "орнындағы қауіпсіздік пен еңбекті қорғауды жақсарту бойынша ұсыныстарыңыз/"
                                          "идеяларыңыз бар ма?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Қажетті оқиғаны таңдап, ҚТ ж ЕҚ кәртішкесін толтырыңыз.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")
    elif message.text == "Қауіпті фактор | шарт":
        db_connect.cm_sv_db(message, 'Қауіпті фактор | шар')
        bot.send_message(message.chat.id, "Егер Сіз жұмыс барысында қауіпті факторды немесе жағдайды байқасаңыз, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")
    elif message.text == "Жұмысты орындау тәртібі":
        db_connect.cm_sv_db(message, 'Жұмысты орындау тәртібі')
        bot.send_message(message.chat.id, "Егер Сіз жұмыстарды орындау кезінде мінез-құлық тәуекелдерін байқасаңыз, "
                                          "төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                        \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/"
                                          "viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз "
                         "/menu енгізу жолағының сол жағындағы командалар мәзірінен.")
    elif message.text == "Ұсыныстар | Идеялар":
        db_connect.cm_sv_db(message, 'Ұсыныстар | Идеялар')
        bot.send_message(message.chat.id, "Егер Сізде ұсыныстар немесе идеялар болса, төмендегі сілтемеге өтіп, "
            "сауалнаманы толтырыңыз:"
            "\nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")


def instructions(bot, message):
    if message.text == "Логотиптер және Брендбук":
        db_connect.cm_sv_db(message, 'Логотиптер және Брендбук')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қазақтелеком АҚ")
        button2_i = types.KeyboardButton("Корпоративтік Университет")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Модемдер | Теңшеу":
        db_connect.cm_sv_db(message, 'Модемдер | Теңшеу')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("ADSL модемі")
        button2_i = types.KeyboardButton("IDTV консолі")
        button3_i = types.KeyboardButton("ONT модемдері")
        button4_i = types.KeyboardButton("Router 4G and Router Ethernet")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Lotus | Нұсқаулар":
        db_connect.cm_sv_db(message, 'Lotus | Нұсқаулар')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Филиал серверлері бойынша деректер")
        button2_i = types.KeyboardButton("Lotus Орнату нұсқаулары")
        button3_i = types.KeyboardButton("Lotus орнату файлы")
        markup_instr.add(button1_i, button2_i, button3_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    # elif message.text == "portal.telecom.kz | Нұсқаулар":
    #     db_connect.cm_sv_db(message, 'portal.telecom.kz | Нұсқаулар')
    #     markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1 = types.KeyboardButton("Мобильді нұсқа")
    #     button2 = types.KeyboardButton("ДК немесе ноутбук")
    #     markup_portal.add(button1, button2)
    #     bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_portal)
    elif message.text == "Checkpoint VPN | Қашықтан жұмыс":
        db_connect.cm_sv_db(message, 'Checkpoint VPN | Қашықтан жұмыс')
        checkpoint(bot, message, portal_bts[1])

    elif message.text == "Жеке кабинет telecom.kz":
        db_connect.cm_sv_db(message, 'Жеке кабинет telecom.kz')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қызметті қалай төлеуге болады")
        button2_i = types.KeyboardButton("Төлем туралы мәліметтерді қалай көруге болады")
        button3_i = types.KeyboardButton("Қосылған қызметтерді қалай көруге болады")
        button4_i = types.KeyboardButton("'Менің Қызметтерім' Бөлімі")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Iссапар | Рәсімдеу тәртібі":
        db_connect.cm_sv_db(message, 'Iссапар | Рәсімдеу тәртібі')
        bot.send_document(message.chat.id, document=open("files/Порядок оформления командировки.pdf", 'rb'))
    elif message.text == "Филиал серверлері бойынша деректер":
        bot.send_document(message.chat.id, document=open("files/Данные по всем lotus серверам.xlsx", 'rb'))
    elif message.text == "Lotus Орнату нұсқаулары":
        bot.send_document(message.chat.id, document=open("files/Инструкция по Lotus Notes на домашнем пк_.docx", 'rb'))
    elif message.text == "Lotus орнату файлы":
        bot.send_message(message.chat.id, "Установочный файл Lotus Notes: "
                                          "\nhttps://drive.google.com/drive/folders/1MrpjeXavmRnUMvYUiTcylhxAIEA6dvBb?usp=drive_link")
    elif message.text == "CheckPoint Орнату нұсқаулығы":
        bot.send_document(message.chat.id, document=open("files/Инструкция по установке CheckPoint.pdf", 'rb'))
    elif message.text == "Checkpoint орнату файлы":
        bot.send_document(message.chat.id, document=open("files/E85.40_CheckPointVPN.msi", 'rb'))
    elif message.text == "Қазақтелеком АҚ":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративтік Университет":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
    elif message.text == "Қызметті қалай төлеуге болады":
        bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
    elif message.text == "Төлем мәліметтерін қалай көруге болады":
        bot.send_document(message.chat.id,
                          document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
    elif message.text == "Қосылған қызметтерді қалай көруге болады":
        bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
    elif message.text == "Менің Қызметтерім 'Бөлімі'":
        bot.send_document(message.chat.id, document=open("files/раздел «МОИ УСЛУГИ».pdf", 'rb'))
    elif message.text == "ADSL модемі":
        bot.send_message(message.chat.id,
                         "'ADSL модемі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1ZMcd4cVuX8_JUJ8OoN0rYx5d5DjwlEbz?usp=drive_link")
    elif message.text == "IDTV консолі":
        bot.send_message(message.chat.id,
                         "'IDTV консолі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1ZFbUrKi9QITBLkJQ93I45dxhINSsgv7H?usp=drive_link")
    elif message.text == "ONT модемдері":
        bot.send_message(message.chat.id,
                         "'ONT модемдері' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1IiLJ14dKF3wQhoLYb18jJMLD6BNz3K7x?usp=drive_link")
    elif message.text == "Router 4G and Router Ethernet":
        bot.send_message(message.chat.id,
                         "'Router 4G and Router Ethernet' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1EkzERKwa-DTnMW86-qJGbc_YAU2k6A74?usp=drive_link")


def kb(bot, message):
    if message.text == "🗃️Білім базасы":
        db_connect.cm_sv_db(message, 'Білім базасы')
        db_connect.set_bool(message, False, False)
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_kb1 = types.KeyboardButton("Нұсқаулық базасы")
        button_kb2 = types.KeyboardButton("Глоссарий")
        button_kb3 = types.KeyboardButton("Пайдалы сілтемелер")
        markup_kb.add(button_kb2, button_kb1, button_kb3)
        bot.send_message(message.chat.id, "Мобильді білім қорына қош келдіңіз!", reply_markup=markup_kb)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Мұнда сіз өзіңізге қажетті Bac нұсқаулығын таба аласыз немесе пайдалана аласыз "
                         "біз өзімізде қолданатын негізгі терминдер бойынша іздеу жүйесінің глоссарийі "
                         "компаниялар күн сайын.")
    elif message.text == "Нұсқаулық базасы":
        db_connect.cm_sv_db(message, 'Нұсқаулық базасы')
        db_connect.set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1_instr = types.KeyboardButton("Логотиптер және Брендбук")
        button2_instr = types.KeyboardButton("Жеке кабинет telecom.kz")
        button3_instr = types.KeyboardButton("Модемдер | Теңшеу")
        button4_instr = types.KeyboardButton("Lotus | Нұсқаулар")
        button6_instr = types.KeyboardButton("Checkpoint VPN | Қашықтан жұмыс")
        button7_instr = types.KeyboardButton("Iссапар | Рәсімдеу тәртібі")
        markup_instr.add(button4_instr, button6_instr, button1_instr, button7_instr, button2_instr, button3_instr)
        bot.send_message(message.chat.id, "Бұл жерде өзіңізге пайдалы нұсқаулықты таба аласыз.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Нұсқаулықты таңдау үшін санатты, содан кейін нұсқаулықтың өзін мәзір-пернетақтадан таңдаңыз⌨️.")
    elif message.text == "Глоссарий":
        db_connect.cm_sv_db(message, 'Глоссарий')
        db_connect.set_bool(message, False, True)
        bot.send_message(message.chat.id, "'Қазақтелеком' AҚ компаниясындағы терминдер мен "
                                          "аббревиатуралардың глоссарийі.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Аббревиатураның немесе терминнің түсіндірмесін немесе сипаттамасын "
                                          "алу үшін сөзді теріп, ақпарат алу үшін жіберіңіз.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Маңызды!\nСөзді қатесіз және артық таңбаларсыз енгізіңіз. Аббревиатураларды бас әріппен "
                         "енгізу маңызды. Мысалы: ЕППК, ОДС, ДИТ.")
    elif message.text == "Пайдалы сілтемелер":
        db_connect.cm_sv_db(message, 'Пайдалы сілтемелер')
        db_connect.set_bool(message, False, False)
        time.sleep(0.5)
        markup = db_connect.useful_links()
        bot.send_message(message.chat.id, "Пайдалы сілтемелер", reply_markup=markup)


def menu(bot, message):
    db_connect.set_bool(message, False, False)
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)


def glossary(bot, message):
    text1 = f"Сіздің сұранысыңыз бойынша келесі мән табылды:"
    text2 = "Біздің info.ktcu@telecom.kz поштамызға хат жолдау арқылы жұмысымызды жақсартуға көмектесе аласыз - " \
            "біз міндетті түрде қарастырамыз."
    db_connect.glossary(bot, message, text1, text2)


def profile(bot, message):
    db_connect.cm_sv_db(message, "🧐Менің профилім")
    markup_ap = types.InlineKeyboardMarkup(row_width=1)
    button1_ap = types.InlineKeyboardButton("Атын Өзгерту", callback_data="Изменить Имя")
    button2_ap = types.InlineKeyboardButton("Тегін өзгерту", callback_data="Изменить Фамилию")
    button3_ap = types.InlineKeyboardButton("Телефон нөмірін өзгерту", callback_data="Изменить номер телефона")
    button4_ap = types.InlineKeyboardButton("Электрондық поштаны өзгерту", callback_data="Изменить email")
    button5_ap = types.InlineKeyboardButton("Табель нөмірін өзгерту", callback_data="Изменить табельный номер")
    button6_ap = types.InlineKeyboardButton("Филиалды өзгерту", callback_data="Изменить филиал")
    markup_ap.add(button1_ap, button2_ap, button3_ap, button4_ap, button5_ap, button6_ap)
    bot.send_message(message.chat.id, f"Сақталған ақпарат\n\n"
                                      f"Аты: {db_connect.get_firstname(message)}\n"
                                      f"Тегі: {db_connect.get_lastname(message)}\n"
                                      f"Телефон нөмірі: {db_connect.get_phone_number(message)}\n"
                                      f"Email: {db_connect.get_email(message)}\n"
                                      f"Табель нөмірі: {db_connect.get_table_number(message)}\n"
                                      f"Филиалы: {db_connect.get_branch(message.chat.id)}",
                     reply_markup=markup_ap)


def questions(bot, message):
    button_q = types.KeyboardButton("Менің өтініштерім")
    button_q1 = types.KeyboardButton("Өтінішті қалдыру")
    button_q2 = types.KeyboardButton("Жиі қойылатын сұрақтар")
    markup_q = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_q.add(button_q2, button_q1, button_q)
    if db_connect.check_id(categories, str(message.chat.id)):
        markup_q.add(types.KeyboardButton("Админ панель для обращений"))
    bot.send_message(str(message.chat.id), "Бұл бөлімде сіз өзіңіздің өтінішіңізді қалдыра аласыз немесе жиі "
                                           "қойылатын сұрақтарға жауаптарды көре аласыз", reply_markup=markup_q)
    time.sleep(0.75)
    bot.send_message(message.chat.id,
                     "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")


def portal(bot, message):
    message_text = message.text
    if message_text == "🖥Портал 'Бірлік'":
        markup_p = types.ReplyKeyboardMarkup(row_width=1)
        markup_p = db_connect.generate_buttons(portal_bts, markup_p)
        bot.send_message(str(message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif message_text == portal_bts[0]:
        with open("images/Birlik_BG.jpg", 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file)
        bot.send_message(str(message.chat.id), "'Бірлік' қызметкерінің порталы - 'Қазақтелеком' АҚ-ның әрбір қызметкері"
                                               " үшін цифрлық трансформация фокустары шеңберінде құрылған бірыңғай "
                                               "интранет жүйесі."
                                               "Порталда бар және дамитын бөлімдер:\n"
                                               "▪ Профиль\n"
                                               "▪ Жаңалықтар\n"
                                               "▪ Қауымдастықтар\n"
                                               "▪ Күнтізбе\n"
                                               "▪ Компания құрылымы және бөлімше картасы\n"
                                               "▪ Кеңейтілген іздеу\n"
                                               "▪ Іс-шаралар афишасы\n"
                                               "▪ Кеңсенің интерактивті картасы\n"
                                               "▪ Сауалнамалар мен тесттер\n"
                                               "▪ Маркет және геймификация жүйесі\n\n"
                                               "'Бірлік' қызметкер порталының артықшылықтары:\n"
                                               "- Бірыңғай ақпараттық кеңістік\n"
                                               "Қажетті ақпаратты жылдам іздеу\n"
                                               "Тиімді ынтымақтастық және топтық жұмыс\n"
                                               "Компанияның корпоративтік мәдениеті мен құндылықтарын нығайту\n"
                                               "Сыртқы модульдерді бір кеңістікке біріктіру")
    elif message_text == portal_[0]:
        markup_p = types.InlineKeyboardMarkup()
        button_p = types.InlineKeyboardButton("Checkpoint керек пе?", callback_data="checkPoint")
        markup_p.add(button_p)
        bot.send_message(str(message.chat.id), "IOS және Android жүйелеріндегі қызметкер порталына қалай кіруге болады | portal.telecom.kz\nhttps://youtu.be/WJdS1aIBe1I", reply_markup=markup_p)
    elif message_text == portal_bts[3]:
        markup_p = types.ReplyKeyboardMarkup(row_width=1)
        markup_p = db_connect.generate_buttons(portal_guide, markup_p)
        bot.send_message(str(message.chat.id), "Сұрақты таңдаңыз", reply_markup=markup_p)
    elif message_text == portal_bts[2]:
            db_connect.set_category(message, "portal")
            appeal(bot, message, message_text)
    else:
        if checkpoint(bot, message, message_text):
            return
        db_connect.check_portal_guide(bot, message, message_text, portal_guide)


def checkpoint(bot, message, message_text):
    if message_text == portal_bts[1]:
        db_connect.cm_sv_db(message, portal_bts[1])
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(portal_[0])
        button2 = types.KeyboardButton(portal_[1])
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_portal)
    elif message_text == portal_[1]:
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_p = types.KeyboardButton("Қалай кіруге болады")
        button2_p = types.KeyboardButton("Жеке профиль")
        button3_p = types.KeyboardButton("Порталдан ССП өту")
        markup_pk.add(button1_p, button2_p, button3_p)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_pk)
    elif message_text == portal_[2]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'ДК арқылы қызметкердің порталына қалай кіруге"
                                          " болады?'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/vsRIDqt_-1A")
    elif message_text == portal_[3]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Жеке профильді қалай толтыруға болады?'"
                                          "төмендегі сілтемеге өтіңіз \nhttps://youtu.be/V9r3ALrIQ48")
    elif message_text == portal_[4]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Порталдан ССП өту'төмендегі сілтемеге өтіңіз"
                                          "\nhttps://youtu.be/wnfI4JpMvmE")
    else:
        return False
    return True
