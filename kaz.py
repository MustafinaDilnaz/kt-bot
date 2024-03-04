from datetime import timedelta
import requests
from telebot import *

import appealsClass
import common_file
import db_connect
import lteClass
import userClass

from appealsClass import set_status, set_date_status, get_appeal_by_id, get_image_data, get_status, set_evaluation, \
    get_appeal_text_all, get_comment, set_comment, set_image_data, add_appeal_gmail, add_appeal, get_appeal_text, \
    set_appeal_text
from commands_historyClass import cm_sv_db
from common_file import (extract_text, extract_number, remove_milliseconds, \
    extract_numbers_from_status_change_decided, generate_buttons, send_gmails, useful_links, check_portal_guide,
                         send_photo_)
from file import check_id, admin_appeal_callback, appeal_inline_markup, admin_appeal, get_user_info, \
    rename_category_to_kaz, rename_category_to_rus
from lteClass import add_internal_sale, set_subscriber_type, set_category_i_s, set_performer_id_i_s, set_is_notified, \
    set_full_name, set_iin, set_phone_num_subscriber, set_subscriber_address, set_product_name, set_action, \
    set_delivery, set_simcard, set_modem, delete_internal_sale
from performerClass import get_performer_by_category, get_regions, list_categories, get_categories_by_parentcategory, \
    get_performer_id_by_category, get_subsubcategories_by_subcategory, get_performer_by_subsubcategory, \
    get_performer_by_category_and_subcategory, get_performers_
from userClass import get_branch, get_firstname, get_user, get_lastname, get_phone_number, get_email, get_table_number
from user_infoClass import set_appeal_field, get_category_users_info, set_category, get_appeal_field, clear_appeals, \
    set_bool, get_subsubsubcategory_users_info, set_subsubcategory_users_info

categories_ = ['Learning.telecom.kz | Техникалық қолдау', 'Оқыту | Корпоративтік Университет',
               '"Нысана" қолдау қызметі', 'Комплаенс қызметіне хабарласыңыз',
               'Сатып алу порталы 2.0 | Техникалық қолдау', 'Ашық тендер', 'Баға ұсыныстарын сұрау',
               'Бір дереккөз және электронды дүкен', 'Шарттар жасасу', 'Логистика', 'Тасымалдау']
faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары", "Қарыздар бойынша сұрақтар",
             "Сатып алу қызметі бойынша сұрақтар", "Сатып алу порталы бойынша сұрақтар"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["👷ҚТ ж ЕҚ кәртішкесін толтыру", "Қауіпті фактор | шарт", "Жұмысты орындау тәртібі", "Ұсыныстар | Идеялар"]
kb_field = ["🗃️Білім базасы", "Нұсқаулық базасы", "Глоссарий", "Пайдалы сілтемелер", "Реттеуші құжаттар"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар",
                "Checkpoint VPN | Қашықтан жұмыс", "Iссапар | Рәсімдеу тәртібі",
                "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту", "Филиал серверлері бойынша деректер",
                "Lotus Орнату нұсқаулары", "Lotus орнату файлы", "Қазақтелеком АҚ",
                "Корпоративтік Университет", "Қызметті қалай төлеуге болады",
                "Төлем туралы мәліметтерді қалай көруге болады",
                "Қосылған қызметтерді қалай көруге болады", "'Менің Қызметтерім' Бөлімі", "ADSL модемі",
                "IDTV консолі", "ONT модемдері", "Router 4G and Router Ethernet", "CheckPoint Орнату нұсқаулығы",
                "Checkpoint орнату файлы", "Сатып алу порталы | Нұсқаулар", 'Хатшылар үшін | Нұсқаулар',
                "Бастамашылар | Нұсқаулар үшін"]
