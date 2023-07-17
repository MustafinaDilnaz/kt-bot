from telebot import *
import db_connect
import openpyxl



categories = {
    'Learning.telecom.kz | Техникалық қолдау': 'info.ktcu@telecom.kz',
    'Оқыту | Корпоративтік Университет': 'info.ktcu@telecom.kz',
    '"Нысана" қолдау қызметі_kaz': 'nysana@cscc.kz',
    'Комплаенс қызметіне хабарласыңыз': 'tlek.issakov@telecom.kz',
}

faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары"]
biot_field = ["БиОТ Картаны толтыру", "қауіпті фактор/шарт", "жұмысты орындау тәртібі", "ұсыныстар / идеялар"]

kb_field = ["Білім базасы", "Нұсқаулық базасы", "Глоссарий"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "модемдер | теңшеу", "Lotus | нұсқаулар",
                "Мобильді нұсқа", "ДК немесе ноутбук", "portal.telecom.kz / нұсқаулар",
                "Checkpoint VPN / қашықтан жұмыс", "іссапар / рәсімдеу тәртібі",
                "Қалай кіруге болады", "жеке профиль", "порталдан ssp-ге өту"]
instr_field = ["Брендбуктар мен логотиптер", "Жеке кабинет telecom.kz", "модемдер | теңшеу", "Lotus & CheckPoint"]
adapt_field = ["Welcome курстар | Бейімделуі"]

new_message, user_name, chosen_category, flag, appeal_field = '', '', '', 0, False

