from telebot import *
import db_connect


categories = {
    'Learning.telecom.kz | Техникалық қолдау': 'info.ktcu@telecom.kz',
    'Оқыту | Корпоративтік Университет': 'info.ktcu@telecom.kz',
    '"Нысана" қолдау қызметі': 'nysana@cscc.kz',
    'Комплаенс қызметіне хабарласыңыз': 'tlek.issakov@telecom.kz',
}

faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары", "Қарыздар бойынша сұрақтар"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["ЕҚЕҚ кәртішкесін толтыру", "Қауіпті фактор | шарт", "Жұмысты орындау тәртібі", "Ұсыныстар | Идеялар"]
kb_field = ["Білім базасы", "Нұсқаулық базасы", "Глоссарий", "Пайдалы сілтемелер"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар",
                "Мобильді нұсқа", "ДК немесе ноутбук", "portal.telecom.kz | Нұсқаулар",
                "Checkpoint VPN | Қашықтан жұмыс", "Iссапар | Рәсімдеу тәртібі",
                "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту", "Филиал серверлері бойынша деректер",
                "Lotus Орнату нұсқаулары", "Lotus орнату файлы", "Қазақтелеком АҚ",
                "Корпоративтік Университет", "Қызметті қалай төлеуге болады", "Төлем туралы мәліметтерді қалай көруге болады",
                "Қосылған қызметтерді қалай көруге болады", "'Менің Қызметтерім' Бөлімі", "ADSL модемі",
                "IDTV консолі", "ONT модемдері", "Router 4G and Router Ethernet", "CheckPoint Орнату нұсқаулығы",
                "Checkpoint орнату файлы"]
instr_field = ["Брендбук және логотиптер", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар"]
adapt_field = ["Welcome курс | Бейімделу"]
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
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Рознечному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("Welcome курс | Бейімделу")
button2 = types.KeyboardButton("Өтінішті қалдыру")
button3 = types.KeyboardButton("Білім базасы")
button4 = types.KeyboardButton("ЕҚЕҚ кәртішкесін толтыру")
button5 = types.KeyboardButton("Жиі қойылатын сұрақтар")
button6 = types.KeyboardButton("Менің профилім")
markup.add(button, button2, button3, button4, button5, button6)


def send_welcome_message(bot, message):
    # welcome_message = f'Сәлем {message.from_user.first_name}👋\
    #                    \nМен - ktbot, Компаниядағы сіздің жеке көмекшіңізбін.\
    #                    \n\nМіне, мен сізге қалай көмектесе аламын:\
    #                    \n  · ✉️ - Оқыту мәселелері бойынша өтініш жіберу;\
    #                    \n  · 🗃️ - Нұсқаулар мен глоссариймен білім қорына қол жеткізуді қамтамасыз етіңіз\
    #                    \n  · 👷 ЕҚЕҚ картасын жіберуге көмектесу;\
    #                    \n  · 📄 Жиі қойылатын сұрақтарға жауап беріңіз.\
    #                    \n\nAл егер сіз жаңа қызметкер болсаңыз, мен Welcome курсынан өтуді ұсынамын 😊.'
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
    if message.text == 'Welcome курс | Бейімделу':
        db_connect.cm_sv_db(message, 'Welcome курс | Бейімделу')
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton('Айтыңызшы!', callback_data='Айтыңызшы!')
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue_kaz.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, 'Бастау үшін сізге мені қалай пайдалану керектігін айтамын 🫡',
                         reply_markup=markup_adapt)