instr_field = ["Брендбук және логотиптер", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар"]
adapt_field = ["😊Welcome курс | Бейімделу"]
portal_bts = ["'Бірлік' порталы дегеніміз не?", "Порталға қалай кіруге болады?", "Порталға өтініш қалдыру"]
# "Бірлік Гид"
portal_ = ["Мобильді нұсқа", "ДК немесе ноутбук", "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту",
           "iOS", "Android", "Есть checkpoint", "Нет checkpoint"]
portal_guide = ["Кері байланыс үшін қайда жүгіну керек-пікірлер мен ұсыныстар?",
                "Порталда компанияның стратегиясымен қайдан танысуға болады?",
                "Қауымдастықты қалай құруға болады?", "Экожүйеде демалысты қалай жоспарлауға болады?",
                "Әріптесіңізге қалай алғыс айтамын?", "Экожүйеде сауалнаманы қалай құруға болады?",
                "Қазақтелеком дүкенінен жеңілдікпен тауарды қалай сатып алуға болады?",
                "Қазақтелеком саудасын қалай сатып алуға болады?",
                "Компания қызметкерлеріне жеңілдіктер мен акцияларды қайдан көруге болады?"]
lte_ = ['🛜 Акция "Пилот LTE"', "Об акции", "А как продать?", "Отправить заявку", "Мои продажи"]
pp = ['ALEM PLUS (1 год) c Bereke 2', 'ALEM PLUS (1 год) c Bereke 1', 'ALEM PLUS (без контракта) c Bereke 1',
      'ALEM PLUS (без контракта) c Bereke 2', 'ALEM TV (без контракта)', 'ALEM TV (1 год)',
      'ALEM MOBILE (без контракта) c Bereke 1', 'ALEM MOBILE (без контракта) c Bereke 2',
      'ALEM MOBILE (1 год) c Bereke 1', 'ALEM MOBILE (1 год) c Bereke 2', 'ТП Алем']
faq_1 = {
    'Қазақтелеком "АҚ-да "Демеу" бағдарламасы кімге бағытталған?':
        'Қазақтелеком" АҚ "Демеу" бағдарламасын әлеуметтік қолдау: (бұдан әрі-Бағдарлама) жұмыскерлерге мәртебесі '
        'бойынша жіберілді: \
    \n1) Көп балалы отбасы-өз құрамында төрт және одан да көп бірге тұратын кәмелетке толмаған балалары, оның ішінде '
        'кәмелетке толғаннан кейін орта, техникалық және кәсіптік, орта білімнен кейінгі, жоғары және (немесе) жоғары '
        'оқу орнынан кейінгі білім беру ұйымдарында күндізгі оқу нысаны бойынша білім алатын балалары бар отбасы  \
    отбасы (бірақ білім алуды аяқтағанға дейін) жиырма үш жасқа толған жетістіктер);  \
    \n2) Мүгедек балалары бар отбасы-өз құрамында он сегіз жасқа дейінгі баласы (балалары) бар, бар, '
        'тұрмыс-тіршілігінің шектелуіне және оны әлеуметтік қорғау қажеттігіне әкеп соқтыратын, ауруларға, мертігулерге'
        ' (жаралануға, жарақаттарға, контузияларға), олардың зардаптарына, кемістіктерге байланысты ағзаның қызметінде'
        ' тұрақты бұзылуы бар отбасын (оларды) әлеуметтік қорғау; \
    \n3) 2-ден астам бала асырап алған/асырап алған отбасы - құрамында 2-ден астам кәмелетке толмаған асырап алған/'
        'асырап алынған балалары бар, денсаулық жағдайы бойынша диспансерлік есепте тұрған және жалғыз асыраушысы '
        'бар отбасы.\
    \n4) A8-B4 грейдінің жұмыскерлеріне балаларының орта арнаулы оқу орнында (бұдан әрі - CYZ) жоғары оқу орнында '
        '(бұдан әрі - BYZ) түлектердің оқу курсына (тұруға және тамақтануға арналған шығыстарды есептемегенде) ақы '
        'төлеу бойынша әлеуметтік қолдау белгіленеді. Барлық әлеуметтік қолдау түрлері әлеуметтік қолдау көрсету '
        'мерзімінде Қоғамда кемінде 3 жыл үздіксіз жұмыс өтілі бар Қоғам жұмыскерлеріне көрсетіледі.',
    'Жұмыскерлерге әлеуметтік қолдау түрлері':
        '1) балалардың сауықтыру лагерьлеріне жолдамалар сатып алуға байланысты шығыстарды өтеу; \
    \n2) Балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін) жолдамалар сатып алуға байланысты '
        'шығыстарды өтеу; \
    \n3) Балаларға арналған дәрілік заттарды сатып алуға материалдық көмек; \
    \n4) Мектеп оқушыларының тамақтануына материалдық көмек; \
    \n5) Оқу жылының басына материалдық көмек; \
    \n6) Медициналық оңалту/баланы оңалтудың жеке бағдарламасы үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n7) Арнайы білім беру бағдарламалары үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n8) Арнайы түзету ұйымдарына барғаны үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n9) Мектеп бітірген күні кәмелетке толмаған және оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек; \
    \n10) Орта арнаулы оқу орнында (бұдан әрі-CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) балаларының бітіруші оқу курсын'
        ' (тұруға және тамақтануға арналған шығыстарды есептемегенде) төлеу жөніндегі шығыстарды (A8 - B4 грейд '
        'қызметкерлеріне) өтеу.',
    'Әлеуметтік комиссияға өтініш беру үдерісі':
        'Филиалдың әлеуметтік комиссиясына өтінішті ресімдеу - др. ДРБ әлеуметтік комиссиясының төрағасы-Погребицкий'
        ' И. Е. әлеуметтік қолдау көрсету үшін қоғам қызметкерлері жүгінген кезде өтініштерді қараудың кезектілік '
        'тәртібі сақталады.',
    'Өтінішті қайда рәсімдеу керек?':
        'Сіз өзіңіздің жұмыс базаңызда(BRD) өтініш жасайсыз. Арнайы базалар жоқ.',
    'Әлеуметтік комиссияның төрағасы': 'Филиалдардағы әлеуметтік комиссияның төрағасы-филиалдың бас директоры. '
                                       'ОА-операциялық тиімділік жөніндегі Бас директор',
}
faq_2 = {
    'Жұмыс орнынан анықтаманы қалай алуға болады?':
        'Жұмыс орнынан анықтама алуға өтінімді "HR ОҚО өтінімдері" базасында ресімдеу қажет. Жаңасын '
        'жасаңыз-филиалыңыздың атауын таңдаңыз - жұмыс орнынан анықтама беруге өтінім – жұмыскердің аты – жөнін, '
        'анықтама түрін және қажетті өлшемдерді толтырыңыз (тілі, өтілі, лауазымдық жалақысы, орташа жалақысы) – '
        'өтінімді сақтаңыз-өтінімді ОҚО-ға жіберіңіз өтінімде сіздің өтініміңіздің орындаушысы автоматты түрде '
        'көрсетіледі.',
    'Lotus Notes есептік жазбасын құру және ИС  және ЖҚБ-ға кіруге болады?':
        'Lotus Notes есептік жазбасын құру үшін  өзіңіздің жетекшілік ететін құрылымдық бөлімшенің басшысына/'
        'тәлімгеріне/іс жүргізушісіне ҚББЖ  (қатынауды басқарудың бірыңғай жүйесі) өтінімді ресімдеу үшін жүгінуіңіз '
        'керек. \nПо есептік жазбаның дайындығына қарай (логині мен паролі бар файл) Help Desk-ке келесі нөмір бойынша '
        'өтінім беру қажет: +7 727 2587304 Lotus Notes есептік жазбасын орнатқаннан кейін, сіз үшін АЖ және ДҚ-ға '
        'қажетті қол жетімділікті көрсете отырып, ҚББЖ базасында өтінімді өз бетіңізше жасау қажет.',
    'Егер сіз Lotus паролін немесе ақауын ұмытып қалсаңыз, қайда барасыз?':
        'Туындаған мәселелер бойынша Help Desk +77272587304 өтінімін қалдырыңыз.',
    'Аурухана парақтары жұмысшыларға төлене ме?':
        '1) компаниядағы үздіксіз жұмыс өтіліне байланысты қызметкерлер (кәсіподақ ұйымының мүшелері және ұжымдық '
        'ұйымға қосылған) үшін (5 жасқа дейін - орташа жалақының 40%, 5 жылдан астам - еңбекке уақытша жарамсыздық '
        'күндері үшін орташа жалақының 70%);\n2) қалған қызметкерлер үшін - заңнамада белгіленген мөлшерде.\n3) Еңбекке'
        ' уақытша жарамсыздық парағы / o парағы',
    'Еңбекке жарамсыздық парағын кім толтырады?':
        'Еңбекке жарамсыздық парағын құрылымдық бөлімшенің  табельшісі/іс жүргізушісі толтырады. Еңбекке жарамсыздық '
        'парағында "Қазақтелеком" АҚ филиалы - "Бөлшек бизнес жөніндегі дивизион" -  филиалының атауы және өз лауазымы'
        ' көрсетіледі.',
    'Еңбекке уақытша жарамсыздық парағын кімге тапсыру керек (аурухана парағы)':
        'Еңбекке уақытша жарамсыздық парағын тапсырар алдында оны толтырып, оның тікелей жетекшісі қол қою керек, '
        'егер сіздің кеңсеңізде OҚO HR фронт-офисінің жұмыскері болмаса - BL екі жағынан сканерлеп, OҚO HR өтінім '
        'базасында өтінім ресімдеңіз; әйтпесе-толтырылған BL түпнұсқасын OҚO HR фронт-офисінің жұмыскеріне '
        'тапсырыңыз.',
    'Әріптестердің телефонын қайдан табуға болады?':
        'Әріптестің телефонын  Қоғамның "Телефон анықтамалығы" базасынан таба аласыз-телефон нөмірлері, жұмыскерлерді '
        'бөлім бойынша іздеу',
    'Айналып өту парағы. Ол қашан ресімделеді?':
        '1) Жұмыстан босату туралы өтінішті ресімдегенде, үшінші парақта автоматты түрде кету парағы жасалады және қол'
        ' қоюшылар көрсетіледі.\n2) филиалға/біржақты тәртіппен/ ауыстыру кезінде кету парағын өз жұмыс '
        'базаларында ресімделеді,'
}
faq_procurement_portal = {
    'Не могу войти на сайт': 'Возможно Вы ввели некоректный адрес. Вам нужно ввести в адресную строку следующий адрес: '
                             'zakup.telecom.kz/app ',
    'Какие логин и пароль нужно ввести для входа?': 'Логин и пароль такие же как на mail.telecom.kz, '
                                                    'CheckPoint или при входе в Ваш ПК',
    'Логин и пароль корректный, но все равно не удалось войти': '"Возможно Вы еще не зарегистрированы на портале '
                                                                'закупок. Для регистрации Вам нужно обратититься к '
                                                                'одному из специалитов технической поддержки портала '
                                                                'закупок. Для обращения Вы можете перейти главное меню '
                                                                'ktbot и оставить Ваше обращения в разделе '
                                                                '""У меня есть вопрос""."',
    'Не могу зайти на сайт хотя ввожу адрес сайта верно': 'Возможно у вас проблемы с интернетом или не подключили '
                                                          'CheckPoint(если входите через ноутбук)'
}
faq_procurement_activities = {
    'Чем регулируются закупки в АО «Казахтелеком»?':
        'Порядок осуществления закупок акционерным обществом «Фонд национального благосостояния «Самрук-Қазына» и '
        'юридическими лицами, пятьдесят и более процентов голосующих акций (долей участия) которых прямо или косвенно '
        'принадлежат АО «Самрук-Қазына» на праве собственности или доверительного управления и Регламент взаимодействия'
        ' Дирекции «Телеком Комплект» с филиалами АО «Казахтелеком».',
    'Как определяется способ закупа и какие виды закупок?':
        """1) тендер: 
- двухэтапный 
- с торгами на понижение (на усмотрение Заказчика, нельзя по СМР, экспертизе, тех.надзору) 
- с ограниченным участием (после 2 несост.тендеров) 
2) запрос ценовых предложений – до 10 000 МРП (обязателен при закупке товаров по реестру доверенного ПО и продукции эл.промышленности и товаров «экономики простых вещей» без ограничений по сумме подлежит исключению с 1 января 2024 года);
3) через товарные биржи; 
4) из одного источника (соответствие с ст. 59 Порядка); 
5) посредством электронного магазина – до 8 млн.тг по 32 категориям товаров на площадке skstore.kz.
6) особый порядок (соответствие с ст. 73 Порядка)""",
    'Какие виды плана закупок существуют в компании?':
        'План закупок (предварительный, годовой, долгосрочный) - документ, содержащий сведения о закупке товаров, '
        'работ, услуг, необходимых для удовлетворения нужд заказчика в течение периода, определённого планом и в '
        'соответствии с графиком плана. ',
    'Что такое демпинг и как применяется в закупках?': """
Демпинг - продажа товаров и услуг по искусственно заниженным ценам, ниже рыночных. 
Ценовое предложение признаётся демпинговым в следующих случаях: 
- ценовое предложение на СМР, комплексные работы по которым имеется сметная, предпроектная, проектная 
(проектно-сметная) документация, утвержденная в установленном порядке, более чем на 5% ниже плановой суммы предпроектные
- проектные и изыскательские работы, работ по комплексной вневедомственной экспертизе проектов строительства и услуг по техническому надзору за строительством объектов более чем на 10% ниже плановой суммы; 
- ценовое предложение на консультационные (консалтинговые) услуги более чем на 70 % ниже среднеарифметической цены всех представленных ценовых предложений; • ценовое предложение на иные работы, услуги более чем на 20 % ниже среднеарифметической цены всех представленных ценовых предложений
- ценовое предложение на товары более чем на 15% ниже плановой суммы.
Антидемпинговые условия не распространяются на закупки с торгами на понижение и тендера по ЗКС (с переговорами на понижение цены)."
    """,
    'Что такое офтейк контракт и как заключается?':
        """
Офтейк-контракт — это гарантия для казахстанских товаропроизводителей на долгосрочный заказ, с учетом организации производства, реализуется в рамках программы импортозамещения.
Для приобретения товара, производимого потенциальным поставщиком в рамках реализации Проекта по созданию новых производств, посредством заключения офтейк-контракта, проводится закупка способом из одного источника на основании пп.8 п.1 Ст.59 Порядка осуществления закупок. 
        """,
    'Что такое пул товаров импортозамещения?':
        'Пул товаров всех ПК Фонда, в которых имеется постоянная и стабильная востребованность группы компаний, '
        'но отсутствует производство в стране.',
    'Как определяется маркетинговая цена?':
        'Маркетинговая цена - цена на товар, применяемая заказчиком для формирования бюджетов расходов/плана(ов) '
        'закупок и не включающая в себя налог на добавленную стоимость. Маркетинговые цены на товары определяются в '
        'соответствии с Приложением № 3 к Порядку."'

}
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']


def get_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    if check_id(str(message.chat.id)):
        markup.add(types.KeyboardButton("Админ панель"))
    button = types.KeyboardButton("😊Welcome курс | Бейімделу")
    button3 = types.KeyboardButton("🗃️Білім базасы")
    button4 = types.KeyboardButton("👷ҚТ ж ЕҚ кәртішкесін толтыру")
    button5 = types.KeyboardButton("📄Менің сұрағым бар")
    button6 = types.KeyboardButton("🧐Менің профилім")
    button7 = types.KeyboardButton('🖥Портал "Бірлік"')
    button8 = types.KeyboardButton(lte_[0])
    markup.add(button)
    if get_branch(message.chat.id) == branches[2]:
        markup.add(button8)
    markup.add(button3, button7, button5, button4, button6)
    return markup


def send_welcome_message(bot, message):
    welcome_message = f'Сәлем {get_firstname(message)}👋'
    markup = get_markup(message)
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    send_photo_(bot, message.chat.id, "images/menu.jpg")
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
    common_file.send_photo_(bot, message.chat.id, 'images/oops_error kaz.jpg')
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Ой, бірдеңе дұрыс болмады... /menu түймесін басу арқылы ботты қайта іске қосып көріңіз")


def adaption(bot, message):
    if message.text == '😊Welcome курс | Бейімделу':
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton('Айтыңызшы!', callback_data='Айтыңызшы!')
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
        send_photo_(bot, message.chat.id, 'images/dear_collegue_kaz.jpg')
        time.sleep(0.75)
        bot.send_message(message.chat.id, 'Бастау үшін сізге мені қалай пайдалану керектігін айтамын 🫡',
                         reply_markup=markup_adapt)


def performer_text(appeal_info, message):
    status = kaz_get_status(message, appeal_info[0])
    performer_info = get_performer_by_category(category=appeal_info[3])
    category = rename_category_to_kaz(categories_, appeal_info[3])
    text = f"<b>ID</b> {appeal_info[0]}\n\n" \
           f" Мәртебесі: {status}\n" \
           f" Құрылған күні: {str(appeal_info[5])}\n" \
           f" Санат: {category}\n" \
           f" Мәтін: {str(appeal_info[4])}\n" \
           f" Соңғы мәртебе өзгерген күн: {str(appeal_info[6])}\n\n" \
           f"Орындаушы\n" \
           f" ТАӘ: {performer_info[4]} {performer_info[3]}\n" \
           f" Телефон нөмірі: {performer_info[5]}\n" \
           f" Email: {performer_info[6]}\n" \
           f" Telegram: {performer_info[7]}\n\n" \
           f" Пікір: {str(appeal_info[8])}"
    return text


def kaz_get_status(message, appeal_id):
    language = userClass.get_language(message)
    status = get_status(appeal_id)[0][0]
    if language == "kaz":
        if status == "Решено":
            return "Шешілді"
        elif status == "В процессе":
            return "Процесінде"
        return "Өтініш қабылданды"
    return status


def call_back(bot, call):
    if call.data == 'Айтыңызшы!':
        cm_sv_db(call.message, 'Айтыңызшы!')
        send_photo_(bot, call.message.chat.id, 'images/picture kaz.jpg')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Менде пернетақта бар⌨️, оның көмегімен сіз бөлімдерге өтіп, өзіңізге "
                                               "қажетті ақпаратты ала аласыз",
                         reply_markup=markup_callback)
    elif call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images/hello kaz.jpg', 'rb'))
        send_photo_(bot, call.message.chat.id, 'images/picture.jpg')

        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Төмендегі түймешікті басыңыз👇🏻, жалғастырамыз.",
                         reply_markup=markup_callback)
    elif call.data == "Кеттік!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo_kaz.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "'Қазақтелеком' АҚ - Қазақстан Республикасы Министрлер Кабинетінің "
                                               "1994 жылғы 17 маусымдағы қаулысына сәйкес құрылған, Қазақстанның ірі "
                                               "телекоммуникациялық компаниясы.📌Бізде сізге арнайы дайындалған "
                                               "Компанияның қысқаша тарихы бар. Төмендегі файлдарды ашып, онымен "
                                               "танысыңыз.")
        bot.send_document(call.message.chat.id, open('images/Наша история 1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/Наша история 2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Ал, Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Егер бәрі түсінікті болса, біз жалғастырамыз ба?",
                         reply_markup=markup_callback)
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
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users_kaz.jpg', 'rb'),
                       reply_markup=markup_callback)
    elif call.data == "Келесі-5":
        bot.send_message(call.message.chat.id,
                         '☎️" Қазақтелеком " АҚ-да "Нысана" жедел желісі біріктірілген, онда әр жұмыскер QR-код арқылы '
                         'немесе төмендегі суретте көрсетілген байланыс нөміріне хабарласа алады. ')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center_kaz.jpg', 'rb'),
                       reply_markup=markup_callback)
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
        cm_sv_db(call.message, 'Welcome курс | Бейімделу end')
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
                                               url="https://apps.apple.com/ru/app/check-point-capsule-connect/"
                                                   "id506669652")
        markup_p.add(button_p1)
        bot.send_message(str(call.message.chat.id),
                         "iOS жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/giK26_GgVgE ",
                         reply_markup=markup_p)
    elif call.data == portal_[6]:
        markup_p = types.InlineKeyboardMarkup()
        button_p2 = types.InlineKeyboardButton(text="PlayMarket сілтемесі",
                                               url="https://play.google.com/store/apps/details?id=com.checkpoint."
                                                   "VPN&hl=en&gl=US&pli=1")
        markup_p.add(button_p2)
        bot.send_message(str(call.message.chat.id),
                         "Android жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/KjL9tpunb4U",
                         reply_markup=markup_p)
    elif call.data == "abbr":
        msg = bot.send_message(call.message.chat.id, "Аббревиатураны енгізіңіз")
        bot.register_next_step_handler(msg, get_abbr, bot)
    elif str(call.data).isdigit():
        appeal_id = str(call.data)
        appeal_info = get_appeal_by_id(appeal_id)[0]
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Орындаушыға жазыңыз', callback_data=str(appeal_info[0]) + 'texting')
        text = performer_text(appeal_info, message=call.message)
        if appeal_info[12] != "" and appeal_info[12] is not None and appeal_info[12] != " ":
            if db_connect.get_sale(appeal_info[12])[10] == "Самостоятельно":
                button_ = types.InlineKeyboardButton("Добавить модем | симкарту",
                                                     callback_data=str(appeal_info[12]) + "add_modem")
                button_1 = types.InlineKeyboardButton("Добавить фотографию Акта",
                                                      callback_data=str(appeal_info[12]) + "add_act")
                markup.add(button_, button_1)
                bot.send_message(call.message.chat.id, text, reply_markup=markup)
                return
        markup.add(btn)
        bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif extract_number(call.data, r'^(\d+)texting') is not None:
        appeal_id = extract_number(call.data, r'^(\d+)texting')
        msg = bot.send_message(call.message.chat.id, 'Түсініктеме енгізіңіз')
        bot.register_next_step_handler(msg, add_comment, bot, appeal_id, False)
    elif extract_text(call.data, r'^.*abbr_save$', 'abbr_save') is not None:
        text = extract_text(call.data, r'^.*abbr_save$', 'abbr_save')
        send_abbr(bot, call.message, text)
    elif extract_text(call.data, r'^.*abbr_add$', 'abbr_add') is not None:
        text = extract_text(call.data, r'^.*abbr_add$', 'abbr_add')
        msg = bot.send_message(call.message.chat.id, "Аббревиатураның транскрипциясын енгізіңіз")
        bot.register_next_step_handler(msg, get_decoding, bot, text)
    elif extract_number(str(call.data), r'^(\d+)add_act') is not None:
        set_appeal_field(call.message, True)
        bot.send_message(call.message.chat.id, "Отправьте фотографию акта")
    elif extract_number(str(call.data), r'^(\d+)add_act') is not None:
        set_appeal_field(call.message, True)
        bot.send_message(call.message.chat.id, "Отправьте фотографию акта")
    elif extract_number(str(call.data), r'^(\d+)add_modem') is not None:
        lte_id = extract_number(str(call.data), r'^(\d+)add_modem')
        msg = bot.send_message(call.message.chat.id, "Введите серийный номер симкарты")
        bot.register_next_step_handler(msg, get_simcard, bot, lte_id)
    elif extract_number(str(call.data), r'^(\d+)statusinprocess') is not None \
            or extract_number(str(call.data), r'^(\d+)statusdecided$') is not None:
        appeal_id = extract_number(str(call.data), r'^(\d+)statusinprocess')
        if appeal_id is None:
            appeal_id = extract_number(str(call.data), r'^(\d+)statusdecided$')
            set_status(appeal_id, "Решено")
        else:
            set_status(appeal_id, "В процессе")
        now = datetime.now() + timedelta(hours=6)
        now_updated = remove_milliseconds(now)
        set_date_status(appeal_id, str(now_updated))
        bot.send_message(call.message.chat.id, "Статус изменен")
        admin_appeal_callback(call, bot, add_comment)
        appeal_info = get_appeal_by_id(appeal_id)[0]
        text = performer_text(appeal_info, message=call.message)
        bot.send_message(appeal_info[1], "Мәртебесі өзгертілді")
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        bot.send_message(appeal_info[1], text)
        if get_status(appeal_id)[0][0] == "Решено":
            appeal_ = get_appeal_by_id(appeal_id)
            if appeal_[0][3] in get_regions():
                bot.send_message(appeal_info[1], "Выша заявка принята. Спасибо большое за содейтвие")
                return
            markup_callback = types.InlineKeyboardMarkup(row_width=5)
            for i in range(1, 6):
                callback_d = str(i) + "evaluation" + str(appeal_info[0])
                button_callback = types.InlineKeyboardButton(i, callback_data=callback_d)
                markup_callback.add(button_callback)
            bot.send_message(appeal_info[1], "Шешілген үндеуді 1-ден 5-ке дейін бағалаңыз\n\nҚайда 1-өте нашар, "
                                             "5-керемет", reply_markup=markup_callback)
    elif extract_numbers_from_status_change_decided(str(call.data)) is not None:
        evaluation, appeal_id = extract_numbers_from_status_change_decided(str(call.data))
        set_evaluation(appeal_id, evaluation)
        bot.edit_message_text("Пікіріңіз үшін рахмет.\nСіз бізге жақсы адам болуға көмектесесіз", call.message.chat.id,
                              call.message.message_id)
        bot.answer_callback_query(call.id)
    elif extract_number(str(call.data), r'^(\d+)lte') is not None:
        sale_id = extract_number(str(call.data), r'^(\d+)lte')
        appeal_id = db_connect.get_appeal_by_lte_id(sale_id)
        text = get_appeal_text_all(appeal_id)
        bot.send_message(call.message.chat.id, text)
    else:
        admin_appeal_callback(call, bot, add_comment)