faq_1 = {
    'Қазақтелеком "АҚ-да "Демеу" бағдарламасы кімге бағытталған?': '"Қазақтелеком" АҚ "Демеу" бағдарламасын әлеуметтік қолдау: (бұдан әрі-Бағдарлама) қызметкерлерге мәртебесі бойынша жіберілді: \
\n 1) көп балалы отбасы-өз құрамында бірге тұратын төрт және одан да көп кәмелетке толмаған балалары, оның ішінде орта білім беру ұйымдарында күндізгі оқу нысаны бойынша оқитын балалары бар отбасы, \
техникалық және кәсіптік, орта білімнен кейінгі, жоғары және (немесе) жоғары оқу орнынан кейінгі білім олар кәмелетке толғаннан кейін білім алуды бітірген уақытқа дейін (бірақ жеткенге дейін) \
); \n2) мүгедек балалары бар отбасы-өз құрамында он сегіз жасқа дейінгі баласы (балалары) бар, денсаулығы бұзылған Co ағза функцияларының тұрақты бұзылуы бар отбасы,\
ауруларға, мертігулерге (жараларға, жарақаттарға, контузияларға), олардың салдарына, тіршілік әрекетінің шектелуіне және ISO (оларды) әлеуметтік қорғау қажеттілігіне әкелетін ақауларға байланысты; \
\n3) 2-x астам баланы асырап алған/асырап алған отбасы - өз құрамында денсаулық жағдайы бойынша диспансерлік есепте тұрған 2-x астам кәмелетке толмаған асырап алынған/асырап алынған балалары және жалғыз асыраушысы бар отбасы. \
\n4) A8-B4 грейдінің қызметкерлеріне балаларының орта арнаулы оқу орнында (бұдан әрі - CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) бітіруші оқу курсына (тұруға және тамақтануға арналған шығыстарды есепке алмағанда) ақы төлеу бойынша әлеуметтік қолдау белгіленеді. \
\n барлық әлеуметтік қолдау түрлері әлеуметтік қолдау көрсету сәтінде қоғамда кемінде 3-x жыл үздіксіз жұмыс өтілі бар Қоғам қызметкерлеріне көрсетіледі.\
\n * <<Қазақтелеком>> АҚ-мен еңбек қатынастарында тұрмайтын жеке тұлғалардың әлеуметтік қолдау/көмек көрсету туралы өтініштері қарауға қабылданбайды.',
    'Жұмыскерлерге арналған әлеуметтік қолдау түрлері': '1) балалардың сауықтыру лагерьлеріне жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n 2) балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін)жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n 3) балаларға арналған дәрілік заттарды сатып алуға материалдық көмек; \
\n 4) мектеп оқушыларының тамақтануына материалдық көмек; \ n5) оқу жылының басына материалдық көмек; \
\n 6) медициналық оңалту/баланы оңалтудың жеке бағдарламасы үшін қаражатты өтеу (мүгедек балалар үшін); \
\n 7) арнайы білім беру бағдарламалары үшін қаражатты өтеу (мүгедек балалар үшін); \
\n 8) арнайы түзету ұйымдарына барғаны үшін қаражатты өтеу (мүгедек балалар үшін); \
\n 9) мектеп бітірген күні кәмелетке толмаған және оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек; \
\n 10) орта арнаулы оқу орнында (бұдан әрі-CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) балаларының бітіруші оқу курсын (тұруға және тамақтануға арналған шығыстарды есептемегенде) төлеу жөніндегі шығыстарды (A8 - B4 грейд қызметкерлеріне) өтеу.',
    'Әлеуметтік комиссияға өтініш беру процесі': 'Филиалдың әлеуметтік комиссиясына өтінішті ресімдеу - др. ДРБ әлеуметтік комиссиясының төрағасы-Погребицкий И. Е.\
\n әлеуметтік қолдау көрсету үшін қоғам қызметкерлері жүгінген кезде өтініштерді қараудың кезектілік тәртібі сақталады.',
    'Өтінішті қайда рәсімдеу керек?': 'Сіз өзіңіздің жұмыс базаңызда(BRD) өтініш жасайсыз. Арнайы базалар жоқ.',
    'ДРБ әлеуметтік комиссиясының төрағасы': 'Погребицкий И. Е.',
    'Қандай құжаттарды ұсыну керек?': 'балалардың туу туралы куәліктері (сканерленген) мүгедектік туралы анықтама \
(өз құрамында мүгедек баласы бар отбасылар үшін) балаларды оқыту мектебінің Co анықтамасы (келу күндері мен кезеңін көрсету, мысалы, 2022-2023 ТАӘ 85 күнге барды) \
балаларды асырап алу/асырап алу балалардың диспансерлік есептегі жай-күйі туралы анықтама баланың аты - жөні көрсетілген жолдаманы төлегенін растайтын құжат-шығындарды өтеу үшін, \
балалардың сауықтыру лагерьлеріне/ балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін) жолдамалар сатып алуға байланысты фискалдық чек тауарлардың атауын көрсете отырып-шығыстарды өтеу үшін, \
1 қыркүйекте кеңсе тауарларын, киімдерді (мектеп формасы/аяқ киім) сатып алуға байланысты. Материалдық көмек растайтын құжаттарсыз ұсынылады o оқу жылының басында тауарларды сатып алу \
қызметкер ағымдағы жылдың 1 қазанына дейін өтініш берген жағдайда. дәрігердің тағайындалуы және дәрілік заттардың атауы көрсетілген фискалдық чек-шығындарды өтеу үшін, \
балаларға арналған дәрілік заттарды сатып алуға байланысты медициналық оңалтуға/жеке тұлғаға байланысты шығыстарды өтеу үшін баланың аты - жөнін көрсете отырып, төлемді растайтын құжат \
баланы оңалту бағдарламасымен (мүгедек балалар үшін), арнаулы білім беру бағдарламаларымен( мүгедек балалар үшін), арнаулы түзету ұйымдарына барумен (мүгедек балалар үшін) \
баланың аты - жөнін көрсете отырып, мектепті бітірген ob аттестаты-оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек төлеу үшін * аударымдар/аударымдар немесе басқа мәмілелер қабылданбайды. \
\n *FIS түпнұсқалары. тауарлардың атауын көрсете отырып, чек "Қазақтелеком"АҚ ДРБ - филиалының кеңсесі, Желтоқсан көшесі, 115 мекен-жайына жіберілсін. ',
}