def call_back(bot, call):
    if call.data == 'Айтыңызшы!':
        db_connect.cm_sv_db(call.message, 'Айтыңызшы!')
        bot.send_photo(call.message.chat.id, photo=open('images/picture kaz.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Менде пернетақта бар, оның көмегімен сіз бөлімдерге өтіп, өзіңізге "
                                               "қажетті ақпаратты ала аласыз",
                         reply_markup=markup_callback)
    elif call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images/hello kaz.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Төмендегі түймешікті басыңыз, жалғастырамыз.", reply_markup=markup_callback)
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
        bot.send_message(call.message.chat.id, "Сізде Бадди бар ма?")
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
                         "Сонымен, корпоративтік e-mail-ді тексеріңіз, сізге Баддиден біздің Компаниядағы бейімделу бағдарламасымен танысу туралы хабарлама келген шығар. ")
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
                         "Айтпақшы, кез-келген бөлімнің жұмыскері Бадди бағдарламасына қатыса алады және бұл өте жақсы-көлденең және тік байланыстар кеңейеді.")
        time.sleep(0.75)
        markup_1 = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton("Керемет, әрі қарай жалғастырамыз!",
                                              callback_data="Керемет, әрі қарай жалғастырамыз!")
        markup_1.add(button_1)
        bot.send_message(call.message.chat.id,
                         text="Болашақта жаңадан келгендерге бейімделуге көмектесіп, сіз де Бадди бола аласыз!  😊",
                         reply_markup=markup_1)
    elif call.data == "Керемет, әрі қарай жалғастырамыз!":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-1")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1_kaz.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Келесі-1":
        bot.send_message(call.message.chat.id,
                         "Біздің компания 9 филиалдан тұрады және олардың аббревиатураларын күн сайын жұмыста міндетті түрде естисіз.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сол себепті Компанияның құрылымымен танысайық.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сізге бейтаныс терминдер немесе аббревиатуралар кездессе, онда біз сізге білім қорында глоссарий дайындадық.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сіз әрқашан негізгі мәзірден білім қорын таба аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-3")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Келесі-3":
        bot.send_message(call.message.chat.id, '"Қазақтелеком" АҚ-да түрлі бағыттар бойынша өнімдер бар:\
                                             \n🌍Ғаламтор \n📞Телефон\n📹Бейнебақылау\n🖥️TV+ \n🛍️Дүкен shop.telecom.kz')
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-4")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Өнімдер мен олардың тарифтері туралы өзекті ақпаратты сіз әрқашан сайттан таба аласыз "
                         "telecom.kz",
                         reply_markup=markup)
    elif call.data == "Келесі-4":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-5")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users_kaz.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Келесі-5":
        bot.send_message(call.message.chat.id,
                         '☎️" Қазақтелеком " АҚ-да "Нысана" жедел желісі біріктірілген, онда әр жұмыскер QR-код арқылы '
                         'немесе төмендегі суретте көрсетілген байланыс нөміріне хабарласа алады. ')
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center_kaz.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Келесі-6":
        bot.send_message(call.message.chat.id,
                         "Керемет! \nКомпания туралы негізгі ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі "
                         "білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.Компания туралы негізгі "
                         "ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын "
                         "сұрақтар бөлімін пайдалана аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Түсінікті!", callback_data="Түсінікті!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/picture kaz.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Түсінікті!":
        db_connect.cm_sv_db(call.message, 'Welcome курс | Бейімделу end')
        bot.send_message(call.message.chat.id,
                         "Құттықтаймыз!\nСіз Welcome курсынан өттіңіз. \n\nКомпанияға қош келдіңіз!")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Негізгі мәзірге өту үшін /menu пәрменін теріңіз немесе басыңыз")


def appeal(bot, message, message_text):
    db_connect.set_appeal_field(message, True)
    if message_text == "Өтінішті қалдыру":
        db_connect.cm_sv_db(message, 'Өтінішті қалдыру')
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Ия, дұрыс")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Ақпарат дұрыс па?", reply_markup=markup_ap)
    elif message_text == 'Ия, дұрыс':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in categories:
            button = types.KeyboardButton(key)
            markup.add(button)
        bot.send_message(message.chat.id,
                         "Бұл бөлімде Корпоративтік университетке сізді қызықтыратын мәселелер бойынша өтініш қалдыра аласыз.",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Санатты таңдау үшін телеграммдағы пернетақтаны басыңыз (әдетте бұл белгі енгізу жолағының оң жағында болады).")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында ")
    elif message.text in categories.keys():
        db_connect.cm_sv_db(message, message.text)
        db_connect.set_category(message, message.text)
        bot.send_message(message.chat.id, "Өтінішіңізді енгізіңіз")
    elif db_connect.get_appeal_field(message) and db_connect.get_category_users_info(message):
        user_info = f"Имя Фамилия: {db_connect.get_firstname(message)} {db_connect.get_lastname(message)}\n" \
                    f"Табельный номер: {db_connect.get_table_number(message)}\n" \
                    f"Номер телефона: {db_connect.get_phone_number(message)}\n" \
                    f"Email: {db_connect.get_email(message)}\n" \
                    f"Филиал: {db_connect.get_branch(message.chat.id)}"
        new_message = f'{user_info} \n {message.text}'
        db_connect.send_gmails(new_message, categories, db_connect.get_category_users_info(message))
        db_connect.clear_appeals(message)
        bot.send_message(message.chat.id,
                         "Сіздің өтінішіңіз қабылданды және өңделуде.\nЖоспарлы рұқсат беру уақыты - 1 жұмыс күні.")
    else:
        send_error(bot, message)
        db_connect.clear_appeals(message)


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
                                              "Қарыздар бойынша барлық сұрақтарды келесі контактілер бойынша жіберуге болады:")
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
    elif message_text == "Дивизион по Рознечному Бизнесу":
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
    if message.text == "ЕҚЕҚ кәртішкесін толтыру":
        db_connect.cm_sv_db(message, 'ЕҚЕҚ кәртішкесін толтыру')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Қауіпті фактор | шарт")
        button2 = types.KeyboardButton("Жұмысты орындау тәртібі")
        button3 = types.KeyboardButton("Ұсыныстар | Идеялар")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id,
                         "Сіз қауіпті факторды байқадыңыз ба, қауіпті мінез-құлық немесе y Bac жұмыс орнындағы қауіпсіздік пен еңбекті қорғауды жақсарту бойынша ұсыныстар/идеялар бар ма?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Қажетті оқиғаны таңдап, ЕҚЕҚ кәртішкесін толтырыңыз.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")
    elif message.text == "Қауіпті фактор | шарт":
        db_connect.cm_sv_db(message, 'Қауіпті фактор | шар')
        bot.send_message(message.chat.id, "Егер Сіз жұмыс барысында қауіпті факторды немесе жағдайды байқасаңыз, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")
    elif message.text == "Жұмысты орындау тәртібі":
        db_connect.cm_sv_db(message, 'Жұмысты орындау тәртібі')
        bot.send_message(message.chat.id, "Егер Сіз жұмыстарды орындау кезінде мінез-құлық тәуекелдерін байқасаңыз, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")
    elif message.text == "Ұсыныстар | Идеялар":
        db_connect.cm_sv_db(message, 'Ұсыныстар | Идеялар')
        bot.send_message(message.chat.id, "Егер Сізде ұсыныстар немесе идеялар болса, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")


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
    elif message.text == "portal.telecom.kz | Нұсқаулар":
        db_connect.cm_sv_db(message, 'portal.telecom.kz | Нұсқаулар')
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Мобильді нұсқа")
        button2 = types.KeyboardButton("ДК немесе ноутбук")
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_portal)
    elif message.text == "Checkpoint VPN | Қашықтан жұмыс":
        db_connect.cm_sv_db(message, 'Checkpoint VPN | Қашықтан жұмыс')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("CheckPoint Орнату нұсқаулығы")
        button2_i = types.KeyboardButton("Checkpoint орнату файлы")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
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
        bot.send_message(message.chat.id, "'Iссапар | Рәсімдеу тәртібі' санаты туралы ақпарат алу үшін "
                                          "төмендегі сілтемеге өтіңіз "
                                          "\nhttps://wiki.telecom.kz/ru/instructionsopl/kommandiroviporyadok")
    elif message.text == "Мобильді нұсқа":
        bot.send_message(message.chat.id, "'Мобильді нұсқа' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз "
                                          "\nhttps://drive.google.com/drive/folders/"
                                          "1ojKgDgsUX9l9h0A1354AFVxFhQY2_ECZ?usp=drive_link")
    elif message.text == "ДК немесе ноутбук":
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Қалай кіруге болады")
        button2 = types.KeyboardButton("Жеке профиль")
        button3 = types.KeyboardButton("Порталдан ССП өту")
        markup_pk.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_pk)
    elif message.text == "Қалай кіруге болады":
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'ДК арқылы қызметкердің порталына қалай кіруге"
                                          " болады?'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/vsRIDqt_-1A")
    elif message.text == "Жеке профиль":
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Жеке профильді қалай толтыруға болады?'"
                                          "төмендегі сілтемеге өтіңіз \nhttps://youtu.be/V9r3ALrIQ48")
    elif message.text == "Порталдан ССП өту":
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Порталдан ССП өту'төмендегі сілтемеге өтіңіз"
                                          "\nhttps://youtu.be/wnfI4JpMvmE")
    elif message.text == "Филиал серверлері бойынша деректер":
        bot.send_message(message.chat.id, "Филиал серверлері бойынша деректер:"
                                          "\nhttps://disk.telecom.kz/index.php/f/695222")
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
                         "'ADSL модемі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/1ZMcd4cVuX8_JUJ8OoN0rYx5d5DjwlEbz?usp=drive_link")
    elif message.text == "IDTV консолі":
        bot.send_message(message.chat.id,
                         "'IDTV консолі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/1ZFbUrKi9QITBLkJQ93I45dxhINSsgv7H?usp=drive_link")
    elif message.text == "ONT модемдері":
        bot.send_message(message.chat.id,
                         "'ONT модемдері' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/1IiLJ14dKF3wQhoLYb18jJMLD6BNz3K7x?usp=drive_link")
    elif message.text == "Router 4G and Router Ethernet":
        bot.send_message(message.chat.id,
                         "'Router 4G and Router Ethernet' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/1EkzERKwa-DTnMW86-qJGbc_YAU2k6A74?usp=drive_link")