def get_abbr(message, bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Аббревиатураны жіберу", callback_data=message.text + "abbr_save")
    button2 = types.InlineKeyboardButton("Транскрипт қосу", callback_data=message.text + "abbr_add")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Келесі қадамды таңдаңыз", reply_markup=markup)


def send_abbr(bot, message, text):
    bot.send_message(message.chat.id, "Аббревиатура сақталды, көмек үшін рахмет")
    bot.send_message('6682886650', "Предложение добавления глоссария\n" + text)


def get_decoding(message, bot, text):
    send_abbr(bot, message, text + " - " + message.text)


def add_comment(message, bot, appeal_id, isAdmin=True):
    comment_ = '\n' + "Пользователь: "
    if isAdmin:
        comment_ = '\n' + "Исполнитель: "
    comment = str(get_comment(appeal_id)[0][0]) + comment_ + message.text
    set_comment(appeal_id, comment)
    appeal_info = get_appeal_by_id(appeal_id)[0]
    image_data = get_image_data(appeal_id)
    text = performer_text(appeal_info, message)
    try:
        bot.send_photo(appeal_info[1], image_data)
    except:
        print("error")

    if isAdmin:
        bot.send_message(appeal_info[1], text)
        bot.send_message(message.chat.id, "Түсініктеме қосылды")
    else:
        bot.send_message(appeal_info[7], text)
        bot.send_message(message.chat.id, "Түсініктеме қосылды")


def appeal(bot, message, message_text):
    set_appeal_field(message, True)
    if message_text == "Менің өтініштерім":
        markup_a = appeal_inline_markup(message, "kaz", categories_)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Мұнда сіз өтініштеріңіздің күйін бақылай аласыз",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Бұл жерде әлі бос,\nбірақ сіз апелляцияны қалдыра аласыз және ол "
                                              "осы жерде көрсетіледі")
    elif message_text == "Өтінішті қалдыру" or message_text == portal_bts[2]:
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Иә")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Ақпарат дұрыс па?", reply_markup=markup_ap)
    elif message_text == "Иә":
        if get_category_users_info(message) == 'Портал "Бірлік"':
            appeal(bot, message, "portal")
            return
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap = generate_buttons(categories_[:4], markup_ap)
        markup_ap.add(types.KeyboardButton("Сатып алу қызметі"))
        markup_ap.add(types.KeyboardButton("EX-ке сұрақ"))
        bot.send_message(message.chat.id, "Өтініш санатын таңдаңыз", reply_markup=markup_ap)
    elif message_text == "portal":
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text == "Сатып алу қызметі":
        markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_a = generate_buttons(categories_[4:], markup_a)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_a)
    elif message_text == "EX-ке сұрақ":
        branch = get_branch(message.chat.id)
        set_category(message, "Вопрос к EX")
        if branch == 'Обьединение Дивизион "Сеть"':
            markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_a = generate_buttons(get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'), markup_a)
            bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text in list_categories() or message_text in categories_ \
            or message_text in get_categories_by_parentcategory("Закупочная деятельность"):
        category = rename_category_to_rus(categories_, message.text)
        set_category(message, category)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text == "Фотосурет қосыңыз":
        bot.send_message(message.chat.id, "Фотосуретті жіберіңіз")
    elif message_text in get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'):
        set_subsubcategory_users_info(message.chat.id, message_text)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message.photo:
        file_info: object = bot.get_file(message.photo[-1].file_id)
        file_url = 'https://api.telegram.org/file/bot{}/{}'.format(db_connect.TOKEN, file_info.file_path)
        file = requests.get(file_url)
        appeal_id = db_connect.get_last_appeal(message.chat.id)[0][0]
        appeal_ = get_appeal_by_id(appeal_id)[0]
        set_image_data(appeal_id, file)
        image_data = get_image_data(appeal_id)
        if appeal_[7] is None or appeal_[7] == '' or len(str(appeal_[7])) == 0:
            end_appeal_gmail(bot, message, appeal_id, file_url)
        else:
            bot.send_photo(appeal_[7], image_data)
            end_appeal(bot, message, appeal_id)
    elif message_text == "Өтініш жіберу":
        appeal_id = db_connect.get_last_appeal(message.chat.id)[0][0]
        appeal_ = get_appeal_by_id(appeal_id)[0]
        if appeal_[7] is None or appeal_[7] == '' or len(str(appeal_[7])) == 0:
            end_appeal_gmail(bot, message, appeal_id)
        else:
            end_appeal(bot, message, appeal_id)
    elif get_appeal_field(message) and get_category_users_info(message) != ' ':
        now = datetime.now() + timedelta(hours=6)
        now_updated = remove_milliseconds(now)
        category = get_category_users_info(message)
        branch = get_branch(message.chat.id)
        if category == "Вопрос к EX":
            if branch == 'Обьединение Дивизион "Сеть"':
                subsubcategory = str(get_subsubsubcategory_users_info(message.chat.id)).strip()
                performer_id = get_performer_by_subsubcategory(subsubcategory)[0][0]
            else:
                performer_id = get_performer_by_category_and_subcategory(category, branch)[0][1]
        else:
            performer_id = get_performer_id_by_category(category)

        if performer_id is None or performer_id == '' or len(str(performer_id)) == 0:
            add_appeal_gmail(message.chat.id, category, message.text, now_updated)
        else:
            performer_id = get_performer_by_category(category)[1]
            add_appeal(message.chat.id, "Обращение принято", category, message.text, now_updated,
                       now_updated, performer_id, ' ', False)
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_ap = types.KeyboardButton("Фотосурет қосыңыз")
        button2_ap = types.KeyboardButton("Өтініш жіберу")
        markup_ap.add(button2_ap, button1_ap)
        bot.send_message(message.chat.id, "Сіз фотосуретті апелляциямен бірге жібере аласыз", reply_markup=markup_ap)
    else:
        admin_appeal(bot, message, message_text)


def end_appeal(bot, message, appeal_id):
    category = appealsClass.get_category_by_appeal_id(appeal_id)[0][0]
    performer_id = get_performer_by_category(category=category)[1]
    text = get_appeal_text_all(appeal_id)
    bot.send_message(performer_id, text)
    bot.send_message(message.chat.id, "Ваше обращения принято")
    clear_appeals(message)
    menu(bot, message)


def end_appeal_gmail(bot, message, appeal_id, file=None):
    appeal_ = get_appeal_by_id(appeal_id)[0]
    text = get_user_info(message.chat.id)
    appeal_text = f'{text} \n {get_appeal_text(appeal_id)}'
    send_gmails(appeal_text, appeal_[3], file)
    bot.send_message(str(message.chat.id), "Сіздің өтінішіңіз сәтті жіберілді")


def faq(bot, message):
    if message.text == "Жиі қойылатын сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("HR сұрақтары")
        button_1 = types.KeyboardButton("Қарыздар бойынша сұрақтар")
        button_p1 = types.KeyboardButton("Сатып алу қызметі бойынша сұрақтар")
        button_p2 = types.KeyboardButton("Сатып алу порталы бойынша сұрақтар")
        markup_faq.add(button_d, button_hr, button_1, button_p1, button_p2)
        bot.send_message(message.chat.id, "Мұнда сіз жиі қойылатын сұрақтарға жауап таба аласыз",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер жаңа бөлім немесе сұрақтарға жауап қосу бойынша ұсыныстар/идеялар болса, бізге жазыңыз "
                         "info.ktcu@telecom.kz - Біз сіздің ұсынысыңызды міндетті түрде қарастырамыз және "
                         "сізбен байланысамыз.")
    elif message.text == "Демеу":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "HR сұрақтары":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "Қарыздар бойынша сұрақтар":
        branch = get_branch(message.chat.id)
        if branch == "Центральный Аппарат":
            markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            markup_faq = generate_buttons(branches[1:], markup_faq)
            bot.send_message(message.chat.id, "Филиалды таңдаңыз", reply_markup=markup_faq)
        elif branch in branches[1:]:
            bot.send_message(message.chat.id, f"Филиал {branch}\n\n"
                                              "Қарыздар бойынша сұрақтарды келесі байланыс нөміріне жіберуге болады")
            func_branch(bot, message, branch)
    elif message.text == "Сатып алу қызметі бойынша сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_activities:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "Сатып алу порталы бойынша сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_portal:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    else:
        func_branch(bot, message, message.text)


def func_branch(bot, message, message_text):
    if message_text == "Корпоративный Университет":
        bot.send_message(message.chat.id, "Таспаева Гульшат Сериккалиевна\nФинансовый блок\nГлавный бухгалтер\n"
                                          "мобильный +7-701-780-64-34")
    elif message_text == "Дивизион Информационных Технологий":
        bot.send_message(message.chat.id, "Рысбеков Нуркен Алтынбаевич\nДепартамент финансового анализа и планирования"
                                          "\nВедущий экономист\nрабочий +7-727-398-91-53, мобильный +7-702-345-6292"
                                          "\n\nДусалиева Жанна Хабидуллаевна\nДепартамент финансового анализа и "
                                          "планирования\nВедущий специалист\nрабочий +7-727-398-91-49, "
                                          "мобильный +7-777-181-8919")
    elif message_text == "Дивизион по Корпоративному Бизнесу":
        bot.send_message(message.chat.id, "Уразбаев Ануар Талғатұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nВедущий экономист\n"
                                          "рабочий +7-727-244-70-54 мобильный +7-747-106-37-63\n\n"
                                          "Зинелов Әділет Маратұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nЭкономист\nрабочий +7-727-272-04-11 "
                                          "мобильный +7-707-315-55-59")
    elif message_text == "Дирекция Управления Проектами":
        bot.send_message(message.chat.id, "Шекенова Нургуль Жантасовна\nEX сектор\nEX operations\nрабочий "
                                          "+7-717-224-97-46 мобильный +7-747-403-82-92)")
    elif message_text == "Дирекция Телеком Комплект":
        bot.send_message(message.chat.id, "Рамазанқызы Айнұр\nОтдел экономики и финансов\nВедущий специалистn\n"
                                          "мобильный +7-777-241-2936")
    elif message_text == "Сервисная Фабрика":
        bot.send_message(message.chat.id, "Тезекбаев Максат Темирбековичn\nОтдел бюджетирования, экономики и финансов\n"
                                          "Ведущий экономист\nмобильный +7-708-694-75-40")
    elif message_text == "Дивизион по Розничному Бизнесу":
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = generate_buttons(drb_regions, markup_r)
        bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_r)
    elif message_text == 'Обьединение Дивизион "Сеть"':
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = generate_buttons(ods_regions, markup_r)
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
        bot.send_message(message.chat.id,
                         "Егер Сіз жұмыс барысында қауіпті факторды немесе жағдайды байқасаңыз, төмендегі сілтемеге "
                         "өтіп, сауалнаманы толтырыңыз:"
                         "\nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")
    elif message.text == "Жұмысты орындау тәртібі":
        bot.send_message(message.chat.id, "Егер Сіз жұмыстарды орындау кезінде мінез-құлық тәуекелдерін байқасаңыз, "
                                          "төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                        \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/"
                                          "viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз "
                         "/menu енгізу жолағының сол жағындағы командалар мәзірінен.")
    elif message.text == "Ұсыныстар | Идеялар":
        bot.send_message(message.chat.id,
                         "Егер Сізде ұсыныстар немесе идеялар болса, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:"
                         "\nhttps://docs.google.com/forms/d/e/"
                         "1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")