faq_2 = {
    'Жұмыс орнынан анықтаманы қалай алуға болады?': '1) жұмыс орнының C анықтамасы HR ОСО базасы арқылы дербес қалыптастырылады, келесі кезеңдер бойынша:\n2) HR Notes Link ОСО базасы. Сіз ешкімді келіспейсіз, қолыңызбен виза аласыз.\
    \n3) B папкада DRB филиалын таңдаңыз-анықтама беруге өтінім c жұмыс орны талап ету орны бойынша (скринмен қоса беріледі),\n4) өз атыңызды таңдап, өтінімді толтырыңыз және HR ОСО-ға жіберіңіз. \
    ҚФ\n 5 жұмыскерлері бағыты бойынша өтінімді пысықтайды) содан кейін өтінім мәртебесі бойынша ҚФ орындаушыларына хабарласыңыз/қоңырау шалыңыз. Өтініштің оң жақ бұрышындағы және жасыл алаңдағы күй Орындаушының телефоны.\n\
    \n * туындаған мәселелер бойынша ҚФ HR БҚО қызметкеріне хабарласыңыз\пжусупова Несибелді +77272581001, 8 701 786 07 92.',
    'HCL Lotus Notes және қоғамның басқа жүйелерін қайдан алуға/ашуға болады?': 'Қоғам жүйелеріне қол жеткізу үшін жетекшілік ететін басшыға/тәлімгерге/іс жүргізушіге хабарласу қажет \
    ЛОТУСҚА кіру үшін логин мен парольді өтінім авторына бір күн ішінде Лотус поштасына жіберетін ақпаратты өңдегеннен кейін бөлімшелер мен пайдаланушыны ЕСУД базасы арқылы лотусқа тіркеуді сұрайды. \
    Содан кейін helpdesk +77272587304 өтінімін қалдырыңыз және жауапты қызметкер HCL Lotus Notes орнатады.',
    'K лотустағы ақаулар кезінде кімге жүгіну керек, парольді ұмытып қалдыңыз ба?': 'Туындаған мәселелер бойынша HelpDesk +77272587304 өтінімін қалдырыңыз.',
    'Аурухана парақтары жұмысшыларға төлене ме?': '1) компаниядағы үздіксіз жұмыс өтіліне байланысты қызметкерлер (кәсіподақ ұйымының мүшелері және ұжымдық ұйымға қосылған) үшін \
    (5 жасқа дейін - орташа жалақының 40%, 5 жылдан астам - еңбекке уақытша жарамсыздық күндері үшін орташа жалақының 70%);\n2) қалған қызметкерлер үшін - заңнамада белгіленген мөлшерде.\
    \n3) еңбекке уақытша жарамсыздық парағы / o парағы:',
    'Аурухана парағын кім толтырады?': 'Аурухана парағын құрылымдық бөлімшенің табельшісі/іс жүргізушісі толтырады. B аурухана парағында "бөлшек бизнес бойынша Дивизион - "Қазақтелеком" АҚ филиалы " филиалының атауы және өз лауазымы көрсетіледі.',
    'Аурухана парағын кімге тапсыру керек?': '1) тікелей басшының y аурухана парағына қол қою;\n2) аурухана парағының сканерлеу нұсқасын жасау;\n3) қызметкердің уақытша болмауы туралы HR O ХҚКО базасында Өтінім ресімдеу;\n4) ХҚКО сервистік фабрикасының қызметкерлеріне аурухана парағының түпнұсқасын тапсыру.',
    'Кәсіподаққа кіргім келеді не істеу керек және ақпарат алу үшін кімге жүгіну керек, ұстап қалуға қанша пайыз бар?': '1) Сіз DRB кәсіподағына кіру туралы өтініш жазуыңыз керек\
    \n2) бұдан әрі кәсіподақ жарналарын ұстап қалуға өтінімді ресімдеу қажет және т. б. өтінім базасында БЖО-да (Жалпы жұмыс құжаты№) \БЖК-да кәсіподақ мәселелері бойынша жүзеге асырылады, Сіз Ишмурзина Әйгерімге жүгіне аласыз',
    'ЕМС бойынша сақтандыру (ерікті медициналық сақтандыру)': 'ЕМС бойынша сақтандыру (ерікті медициналық сақтандыру) сақтандыру өтемі мүмкін болған жағдайда қоғамда 3 жылдан астам жұмыс өтілі бар қызметкерлерге жүзеге асырылады',
    'Әріптестердің телефонын қайдан табуға болады?': 'Әріптестің телефоны Сіз "қоғамның Телефон анықтамалығы" базасын таба аласыз-телефон нөмірлері, қызметкерлерді бөлім бойынша іздеу',
    'Айналма Парақ. ISO қашан рәсімделеді?': '1) жұмыстан босату туралы өтінішті ресімдеген кезде, үшінші парақта автоматты түрде айналып өту парағы құрылады және қол қоюшылар көрсетіледі.\ n2) филиалға/біржақты тәртіппен/ ауыстыру кезінде айналып өту парағын өз жұмыс базаларында ресімдейміз',
}

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("Welcome курстар | Бейімделуі")
button2 = types.KeyboardButton("Өтінішті қалдыру")
button3 = types.KeyboardButton("Білім базасы")
button4 = types.KeyboardButton("БиОТ Картаны толтыру")
button5 = types.KeyboardButton("Жиі қойылатын сұрақтар")
markup.add(button, button2, button3, button4, button5)


