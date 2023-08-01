from telebot import *
import db_connect
import openpyxl

categories = {
    'Learning.telecom.kz | Техникалық қолдау': 'info.ktcu@telecom.kz',
    'Оқыту | Корпоративтік Университет': 'info.ktcu@telecom.kz',
    '"Нысана" қолдау қызметі': 'nysana@cscc.kz',
    'Комплаенс қызметіне хабарласыңыз': 'tlek.issakov@telecom.kz',
}

faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары"]
biot_field = ["ЕҚЕҚ кәртішкесін толтыру", "Қауіпті фактор | шарт", "Жұмысты орындау тәртібі", "Ұсыныстар | Идеялар"]

kb_field = ["Білім базасы", "Нұсқаулық базасы", "Глоссарий"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар",
                "Мобильді нұсқа", "ДК немесе ноутбук", "portal.telecom.kz | Нұсқаулар",
                "Checkpoint VPN | Қашықтан жұмыс", "Iссапар | Рәсімдеу тәртібі",
                "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту", "Филиал серверлері бойынша деректер",
                "Lotus Орнату нұсқаулары", "Lotus орнату файлы", "Қазақтелеком АҚ",
                "Корпоративтік Университет", "Қызметті қалай төлеуге болады", "Төлем мәліметтерін қалай көруге болады",
                "Қосылған қызметтерді қалай көруге болады", "Менің Қызметтерім 'Бөлімі'", "ADSL модемі",
                "IDTV консолі", "ONT модемдері", "Router 4G and Router Ethernet", "CheckPoint Орнату нұсқаулығы",
                "Checkpoint орнату файлы"]
adapt_field = ["Welcome курс | Бейімделу"]

new_message, user_name, chosen_category, flag, appeal_field = '', '', '', 0, False