def instructions(bot, message):
    if message.text == "Логотиптер және Брендбук":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қазақтелеком АҚ")
        button2_i = types.KeyboardButton("Корпоративтік Университет")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Модемдер | Теңшеу":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("ADSL модемі")
        button2_i = types.KeyboardButton("IDTV консолі")
        button3_i = types.KeyboardButton("ONT модемдері")
        button4_i = types.KeyboardButton("Router 4G and Router Ethernet")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Lotus | Нұсқаулар":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Филиал серверлері бойынша деректер")
        button2_i = types.KeyboardButton("Lotus Орнату нұсқаулары")
        button3_i = types.KeyboardButton("Lotus орнату файлы")
        markup_instr.add(button1_i, button2_i, button3_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Checkpoint VPN | Қашықтан жұмыс":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("CheckPoint Орнату нұсқаулығы")
        button2_i = types.KeyboardButton("Checkpoint орнату файлы")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Жеке кабинет telecom.kz":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қызметті қалай төлеуге болады")
        button2_i = types.KeyboardButton("Төлем туралы мәліметтерді қалай көруге болады")
        button3_i = types.KeyboardButton("Қосылған қызметтерді қалай көруге болады")
        button4_i = types.KeyboardButton("'Менің Қызметтерім' Бөлімі")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Iссапар | Рәсімдеу тәртібі":
        bot.send_document(message.chat.id, document=open("files/Порядок оформления командировки.pdf", 'rb'))
    elif message.text == "Филиал серверлері бойынша деректер":
        bot.send_document(message.chat.id, document=open("files/Данные по всем lotus серверам.xlsx", 'rb'))
    elif message.text == "Lotus Орнату нұсқаулары":
        bot.send_document(message.chat.id, document=open("files/Инструкция по Lotus Notes на домашнем пк_.docx", 'rb'))
    elif message.text == "Lotus орнату файлы":
        bot.send_message(message.chat.id,
                         "Установочный файл Lotus Notes: "
                         "\nhttps://drive.google.com/drive/folders/1MrpjeXavmRnUMvYUiTcylhxAIEA6dvBb?usp=drive_link")
    elif message.text == "CheckPoint Орнату нұсқаулығы":
        bot.send_document(message.chat.id, document=open("files/Инструкция по установке CheckPoint.pdf", 'rb'))
    elif message.text == "Checkpoint орнату файлы":
        bot.send_document(message.chat.id, document=open("files/E85.40_CheckPointVPN.msi", 'rb'))
    elif message.text == "Қазақтелеком АҚ":
        bot.send_message(message.chat.id,
                         "'Қазақтелеком' АҚ логотиптерімен және брендбукімен қайдан танысуға болады\n"
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративтік Университет":
        bot.send_message(message.chat.id,
                         "Мұнда сіз Корпоративтік университеттің логотиптері мен брендбуктерін таба аласыз"
                         "\nhttps://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
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
    elif message.text == "Сатып алу порталы | Нұсқаулар":
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_kb = types.KeyboardButton("Бастамашылар | Нұсқаулар үшін")
        button2_kb = types.KeyboardButton("Хатшылар үшін | Нұсқаулар")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Нұсқаулықты таңдаңыз", reply_markup=markup_kb)
    elif message.text == "Бастамашылар | Нұсқаулар үшін":
        bot.send_message(message.chat.id, "https://youtu.be/RsNAa02QO0M")
        bot.send_document(message.chat.id, open("files/Инструкция по работе в системе Портал закупок 2.0.docx", "rb"))
    elif message.text == "Хатшылар үшін | Нұсқаулар":
        bot.send_message(message.chat.id, "Хатшыларға арналған нұсқаулар"
                                          "\nhttps://disk.telecom.kz/index.php/s/kc8PfD44Qw6X8jM")
        bot.send_message(message.chat.id, "Құпия сөз:\nsF21hOvUOp")


def kb(bot, message):
    if message.text == "🗃️Білім базасы":
        set_bool(message, False, False)
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_kb1 = types.KeyboardButton("Нұсқаулық базасы")
        button_kb2 = types.KeyboardButton("Глоссарий")
        button_kb3 = types.KeyboardButton("Пайдалы сілтемелер")
        button_kb4 = types.KeyboardButton("Реттеуші құжаттар")
        markup_kb.add(button_kb2, button_kb1, button_kb3, button_kb4)
        bot.send_message(message.chat.id, "Мобильді білім қорына қош келдіңіз!", reply_markup=markup_kb)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Мұнда сіз өзіңізге қажетті Bac нұсқаулығын таба аласыз немесе пайдалана аласыз "
                         "біз өзімізде қолданатын негізгі терминдер бойынша іздеу жүйесінің глоссарийі "
                         "компаниялар күн сайын.")
    elif message.text == "Нұсқаулық базасы":
        set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1_instr = types.KeyboardButton("Логотиптер және Брендбук")
        button2_instr = types.KeyboardButton("Жеке кабинет telecom.kz")
        button3_instr = types.KeyboardButton("Модемдер | Теңшеу")
        button4_instr = types.KeyboardButton("Lotus | Нұсқаулар")
        button6_instr = types.KeyboardButton("Checkpoint VPN | Қашықтан жұмыс")
        button7_instr = types.KeyboardButton("Iссапар | Рәсімдеу тәртібі")
        button8_instr = types.KeyboardButton("Сатып алу порталы | Нұсқаулар")
        markup_instr.add(button4_instr, button6_instr, button1_instr, button7_instr, button2_instr, button3_instr,
                         button8_instr)
        bot.send_message(message.chat.id, "Бұл жерде өзіңізге пайдалы нұсқаулықты таба аласыз.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Нұсқаулықты таңдау үшін санатты, содан кейін нұсқаулықтың "
                         "өзін мәзір-пернетақтадан таңдаңыз⌨️.")
    elif message.text == "Глоссарий":
        set_bool(message, False, True)
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
        set_bool(message, False, False)
        time.sleep(0.5)
        markup = useful_links()
        bot.send_message(message.chat.id, "Пайдалы сілтемелер", reply_markup=markup)
    elif message.text == "Реттеуші құжаттар":
        bot.send_document(message.chat.id, open("files/Регламент взаимодействия.doc", 'rb'))
        bot.send_document(message.chat.id, open("files/Порядок осуществления закупок.docx", "rb"))


def menu(bot, message):
    set_bool(message, False, False)
    markup = get_markup(message)
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)