def send_welcome_message(bot, message):
    welcome_message = f'Сәлем {message.from_user.first_name}👋\
                       \nМен - ktbot, сіздің компаниядағы жеке көмекшіңіз.\
                       \n\nМіне, мен сізге қалай көмектесе аламын:\
                       \n  · ✉️-оқыту мәселелері бойынша өтініш жіберу;\
                       \n  · 🗃️ - нұсқаулар мен глоссариймен білім қорына қол жетімділікті қамтамасыз ету;\
                       \n  · 👷Biot картасын жіберуге көмектесу;\
                       \n  · 📄 Жиі қойылатын сұрақтарға жауап беріңіз.\
                       \n\nA егер сіз жаңа қызметкер болсаңыз, Мен сізге Welcome курсын өтуді ұсынамын 😊.'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    with open("images/menu.jpg", 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Менің сценарийімде бірнеше командалар бар:\
                                          \n/menu — негізгі мәзірге оралу (сіз мұны демонстрация кезінде кез келген уақытта жасай аласыз!)\
                                          \n/help - әзірлеушілермен байланысыңыз (егер сіз қиындықтарға тап болсаңыз немесе осы команданы қолданыңыз y жақсарту үшін ұсыныстар бар)\
                                          \n/start — ботты қайта іске қосыңыз\
                                          \n/language - тілді таңдаңыз\
                                          \n\n Командалар сіз хабарламалар жолағындағы \"мәзір\" қойындысынан таба аласыз (төменгі сол жақта) немесе жай ғана команданың атауы келді, тек <</>> ұмытпаңыз!")


def send_error(bot, message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Ой, бірдеңе дұрыс болмады...\ пботаны /menu түймесін басу арқылы қайта іске қосып көріңіз")


def adaption(bot, message):
    if message.text == 'Welcome курстар | Бейімделуі':
        db_connect.cm_sv_db(message, 'Welcome курстар | Бейімделуі')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('Айта бер!', callback_data='Айта бер!')
        markup.add(button)
        bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
        time.sleep(0.75)
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, 'Бастар алдында, мені қалай қолдануды көрсетемін 🫡', reply_markup=markup)