faq_1 = {
    'Қазақтелеком "АҚ-да "Демеу" бағдарламасы кімге бағытталған?': 'Қазақтелеком" АҚ "Демеу" бағдарламасын әлеуметтік қолдау: (бұдан әрі-Бағдарлама) жұмыскерлерге мәртебесі бойынша жіберілді: \
\n1) Көп балалы отбасы-өз құрамында төрт және одан да көп бірге тұратын кәмелетке толмаған балалары, оның ішінде кәмелетке толғаннан кейін орта, техникалық және кәсіптік, орта білімнен кейінгі, жоғары және (немесе) жоғары оқу орнынан кейінгі білім беру ұйымдарында күндізгі оқу нысаны бойынша білім алатын балалары бар отбасы  \
отбасы (бірақ білім алуды аяқтағанға дейін) жиырма үш жасқа толған жетістіктер);  \
\n2) Мүгедек балалары бар отбасы-өз құрамында он сегіз жасқа дейінгі баласы (балалары) бар, бар, тұрмыс-тіршілігінің шектелуіне және оны әлеуметтік қорғау қажеттігіне әкеп соқтыратын, ауруларға, мертігулерге (жаралануға, жарақаттарға, контузияларға), олардың зардаптарына, кемістіктерге байланысты ағзаның қызметінде тұрақты бұзылуы бар отбасын (оларды) әлеуметтік қорғау; \
\n3) 2-ден астам бала асырап алған/асырап алған отбасы - құрамында 2-ден астам кәмелетке толмаған асырап алған/асырап алынған балалары бар, денсаулық жағдайы бойынша диспансерлік есепте тұрған және жалғыз асыраушысы бар отбасы.\
\n4) A8-B4 грейдінің жұмыскерлеріне балаларының орта арнаулы оқу орнында (бұдан әрі - CYZ) жоғары оқу орнында (бұдан әрі - BYZ) түлектердің оқу курсына (тұруға және тамақтануға арналған шығыстарды есептемегенде) ақы төлеу бойынша әлеуметтік қолдау белгіленеді. Барлық әлеуметтік қолдау түрлері әлеуметтік қолдау көрсету мерзімінде Қоғамда кемінде 3 жыл үздіксіз жұмыс өтілі бар Қоғам жұмыскерлеріне көрсетіледі.',
    'Жұмыскерлерге әлеуметтік қолдау түрлері': '1) балалардың сауықтыру лагерьлеріне жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n2) Балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін) жолдамалар сатып алуға байланысты шығыстарды өтеу; \
\n3) Балаларға арналған дәрілік заттарды сатып алуға материалдық көмек; \
\n4) Мектеп оқушыларының тамақтануына материалдық көмек; \
\n5) Оқу жылының басына материалдық көмек; \
\n6) Медициналық оңалту/баланы оңалтудың жеке бағдарламасы үшін қаражатты өтеу (мүгедек балалар үшін); \
\n7) Арнайы білім беру бағдарламалары үшін қаражатты өтеу (мүгедек балалар үшін); \
\n8) Арнайы түзету ұйымдарына барғаны үшін қаражатты өтеу (мүгедек балалар үшін); \
\n9) Мектеп бітірген күні кәмелетке толмаған және оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек; \
\n10) Орта арнаулы оқу орнында (бұдан әрі-CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) балаларының бітіруші оқу курсын (тұруға және тамақтануға арналған шығыстарды есептемегенде) төлеу жөніндегі шығыстарды (A8 - B4 грейд қызметкерлеріне) өтеу.',
    'Әлеуметтік комиссияға өтініш беру үдерісі': 'Филиалдың әлеуметтік комиссиясына өтінішті ресімдеу - др. ДРБ әлеуметтік комиссиясының төрағасы-Погребицкий И. Е. әлеуметтік қолдау көрсету үшін қоғам қызметкерлері жүгінген кезде өтініштерді қараудың кезектілік тәртібі сақталады.',
    'Өтінішті қайда рәсімдеу керек?': 'Сіз өзіңіздің жұмыс базаңызда(BRD) өтініш жасайсыз. Арнайы базалар жоқ.',
    'ДРБ әлеуметтік комиссиясының төрағасы': 'Погребицкий И. Е.',
    'Қандай құжаттарды ұсыну керек?': 'Балалардың туу туралы куәліктері (сканерленген) мүгедектік туралы анықтама \
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
    'Жұмыс орнынан анықтаманы қалай алуға болады?': 'Жұмыс орнынан анықтама алуға өтінімді "HR ОҚО өтінімдері" базасында ресімдеу қажет. Жаңасын жасаңыз-филиалыңыздың атауын таңдаңыз - жұмыс орнынан анықтама беруге өтінім – жұмыскердің аты – жөнін, анықтама түрін және қажетті өлшемдерді толтырыңыз (тілі, өтілі, лауазымдық жалақысы, орташа жалақысы) – өтінімді сақтаңыз-өтінімді ОҚО-ға жіберіңіз өтінімде сіздің өтініміңіздің орындаушысы автоматты түрде көрсетіледі.',
    'Lotus Notes есептік жазбасын құру және ИС  және ЖҚБ-ға кіруге болады?': 'Lotus Notes есептік жазбасын құру үшін  өзіңіздің жетекшілік ететін құрылымдық бөлімшенің басшысына/тәлімгеріне/іс жүргізушісіне ҚББЖ  (қатынауды басқарудың бірыңғай жүйесі) өтінімді ресімдеу үшін жүгінуіңіз керек. \nПо есептік жазбаның дайындығына қарай (логині мен паролі бар файл) Help Desk-ке келесі нөмір бойынша өтінім беру қажет: +7 727 2587304 Lotus Notes есептік жазбасын орнатқаннан кейін, сіз үшін АЖ және ДҚ-ға қажетті қол жетімділікті көрсете отырып, ҚББЖ базасында өтінімді өз бетіңізше жасау қажет.',
    'Егер сіз Lotus паролін немесе ақауын ұмытып қалсаңыз, қайда барасыз?': 'Туындаған мәселелер бойынша Help Desk +77272587304 өтінімін қалдырыңыз.',
    'Аурухана парақтары жұмысшыларға төлене ме?': '1) компаниядағы үздіксіз жұмыс өтіліне байланысты қызметкерлер (кәсіподақ ұйымының мүшелері және ұжымдық ұйымға қосылған) үшін (5 жасқа дейін - орташа жалақының 40%, 5 жылдан астам - еңбекке уақытша жарамсыздық күндері үшін орташа жалақының 70%);\n2) қалған қызметкерлер үшін - заңнамада белгіленген мөлшерде.\n3) Еңбекке уақытша жарамсыздық парағы / o парағы',
    'Еңбекке жарамсыздық парағын кім толтырады?': 'Еңбекке жарамсыздық парағын құрылымдық бөлімшенің  табельшісі/іс жүргізушісі толтырады. Еңбекке жарамсыздық парағында "Қазақтелеком" АҚ филиалы - "Бөлшек бизнес жөніндегі дивизион" -  филиалының атауы және өз лауазымы көрсетіледі.',
    'Еңбекке уақытша жарамсыздық парағын кімге тапсыру керек (аурухана парағы)': 'Еңбекке уақытша жарамсыздық парағын тапсырар алдында оны толтырып, оның тікелей жетекшісі қол қою керек, егер сіздің кеңсеңізде OҚO HR фронт-офисінің жұмыскері болмаса - BL екі жағынан сканерлеп, OҚO HR өтінім базасында өтінім ресімдеңіз; әйтпесе-толтырылған BL түпнұсқасын OҚO HR фронт-офисінің жұмыскеріне тапсырыңыз.',
    'Әріптестердің телефонын қайдан табуға болады?': 'Әріптестің телефонын  Қоғамның "Телефон анықтамалығы" базасынан таба аласыз-телефон нөмірлері, жұмыскерлерді бөлім бойынша іздеу',
    'Айналып өту парағы. Ол қашан ресімделеді?': '1) Жұмыстан босату туралы өтінішті ресімдегенде, үшінші парақта автоматты түрде кету парағы жасалады және қол қоюшылар көрсетіледі.\n2) филиалға/біржақты тәртіппен/ ауыстыру кезінде кету парағын өз жұмыс базаларында ресімделеді,'
}

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("Welcome курс | Бейімделу")
button2 = types.KeyboardButton("Өтінішті қалдыру")
button3 = types.KeyboardButton("Білім базасы")
button4 = types.KeyboardButton("ЕҚЕҚ кәртішкесін толтыру")
button5 = types.KeyboardButton("Жиі қойылатын сұрақтар")
markup.add(button, button2, button3, button4, button5)