def glossary(bot, message):
    text1 = f"Сіздің сұранысыңыз бойынша келесі мән табылды:"
    text2 = ("Бізге жақсы адам болуға көмектесіңіз!\nБіз сіздің пікіріңіз бен ұсыныстарыңызды күтеміз.\n\n"
             "Сіз бізге 'хабарлама Жазу' батырмасын басу немесе хат жіберу арқылы кері байланысыңызды жібере аласыз "
             "info.ktcu@telecom.kz.")
    button_text = "Аббревиатураны жазыңыз"
    common_file.glossary(bot, message, text1, text2, button_text)


def profile(bot, message):
    markup_ap = types.InlineKeyboardMarkup(row_width=1)
    button1_ap = types.InlineKeyboardButton("Атын Өзгерту", callback_data="Изменить Имя")
    button2_ap = types.InlineKeyboardButton("Тегін өзгерту", callback_data="Изменить Фамилию")
    button3_ap = types.InlineKeyboardButton("Телефон нөмірін өзгерту", callback_data="Изменить номер телефона")
    button4_ap = types.InlineKeyboardButton("Электрондық поштаны өзгерту", callback_data="Изменить email")
    button5_ap = types.InlineKeyboardButton("Табель нөмірін өзгерту", callback_data="Изменить табельный номер")
    button6_ap = types.InlineKeyboardButton("Филиалды өзгерту", callback_data="Изменить филиал")
    markup_ap.add(button1_ap, button2_ap, button3_ap, button4_ap, button5_ap, button6_ap)
    bot.send_message(message.chat.id, f"Сақталған ақпарат\n\n"
                                      f"Аты: {get_firstname(message)}\n"
                                      f"Тегі: {get_lastname(message)}\n"
                                      f"Телефон нөмірі: {get_phone_number(message)}\n"
                                      f"Email: {get_email(message)}\n"
                                      f"Табель нөмірі: {get_table_number(message)}\n"
                                      f"Филиалы: {get_branch(message.chat.id)}",
                     reply_markup=markup_ap)