def call_back(bot, call):
    if call.data == 'Айта бер!':
        db_connect.cm_sv_db(call.message, 'Айта бер!')
        bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'))
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Менде пернетақта бар, оның көмегімен сіз бөлімдерге өтіп, сізге қажетті ақпаратты ала аласыз",
                         reply_markup=markup)

    if call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images\hello.jpg', 'rb'))
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup.add(button)
        bot.send_message(call.message.chat.id, "Төмендегі түймені басыңыз, біз жалғастырамыз.", reply_markup=markup)

    if call.data == "Кеттік!":
        bot.send_photo(call.message.chat.id, photo=open('images\kaztelecom_credo.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "AO 'Қазақтелеком' - Қазақстанның ірі телекоммуникациялық компаниясы, "
                                               "Республика Министрлер Кабинетінің қаулысына сәйкес құрылған 1994 "
                                               "жылғы 17 маусымдағы Қазақстан.\n\n📌Бізде арнайы дайындаған "
                                               "компанияның қысқаша тарихы бар сіз үшін. Төмендегі файлдарды ашып, "
                                               "онымен танысыңыз.")
        bot.send_document(call.message.chat.id, open('images\PDF-1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images\PDF-2.jpg', 'rb'))
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Кеттік!", callback_data="Ал, Кеттік!")
        markup.add(button)
        bot.send_message(call.message.chat.id, "Егер бәрі түсінікті болса, біз жалғастырамыз ба?", reply_markup=markup)

    if call.data == "Ал, Кеттік!":
        bot.send_message(call.message.chat.id, "Сізде Бадди бар ма?")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Егер жоқ болса, ренжімеңіз, ол сізді жақын арада табады!")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Ия, көбірек білгім келеді!", callback_data="Ия, көбірек білгім келеді!")
        markup.add(button)
        bot.send_message(call.message.chat.id, "Сіз бұл кім екенін және маған не үшін керек екенін сұрайсыз ба? Мен жауап беремін)", reply_markup=markup)

    if call.data == "Ия, көбірек білгім келеді!":
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сонымен, корпоративті e-mail-ді тексеріңіз, мүмкін сізге Баддиден "
                                               "кездесу, танысу және айту туралы хабарлама келген шығар o біздің "
                                               "компаниядағы бейімделу бағдарламасы.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Қабылданды!", callback_data="Қабылданды!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-3.jpg', 'rb'), reply_markup=markup)

    if call.data == "Қабылданды!":
        bot.send_message(call.message.chat.id,
                         "Әдетте сүйемелдеу бір айға созылады, бірақ көбінесе сынақ мерзімі сәтті аяқталғанға дейін "
                         "жалғасады.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Айтпақшы, кез - келген бөлімнің қызметкері Бадди бағдарламасына қатыса алады және бұл өте "
                         "жақсы-көлденең және тік байланыстар кеңейеді.")
        time.sleep(0.75)
        markup_1 = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton("Бәрекелді, әрі қарай жалғастырыңыз!", callback_data="azaza")
        markup_1.add(button_1)
        bot.send_message(call.message.chat.id,text = "Кейінірек сіз де Бадди бола аласыз және болашақ жаңадан "
                                                     "келгендерге бейімделуге көмектесе аласыз! 😊",
                         reply_markup=markup_1)

    if call.data == "azaza":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-1")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\credo_1.jpeg', 'rb'), reply_markup=markup)
    if call.data == "Келесі-1":
        bot.send_message(call.message.chat.id, "Біздің компания 9 филиалдан тұрады сіз күн сайын жұмыста еститін "
                                               "аббревиатуралар.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сондықтан компанияның құрылымымен танысайық.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images\struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "A егер сіз сіз үшін бейтаныс адамдармен кездессеңіз\
                                             терминдермен немесе аббревиатуралармен біз сізге білім қорында глоссарий дайындадық.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сіз әрқашан негізгі мәзірден білім қорын таба аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-3")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\gloss.jpg', 'rb'), reply_markup=markup)

    if call.data == "Келесі-3":
        bot.send_message(call.message.chat.id, 'B "Қазақтелеком" AO компаниясының түрлі бағыттар бойынша өнімдері бар:\
                                             \n🌍Ғаламтор \n📞Телефон\n📹Бейнебақылау\n🖥️TV+ \n🛍️Дүкен shop.telecom.kz')
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-4")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Өнімдер мен олардың тарифтері туралы өзекті ақпаратты сіз әрқашан сайттан таба аласыз "
                         "telecom.kz",
                         reply_markup=markup)
    if call.data == "Келесі-4":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-5")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\dear_users.jpeg', 'rb'), reply_markup=markup)
    if call.data == "Келесі-5":
        bot.send_message(call.message.chat.id, '☎️B AO "Қазақтелеком "интеграцияланған "Нысана" жедел желісі, '
                                               'онда әрқайсысы қызметкер QR коды арқылы немесе төмендегі суреттегі '
                                               'контактілер арқылы байланыса алады')
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\call_center.jpeg', 'rb'), reply_markup=markup)

    if call.data == "Келесі-6":
        bot.send_message(call.message.chat.id, "Керемет! \nСіз бен біз компания туралы негізгі ақпаратпен таныстық.\
                                             \n \nСіз әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Түсінікті!", callback_data="Түсінікті!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'), reply_markup=markup)

    if call.data == "Түсінікті!":
        bot.send_message(call.message.chat.id, "Құттықтаймыз!\nСен Welcome курсын өтті.\n\nкомпанияға қош келдіңіз!.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Негізгі мәзірге өту үшін /menu пәрменін теріңіз немесе басыңыз")


def appeal(bot, message):
    db_connect.set_appeal_field(message)
    if message.text == "Өтінішті қалдыру":
        db_connect.cm_sv_db(message, 'Өтінішті қалдыру')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in categories:
            button = types.KeyboardButton(key)
            markup.add(button)
        bot.send_message(message.chat.id,
                         "B осы бөлімде Сіз Bac-ті қызықтыратын мәселелер бойынша өтінішіңізді корпоративтік университетке қалдыра аласыз.",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Санатты таңдау үшін жеделхаттағы пернетақтаны нұқыңыз (әдетте бұл енгізу жолағының оң жағындағы белгіше).")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")

    elif message.text.startswith('+7'):
        db_connect.set_appeal_message(message, message.text)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')

    elif message.text in categories.keys():
        db_connect.cm_sv_db(message, message.text)
        db_connect.set_chosen_category(message, message.text)
        bot.send_message(message.chat.id,
                         "Өтінішіңізді қалдыру үшін байланыс деректерін форматта көрсетіңіз: \n+7 ### ### ## ##  \nАты Тегі  \nЭлектрондық пошта мекенжайы")

    elif db_connect.get_appeal_field(message) and db_connect.get_appeal_message(message) != '':
        new_message = f'{db_connect.get_appeal_message(message)} \n {message.text}'
        db_connect.send_gmails(new_message, categories, db_connect.get_chosen_category(message))
        db_connect.clear_appeals(message)
        bot.send_message(message.chat.id,
                         "Сіздің өтінішіңіз қабылданды және өңделуде.\nЖоспарлы рұқсат уақыты - 1 жұмыс күні.")
    else:
        send_error(message)
        db_connect.clear_appeals(message)


def faq(bot, message):
    if message.text == "Жиі қойылатын сұрақтар":
        db_connect.cm_sv_db(message, 'Жиі қойылатын сұрақтар')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("HR сұрақтары")
        markup_faq.add(button_d, button_hr)
        bot.send_message(message.chat.id, "Мұнда сіз жиі қойылатын сұрақтарға жауап таба аласыз",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Егер y Bac жаңа бөлімдер немесе сұрақтарға жауаптар қосу бойынша "
                                          "ұсыныстар/идеялар бар, онда бізге жазыңыз info.ktcu@telecom.kz - біз "
                                          "сіздің ұсынысыңызды міндетті түрде қарастырамыз және сізбен байланысамыз.")

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


def biot(bot, message):
    if message.text == "БиОТ Картаны толтыру":
        db_connect.cm_sv_db(message, 'БиОТ Картаны толтыру')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("қауіпті фактор/шарт")
        button2 = types.KeyboardButton("жұмысты орындау тәртібі")
        button3 = types.KeyboardButton("ұсыныстар / идеялар")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id,
                         "Сіз қауіпті факторды байқадыңыз ба, қауіпті мінез-құлық немесе y Bac жұмыс орнындағы қауіпсіздік пен еңбекті қорғауды жақсарту бойынша ұсыныстар/идеялар бар ма?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Қажетті оқиғаның жіктелуін таңдап, БиОТ картасын толтырыңыз.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")

    elif message.text == "қауіпті фактор/шарт":
        db_connect.cm_sv_db(message, 'қауіпті фактор/шарт')
        bot.send_message(message.chat.id, "Егер сіз жұмыс барысында қауіпті факторды немесе жағдайды байқасаңыз, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")

    elif message.text == "жұмысты орындау тәртібі":
        db_connect.cm_sv_db(message, 'Поведение при выполнении работ')
        bot.send_message(message.chat.id, "Если Вы заметили риски в поведении при выполнении работ, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")

    elif message.text == "ұсыныстар / идеялар":
        db_connect.cm_sv_db(message, 'Предложения/Идеи')
        bot.send_message(message.chat.id, "Если y Bac есть предложения или идеи, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол жағындағы командалар мәзірінен.")


