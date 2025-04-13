import aiosqlite

DB_NAME = "movies.db"

async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            genre_key TEXT,
            genre_name TEXT
        );
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            genre_key TEXT,
            movie_name TEXT
        );
        CREATE TABLE IF NOT EXISTS series_genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            genre_key TEXT,
            genre_name TEXT
        );
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            genre_key TEXT,
            series_name TEXT
        );
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT
        );
        """)
        await db.commit()

async def insert_data():
    movie_genres = {
    "uz": {
        "action": "Jangari Kinolar",
        "crime": "Kriminal kinolar",
        "comedy": "Komediya Kinolar",
        "drama": "Drama Kinolar",
        "horror": "Qo`rqinchli Kinolar",
        "detective": "Detektiv kinolar",
        "melodrama": "Melodrama Kinolar",
        "adventures": "Sarguzasht Kinolar",
        "romantic": "Romantik Kinolar",
        "fantasy": "Fantastik Kinolar",
        "historical": "Tarixiy Kinolar",
        "zombi": "Zombi Kinolar",
        "marvel": "Marvel"
    },
    
    "ru": {
        "action": "Боевики",
        "crime": "Криминальный",
        "comedy": "Комедии",
        "drama": "Драмы",
        "horror": "Ужасы",
        "detective": "Детектив",
        "melodrama": "Мелодрама",
        "adventures": "Приключения",
        "romantic": "Романтические",
        "fantasy": "Фантастические",
        "historical": "Исторические",
        "zombi": "Зомби",
        "marvel": "Марвел"
    },

    "en": {
        "action": "Action Movies",
        "crime": "Crime Movies",
        "comedy": "Comedy Movies",
        "drama": "Drama Movies",
        "horror": "Horror Movies",
        "detective": "Detective Movies",
        "melodrama": "Melodrama Movies",
        "adventures": "Adventures Movies",
        "romantic": "Romantic Movies",
        "fantasy": "Fantasy Movies",
        "historical": "Historical Movies",
        "zombi": "Zombi Movies", 
        "marvel": "Marvel"
    },
  
}
    movie_list = {
    "uz": {
        "action": ["Telba Max - https://uzmovi.tv/tarjima-kinolarri/6287-telba-aqlsiz-maks-max-furiosa-dostoni-uzbek-ozbek-tilida.html", "Jon Uik - http://asilmedia.org/7189-jon-uik-uzbek-ozbek-tilida-tas-ix-skachat-download.html","O`qdan tez - http://asilmedia.org/14491-oqdan-tez-tezkor-oqlar-bred-pitt-ishtirokida-uzbek-tilida-2022-ozbekcha-tarjima-film-full-hd-skachat.html","Betman Qora ritser - http://asilmedia.org/8580-betmen-jokerga-qarshi-qora-ritsar-temnyy-rycar-betmen-protiv-dzhokera-hd-uzbek-ozbek-tilida-tas-ix-skachat-download.html","Gladiator - http://asilmedia.org/7922-gladiator-uzbek-ozbek-tilida-tas-ix-skachat-download.html","Muqqadima - https://asilmedia.org/10761-muqaddima-uzbek-tilida-2010-ozbek-tarjima-kino-hd.html"],
        "crime": ["Gentelmanlar - https://uzmovii.com/tarjima-kinolar/126-jentelmenlar-uzbek-tilida.html","U.N.C.L.E. agentlari - http://asilmedia.org/8362-ankl-agentlari-agenty-ankl-uzbek-ozbek-tilida-tas-ix-skachat-download.html","Jango - http://asilmedia.org/10979-ozod-jango-uzbek-tilida-2012-ozbekcha-tarjima-kino-hd.html"," hurmatsiz urush vazirligi - https://uzbeklar.tv/8921-nojentelmencha-ishlar-vazirligi.html",
        "chandig' yuz - https://m.ok.ru/video/6692364618463","Cho`qintirgan ota - https://yandex.ru/video/preview/12097537868097486232", "Rango - http://asilmedia.org/13137-rango-uzbek-tilida-multfilm-2011-ozbek-tarjima-kino-hd.html", "Oushenning 11 do'sti - http://asilmedia.org/12590-oushenning-11-dosti-uzbek-tilida-2001-ozbekcha-tarjima-kino-hd.html", "Oushenning 12 do`sti - https://yandex.ru/video/preview/16777860511480528578", "Oushenning 13 do`sti - https://yandex.ru/video/preview/15550270963068814589 "],
        "comedy": ["Ajoyib dostlar - https://yandex.ru/video/preview/10235573619305627702", "Tig`iz payt - http://asilmedia.org/2673-tigiz-payt-chas-pik.html","Ahmoqdan ahmoqroq - https://yandex.ru/video/preview/5240208174658768640","Birodarlar - https://yandex.ru/video/preview/16829949076606585980", "Ko`rkam va semiz  - https://yandex.ru/video/preview/1736019921186315022", "Ace Ventura - http://asilmedia.org/7912-eys-ventura-super-komediya-uzbek-ozbek-tilida-tas-ix-skachat-download.html", "Niqob - http://asilmedia.org/10008-niqob-uzbek-tilida-1994-hd-ozbek-tarjima-tas-ix-skachat.html"],
        "drama": ["Showshankdan Qochish - https://asilmedia.org/7540-shoushenkdan-qochsih-uzbek-ozbek-tilida-tas-ix-skachat-download.html", "Forrest Gump - https://kinolar.tv/load/komedija/forrest_gamp_uzbek_tilida_1994_kino_skachat_fhd/17-1-0-5107", "Qoidalarsiz o'yin - http://asilmedia.org/11423-qoidalarsiz-oyin-girrom-oyin-uzbek-tilida-2010-ozbekcha-tarjima-kino-hd.html", "yashil maskan - https://yandex.ru/video/preview/14249570244539021863", "Metin Iroda ovi - https://yandex.ru/video/preview/16491320964520153494", "Shindler ro'yxati - https://yandex.ru/video/preview/10833520297864770630", "Baxt izlab - https://yandex.ru/video/preview/8775926908991309239"],
        "horror": ["Lanat - https://yandex.ru/video/preview/1645476799433543386", "Ono - http://asilmedia.org/10770-u-u-1-ono-1-ozbekcha-subtitr-uzbek-tilida-2017-ozbek-tarjima-kino-hd.html", "Exorcist - http://asilmedia.org/15250-ekzorsist-vatikan-jin-chiqaruvchisi-ujas-kino-uzbek-tilida-2023-ozbekcha-tarjima-kino-hd.html",  " Babaduk - https://yandex.ru/video/preview/2788913059885672821", "Astral - https://yandex.ru/video/preview/3203663039931224226", "Sinister dahshati - https://uzmovi.co/tarjima-kinolar/1082-sinister-1-uzbek-tilida.html"],
        "detective": ["Sherlok Xolms - https://asilmedia.org/7732-sherlok-holms-uzbek-ozbek-tilida-tas-ix-skachat-download.html", "Yetti - http://asilmedia.org/15841-yetti-se7en-uzbek-tilida-1995-ozbekcha-tarjima-kino-hd.html", "Turist - http://asilmedia.org/9590-turist-ozbek-tilida-2010-uzbekcha-tarjima-turist-the-tourist-tas-ix-skachat.html","Tig`idan chiqqan Pichoqlar - https://yandex.ru/video/preview/3140119434558002749", "Old boy - http://asilmedia.org/12306-oldboy-uzbek-tilida-2003-ozbekcha-tarjima-kino-hd.html", "Asiralar - https://yandex.ru/video/preview/17691507523491699988 ", "Parazitlar - https://yandex.ru/video/preview/13235961790498591313"], 
        "melodrama": ["Titanik - http://kinolaruz.ru/films/tarjima_kinolar/9516-titanik-uzbekcha-tarjima-1997-ozbek-tilida-titanik-titanic-tas-ix-skachat.html", "Xotira kundaligi - https://yandex.ru/video/preview/136725144904590379", "Janob va Xonim smit - https://yandex.ru/video/preview/2457399387001541533","Tanishing Joe Black - https://yandex.ru/video/preview/17948082466725053144", "sizdan oldingi hayotim - http://asilmedia.org/10756-sen-bilan-uchrashguncha-uzbek-tilida-2016-ozbek-tarjima-kino-hd.html","Romeo va Julieta - https://yandex.ru/video/preview/12843887855521099112", "Arvoh - https://yandex.ru/video/preview/8066443198876726868", "mening qizim - https://yandex.ru/video/preview/16407352390098880157"],
        "adventures": ["Indiana Jones - https://yandex.ru/video/preview/16330929273905173469", "Karib Dengizi Qaroqchilari - https://yandex.ru/video/preview/12542628625363550149", "Jumanji - http://asilmedia.org/2179-jumanji-2-jungle-chorlaydi-premyera.html", "Mr Bin sayohatda - https://yandex.ru/video/preview/2534396966292719590 ", "Ekipaj - https://uzbeklar.tv/1900-ekipaj.html"],
        "romantic": ["Mag'rurlik va Xurofot - https://yandex.ru/video/preview/9088161923029610950", "La La Land - http://asilmedia.org/8478-la-la-lend-zheleznyy-chelovek-3-uzbek-ozbek-tilida-tas-ix-skachat-download.html","Yulduzlar Aybi - https://yandex.ru/video/preview/17276876668447674446","Noting Hill - https://yandex.ru/video/preview/15200152430813361107"," Men Sizdan Nafratlanadigan 10 Narsa - https://yandex.ru/video/preview/7971243644093620662", "Asl Sevgi - http://asilmedia.org/7448-asl-sevgi-uzbek-ozbek-tilida-tas-ix-skachat-download.html", "Benjamin Button - https://uzmovii.org/tarjima-kinolar/5443-benjamin-buttonning-qiziq-voqeasi-uzbek-tilida.html"],
        "fantasy": ["Uzuklar Humdori - https://asilmedia.org/4349-uzuklar-hukmdori-1-ozbek-tilida.html", "Garri Potter - http://asilmedia.org/9060-garri-potter-1-hikmatlar-toshi-uzbek-tarjima-2001-hd-ozbek-tilida-tas-ix-skachat.html", "Narniya Saltanati - https://yandex.ru/video/preview/7015118863288643731","Alisa mojizalar mamlakatida - https://yandex.ru/video/preview/12202391922250238400", "Samoviy yo`l - https://yandex.ru/video/preview/12659530076485604669", "Pan labirint - https://yandex.ru/video/preview/1216798461472116672", "Xobbit - http://asilmedia.org/3242-hobbit-ozbek-tilida.html", "Persi Jekson - https://yandex.ru/video/preview/14563292618104779272","labirintdagilar - https://yandex.ru/video/preview/11183099952095180430"],
        "historical": ["Sher yurak - https://yandex.ru/video/preview/13874830699191377098", "Troya - http://asilmedia.org/8396-troya-troya-full-hd-uzbek-ozbek-tilida-tas-ix-skachat-download.html", "Kolovrat afsonasi - https://yandex.ru/video/preview/9401807074145557352", "Qirol Arturning qilichi - https://yandex.ru/video/preview/8902174865404653965", "Pianinachi - https://tas-ix.media/films/melodrama/7551-pianist.html"],
        "zombi": ["Z jahon urushi - https://yandex.ru/video/preview/17869777242893002046", "Yovuzlik maskani - https://yandex.ru/video/preview/16851678046823618734", "Pusanga  ketyotgan poyezd - https://yandex.ru/video/preview/1058089952645602086", "28 kundan keyin - https://yandex.ru/video/preview/207721904695828637", "O`liklar tongi - https://yandex.ru/video/preview/16160611712617596589",  "Zombilend - https://yandex.ru/video/preview/9861466346593021887", "O‘liklar armiyasi - https://yandex.ru/video/preview/10916926107580855028","Men afsonaman - https://yandex.ru/video/preview/5671921437243688738", "SHon ismli zombi - http://asilmedia.org/12239-shon-ismli-zombi-uzbek-tilida-2004-ozbekcha-tarjima-kino-hd.html"],
        "marvel": [ "Qasoskorlar Yakun - https://ok.ru/video/1278204316359","Qasoskorlar Cheksizlik urushi - https://yandex.ru/video/preview/4048007840551386363","Temir odam - https://uzmoviy.org/3281-temir-odam-1-uzbek-tilida.html","Qasoskorlar - https://ok.ru/video/1278204316359", "Kapitan Amerika - https://uzmovie.net/kino/tarfilm/5635-birinchi-qasoskor-1-kapitan-amerika-1-uzbek-tilida-2011.html", "Qora Pantera - https://uzmovi.bot/tarjima-kinolar/532-qora-qoplon-qora-pantera-uzbek-tilida.html","Tor Ragnarok - https://uzmoviy.org/3294-tor-3-ragnarok-uzbek-tilida.html","O'rgimchak odam Uydan uzoqda - http://asilmedia.org/8379-orgimchak-odam-uydan-uzoqda-chelovek-pauk-vdali-ot-doma-uzbek-ozbek-tilida-tas-ix-skachat-download.html","Doktor Strange - https://uzmovii.com/tarjima-kinolar/2476-doktor-strenj-2-aqlsiz-multiolam-uzbek-tilida.html"]
    },

    "ru": {
    "action": ["безумный Макс - http://yandex.ru/video/preview/12034942780454102348","джон Уик - https://yandex.ru/video/preview/10641844962732418263","быстрее пули - https://yandex.ru/video/preview/6153522411346263997","черный рыцарь Бетмана - https://yandex.ru/video/preview/2608680403987910967","гладиатор - https://yandex.ru/video/preview/2414603818404336508","начало - https://yandex.ru/video/preview/15093385460223896238"],
    "crime": ["джентльмены - https://gs.yandex.com.tr/video/preview/17819407072991987256","тренировочный день - https://yandex.ru/video/preview/7159021825940912955","агенты А.Н.К.Л. - https://yandex.ru/video/preview/7279781807746823381","джанго освобожденный - https://yandex.ru/video/preview/11709251018688485847","министерство неджентльменской войны - https://yandex.ru/video/preview/523427015548618537","лицо со шрамом - https://yandex.ru/video/preview/6533275534218334170","крёстный отец - https://yandex.ru/video/preview/7258750674900658372","ранго - https://yandex.ru/video/preview/18277364762141317136","одиннадцать друзей Оушена - https://yandex.ru/video/preview/3751495479645036652","двенадцать друзей Оушена - https://yandex.ru/video/preview/4299694579810320961","тринадцать друзей Оушена - https://yandex.ru/video/preview/6211305443910286383"],
    "comedy": ["мальчик в вегасе - https://yandex.ru/video/preview/10235573619305627702","superПерцы - https://yandex.ru/video/preview/8730584173425568302","час пик - https://yandex.ru/video/preview/16560468121289408783","тупой ещё тупее - https://yandex.ru/video/preview/14520068193249061166","сводные братья - https://yandex.ru/video/preview/16829949076606585980","мачо и ботан - https://yandex.ru/video/preview/1736019921186315022","эйс вентура - https://yandex.ru/video/preview/8402094611903032656","маска - https://yandex.ru/video/preview/16577272776041814523"],
    "drama": ["побег из шоушенка - https://yandex.ru/video/preview/16281330000920821396","форрест гамп - https://yandex.ru/video/preview/286161629633046129","крестный отец - https://yandex.ru/video/preview/7258750674900658372","игры разума - https://yandex.ru/video/preview/8205493610281887211","зелёная миля - https://yandex.ru/video/preview/5503041099233749159","умница Уилл Хантинг - https://yandex.ru/video/preview/7068238162444269956","список шиндлера - https://yandex.ru/video/preview/1747846058158849525","в поисках счастья - https://yandex.ru/video/preview/6875455071189281063"],
    "horror": ["проклятие - https://yandex.ru/video/preview/16789063793990413949","оно - https://yandex.ru/video/preview/13601113100241636869","ужас на улице Вязов - https://yandex.ru/video/preview/11142835794257013205","экзорцист - https://yandex.ru/video/preview/7014508484003974921","реинкарнация - https://yandex.ru/video/preview/16778655416784443214","бабадук - https://yandex.ru/video/preview/11073019934273019617","астрал  - https://yandex.ru/video/preview/2491590929854220076","синистер  - https://yandex.ru/video/preview/6644946582230537249"],
    "detective": ["шерлок холмс - https://yandex.ru/video/preview/15793541728329115914","семь - https://yandex.ru/video/preview/307086500442259807","турист - https://yandex.ru/video/preview/8590670155744106330","достать ножи - https://yandex.ru/video/preview/14906436005183366061","исчезнувшая - https://yandex.ru/video/preview/7547630591646287521","олдбой - https://yandex.ru/video/preview/4110829553826744794","пленницы - https://yandex.ru/video/preview/2747402130202894414","паразиты - https://yandex.ru/video/preview/3246945268619132565"],
    "melodrama": ["титаник - https://yandex.ru/video/preview/12685761475569912191","дневник памяти - https://yandex.ru/video/preview/2310616134923302127","мистер и миссис смит - https://yandex.ru/video/preview/2353269466624609524","знакомьтесь, джо блэк - https://yandex.ru/video/preview/15929178578549142347","звезда родилась - https://yandex.ru/video/preview/205116134661761565","до встречи с тобой - https://yandex.ru/video/preview/4311312537361631611","ромео и джульетта - https://yandex.ru/video/preview/12843887855521099112","призрак - https://yandex.ru/video/preview/8066443198876726868","моя девочка - https://yandex.ru/video/preview/6568658603939062084"],
    "adventures": ["индиана джонс - https://yandex.ru/video/preview/1465286013999443512","пираты карибского моря - https://yandex.ru/video/preview/2484618363851037162","джуманджи - https://yandex.ru/video/preview/12581397459883651274","мистер бин на отдыхе - https://yandex.ru/video/preview/9701536745634806876","джанго освобожденный - https://yandex.ru/video/preview/11709251018688485847","экипаж - https://yandex.ru/video/preview/1181983750134664029"],
    "romantic": ["гордость и предубеждение - https://yandex.ru/video/preview/699521713314786762","ла ла ланд - https://yandex.ru/video/preview/9909980561903561788","виноваты звёзды - https://yandex.ru/video/preview/1029374615191832428","ноттинг-хилл - https://yandex.ru/video/preview/12162102337876979936","10 вещей, которые я ненавижу в тебе - https://yandex.ru/video/preview/7971243644093620662","настоящая любовь - https://yandex.ru/video/preview/15464780081932162155","бенжамин буттон - https://yandex.ru/video/preview/11337546526107439557"],
    "fantasy": ["властелин колец - https://yandex.ru/video/preview/5753178030029492832","гарри поттер - https://yandex.ru/video/preview/8941262572811513554","королевство нарния - https://yandex.ru/video/preview/6637898489663527616","алиса в стране чудес - https://yandex.ru/video/preview/12202391922250238400","звездная пыль - https://yandex.ru/video/preview/12123862917419392420","лабиринт пан - https://yandex.ru/video/preview/1216798461472116672","хоббит - https://yandex.ru/video/preview/16037394492439347218","перси джексон - https://yandex.ru/video/preview/15476031515185226004","бегущий в лабиринте - https://yandex.ru/video/preview/14678305615702676294"],
    "historical": ["храброе сердце - https://yandex.ru/video/preview/17626069744554894332","легенда о коловрате - https://yandex.ru/video/preview/8573487150705546451","троя - https://yandex.ru/video/preview/6014418215683103824","меч короля артура - https://yandex.ru/video/preview/12865077344509724747", "пианист - https://yandex.ru/video/preview/3854469823757622944"],
    "zombi": ["война миров z - https://yandex.ru/video/preview/15834093964777652438","обитель зла - https://yandex.ru/video/preview/12725293418865249480","поезд в пусан - https://yandex.ru/video/preview/1058089952645602086","28 дней спустя - https://yandex.ru/video/preview/207721904695828637","рассвет мертвецов - https://yandex.ru/video/preview/16160611712617596589","добро пожаловать в зомбилэнд - https://yandex.ru/video/preview/9861466346593021887","армия мертвецов - https://yandex.ru/video/preview/10276233339808130409","я легенда - https://yandex.ru/video/preview/16909271728467165316","зомби по имени шон - https://rutube.ru/video/7c9cb3c368ac4ed828e769316b4a91b0/"],
    "marvel": ["мстители финал - https://rutube.ru/video/6411d33b66a9bde84eb5435ebb12e022/","мстители война бесконечности - https://rutube.ru/video/13ab8d24ce9e9c8119b4d67af9daf482/","железный человек - https://rutube.ru/video/aacd1dbe5fbb1a808257060c0436a80e/","мстители - https://rutube.ru/video/e7fa3f8316733b04210c53a801af38e0/","капитан америка - https://rutube.ru/video/d1a9b4df10b643ac96719e082b563ff9/","чёрная пантера - https://rutube.ru/video/a65af08047f9d37b59557a54767b4b5e/","тор рагнарёк - https://rutube.ru/video/548511b3d6154aacd1577cf58550ef3f/","человек-паук: вдали от дома - https://rutube.ru/video/301cefc5161846ebf191870ef69f69a9/","доктор стрэндж - https://rutube.ru/video/336c4d7aaebc8f56b8af55d082ac4388/"]
    
},
    "en": {
        "action": ["Mad Max - https://inoriginal.net/films/234-mad-max-fury-road-2015.html " ,"John Wick - https://inoriginal.net/films/460-john-wick-2014.html", "Bullet Train - https://inoriginal.net/films/715-bullet-train-2022.html","The Dark Knight - https://inoriginal.net/films/397-the-dark-knight-2008.html","Gladiator - https://inoriginal.net/films/1346-gladiator-2000.html","Inception - https://inoriginal.net/films/206-inception-2010.html"],
        "crime": ["Gentelman - https://www.imdb.com/title/tt8367814/?ref_=ext_shr_lnk","Trainin day - https://inoriginal.net/films/1798-training-day-2001.html","The Man from U.N.C.L.E. - https://inoriginal.net/films/659-the-man-from-u-n-c-l-e-2015.html","Django - https://inoriginal.net/films/149-django-unchained-2012.html","ministry of ungentlemanly warfare - https://www.imdb.com/title/tt5177120/?ref_=ext_shr_lnk","scarface - https://inoriginal.net/films/961-scarface-1983.html","The Godfather - https://inoriginal.net/films/609-the-godfather-1972.html","Rango - https://inoriginal.net/films/140-rango-2011.html", "Ocean eleven - https://inoriginal.net/films/781-ocean-s-eleven-2001.html", "Ocean twelve - https://inoriginal.net/films/2120-ocean-s-twelve-2004.html", "Oceans thirteen - https://inoriginal.net/films/2283-ocean-s-thirteen-2007.html" ],
        "comedy": ["The Hangover - https://inoriginal.net/films/1927-the-hangover-2009.html", "Superbad - https://inoriginal.net/films/1175-superbad-2007.html", "Rush Hour - https://inoriginal.net/films/846-rush-hour-1998.html","Dumb and Dumber - https://inoriginal.net/films/907-dumb-and-dumber-1994.html", "Step Brothers - https://www.imdb.com/title/tt0838283/?ref_=ext_shr_lnk", "21 Jump Street - https://inoriginal.net/films/1606-21-jump-street-2012.html", "Ace Ventura - https://inoriginal.net/films/2009-ace-ventura-pet-detective-1993.html", "Mask - https://inoriginal.net/films/428-the-mask-1994.html"],
        "drama": ["The Shawshank Redemption - https://inoriginal.net/films/799-the-shawshank-redemption-1994.html", "Forrest Gump - https://inoriginal.net/films/166-forrest-gump-1994.html", "A Beautiful Mind - https://inoriginal.net/films/54-a-beautiful-mind-2001.html", "The Green Mile - https://inoriginal.net/films/413-the-green-mile-1999.html", "Good Will Hunting - https://inoriginal.net/films/650-good-will-hunting-1997.html", "Schindler’s List - https://www.imdb.com/title/tt0108052/?ref_=ext_shr_lnk", "The Pursuit of Happyness - https://inoriginal.net/films/797-the-pursuit-of-happyness-2006.html","Scent of a Woman - https://inoriginal.net/films/333-scent-of-a-woman-1992.html"],
        "horror": ["The Conjuring - https://inoriginal.net/films/841-the-conjuring-2013.html", "It - https://www.imdb.com/title/tt1396484/?ref_=ext_shr_lnk ", "A Nightmare on Elm Street - https://www.imdb.com/title/tt1179056/?ref_=ext_shr_lnk", "The Exorcist - https://www.imdb.com/title/tt5368542/?ref_=ext_shr_lnk", "Hereditary - https://inoriginal.net/films/818-hereditary-2018.html", "The Babadook - https://inoriginal.net/films/2292-the-babadook-2014.html", "Insidious - https://inoriginal.net/films/2567-insidious-2010.html", "Sinister - https://inoriginal.net/films/4581-sinister-2-2015.html"],
        "detective": ["Sherlock Holmes - https://inoriginal.net/films/662-sherlok-holmes-2009.html", "Seven - https://www.imdb.com/title/tt0114369/?ref_=ext_shr_lnk", "Tourist - https://inoriginal.net/films/990-the-tourist-2010.html", "Knives Out - https://inoriginal.net/films/224-knives-out-2019.html", "Gone Girl - https://inoriginal.net/films/1327-gone-girl-2014.html", "Old Boy - https://www.imdb.com/title/tt0364569/?ref_=ext_shr_lnk", "Prisoners - https://inoriginal.net/films/952-prisoners-2013.html", "Parasite - https://www.imdb.com/title/tt6751668/?ref_=ext_shr_lnk"],
        "melodrama": ["Titanic - https://inoriginal.net/films/445-titanik.html", "The Notebook - https://inoriginal.net/films/960-the-notebook-2004.html", " Mr & Mrs smith - https://inoriginal.net/films/258-mr-and-mrs-smith-2005.html", "Meet Joe Black - https://inoriginal.net/films/242-meet-joe-black-1998.html", "A Star is Born - https://inoriginal.net/films/472-a-star-is-born-2018.html", "Me before you - https://inoriginal.net/films/684-me-before-you-2016.html", "Romeo and Juliet - https://inoriginal.net/films/88-romeo-and-juliet-1996.html", "Ghost - https://inoriginal.net/films/172-ghost-1990.html", "My girl - https://www.imdb.com/title/tt0102492/?ref_=ext_shr_lnk"],
        "adventures": ["Indiana Jones - https://inoriginal.net/films/1756-indiana-jones-and-the-temple-of-doom-1984.html", "Pirates of the Caribbean - https://inoriginal.net/films/278-pirates-of-the-caribbean-the-curse-of-the-black-pearl-2003.html", "Jumanji - https://inoriginal.net/films/595-jumanji-welcome-to-the-jungle-2017.html"," Mr Been Holiday -  https://youtu.be/hSxLUd8aly4?si=dMlC573D_H6Y76TU","The crew -  https://youtu.be/TrGuYJX2tYM?si=mlX0XYDYgPTXG0eM" ],
        "romantic": ["Pride and Prejudice - https://www.imdb.com/title/tt0414387/?ref_=ext_shr_lnk", "La La Land - https://www.imdb.com/title/tt3783958/?ref_=ext_shr_lnk", "The FaultStars in Our  -  https://www.imdb.com/title/tt2582846/?ref_=ext_shr_lnk","Notting Hill - https://inoriginal.net/films/2073-notting-hill-1999.html", "10 Things I Hate About You - https://inoriginal.net/films/25-10-prichin-moej-nenavisti.html", "Love Actually - https://inoriginal.net/films/2267-love-actually-2003.html", "Benjamin Button - https://inoriginal.net/films/783-the-curious-case-of-benjamin-button-2008.html"],
        "fantasy": ["The Lord of the Rings - https://inoriginal.net/films/424-the-lord-of-the-rings-the-fellowship-of-the-ring-2001.html", "Harry Potter - https://inoriginal.net/films/189-harry-potter-and-the-sorcerer-s-stone-2001.html", "The Chronicles of Narnia - https://inoriginal.net/films/627-the-chronicles-of-narnia-the-lion-the-witch-and-the-wardrobe-2005.html", "Alice in Wonderland - https://inoriginal.net/films/305-alice-in-wonderland-2010.html", "Stardust - https://inoriginal.net/films/747-stardust-2007.html", "Pan’s Labyrinth - https://www.imdb.com/title/tt0457430/?ref_=ext_shr_lnk", "The Hobbit - https://inoriginal.net/films/408-the-hobbit-an-unexpected-journey-2012.html", "Percy Jackson - https://inoriginal.net/films/1514-percy-jackson-and-the-olympians-the-lightning-thief-2010.html", "Maze Runner - https://inoriginal.net/films/437-the-maze-runner-2014.html"],
        "historical": ["Braveheart - https://inoriginal.net/films/114-braveheart-1995.html", "Troy - https://inoriginal.net/films/640-troy-2004.html", "King Arthur: Legend of the sword - https://inoriginal.net/films/1329-king-arthur-legend-of-the-sword-2017.html", "The pianists - https://inoriginal.net/films/794-the-pianist-2002.html"],
        "zombi": [  "World War Z - https://inoriginal.net/films/355-world-war-z-2013.html","Resident Evil - https://inoriginal.net/films/106-resident-evil-apocalypse-2004.html","28 Days Later - https://inoriginal.net/films/31-28-days-later-2002.html","Dawn of the Dead - https://inoriginal.net/films/1181-dawn-of-the-dead-2004.html","Zombieland - https://inoriginal.net/films/696-zombieland-2009.html","Army of the Dead - https://inoriginal.net/films/73-army-of-the-dead-2021.html","I Am Legend - https://inoriginal.net/?story=I+Am+Legend&do=search&subaction=search","Shaun of the Dead - https://www.imdb.com/title/tt0365748/"],
        "marvel": ["Avengers Endgame - https://inoriginal.net/films/78-avengers-endgame-2019.html","Avengers Infinity War - https://inoriginal.net/films/79-avengers-infinity-war-2018.html","Iron Man - https://inoriginal.net/films/211-iron-man-2008.html","The Avengers - https://inoriginal.net/films/389-the-avengers-2012.html","Captain America - https://inoriginal.net/films/769-captain-america-the-first-avenger-2011.html","Black Panther - https://inoriginal.net/films/777-black-panther-2018.html","Thor Ragnarok - https://inoriginal.net/films/1677-thor-ragnarok-2017.html", "SpiderMan Far From Home - https://inoriginal.net/films/482-spider-man-far-from-home-2019.html","Doctor Strange - https://inoriginal.net/films/1660-doctor-strange-2016.html"]
    },

}

    series_genres = {
    "uz":{
        "Crime/Thriller": "Jinoyat/Triller",
        "Sci-Fi/Fantasy": "Fantastika",
        "Comedy": "Komediya",
        "Drama": "Drama",
        "K-drama": "K-drama"
    },

    "ru": {
        "Crime/Thriller": "Криминал/Триллер",
        "Sci-Fi/Fantasy": "Фантастика",  
        "Comedy": "Комедия",
        "Drama": "Драмы",
        "K-drama": "К-Драмы"
    },

    "en": {
        "Crime/Thriller": "Crime/Thriller",
        "Sci-Fi/Fantasy": "Sci-Fi/Fantasy",
        "Comedy": "Comedy",
        "Drama": "Drama",
        "K-drama": "K-drama"
    }
}   
  

    series_list = {
    "uz": {
        "Crime/Thriller": ["Mashaqqatlar sari - https://topkino.me/serial/2199-mashaqqatlar-sari.html", "Yaxshisi Saulga qo‘ng‘iroq qiling - https://kinok.net/shows/yaxshisi-soulga-qongiroq-qiling-better-call-saul/1-qism/714", "Narkos - https://rutube.ru/plst/337759/", "Shelbilar oilasi - http://asilmedia.org/11211-shelbilar-oilasi-otkir-viqorlilar-uzbek-tilida-barcha-qismlar-britaniya-seriali-ozbek-tilida-2013-ozbekcha-tarjima.html", 
        "Qog‘oz bino - http://asilmedia.org/13561-qogozdan-yasalgan-uy-netflix-ispaniya-seriali-barcha-qismlar-ozbek-tilida-2017-2022-uzbekcha-tarjima.ht","Kartalar uyi - https://rutube.ru/plst/385210/", "Panjara ortida - http://asilmedia.org/5687-panjara-ortida-pobeg-iz-tyurmy-prison-break-fasl-1-qismlar-1-22-jami-22.html", "Dexter - https://kinok.net/shows/dekster-dexter/2-qism/166", "Gentelmenlar - https://rutube.ru/plst/380420/", "Reacher - https://rutube.ru/plst/350617/"],
        "Sci-Fi/Fantasy": ["Taxtlar o‘yini - http://asilmedia.org/10118-taxtlar-oyini-uzbek-tilida-barcha-qismlar-hd.html", "G‘alati ishlar - http://asilmedia.org/14988-ajabtovur-ishlar-galati-narsalar-seriali-barcha-qismlar-ozbek-tilida-2016-uzbekcha-tarjima.html", "Ajal o‘yini - https://uzmovii.com/serial/5981-ajal-oyini-barcha-qismlar-uzbek-tilida.html", "Yiggitlar - https://hdkinolar.org/serial/2588-yigitlar-1-2-3-4-5-6-7-8-9-10-qismlar-uzbek-tilida.html", "Loki - https://uzmovi.bot/tarjima-seriallar/1489-loki-barcha-qismlar-uzbek-tilida.html", 
        "Biz so‘ngilarmiz - http://asilmedia.org/14835-bizning-songimiz-seriali-barcha-qismlar-ozbek-tilida-2023-uzbekcha-tarjima.html", "Kalmalar o‘yini - https://uzmoovi.org/serial/3380-kalmar-oyini-1-fasl-barcha-qismlar-uzbek-tilida.html", "Ambrella akademiyasi - https://uzbeklar.tv/4580-ambrella-akademiyasi.html", "Biz barchamiz o`likmiz - http://asilmedia.org/13670-biz-hammamiz-oliklarmiz-hammasi-olganlar-olikmiz-netflix-koreya-seriali-barcha-qismlar-ozbek-tilida-2022-uzbekcha-tarjima.html"],
        "Comedy": ["Do‘stlar -  https://rutube.ru/plst/336529/","Dexter - https://kinok.net/shows/dekster-dexter/2-qism/166", "Gentelmenlar - https://rutube.ru/plst/380420/", "Suits - https://rutube.ru/plst/882733/"],
        "Drama": ["Vorislik - https://www.kinopoisk.ru/series/986788/", "Oliy tablilar - https://rutube.ru/plst/882733/" , "Chernobil - http://asilmedia.org/9252-chernobil-chernobyl-serial-uzbek-tilida-2019-hd-ozbek-tarjima-tas-ix-skachat.html", "Panjara ortida - http://asilmedia.org/5687-panjara-ortida-pobeg-iz-tyurmy-prison-break-fasl-1-qismlar-1-22-jami-22.html"],
        "K-drama": ["Goblin - https://playuz.net/654-goblin-1-3-5-7-9-11-13-14-16-qism-uzbek-tilida-koreya-serial-2016-barcha-qismlar-tarjima-serial-uzbekcha-skachat/episode/15.html","Vinchenzo - https://uzmovee.net/seriallar_uzbek_tilida/215-vinchenzo-koreys-serial-uzbek-tilida-2021-barcha-qismlar-720-hd-yuklab-olish.html","Vorislar - http://asilmedia.org/9005-vorislar-korea-seriali-12345678910-qism-nasledniki-serial-sangsokjadeul-2013-hd-tas-ix-skachat.html","Quyosh avlodlari - https://uzmovii.com/serial/6020-quyosh-avlodlari-barcha-qismlar-uzbek-tilida.html","F4 - https://uzmoovi.com/serial/3995-guldan-gozal-yigitlar-barcha-qismlar-koreys-serial-uzbek-tilida.html","Del Luna mehmonxonasi - https://uzbektilida.org/serial/3455-mehmonxona-bekasi-barcha-qismlar-uzbek-tilida/episode/1.html",
        "Kuchli ayol Do Bong Soon - https://uzmovii.com/serial/3940-kuchli-qiz-do-bong-son-barcha-qismlar-uzbek-tilida.html","Qirol: Abadiy monarx - https://uzmovii.com/serial/5049-qirol-abadiy-monarx-barcha-qismlar-uzbek-tilida.html","Qonxor itlar - https://uzproo.com/serial/437-ovchi-qonxor-itlar-2-fasl-1-2-3-4-5-6-7-8-9-10-11-12-15-qismlar-barcha-uzbek-tilida-2025-ozbekcha-tarjima.html","Asl gozallik - https://playuz.net/seriallar_2025/31-asl-gozalik-korea-seryali-2020-uzbek-tilida-1-2-3-510-15-16-qism-barcha-qismlar.html"]
    },    
    "ru": {
        "Crime/Thriller": ["Во все тяжкие - https://rutube.ru/plst/362343/", "Лучше звоните Солу - https://rutube.ru/plst/422294/", "Нарко - https://rutube.ru/plst/337759/", "Острые козырьки - https://rutube.ru/plst/336313/", "Бумажный дом - https://rutube.ru/plst/338189/", "Карточный домик - https://rutube.ru/plst/385210/", "Побег - https://rutube.ru/plst/394021/", "Декстер - https://rutube.ru/plst/731631/", "Джентльмен - https://rutube.ru/plst/380420/", "Ричер - https://rutube.ru/plst/350617/"],
        "Sci-Fi/Fantasy": ["Игра престолов - https://www.kinopoisk.ru/series/464963/", "Очень странные дела - https://rutube.ru/plst/363538/", "Алиса в Пограничье - https://rutube.ru/plst/349405/", "Пацаны - https://rutube.ru/plst/337761/", "Локи - https://rutube.ru/plst/415973/", "Одни из нас - https://rutube.ru/plst/616438/", "Игра в кальмара - https://rutube.ru/plst/333276/", "Академия Амбрелла - https://rutube.ru/plst/367214/", "Мы все мертвы - https://rutube.ru/plst/347745/"],
        "Comedy": ["Друзья - https://rutube.ru/plst/336529/", "Декстер - https://rutube.ru/plst/731631/", "Джентльмен - https://rutube.ru/plst/380420/", "Форс-мажоры - https://rutube.ru/plst/882733/"],
        "Drama": ["Наследники - https://rezka.ag/series/drama/27870-nasledniki-2018.html", "Форс-мажоры - https://rutube.ru/plst/882733/", "Чернобыль - https://hd.kinopoisk.ru/ru-uz/film/4a736aa840d5a895a94448a999495906", "Побег - https://rutube.ru/plst/394021/"],
        "K-drama": ["Гоблин - https://rutube.ru/metainfo/tv/211679/","Винченцо","Наследники кореа - https://rutube.ru/plst/376445/","Потомки солнца - https://rutube.ru/metainfo/tv/198471/","Мальчики краше цветов- https://rutube.ru/metainfo/tv/548868/","Отель «Дел Луна - https://rutube.ru/metainfo/tv/198474/","Сильная женщина До Бон Сон - https://rutube.ru/metainfo/tv/211671/","Король: Вечный монарх - https://rutube.ru/plst/369873/", "Охотничьи псы - https://rutube.ru/plst/381335/","Истинная красота - https://rutube.ru/metainfo/tv/540787/" ]
    },
    "en": {
        "Crime/Thriller": ["Breaking Bad - https://inoriginal.net/series/432-breaking-bad-2008.html", "Better Call Saul - https://inoriginal.net/series/1228-better-call-saul-2015.html", "Narcos - https://www.imdb.com/title/tt2707408/?ref_=ext_shr_lnk", "Peaky Blinders - https://inoriginal.net/series/431-peaky-blinders-2013.html", "Money Heist - https://inoriginal.net/series/4645-money-heist-2017.html","House of Cards - https://inoriginal.net/series/1338-house-of-cards-2013.html", "Prison Break - https://inoriginal.net/series/1893-prison-break-2005.html", "Dexter - https://inoriginal.net/series/1170-dexter-2006.html", "The Gentelman - https://www.imdb.com/title/tt13210838/?ref_=ext_shr_lnk","Reacher - https://inoriginal.net/series/2204-reacher-2022.html"],
        "Sci-Fi/Fantasy": ["Game of Thrones - https://www.imdb.com/title/tt0944947/?ref_=ext_shr_lnk", "Stranger Things - https://inoriginal.net/series/489-stranger-things-2016.html", "Alice in Borderland - https://www.imdb.com/title/tt10795658/?ref_=ext_shr_lnk", "The Boys - https://inoriginal.net/series/1086-the-boys-2019.html", "Loki - https://inoriginal.net/series/1125-loki-2021.html", "The Last of Us - https://inoriginal.net/series/410-the-last-of-us-2023.html", "Squid Game - https://inoriginal.net/series/1114-squid-game-2021.html","The Umbrella Academy - https://inoriginal.net/series/1156-the-umbrella-academy-2019.html", "All of us are dead - https://www.imdb.com/title/tt14169960/"],
        "Comedy": ["Friends - https://inoriginal.net/series/356-friends-1994.html", "Dexter - https://inoriginal.net/series/1170-dexter-2006.html", " The Gentelman - https://www.imdb.com/title/tt13210838/?ref_=ext_shr_lnk", "Suits - https://inoriginal.net/series/2074-suit-2011.html","Prison Break - https://inoriginal.net/series/1893-prison-break-2005.html"],
        "Drama": ["Succession - https://inoriginal.net/series/1133-succession-2018.html", "Suits - https://inoriginal.net/series/2074-suit-2011.html" , "Chernobyl - https://inoriginal.net/series/730-chernobyl-2019.html"],
        "K-drama": ["Goblin - https://uzmovii.com/serial/3940-kuchli-qiz-do-bong-son-barcha-qismlar-uzbek-tilida.html","Vincenzo - https://uzmovee.net/seriallar_uzbek_tilida/215-vinchenzo-koreys-serial-uzbek-tilida-2021-barcha-qismlar-720-hd-yuklab-olish.html","The Heirs - http://asilmedia.org/9005-vorislar-korea-seriali-12345678910-qism-nasledniki-serial-sangsokjadeul-2013-hd-tas-ix-skachat.html","Descendants of the Sun - https://uzmovii.com/serial/6020-quyosh-avlodlari-barcha-qismlar-uzbek-tilida.html","Boys Over Flowers - https://uzmoovi.com/serial/3995-guldan-gozal-yigitlar-barcha-qismlar-koreys-serial-uzbek-tilida.html","Hotel Del Luna -  https://uzbektilida.org/serial/3455-mehmonxona-bekasi-barcha-qismlar-uzbek-tilida/episode/1.html",
        "Strong Woman Do Bong Soon - https://uzmovii.com/serial/3940-kuchli-qiz-do-bong-son-barcha-qismlar-uzbek-tilida.html","The King: Eternal Monarch - https://uzmovii.com/serial/5049-qirol-abadiy-monarx-barcha-qismlar-uzbek-tilida.html", "Bloodhounds - https://uzproo.com/serial/437-ovchi-qonxor-itlar-2-fasl-1-2-3-4-5-6-7-8-9-10-11-12-15-qismlar-barcha-uzbek-tilida-2025-ozbekcha-tarjima.html", "True beauty - https://playuz.net/seriallar_2025/31-asl-gozalik-korea-seryali-2020-uzbek-tilida-1-2-3-510-15-16-qism-barcha-qismlar.html"]
    }
}


    async with aiosqlite.connect(DB_NAME) as db:
        # Ma'lumotlarni avvaldan belgilangan dictionarylardan kiritish
        for lang, genres in movie_genres.items():
            for genre_key, genre_name in genres.items():
                await db.execute("INSERT INTO genres (language, genre_key, genre_name) VALUES (?, ?, ?)",
                                 (lang, genre_key, genre_name))

        for lang, genres in movie_list.items():
            for genre_key, movies in genres.items():
                for movie_name in movies:
                    await db.execute("INSERT INTO movies (language, genre_key, movie_name) VALUES (?, ?, ?)",
                                     (lang, genre_key, movie_name))

        for lang, genres in series_genres.items():
            for genre_key, genre_name in genres.items():
                await db.execute("INSERT INTO series_genres (language, genre_key, genre_name) VALUES (?, ?, ?)",
                                 (lang, genre_key, genre_name))

        for lang, genres in series_list.items():
            for genre_key, series in genres.items():
                for series_name in series:
                    await db.execute("INSERT INTO series (language, genre_key, series_name) VALUES (?, ?, ?)",
                                     (lang, genre_key, series_name))

        await db.commit()


# 3. Foydalanuvchi tilini saqlash
async def save_user_language(user_id: int, lang: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users (user_id, language)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
        """, (user_id, lang))
        await db.commit()