def send_welcome_message(bot, message):
    # welcome_message = f'Сәлем {message.from_user.first_name}👋\
    #                    \nМен - ktbot, Компаниядағы сіздің жеке көмекшіңізбін.\
    #                    \n\nМіне, мен сізге қалай көмектесе аламын:\
    #                    \n  · ✉️ - Оқыту мәселелері бойынша өтініш жіберу;\
    #                    \n  · 🗃️ - Нұсқаулар мен глоссариймен білім қорына қол жеткізуді қамтамасыз етіңіз\
    #                    \n  · 👷 ЕҚЕҚ картасын жіберуге көмектесу;\
    #                    \n  · 📄 Жиі қойылатын сұрақтарға жауап беріңіз.\
    #                    \n\nAл егер сіз жаңа қызметкер болсаңыз, мен Welcome курсынан өтуді ұсынамын 😊.'
    welcome_message = f'Сәлем {message.chat.first_name}👋'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    with open("images/menu.jpg", 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Менің сценарийімде бірнеше пәрмендер бар:\
                                          \n/menu — негізгі мәзірге оралу (сіз мұны демонстрация кезінде кез келген уақытта жасай аласыз!)\
                                          \n/help - әзірлеушілермен байланысыңыз (егер қиындықтарға тап болсаңыз немесе сізде жақсарту үшін ұсыныстар болса, осы пәрменді қолданыңыз) \
                                          \n/start — ботты қайта іске қосыңыз\
                                          \n/language - боттың тілін өзгерту\
                                          \n\n Пәрмендерді /menu бөлігіндегі хабарламалар жолағынан таба аласыз (төменгі сол жақта) немесе жай ғана пәрменнің атауына, '/' ұмытпаңыз! белгісіне келіңіз.")


def send_error(bot, message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Ой, бірдеңе дұрыс болмады... /menu түймесін басу арқылы ботты қайта іске қосып көріңіз")


def adaption(bot, message):
    if message.text == 'Welcome курс | Бейімделу':
        db_connect.cm_sv_db(message, 'Welcome курс | Бейімделу')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('Айтыңызшы!', callback_data='Айтыңызшы!')
        markup.add(button)
        bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, 'Бастау үшін сізге мені қалай пайдалану керектігін айтамын 🫡',
                         reply_markup=markup)


def call_back(bot, call):
    if call.data == 'Айтыңызшы!':
        db_connect.cm_sv_db(call.message, 'Айтыңызшы!')
        bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'))
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Менде пернетақта бар, оның көмегімен сіз бөлімдерге өтіп, өзіңізге қажетті ақпаратты ала аласыз",
                         reply_markup=markup)
    if call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images\hello.jpg', 'rb'))
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup.add(button)
        bot.send_message(call.message.chat.id, "Төмендегі түймешікті басыңыз, жалғастырамыз.", reply_markup=markup)

    if call.data == "Кеттік!":
        bot.send_photo(call.message.chat.id, photo=open('images\kaztelecom_credo.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "'Қазақтелеком' АҚ - Қазақстан Республикасы Министрлер Кабинетінің 1994 жылғы 17 маусымдағы қаулысына сәйкес құрылған, Қазақстанның ірі телекоммуникациялық компаниясы.📌Бізде сізге арнайы дайындалған Компанияның қысқаша тарихы бар. Төмендегі файлдарды ашып, онымен танысыңыз.")
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
        bot.send_message(call.message.chat.id, "Егер жоқ болса, көңіліңізді түсірмеңіз, ол сізді жақын арада табады!")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Ия, көбірек білгім келеді!", callback_data="Ия, көбірек білгім келеді!")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Сізде бұл кім және маған не үшін қажет деген сұрақ туындаса, мен жауап беремін",
                         reply_markup=markup)

    if call.data == "Ия, көбірек білгім келеді!":
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сонымен, корпоративтік e-mail-ді тексеріңіз, сізге Баддиден біздің Компаниядағы бейімделу бағдарламасымен танысу туралы хабарлама келген шығар. ")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Қабылданды!", callback_data="Қабылданды!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\Buddy-3.jpg', 'rb'), reply_markup=markup)

    if call.data == "Қабылданды!":
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

    if call.data == "Керемет, әрі қарай жалғастырамыз!":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-1")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\credo_1.jpeg', 'rb'), reply_markup=markup)
    if call.data == "Келесі-1":
        bot.send_message(call.message.chat.id,
                         "Біздің компания 9 филиалдан тұрады және олардың аббревиатураларын күн сайын жұмыста міндетті түрде естисіз.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сол себепті Компанияның құрылымымен танысайық.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images\struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сізге бейтаныс терминдер немесе аббревиатуралар кездессе, онда біз сізге білім қорында глоссарий дайындадық.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сіз әрқашан негізгі мәзірден білім қорын таба аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-3")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\gloss.jpg', 'rb'), reply_markup=markup)

    if call.data == "Келесі-3":
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
    if call.data == "Келесі-4":
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-5")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\dear_users.jpeg', 'rb'), reply_markup=markup)
    if call.data == "Келесі-5":
        bot.send_message(call.message.chat.id,
                         '☎️" Қазақтелеком " АҚ-да "Нысана" жедел желісі біріктірілген, онда әр жұмыскер QR-код арқылы немесе төмендегі суретте көрсетілген байланыс нөміріне хабарласа алады. ')
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\call_center.jpeg', 'rb'), reply_markup=markup)

    if call.data == "Келесі-6":
        bot.send_message(call.message.chat.id,
                         "Керемет! \nКомпания туралы негізгі ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.Компания туралы негізгі ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Түсінікті!", callback_data="Түсінікті!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images\picture.jpg', 'rb'), reply_markup=markup)

    if call.data == "Түсінікті!":
        bot.send_message(call.message.chat.id,
                         "Құттықтаймыз!\nСіз Welcome курсынан өттіңіз. \n\nКомпанияға қош келдіңіз!")
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
                         "Бұл бөлімде Корпоративтік университетке сізді қызықтыратын мәселелер бойынша өтініш қалдыра аласыз.",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Санатты таңдау үшін телеграммдағы пернетақтаны басыңыз (әдетте бұл белгі енгізу жолағының оң жағында болады).")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында ")

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
                         "Сіздің өтінішіңіз қабылданды және өңделуде.\nЖоспарлы рұқсат беру уақыты - 1 жұмыс күні.")
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
        bot.send_message(message.chat.id,
                         "Егер жаңа бөлім немесе сұрақтарға жауап қосу бойынша ұсыныстар/идеялар болса, бізге жазыңыз info.ktcu@telecom.kz - Біз сіздің ұсынысыңызды міндетті түрде қарастырамыз және сізбен байланысамыз.")

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
    elif message.text == "Жеке кабинет telecom.kz":
        db_connect.cm_sv_db(message, 'Жеке кабинет telecom.kz')
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қызметті қалай төлеуге болады")
        button2_i = types.KeyboardButton("Төлем мәліметтерін қалай көруге болады")
        button3_i = types.KeyboardButton("Қосылған қызметтерді қалай көруге болады")
        button4_i = types.KeyboardButton("Менің Қызметтерім 'Бөлімі'")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
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
    elif message.text == "Iссапар | Рәсімдеу тәртібі":
        bot.send_message(message.chat.id,
                         "'Iссапар | Рәсімдеу тәртібі' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://wiki.telecom.kz/ru/instructionsopl/kommandiroviporyadok")
    elif message.text == "Мобильді нұсқа":
        bot.send_message(message.chat.id,
                         "'Мобильді нұсқа' санаты туралы ақпарат алу үшін төмендегі сілтемеге өтіңіз \nhttps://drive.google.com/drive/folders/1ojKgDgsUX9l9h0A1354AFVxFhQY2_ECZ?usp=drive_link")
    elif message.text == "ДК немесе ноутбук":
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Қалай кіруге болады")
        button2 = types.KeyboardButton("Жеке профиль")
        button3 = types.KeyboardButton("Порталдан ССП өту")
        markup_pk.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_pk)
    elif message.text == "Қалай кіруге болады":
        bot.send_message(message.chat.id,
                         "Санат туралы ақпарат алу үшін 'ДК арқылы қызметкердің порталына қалай кіруге болады?'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/vsRIDqt_-1A")
    elif message.text == "Жеке профиль":
        bot.send_message(message.chat.id,
                         "Санат туралы ақпарат алу үшін 'Жеке профильді қалай толтыруға болады?'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/V9r3ALrIQ48")
    elif message.text == "Порталдан ССП өту":
        bot.send_message(message.chat.id,
                         "Санат туралы ақпарат алу үшін 'Порталдан ССП өту'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/wnfI4JpMvmE")
    elif message.text == "Филиал серверлері бойынша деректер":
        bot.send_message(message.chat.id, "Филиал серверлері бойынша деректер: "
                                          "\nhttps://disk.telecom.kz/index.php/f/695222")
    elif message.text == "Lotus Орнату нұсқаулары":
        bot.send_message(message.chat.id,
                         "'Lotus Орнату нұсқаулары' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз"
                         "\nhttps://wiki.telecom.kz/ru/corp_systems/lotus_instruction")
    elif message.text == "Lotus орнату файлы":
        bot.send_message(message.chat.id, "Lotus Notes орнату файлы: \nhttps://disk.telecom.kz/index.php/f/695258")
    elif message.text == "CheckPoint Орнату нұсқаулығы":
        bot.send_message(message.chat.id,
                         "'CheckPoint Орнату нұсқаулығы' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз"
                         "\nhttps://wiki.telecom.kz/ru/corp_systems/checkpoint_instruction")
    elif message.text == "Checkpoint орнату файлы":
        bot.send_message(message.chat.id, "Checkpoint орнату файлы:\nhttps://disk.telecom.kz/index.php/f/695264")
    elif message.text == "Қазақтелеком АҚ":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративтік Университет":
        bot.send_message(message.chat.id,
                         "https://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
    elif message.text == "Қызметті қалай төлеуге болады":
        bot.send_document(message.chat.id, document=open("files/КАК ОПЛАТИТЬ УСЛУГИ КАЗАХТЕЛЕКОМ.pptx (1).pdf", 'rb'))
    elif message.text == "Төлем мәліметтерін қалай көруге болады":
        bot.send_document(message.chat.id,
                          document=open("files/КАК ПОСМОТРЕТЬ ИНФОРМАЦИЮ О ДЕТАЛЯХ ОПЛАТЫ (1).pdf", 'rb'))
    elif message.text == "Қосылған қызметтерді қалай көруге болады":
        bot.send_document(message.chat.id, document=open("files/КАК ПОСМОТРЕТЬ МОИ ПОДКЛЮЧЕННЫЕ УСЛУГИ (1).pdf", 'rb'))
    elif message.text == "Менің Қызметтерім 'Бөлімі'":
        bot.send_document(message.chat.id, document=open("files/РАЗДЕЛ «МОИ УСЛУГИ» (1).pdf", 'rb'))
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
        bot.send_message(message.chat.id,
                         "'Қазақтелеком' AҚ компаниясындағы терминдер мен аббревиатуралардың глоссарийі.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Аббревиатураның немесе терминнің түсіндірмесін немесе сипаттамасын алу үшін сөзді теріп, ақпарат алу үшін жіберіңіз.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Маңызды!\nСөзді қатесіз және артық таңбаларсыз енгізіңіз. Аббревиатураларды бас әріппен енгізу маңызды. Мысалы: ДК, ЖДБ, АТД.")


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
        bot.send_message(message.chat.id, "Біздің info.ktcu@telecom.kz поштамызға хат жолдау арқылы жұмысымызды жақсартуға көмектесе аласыз - біз міндетті түрде қарастырамыз.")


def menu(bot, message):
    db_connect.set_bool(message, False, False)
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)