def instructions(bot, message):
    if message.text == "Логотиптер және Брендбук":
        db_connect.cm_sv_db(message, 'Логотиптер және Брендбук')
        bot.send_message(message.chat.id,
                         "Брендбук және логотиптер санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/1RnTAuvjskl2bcxQbz9SsGLveGSaVUmJ8?usp=drive_link")
    elif message.text == "Жеке кабинет telecom.kz":
        db_connect.cm_sv_db(message, 'Жеке кабинет telecom.kz')
        bot.send_message(message.chat.id,
                         "'Жеке кабинет' санаты туралы ақпарат алу үшін telecom.kz ' төмендегі сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/10g5ZWQGFo3iCtF27mVh40Rs1eVHdLXE4?usp=drive_link")
    elif message.text == "модемдер | теңшеу":
        db_connect.cm_sv_db(message, 'модемдер | теңшеу')
        bot.send_message(message.chat.id,
                         "Модемдер / теңшеу санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз\nhttps://drive.google.com/drive/folders/1rhsAYmRUJKSS_Pi9aEzWHTczC1Q6MIlF?usp=drive_link")
    elif message.text == "Lotus | нұсқаулар":
        db_connect.cm_sv_db(message, 'Lotus | нұсқаулар')
        bot.send_message(message.chat.id,
                         "'Lotus | нұсқаулар' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/18yrrAkjmwpp1oxToPE6JBGqIkLi2zhmz?usp=drive_link")
    elif message.text == "portal.telecom.kz / нұсқаулар":
        db_connect.cm_sv_db(message, 'portal.telecom.kz / нұсқаулар')
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1 = types.KeyboardButton("Мобильді нұсқа")
        button2 = types.KeyboardButton("ДК немесе ноутбук")
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_portal)
    elif message.text == "Checkpoint VPN / қашықтан жұмыс":
        db_connect.cm_sv_db(message, 'Checkpoint VPN / қашықтан жұмыс')
        bot.send_message(message.chat.id,
                         "'Checkpoint VPN / қашықтан жұмыс' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/1obzIvUKiVO5UvxX-2t7YFMHZWgDE5_Fj?usp=drive_link")
    elif message.text == "іссапар / рәсімдеу тәртібі":
        bot.send_message(message.chat.id,
                         "'Іссапар / рәсімдеу тәртібі' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/1AsWzCc-a1EgveMeuqJVkiBmKsXSm9TB3?usp=drive_link")
    elif message.text == "Мобильді нұсқа":
        bot.send_message(message.chat.id,
                         "'Мобильді нұсқа' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/1ojKgDgsUX9l9h0A1354AFVxFhQY2_ECZ?usp=drive_link")
    elif message.text == "ДК немесе ноутбук":
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Қалай кіруге болады")
        button2 = types.KeyboardButton("жеке профиль")
        button3 = types.KeyboardButton("порталдан ssp-ге өту")
        markup_pk.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_pk)
    elif message.text == "Қалай кіруге болады":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как авторизоваться на портале работника через ПК?' перейдите по ссылке ниже \nhttps://youtu.be/vsRIDqt_-1A")
    elif message.text == "жеке профиль":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как заполнить личный профиль?' перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    elif message.text == "порталдан ssp-ге өту":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как перейти из портала перейти в ССП' перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")