def questions(bot, message):
    button_q = types.KeyboardButton("Менің өтініштерім")
    button_q1 = types.KeyboardButton("Өтінішті қалдыру")
    button_q2 = types.KeyboardButton("Жиі қойылатын сұрақтар")
    markup_q = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_q.add(button_q2, button_q1, button_q)
    bot.send_message(str(message.chat.id), "Бұл бөлімде сіз өзіңіздің өтінішіңізді қалдыра аласыз немесе жиі "
                                           "қойылатын сұрақтарға жауаптарды көре аласыз", reply_markup=markup_q)
    time.sleep(0.75)
    bot.send_message(message.chat.id,
                     "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")


def portal(bot, message):
    message_text = message.text
    if message_text == '🖥Портал "Бірлік"':
        markup_p = types.ReplyKeyboardMarkup(row_width=1)
        markup_p = generate_buttons(portal_bts, markup_p)
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
        bot.send_message(str(message.chat.id),
                         "IOS және Android жүйелеріндегі қызметкер порталына қалай кіруге болады | portal.telecom.kz"
                         "\nhttps://youtu.be/WJdS1aIBe1I",
                         reply_markup=markup_p)
    # elif message_text == portal_bts[3]:
    #     markup_p = types.ReplyKeyboardMarkup(row_width=1)
    #     markup_p = db_connect.generate_buttons(portal_guide, markup_p)
    #     bot.send_message(str(message.chat.id), "Сұрақты таңдаңыз", reply_markup=markup_p)
    elif message_text == portal_bts[2]:
        set_category(message, 'Портал "Бірлік"')
        appeal(bot, message, message_text)
    else:
        if checkpoint(bot, message, message_text):
            return
        check_portal_guide(bot, message, message_text, portal_guide)