def kb(bot, message):
    if message.text == "Білім базасы":
        db_connect.cm_sv_db(message, 'Білім базасы')
        db_connect.set_bool(message, False, False)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button = types.KeyboardButton("Нұсқаулық базасы")
        button2 = types.KeyboardButton("Глоссарий")
        button3 = types.KeyboardButton("Пайдалы сілтемелер")
        markup.add(button2, button, button3)
        bot.send_message(message.chat.id, "Мобильді білім қорына қош келдіңіз!", reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Мұнда сіз өзіңізге қажетті Bac нұсқаулығын таба аласыз немесе пайдалана аласыз "
                         "біз өзімізде қолданатын негізгі терминдер бойынша іздеу жүйесінің глоссарийі "
                         "компаниялар күн сайын.")
    elif message.text == "Нұсқаулық базасы":
        db_connect.cm_sv_db(message, 'Нұсқаулық базасы')
        db_connect.set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1 = types.KeyboardButton("Логотиптер және Брендбук")
        button2 = types.KeyboardButton("Жеке кабинет telecom.kz")
        button3 = types.KeyboardButton("Модемдер | Теңшеу")
        button4 = types.KeyboardButton("Lotus | Нұсқаулар")
        button5 = types.KeyboardButton("portal.telecom.kz | Нұсқаулар")
        button6 = types.KeyboardButton("Checkpoint VPN | Қашықтан жұмыс")
        button7 = types.KeyboardButton("Iссапар | Рәсімдеу тәртібі")
        markup_instr.add(button5, button4, button6, button1, button7, button2, button3)

        bot.send_message(message.chat.id, "Бұл жерде өзіңізге пайдалы нұсқаулықты таба аласыз.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Нұсқаулықты таңдау үшін санатты, содан кейін нұсқаулықтың өзін мәзір-пернетақтадан таңдаңыз.")
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
                         "енгізу маңызды. Мысалы: ДК, ЖДБ, АТД.")
    elif message.text == "Пайдалы сілтемелер":
        db_connect.cm_sv_db(message, 'Пайдалы сілтемелер')
        db_connect.set_bool(message, False, False)
        time.sleep(0.5)
        markup = db_connect.useful_links()
        bot.send_message(message.chat.id, "Пайдалы сілтемелер", reply_markup=markup)


# def kb_service(bot, message):
#     if message.text == "Жеке кабинет telecom.kz":
#         db_connect.cm_sv_db(message, 'Жеке кабинет telecom.kz')
#         markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_i = types.KeyboardButton("Қызметті қалай төлеуге болады")
#         button2_i = types.KeyboardButton("Төлем мәліметтерін қалай көруге болады")
#         button3_i = types.KeyboardButton("Қосылған қызметтерді қалай көруге болады")
#         button4_i = types.KeyboardButton("Менің Қызметтерім 'Бөлімі'")
#         markup_instr.add(button1_i, button2_i, button3_i, button4_i)
#         bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
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
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)


def glossary(bot, message):
    text1 = f"Сіздің сұранысыңыз бойынша келесі мән табылды:"
    text2 = "Біздің info.ktcu@telecom.kz поштамызға хат жолдау арқылы жұмысымызды жақсартуға көмектесе аласыз - " \
            "біз міндетті түрде қарастырамыз."
    db_connect.glossary(bot, message, text1, text2)


def profile(bot, message):
    db_connect.cm_sv_db(message, "Менің профилім")
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