def kb(bot, message):
    if message.text == "Білім базасы":
        db_connect.cm_sv_db(message, 'Білім базасы')
        db_connect.set_bool(message, False, False)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton("Нұсқаулық базасы")
        button2 = types.KeyboardButton("Глоссарий")
        markup.add(button, button2)
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
        button3 = types.KeyboardButton("модемдер | теңшеу")
        button4 = types.KeyboardButton("Lotus | нұсқаулар")
        button5 = types.KeyboardButton("portal.telecom.kz / нұсқаулар")
        button6 = types.KeyboardButton("Checkpoint VPN / қашықтан жұмыс")
        button7 = types.KeyboardButton("іссапар / рәсімдеу тәртібі")
        markup_instr.add(button5, button4, button6, button1, button7, button2, button3)

        bot.send_message(message.chat.id, "Мұнда Сіз Bac үшін пайдалы нұсқаулықты таба аласыз.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Нұсқаулықты таңдау үшін таңдаңыз санат, содан кейін Нұсқаулықтың өзі пернетақта мәзірінде.")

    elif message.text == "Глоссарий":
        db_connect.cm_sv_db(message, 'Глоссарий')
        db_connect.set_bool(message, False, True)
        bot.send_message(message.chat.id, "Қазақтелеком AO компаниясындағы терминдер мен аббревиатуралардың глоссарийі.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Аббревиатураның транскрипциясын немесе терминнің сипаттамасын алу үшін- "
                                            "сөзді теруді бастаңыз және ақпарат алу үшін жіберіңіз.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Маңызды!\n \ n - қатесіз және артық таңбаларсыз сөзді енгізіңіз.\ N-аббревиатураларды бас әріппен теру маңызды. Мысалы: ДК, ОДС, ДИТ.")


def glossary(bot, message):
    wb = openpyxl.load_workbook('tests_kaz.xlsx')
    excel = wb['Лист1']
    abbr, defs = [], []

    for row in excel.iter_rows(min_row=2, max_row=1264, values_only=True):
        abbr.append(row[1])
        defs.append(row[2])

    if message.text.upper() in abbr:
        index = abbr.index(message.text.upper())
        bot.send_message(message.chat.id, f"Сіздің сұранысыңыз бойынша келесі мән табылды: \n{defs[index]}")

    else:
        bot.send_photo(message.chat.id, photo=open('images/oops.jpg', 'rb'))
        bot.send_message(message.chat.id, "Ho бізге хат жіберу арқылы жақсырақ болуға және мән қосуға көмектесе аласыз \
                                      info.ktcu@telecom.kz - біз міндетті түрде Eco-ны қарастырамыз.")


def menu(bot, message):
    db_connect.set_bool(message, False, False)
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)