# 4. Foydalanuvchi tilini olish
async def get_user_language(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else "uz"  # Default til: uz


# 5. Kinolar janrlarini olish
async def get_movie_genres(language):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT genre_key, genre_name FROM genres WHERE language = ?", (language,))
        return {row[0]: row[1] for row in await cursor.fetchall()}


# 6. Kinolarni janr bo‘yicha olish
async def get_movies_by_genre(language, genre_key):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT movie_name FROM movies WHERE language = ? AND genre_key = ?", (language, genre_key))
        return [row[0] for row in await cursor.fetchall()]


# 7. Serial janrlarini olish
async def get_series_genres(language):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT genre_key, genre_name FROM series_genres WHERE language = ?", (language,))
        return {row[0]: row[1] for row in await cursor.fetchall()}


# 8. Serialni janr bo‘yicha olish
async def get_series_by_genre(language, genre_key):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT series_name FROM series WHERE language = ? AND genre_key = ?", (language, genre_key))
        return [row[0] for row in await cursor.fetchall()]


async def search_movies_and_series(language, query):
    async with aiosqlite.connect(DB_NAME) as db:
        # Qidiruvni kichik harfga aylantiramiz
        query = query.lower()
        
        # Kinolarni qidirish
        cursor = await db.execute(
            "SELECT movie_name FROM movies WHERE language = ? AND LOWER(movie_name) LIKE ?",
            (language, f"%{query}%")
        )
        movies = [row[0] for row in await cursor.fetchall()]

        # Seriallarni qidirish
        cursor = await db.execute(
            "SELECT series_name FROM series WHERE language = ? AND LOWER(series_name) LIKE ?",
            (language, f"%{query}%")
        )
        series = [row[0] for row in await cursor.fetchall()]

    return movies + series  # Kinolar va seriallarni birlashtirib qaytaramiz

async def setup_database():
    await create_db()
    await insert_data()