def checkpoint(bot, message, message_text):
    if message_text == portal_bts[1]:
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


subscriber_types = ['Новый', 'Действующий']
lte_files = ["Инструкция 'Пилот LTE'", "Как подписать договор онлайн", "Скрипт на Алем",
             "Акт сдачи-приема выполненных работ", "Тарифы"]


def lte(message, bot, message_text=None):
    if message_text is None:
        message_text = message.text
    if message.text == lte_[0]:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_l = types.KeyboardButton(lte_[1])
        button2_l = types.KeyboardButton(lte_[2])
        button3_l = types.KeyboardButton(lte_[3])
        button4_l = types.KeyboardButton(lte_[4])
        markup_l.add(button1_l, button2_l, button3_l, button4_l)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_l)
    elif message.text == lte_[1]:
        bot.send_message(message.chat.id,
                         """
Представляем вам проект "Пилот LTE", нацеленный на укрепление нашей позиции на рынке и увеличение продаж в сегменте LTE. 

Наша цель
Достичь новых высот в продажах и увеличить нашу долю на растущем рынке LTE.

Длительность
до 31.12.2023 года.

Участники
 - по продаже услуг и «LTE», проект открыт для всех сотрудников структурных подразделений Дивизиона по розничному бизнесу АО "Казахтелеком", исключая участников ЕМП.
  - по доставке клиентского оборудования, проект открыт для всех сотрудников структурных подразделений Дивизиона по розничному бизнесу АО "Казахтелеком", исключая участников ЕМП, кроме работников канала продаж «УП» и работников Отдела управления внешними каналами продаж

Преимущество участия в проекте заключается в том, что вы сможете увеличить свой доход, получая следующие бонусы:
 - 2500 тенге за успешную продажу услуги LTE.
 - 1591 тенге за доставку и настройку модема и сим-карты.
 - 
Присоединитесь к "Пилоту LTE" и помогите нам достичь новых успехов на рынке, а также увеличить вашу прибыль. 

Вместе мы сможем добиться больших результатов!""")
    elif message.text == lte_[2]:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(lte_files[0])
        button2 = types.KeyboardButton(lte_files[1])
        button3 = types.KeyboardButton(lte_files[2])
        button4 = types.KeyboardButton(lte_files[3])
        button5 = types.KeyboardButton(lte_files[4])
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, "Выберите файл", reply_markup=markup)
    elif message_text == lte_[3]:
        id_ = add_internal_sale(str(message.chat.id))
        markup_lte = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_lte = generate_buttons(subscriber_types, markup_lte)
        msg = bot.send_message(message.chat.id, "Выберите тип абонента", reply_markup=markup_lte)
        bot.register_next_step_handler(msg, add_subscriber, bot, id_)
    elif message_text == lte_[4]:
        markup_a = db_connect.my_lte(message.chat.id)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Здесь вы можете отслеживать статусы ваших продаж",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Продаж не было")
    elif message_text == lte_files[0]:
        bot.send_document(message.chat.id, open('files/Инструкция Пилот LTE.pdf', 'rb'))
    elif message_text == lte_files[1]:
        bot.send_document(message.chat.id, open('files/Как подписать договор онлайн.pdf', 'rb'))
    elif message_text == lte_files[2]:
        bot.send_document(message.chat.id, open('files/Скрипт на Алем.docx', 'rb'))
        bot.send_document(message.chat.id, open('files/Скрипт на Алем.pdf', 'rb'))
    elif message_text == lte_files[3]:
        bot.send_document(message.chat.id, open('files/Акт сдачи-приема выполненных работ, '
                                                'оборудования и материалов.docx', 'rb'))
        bot.send_document(message.chat.id, open('files/Орындалған жұмыстарды, жабдықтар мен материалдарды қабылдау '
                                                'өткізу актісі.docx', 'rb'))
    elif message_text == lte_files[4]:
        bot.send_document(message.chat.id, open('files/Тарифы.pdf', 'rb'))


def add_subscriber(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in subscriber_types:
        markup_lte = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_lte = generate_buttons(subscriber_types, markup_lte)
        msg = bot.send_message(message.chat.id, "Выберите тип абонента из списка", reply_markup=markup_lte)
        bot.register_next_step_handler(msg, add_subscriber, bot, id_i_s)
        return
    set_subscriber_type(id_i_s, message.text)
    regions = get_regions()
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_l = generate_buttons(regions, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_region, bot, id_i_s, regions)


def get_region(message, bot, id_i_s, regions):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in regions:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_l = generate_buttons(regions, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите регион из списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_region, bot, id_i_s, regions)
        return
    performer_id = get_performer_id_by_category(message.text)
    set_category_i_s(id_i_s, message.text)
    set_performer_id_i_s(id_i_s, performer_id)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_l.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    msg = bot.send_message(message.chat.id,
                           "Абонент уведомлен о необходимости  предоставления следующих кодов/SMS работнику отдела CRM "
                           "и КС: \nкод для цифровых документов;\nSMS для верификации номера;\nкод для автоподписания "
                           "бланка заявления.", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_is_notified, bot, id_i_s)


def get_is_notified(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text != "Нет" and message.text != "Да":
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_l.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        msg = bot.send_message(message.chat.id, "Выберите варианты из предложенного списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_is_notified, bot, id_i_s)
        return
    is_notified = True
    if message.text == "Нет":
        is_notified = False
    set_is_notified(id_i_s, is_notified)
    msg = bot.send_message(message.chat.id, "Введите ФИО абонента")
    bot.register_next_step_handler(msg, get_full_name, bot, id_i_s)


def get_full_name(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_full_name(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите ИИН")
    bot.register_next_step_handler(msg, get_iin, bot, id_i_s)


def get_iin(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if not message.text.isdigit() or len(message.text) != 12:
        msg = bot.send_message(message.chat.id, "Введенная информация не соответствует шаблону ИИН, введите еще раз")
        bot.register_next_step_handler(msg, get_iin, bot, id_i_s)
        return
    set_iin(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите номер телефона")
    bot.register_next_step_handler(msg, get_phone_num_i_s, bot, id_i_s)


def get_phone_num_i_s(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    pattern = r'^(\+?7|8)(\d{10})$'
    if not re.match(pattern, message.text):
        msg = bot.send_message(message.chat.id, "Введенная информация не соответствует шаблону 87001110000")
        bot.register_next_step_handler(msg, get_phone_num_i_s, bot, id_i_s)
        return
    set_phone_num_subscriber(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите адрес абонента")
    bot.register_next_step_handler(msg, get_address_subscriber, bot, id_i_s)


def get_address_subscriber(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_subscriber_address(id_i_s, message.text)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_l = generate_buttons(pp, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите ПП из списка", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_pp, bot, id_i_s)


delivery = ["Самостоятельно", "Силами другого подразделения"]
arr = ["Я продал!", "Я доставил!"]


def get_pp(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in pp:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(pp, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите ПП из списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_pp, bot, id_i_s)
        return
    set_product_name(id_i_s, message.text)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_l = generate_buttons(arr, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_l)
    bot.register_next_step_handler(msg, func_lte, bot, id_i_s)


def func_lte(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in arr:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(arr, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_l)
        bot.register_next_step_handler(msg, func_lte, bot, id_i_s)
        return
    if message.text == arr[0]:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(delivery, markup_l)
        set_action(id_i_s, "Продажа")
        msg = bot.send_message(message.chat.id, "Как будет осуществлена доставка?", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_delivery, bot, id_i_s)
    else:
        set_action(id_i_s, "Доставка")
        set_delivery(id_i_s, delivery[0])
        add_lte_appeal(bot, message, id_i_s)


def get_delivery(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in delivery:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(delivery, markup_l)
        msg = bot.send_message(message.chat.id, "Как будет осуществлена доставка?", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_delivery, bot, id_i_s)
        return
    set_delivery(id_i_s, message.text)
    add_lte_appeal(bot, message, id_i_s)


def get_simcard(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_simcard(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите серийный номер модема")
    bot.register_next_step_handler(msg, get_modem, bot, id_i_s)


def get_modem(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_modem(id_i_s, message.text)
    appeal_ = db_connect.get_appeal_by_lte_id(id_i_s)
    simcard = lteClass.get_simcard(id_i_s)
    lte_info = db_connect.get_sale(id_i_s)
    is_notified = "Да"
    if not lte_info[7]:
        is_notified = "Нет"
    text = f"\n\tФИО абонента: {lte_info[3]}\n" \
           f"\tИИН: {lte_info[4]}\n" \
           f"\tНомер телефона абонента: {lte_info[5]}\n" \
           f"\tТип абонента: {lte_info[6]}\n" \
           f"\tУведомлен? {is_notified}\n" \
           f"\tАдрес абонента: {lte_info[8]}\n" \
           f"\tПП: {lte_info[9]}\n" \
           f"\tДоставка: {lte_info[10]}" \
           f"\n\tSimcard: {simcard}\n" \
           f"\tМодем: {message.text}"
    set_appeal_text(appeal_[0], text)
    bot.send_message(message.chat.id, "Информация сохранена")
    appeal_info = get_appeal_by_id(appeal_[0])[0]
    text = performer_text(appeal_info, message)
    bot.send_message(appeal_info[7], "Информация по серийному номеру сим карты и модема добавлен")
    bot.send_message(appeal_info[7], text)


def add_lte_appeal(bot, message, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    lte_info = db_connect.get_sale(id_i_s)
    now = datetime.now() + timedelta(hours=6)
    now_updated = remove_milliseconds(now)
    is_notified = "Да"
    if not lte_info[7]:
        is_notified = "Нет"
    text = f"\n\tФИО абонента: {lte_info[3]}\n" \
           f"\tИИН: {lte_info[4]}\n" \
           f"\tНомер телефона абонента: {lte_info[5]}\n" \
           f"\tТип абонента: {lte_info[6]}\n" \
           f"\tУведомлен? {is_notified}\n" \
           f"\tАдрес абонента: {lte_info[8]}\n" \
           f"\tПП: {lte_info[9]}\n" \
           f"\tДействие: {lte_info[14]}\n" \
           f"\tДоставка: {lte_info[10]}"
    if lte_info[10] == "Самостоятельно":
        text += f"\n\tSimcard: {is_none(lte_info[11])}\n" \
                f"\tМодем: {is_none(lte_info[12])}"

    appeal_id = add_appeal(message.chat.id, 'Обращение принято', lte_info[13], text, now_updated,
                           now_updated,
                           lte_info[2], ' ', False, id_i_s)
    text = get_appeal_text_all(appeal_id)
    bot.send_message(lte_info[2], text)
    bot.send_message(message.chat.id, "Ваша информация сохранена")


def is_none(line):
    if line is None:
        return " "
    return line


def redirect(bot, message, id_i_s):
    text = message.text
    if text == "/menu":
        delete_internal_sale(id_i_s)
        menu(bot, message)
        return True
    elif text == "/start":
        delete_internal_sale(id_i_s)
        send_welcome_message(bot, message)
        return True
    return False
