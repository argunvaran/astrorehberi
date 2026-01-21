
# Valid 81 Province Map (Plate Code -> Name)
PROVINCE_NAMES = {
    "01": "Adana", "02": "Adıyaman", "03": "Afyonkarahisar", "04": "Ağrı", "05": "Amasya",
    "06": "Ankara", "07": "Antalya", "08": "Artvin", "09": "Aydın", "10": "Balıkesir",
    "11": "Bilecik", "12": "Bingöl", "13": "Bitlis", "14": "Bolu", "15": "Burdur",
    "16": "Bursa", "17": "Çanakkale", "18": "Çankırı", "19": "Çorum", "20": "Denizli",
    "21": "Diyarbakır", "22": "Edirne", "23": "Elazığ", "24": "Erzincan", "25": "Erzurum",
    "26": "Eskişehir", "27": "Gaziantep", "28": "Giresun", "29": "Gümüşhane", "30": "Hakkari",
    "31": "Hatay", "32": "Isparta", "33": "Mersin", "34": "İstanbul", "35": "İzmir",
    "36": "Kars", "37": "Kastamonu", "38": "Kayseri", "39": "Kırklareli", "40": "Kırşehir",
    "41": "Kocaeli", "42": "Konya", "43": "Kütahya", "44": "Malatya", "45": "Manisa",
    "46": "Kahramanmaraş", "47": "Mardin", "48": "Muğla", "49": "Muş", "50": "Nevşehir",
    "51": "Niğde", "52": "Ordu", "53": "Rize", "54": "Sakarya", "55": "Samsun",
    "56": "Siirt", "57": "Sinop", "58": "Sivas", "59": "Tekirdağ", "60": "Tokat",
    "61": "Trabzon", "62": "Tunceli", "63": "Şanlıurfa", "64": "Uşak", "65": "Van",
    "66": "Yozgat", "67": "Zonguldak", "68": "Aksaray", "69": "Bayburt", "70": "Karaman",
    "71": "Kırıkkale", "72": "Batman", "73": "Şırnak", "74": "Bartın", "75": "Ardahan",
    "76": "Iğdır", "77": "Yalova", "78": "Karabük", "79": "Kilis", "80": "Osmaniye",
    "81": "Düzce"
}

# FULL 81 PROVINCE DATASET
TR_DATA = {
    "01": {"name": "Adana", "districts": [
        {"name": "Seyhan", "lat": 37.0017, "lon": 35.3289}, {"name": "Ceyhan", "lat": 37.0247, "lon": 35.8175},
        {"name": "Çukurova", "lat": 37.0560, "lon": 35.2860}, {"name": "Yüreğir", "lat": 36.9853, "lon": 35.3436},
        {"name": "Sarıçam", "lat": 37.0620, "lon": 35.4190}, {"name": "Kozan", "lat": 37.4552, "lon": 35.8111}
    ]},
    "02": {"name": "Adıyaman", "districts": [
        {"name": "Merkez", "lat": 37.7644, "lon": 38.2763}, {"name": "Kahta", "lat": 37.7850, "lon": 38.6189},
        {"name": "Besni", "lat": 37.6933, "lon": 37.8631}, {"name": "Gölbaşı", "lat": 37.7833, "lon": 37.6333}
    ]},
    "03": {"name": "Afyonkarahisar", "districts": [
        {"name": "Merkez", "lat": 38.7569, "lon": 30.5386}, {"name": "Sandıklı", "lat": 38.4667, "lon": 30.2667},
        {"name": "Bolvadin", "lat": 38.7117, "lon": 31.0494}, {"name": "Dinar", "lat": 38.0650, "lon": 30.1656}
    ]},
    "04": {"name": "Ağrı", "districts": [
        {"name": "Merkez", "lat": 39.7194, "lon": 43.0506}, {"name": "Doğubayazıt", "lat": 39.5458, "lon": 44.0958},
        {"name": "Patnos", "lat": 39.2319, "lon": 42.8622}, {"name": "Diyadin", "lat": 39.5447, "lon": 43.6667}
    ]},
    "05": {"name": "Amasya", "districts": [
        {"name": "Merkez", "lat": 40.6524, "lon": 35.8288}, {"name": "Merzifon", "lat": 40.8719, "lon": 35.4608},
        {"name": "Suluova", "lat": 40.8353, "lon": 35.6561}, {"name": "Taşova", "lat": 40.7600, "lon": 36.3267}
    ]},
    "06": {"name": "Ankara", "districts": [
        {"name": "Çankaya", "lat": 39.9208, "lon": 32.8542}, {"name": "Keçiören", "lat": 39.9961, "lon": 32.8625},
        {"name": "Yenimahalle", "lat": 39.9578, "lon": 32.7997}, {"name": "Mamak", "lat": 39.9436, "lon": 32.9367},
        {"name": "Etimesgut", "lat": 39.9497, "lon": 32.6631}, {"name": "Sincan", "lat": 39.9619, "lon": 32.5761},
        {"name": "Gölbaşı", "lat": 39.7917, "lon": 32.8064}, {"name": "Polatlı", "lat": 39.5833, "lon": 32.1333},
        {"name": "Altındağ", "lat": 39.9414, "lon": 32.8600}, {"name": "Beypazarı", "lat": 40.1683, "lon": 31.9206}
    ]},
    "07": {"name": "Antalya", "districts": [
        {"name": "Muratpaşa", "lat": 36.8858, "lon": 30.7075}, {"name": "Kepez", "lat": 36.9328, "lon": 30.6844},
        {"name": "Konyaaltı", "lat": 36.8656, "lon": 30.6386}, {"name": "Alanya", "lat": 36.5436, "lon": 31.9997},
        {"name": "Manavgat", "lat": 36.7833, "lon": 31.4500}, {"name": "Kemer", "lat": 36.6025, "lon": 30.5606},
        {"name": "Serik", "lat": 36.9167, "lon": 31.1000}, {"name": "Kaş", "lat": 36.2000, "lon": 29.6333}
    ]},
    "08": {"name": "Artvin", "districts": [
        {"name": "Merkez", "lat": 41.1822, "lon": 41.8194}, {"name": "Hopa", "lat": 41.4056, "lon": 41.4339},
        {"name": "Borçka", "lat": 41.3578, "lon": 41.6789}, {"name": "Arhavi", "lat": 41.3503, "lon": 41.3061}
    ]},
    "09": {"name": "Aydın", "districts": [
        {"name": "Efeler", "lat": 37.8444, "lon": 27.8458}, {"name": "Nazilli", "lat": 37.9150, "lon": 28.3228},
        {"name": "Kuşadası", "lat": 37.8575, "lon": 27.2608}, {"name": "Söke", "lat": 37.7511, "lon": 27.4086},
        {"name": "Didim", "lat": 37.3822, "lon": 27.2575}
    ]},
    "10": {"name": "Balıkesir", "districts": [
        {"name": "Altıeylül", "lat": 39.6450, "lon": 27.8828}, {"name": "Karesi", "lat": 39.6500, "lon": 27.8900},
        {"name": "Bandırma", "lat": 40.3536, "lon": 27.9714}, {"name": "Edremit", "lat": 39.5961, "lon": 27.0244},
        {"name": "Ayvalık", "lat": 39.3178, "lon": 26.6961}
    ]},
    "11": {"name": "Bilecik", "districts": [
        {"name": "Merkez", "lat": 40.1419, "lon": 29.9800}, {"name": "Bozüyük", "lat": 39.9078, "lon": 30.0381},
        {"name": "Osmaneli", "lat": 40.3581, "lon": 30.0169}
    ]},
    "12": {"name": "Bingöl", "districts": [
        {"name": "Merkez", "lat": 38.8833, "lon": 40.4936}, {"name": "Genç", "lat": 38.7517, "lon": 40.5600},
        {"name": "Solhan", "lat": 38.9667, "lon": 41.0500}
    ]},
    "13": {"name": "Bitlis", "districts": [
        {"name": "Merkez", "lat": 38.4006, "lon": 42.1094}, {"name": "Tatvan", "lat": 38.5028, "lon": 42.2778},
        {"name": "Ahlat", "lat": 38.7525, "lon": 42.4864}, {"name": "Güroymak", "lat": 38.5636, "lon": 42.0253}
    ]},
    "14": {"name": "Bolu", "districts": [
        {"name": "Merkez", "lat": 40.7350, "lon": 31.6061}, {"name": "Gerede", "lat": 40.8000, "lon": 32.1969},
        {"name": "Mudurnu", "lat": 40.4619, "lon": 31.2106}
    ]},
    "15": {"name": "Burdur", "districts": [
        {"name": "Merkez", "lat": 37.7203, "lon": 30.2908}, {"name": "Bucak", "lat": 37.4583, "lon": 30.5878},
        {"name": "Gölhisar", "lat": 37.1478, "lon": 29.5089}
    ]},
    "16": {"name": "Bursa", "districts": [
        {"name": "Osmangazi", "lat": 40.2000, "lon": 29.0500}, {"name": "Nilüfer", "lat": 40.2150, "lon": 28.9381},
        {"name": "Yıldırım", "lat": 40.1833, "lon": 29.1333}, {"name": "İnegöl", "lat": 40.0833, "lon": 29.5167},
        {"name": "Gemlik", "lat": 40.4333, "lon": 29.1500}, {"name": "Mudanya", "lat": 40.3833, "lon": 28.8833}
    ]},
    "17": {"name": "Çanakkale", "districts": [
        {"name": "Merkez", "lat": 40.1553, "lon": 26.4142}, {"name": "Biga", "lat": 40.2294, "lon": 27.2436},
        {"name": "Çan", "lat": 40.0333, "lon": 27.0500}, {"name": "Gelibolu", "lat": 40.4103, "lon": 26.6706}
    ]},
    "18": {"name": "Çankırı", "districts": [
        {"name": "Merkez", "lat": 40.6014, "lon": 33.6136}, {"name": "Çerkeş", "lat": 40.8039, "lon": 32.8883},
        {"name": "Ilgaz", "lat": 40.9256, "lon": 33.6300}
    ]},
    "19": {"name": "Çorum", "districts": [
        {"name": "Merkez", "lat": 40.5506, "lon": 34.9556}, {"name": "Sungurlu", "lat": 40.1667, "lon": 34.3667},
        {"name": "Osmancık", "lat": 40.9750, "lon": 34.8000}
    ]},
    "20": {"name": "Denizli", "districts": [
        {"name": "Pamukkale", "lat": 37.7765, "lon": 29.0864}, {"name": "Merkezefendi", "lat": 37.7850, "lon": 29.0700},
        {"name": "Çivril", "lat": 38.2936, "lon": 29.7369}, {"name": "Acıpayam", "lat": 37.4333, "lon": 29.3500}
    ]},
    "21": {"name": "Diyarbakır", "districts": [
        {"name": "Bağlar", "lat": 37.9150, "lon": 40.2294}, {"name": "Kayapınar", "lat": 37.9403, "lon": 40.1983},
        {"name": "Yenişehir", "lat": 37.9250, "lon": 40.2319}, {"name": "Sur", "lat": 37.9144, "lon": 40.2306},
        {"name": "Ergani", "lat": 38.2650, "lon": 39.7619}, {"name": "Bismil", "lat": 37.8483, "lon": 40.6653}
    ]},
    "22": {"name": "Edirne", "districts": [
        {"name": "Merkez", "lat": 41.6764, "lon": 26.5558}, {"name": "Keşan", "lat": 40.8528, "lon": 26.6344},
        {"name": "Uzunköprü", "lat": 41.2700, "lon": 26.6850}
    ]},
    "23": {"name": "Elazığ", "districts": [
        {"name": "Merkez", "lat": 38.6811, "lon": 39.2228}, {"name": "Kovancılar", "lat": 38.7183, "lon": 39.8592},
        {"name": "Karakoçan", "lat": 38.9567, "lon": 40.0333}
    ]},
    "24": {"name": "Erzincan", "districts": [
        {"name": "Merkez", "lat": 39.7500, "lon": 39.5000}, {"name": "Tercan", "lat": 39.7783, "lon": 40.3922}
    ]},
    "25": {"name": "Erzurum", "districts": [
        {"name": "Yakutiye", "lat": 39.9050, "lon": 41.2764}, {"name": "Palandöken", "lat": 39.8972, "lon": 41.2725},
        {"name": "Aziziye", "lat": 39.9500, "lon": 41.1667}, {"name": "Oltu", "lat": 40.5528, "lon": 41.9964}
    ]},
    "26": {"name": "Eskişehir", "districts": [
        {"name": "Odunpazarı", "lat": 39.7767, "lon": 30.5206}, {"name": "Tepebaşı", "lat": 39.7900, "lon": 30.5050},
        {"name": "Sivrihisar", "lat": 39.4503, "lon": 31.5361}, {"name": "Çifteler", "lat": 39.3833, "lon": 31.0333}
    ]},
    "27": {"name": "Gaziantep", "districts": [
        {"name": "Şahinbey", "lat": 37.0600, "lon": 37.3600}, {"name": "Şehitkamil", "lat": 37.0750, "lon": 37.3850},
        {"name": "Nizip", "lat": 37.0108, "lon": 37.7942}, {"name": "İslahiye", "lat": 37.0272, "lon": 36.6339}
    ]},
    "28": {"name": "Giresun", "districts": [
        {"name": "Merkez", "lat": 40.9169, "lon": 38.3872}, {"name": "Bulancak", "lat": 40.9383, "lon": 38.2289},
        {"name": "Espiye", "lat": 40.9472, "lon": 38.7183}, {"name": "Görele", "lat": 41.0333, "lon": 39.0067}
    ]},
    "29": {"name": "Gümüşhane", "districts": [
        {"name": "Merkez", "lat": 40.4597, "lon": 39.4767}, {"name": "Kelkit", "lat": 40.1333, "lon": 39.4333},
        {"name": "Şiran", "lat": 40.1833, "lon": 39.1333}
    ]},
    "30": {"name": "Hakkari", "districts": [
        {"name": "Merkez", "lat": 37.5833, "lon": 43.7333}, {"name": "Yüksekova", "lat": 37.5647, "lon": 44.2858},
        {"name": "Şemdinli", "lat": 37.2981, "lon": 44.5708}, {"name": "Çukurca", "lat": 37.2500, "lon": 43.6067}
    ]},
    "31": {"name": "Hatay", "districts": [
        {"name": "Antakya", "lat": 36.2025, "lon": 36.1606}, {"name": "İskenderun", "lat": 36.5864, "lon": 36.1706},
        {"name": "Defne", "lat": 36.1361, "lon": 36.0950}, {"name": "Dörtyol", "lat": 36.8394, "lon": 36.2236},
        {"name": "Samandağ", "lat": 36.0847, "lon": 35.9772}, {"name": "Kırıkhan", "lat": 36.5000, "lon": 36.3500}
    ]},
    "32": {"name": "Isparta", "districts": [
        {"name": "Merkez", "lat": 37.7648, "lon": 30.5567}, {"name": "Yalvaç", "lat": 38.2939, "lon": 31.1764},
        {"name": "Eğirdir", "lat": 37.8761, "lon": 30.8406}, {"name": "Şarkikaraağaç", "lat": 38.0772, "lon": 31.3658}
    ]},
    "33": {"name": "Mersin", "districts": [
        {"name": "Akdeniz", "lat": 36.8121, "lon": 34.6405}, {"name": "Yenişehir", "lat": 36.7778, "lon": 34.5956},
        {"name": "Toroslar", "lat": 36.8522, "lon": 34.6067}, {"name": "Mezitli", "lat": 36.7539, "lon": 34.5422},
        {"name": "Tarsus", "lat": 36.9164, "lon": 34.8953}, {"name": "Erdemli", "lat": 36.6053, "lon": 34.3075},
        {"name": "Silifke", "lat": 36.3778, "lon": 33.9344}, {"name": "Anamur", "lat": 36.0750, "lon": 32.8361}
    ]},
    "34": {"name": "İstanbul", "districts": [
        {"name": "Kadıköy", "lat": 40.9856, "lon": 29.0274}, {"name": "Beşiktaş", "lat": 41.0428, "lon": 29.0075},
        {"name": "Üsküdar", "lat": 41.0264, "lon": 29.0167}, {"name": "Şişli", "lat": 41.0536, "lon": 28.9877},
        {"name": "Beyoğlu", "lat": 41.0284, "lon": 28.9736}, {"name": "Fatih", "lat": 41.0118, "lon": 28.9483},
        {"name": "Bakırköy", "lat": 40.9781, "lon": 28.8744}, {"name": "Ataşehir", "lat": 40.9928, "lon": 29.1169},
        {"name": "Ümraniye", "lat": 41.0256, "lon": 29.0964}, {"name": "Maltepe", "lat": 40.9247, "lon": 29.1311},
        {"name": "Kartal", "lat": 40.8906, "lon": 29.1931}, {"name": "Pendik", "lat": 40.8769, "lon": 29.2347},
        {"name": "Sarıyer", "lat": 41.1681, "lon": 29.0536}, {"name": "Beykoz", "lat": 41.1181, "lon": 29.1000},
        {"name": "Zeytinburnu", "lat": 40.9903, "lon": 28.9036}, {"name": "Avcılar", "lat": 40.9781, "lon": 28.7239},
        {"name": "Başakşehir", "lat": 41.0831, "lon": 28.8131}, {"name": "Beylikdüzü", "lat": 41.0011, "lon": 28.6419},
        {"name": "Esenyurt", "lat": 41.0333, "lon": 28.6833}, {"name": "Çekmeköy", "lat": 41.0333, "lon": 29.1667}
    ]},
    "35": {"name": "İzmir", "districts": [
        {"name": "Konak", "lat": 38.4189, "lon": 27.1286}, {"name": "Karşıyaka", "lat": 38.4597, "lon": 27.1089},
        {"name": "Bornova", "lat": 38.4617, "lon": 27.2183}, {"name": "Buca", "lat": 38.3847, "lon": 27.1700},
        {"name": "Çeşme", "lat": 38.3167, "lon": 26.3000}, {"name": "Urla", "lat": 38.3167, "lon": 26.7667},
        {"name": "Menemen", "lat": 38.6000, "lon": 27.0667}, {"name": "Seferihisar", "lat": 38.2000, "lon": 26.8333},
        {"name": "Selçuk", "lat": 37.9500, "lon": 27.3667}, {"name": "Foça", "lat": 38.6667, "lon": 26.7500}
    ]},
    "36": {"name": "Kars", "districts": [
        {"name": "Merkez", "lat": 40.6019, "lon": 43.0950}, {"name": "Sarıkamış", "lat": 40.3342, "lon": 42.5939},
        {"name": "Kağızman", "lat": 40.1500, "lon": 43.1167}
    ]},
    "37": {"name": "Kastamonu", "districts": [
        {"name": "Merkez", "lat": 41.3887, "lon": 33.7827}, {"name": "Tosya", "lat": 41.0161, "lon": 34.0322},
        {"name": "Taşköprü", "lat": 41.5161, "lon": 34.2167}, {"name": "İnebolu", "lat": 41.9747, "lon": 33.7608}
    ]},
    "38": {"name": "Kayseri", "districts": [
        {"name": "Melikgazi", "lat": 38.7303, "lon": 35.5392}, {"name": "Kocasinan", "lat": 38.7389, "lon": 35.4853},
        {"name": "Talas", "lat": 38.6908, "lon": 35.5564}, {"name": "Develi", "lat": 38.3917, "lon": 35.4917},
        {"name": "Yahyalı", "lat": 38.1000, "lon": 35.3500}, {"name": "Bünyan", "lat": 38.8500, "lon": 35.8667}
    ]},
    "39": {"name": "Kırklareli", "districts": [
        {"name": "Merkez", "lat": 41.7351, "lon": 27.2252}, {"name": "Lüleburgaz", "lat": 41.4039, "lon": 27.3539},
        {"name": "Babaeski", "lat": 41.4333, "lon": 27.0833}, {"name": "Vize", "lat": 41.5714, "lon": 27.7661}
    ]},
    "40": {"name": "Kırşehir", "districts": [
        {"name": "Merkez", "lat": 39.1458, "lon": 34.1639}, {"name": "Kaman", "lat": 39.3564, "lon": 33.7258},
        {"name": "Mucur", "lat": 39.0667, "lon": 34.3833}
    ]},
    "41": {"name": "Kocaeli", "districts": [
        {"name": "İzmit", "lat": 40.7667, "lon": 29.9167}, {"name": "Gebze", "lat": 40.8000, "lon": 29.4333},
        {"name": "Darıca", "lat": 40.7667, "lon": 29.4000}, {"name": "Gölcük", "lat": 40.7167, "lon": 29.8167},
        {"name": "Körfez", "lat": 40.7758, "lon": 29.7431}, {"name": "Derince", "lat": 40.7583, "lon": 29.8333},
        {"name": "Kartepe", "lat": 40.7567, "lon": 30.0197}, {"name": "Karamürsel", "lat": 40.6922, "lon": 29.6156}
    ]},
    "42": {"name": "Konya", "districts": [
        {"name": "Selçuklu", "lat": 37.8997, "lon": 32.4853}, {"name": "Meram", "lat": 37.8653, "lon": 32.4667},
        {"name": "Karatay", "lat": 37.8681, "lon": 32.5056}, {"name": "Ereğli", "lat": 37.5133, "lon": 34.0561},
        {"name": "Akşehir", "lat": 38.3575, "lon": 31.4164}, {"name": "Beyşehir", "lat": 37.6778, "lon": 31.7225}
    ]},
    "43": {"name": "Kütahya", "districts": [
        {"name": "Merkez", "lat": 39.4200, "lon": 29.9839}, {"name": "Tavşanlı", "lat": 39.5442, "lon": 29.4822},
        {"name": "Simav", "lat": 39.0911, "lon": 28.9767}, {"name": "Gediz", "lat": 39.0333, "lon": 29.4000}
    ]},
    "44": {"name": "Malatya", "districts": [
        {"name": "Battalgazi", "lat": 38.3552, "lon": 38.3094}, {"name": "Yeşilyurt", "lat": 38.3000, "lon": 38.2500},
        {"name": "Doğanşehir", "lat": 38.0833, "lon": 37.8833}, {"name": "Darende", "lat": 38.5667, "lon": 37.5000}
    ]},
    "45": {"name": "Manisa", "districts": [
        {"name": "Yunusemre", "lat": 38.6300, "lon": 27.4200}, {"name": "Şehzadeler", "lat": 38.6191, "lon": 27.4289},
        {"name": "Akhisar", "lat": 38.9247, "lon": 27.8394}, {"name": "Turgutlu", "lat": 38.4950, "lon": 27.7058},
        {"name": "Salihli", "lat": 38.4800, "lon": 28.1389}, {"name": "Soma", "lat": 39.1867, "lon": 27.6083}
    ]},
    "46": {"name": "Kahramanmaraş", "districts": [
        {"name": "Onikişubat", "lat": 37.5858, "lon": 36.9371}, {"name": "Dulkadiroğlu", "lat": 37.5753, "lon": 36.9228},
        {"name": "Elbistan", "lat": 38.2056, "lon": 37.1953}, {"name": "Afşin", "lat": 38.2467, "lon": 36.9139},
        {"name": "Pazarcık", "lat": 37.4858, "lon": 37.2917}
    ]},
    "47": {"name": "Mardin", "districts": [
        {"name": "Artuklu", "lat": 37.3129, "lon": 40.7350}, {"name": "Kızıltepe", "lat": 37.1939, "lon": 40.5878},
        {"name": "Midyat", "lat": 37.4186, "lon": 41.3417}, {"name": "Nusaybin", "lat": 37.0778, "lon": 41.2178},
        {"name": "Derik", "lat": 37.3622, "lon": 40.2683}
    ]},
    "48": {"name": "Muğla", "districts": [
        {"name": "Menteşe", "lat": 37.2153, "lon": 28.3636}, {"name": "Bodrum", "lat": 37.0383, "lon": 27.4292},
        {"name": "Fethiye", "lat": 36.6217, "lon": 29.1164}, {"name": "Marmaris", "lat": 36.8550, "lon": 28.2742},
        {"name": "Milas", "lat": 37.3164, "lon": 27.7839}, {"name": "Ortaca", "lat": 36.8361, "lon": 28.7667},
        {"name": "Datça", "lat": 36.7233, "lon": 27.6833}
    ]},
    "49": {"name": "Muş", "districts": [
        {"name": "Merkez", "lat": 38.9462, "lon": 41.7539}, {"name": "Bulanık", "lat": 39.0911, "lon": 42.2611},
        {"name": "Malazgirt", "lat": 39.1461, "lon": 42.5408}
    ]},
    "50": {"name": "Nevşehir", "districts": [
        {"name": "Merkez", "lat": 38.6250, "lon": 34.7122}, {"name": "Ürgüp", "lat": 38.6308, "lon": 34.9125},
        {"name": "Avanos", "lat": 38.7183, "lon": 34.8450}, {"name": "Derinkuyu", "lat": 38.3725, "lon": 34.7333}
    ]},
    "51": {"name": "Niğde", "districts": [
        {"name": "Merkez", "lat": 37.9698, "lon": 34.6766}, {"name": "Bor", "lat": 37.8931, "lon": 34.5619},
        {"name": "Çiftlik", "lat": 38.1667, "lon": 34.5000}
    ]},
    "52": {"name": "Ordu", "districts": [
        {"name": "Altınordu", "lat": 40.9861, "lon": 37.8797}, {"name": "Ünye", "lat": 41.1278, "lon": 37.2833},
        {"name": "Fatsa", "lat": 41.0289, "lon": 37.5028}, {"name": "Perşembe", "lat": 41.0667, "lon": 37.7667}
    ]},
    "53": {"name": "Rize", "districts": [
        {"name": "Merkez", "lat": 41.0208, "lon": 40.5219}, {"name": "Çayeli", "lat": 41.0833, "lon": 40.7333},
        {"name": "Ardeşen", "lat": 41.1928, "lon": 40.9881}, {"name": "Pazar", "lat": 41.1739, "lon": 40.8711}
    ]},
    "54": {"name": "Sakarya", "districts": [
        {"name": "Adapazarı", "lat": 40.7731, "lon": 30.4019}, {"name": "Serdivan", "lat": 40.7583, "lon": 30.3667},
        {"name": "Akyazı", "lat": 40.6833, "lon": 30.6167}, {"name": "Erenler", "lat": 40.7500, "lon": 30.4167},
        {"name": "Hendek", "lat": 40.7933, "lon": 30.7492}, {"name": "Karasu", "lat": 41.1064, "lon": 30.6939}
    ]},
    "55": {"name": "Samsun", "districts": [
        {"name": "İlkadım", "lat": 41.2867, "lon": 36.3300}, {"name": "Atakum", "lat": 41.3283, "lon": 36.2625},
        {"name": "Canik", "lat": 41.2725, "lon": 36.3683}, {"name": "Bafra", "lat": 41.5678, "lon": 35.9069},
        {"name": "Çarşamba", "lat": 41.2000, "lon": 36.7333}, {"name": "Terme", "lat": 41.2094, "lon": 36.9739}
    ]},
    "56": {"name": "Siirt", "districts": [
        {"name": "Merkez", "lat": 37.9333, "lon": 41.9500}, {"name": "Kurtalan", "lat": 37.9272, "lon": 41.7028},
        {"name": "Pervari", "lat": 37.9333, "lon": 42.5333}
    ]},
    "57": {"name": "Sinop", "districts": [
        {"name": "Merkez", "lat": 42.0267, "lon": 35.1511}, {"name": "Boyabat", "lat": 41.4667, "lon": 34.7667},
        {"name": "Ayancık", "lat": 41.9500, "lon": 34.5833}
    ]},
    "58": {"name": "Sivas", "districts": [
        {"name": "Merkez", "lat": 39.7505, "lon": 37.0150}, {"name": "Şarkışla", "lat": 39.3517, "lon": 36.4117},
        {"name": "Yıldızeli", "lat": 39.8667, "lon": 36.5833}, {"name": "Suşehri", "lat": 40.1650, "lon": 38.0867}
    ]},
    "59": {"name": "Tekirdağ", "districts": [
        {"name": "Süleymanpaşa", "lat": 40.9781, "lon": 27.5117}, {"name": "Çorlu", "lat": 41.1608, "lon": 27.7978},
        {"name": "Çerkezköy", "lat": 41.2856, "lon": 28.0006}, {"name": "Kapaklı", "lat": 41.3106, "lon": 27.9869}
    ]},
    "60": {"name": "Tokat", "districts": [
        {"name": "Merkez", "lat": 40.3167, "lon": 36.5500}, {"name": "Erbaa", "lat": 40.6922, "lon": 36.5683},
        {"name": "Turhal", "lat": 40.3953, "lon": 36.0883}, {"name": "Niksar", "lat": 40.5900, "lon": 36.9533}
    ]},
    "61": {"name": "Trabzon", "districts": [
        {"name": "Ortahisar", "lat": 41.0015, "lon": 39.7178}, {"name": "Akçaabat", "lat": 41.0206, "lon": 39.5703},
        {"name": "Araklı", "lat": 40.9386, "lon": 40.0583}, {"name": "Of", "lat": 40.9428, "lon": 40.2708},
        {"name": "Yomra", "lat": 40.9483, "lon": 39.8567}, {"name": "Vakfıkebir", "lat": 41.0528, "lon": 39.2942}
    ]},
    "62": {"name": "Tunceli", "districts": [
        {"name": "Merkez", "lat": 39.1081, "lon": 39.5483}, {"name": "Pertek", "lat": 38.8681, "lon": 39.3244}
    ]},
    "63": {"name": "Şanlıurfa", "districts": [
        {"name": "Eyyübiye", "lat": 37.1500, "lon": 38.7940}, {"name": "Haliliye", "lat": 37.1600, "lon": 38.8100},
        {"name": "Karaköprü", "lat": 37.2000, "lon": 38.8200}, {"name": "Siverek", "lat": 37.7558, "lon": 39.3175},
        {"name": "Virânşehir", "lat": 37.2306, "lon": 39.7633}, {"name": "Birecik", "lat": 37.0289, "lon": 37.9781}
    ]},
    "64": {"name": "Uşak", "districts": [
        {"name": "Merkez", "lat": 38.6823, "lon": 29.4082}, {"name": "Banaz", "lat": 38.7333, "lon": 29.7500},
        {"name": "Eşme", "lat": 38.4000, "lon": 28.9667}
    ]},
    "65": {"name": "Van", "districts": [
        {"name": "İpekyolu", "lat": 38.5019, "lon": 43.3933}, {"name": "Tuşba", "lat": 38.5300, "lon": 43.3800},
        {"name": "Edremit", "lat": 38.4233, "lon": 43.2533}, {"name": "Erciş", "lat": 39.0278, "lon": 43.3581}
    ]},
    "66": {"name": "Yozgat", "districts": [
        {"name": "Merkez", "lat": 39.8200, "lon": 34.8044}, {"name": "Sorgun", "lat": 39.8103, "lon": 35.1861},
        {"name": "Yerköy", "lat": 39.6383, "lon": 34.3072}, {"name": "Boğazlıyan", "lat": 39.1931, "lon": 35.2458}
    ]},
    "67": {"name": "Zonguldak", "districts": [
        {"name": "Merkez", "lat": 41.4564, "lon": 31.7987}, {"name": "Ereğli", "lat": 41.2831, "lon": 31.4142},
        {"name": "Çaycuma", "lat": 41.4239, "lon": 32.0783}, {"name": "Devrek", "lat": 41.2208, "lon": 31.9567}
    ]},
    "68": {"name": "Aksaray", "districts": [
        {"name": "Merkez", "lat": 38.3686, "lon": 34.0297}, {"name": "Ortaköy", "lat": 38.7408, "lon": 34.0378},
        {"name": "Eskil", "lat": 38.4000, "lon": 33.4167}
    ]},
    "69": {"name": "Bayburt", "districts": [
        {"name": "Merkez", "lat": 40.2603, "lon": 40.2286}, {"name": "Demirözü", "lat": 40.1667, "lon": 39.9000}
    ]},
    "70": {"name": "Karaman", "districts": [
        {"name": "Merkez", "lat": 37.1811, "lon": 33.2222}, {"name": "Ermenek", "lat": 36.6267, "lon": 32.8858}
    ]},
    "71": {"name": "Kırıkkale", "districts": [
        {"name": "Merkez", "lat": 39.8453, "lon": 33.5064}, {"name": "Yahşihan", "lat": 39.8333, "lon": 33.4667},
        {"name": "Keskin", "lat": 39.6739, "lon": 33.6133}
    ]},
    "72": {"name": "Batman", "districts": [
        {"name": "Merkez", "lat": 37.8874, "lon": 41.1325}, {"name": "Kozluk", "lat": 38.1925, "lon": 41.4883},
        {"name": "Sason", "lat": 38.3267, "lon": 41.4133}
    ]},
    "73": {"name": "Şırnak", "districts": [
        {"name": "Merkez", "lat": 37.5194, "lon": 42.4572}, {"name": "Cizre", "lat": 37.3272, "lon": 42.1906},
        {"name": "Silopi", "lat": 37.2497, "lon": 42.4694}, {"name": "İdil", "lat": 37.3425, "lon": 41.8894}
    ]},
    "74": {"name": "Bartın", "districts": [
        {"name": "Merkez", "lat": 41.6358, "lon": 32.3375}, {"name": "Amasra", "lat": 41.7483, "lon": 32.3861}
    ]},
    "75": {"name": "Ardahan", "districts": [
        {"name": "Merkez", "lat": 41.1122, "lon": 42.7022}, {"name": "Göle", "lat": 40.7833, "lon": 42.6167}
    ]},
    "76": {"name": "Iğdır", "districts": [
        {"name": "Merkez", "lat": 39.9239, "lon": 44.0442}, {"name": "Tuzluca", "lat": 40.0331, "lon": 43.6664}
    ]},
    "77": {"name": "Yalova", "districts": [
        {"name": "Merkez", "lat": 40.6550, "lon": 29.2769}, {"name": "Çiftlikköy", "lat": 40.6631, "lon": 29.3242},
        {"name": "Çınarcık", "lat": 40.6433, "lon": 29.1172}, {"name": "Altınova", "lat": 40.6939, "lon": 29.5083}
    ]},
    "78": {"name": "Karabük", "districts": [
        {"name": "Merkez", "lat": 41.2049, "lon": 32.6277}, {"name": "Safranbolu", "lat": 41.2508, "lon": 32.6942},
        {"name": "Yenice", "lat": 41.2000, "lon": 32.3333}
    ]},
    "79": {"name": "Kilis", "districts": [
        {"name": "Merkez", "lat": 36.7161, "lon": 37.1150}, {"name": "Musabeyli", "lat": 36.9000, "lon": 36.9167}
    ]},
    "80": {"name": "Osmaniye", "districts": [
        {"name": "Merkez", "lat": 37.0746, "lon": 36.2464}, {"name": "Kadirli", "lat": 37.3739, "lon": 36.0964},
        {"name": "Düziçi", "lat": 37.2417, "lon": 36.4550}
    ]},
    "81": {"name": "Düzce", "districts": [
        {"name": "Merkez", "lat": 40.8389, "lon": 31.1625}, {"name": "Akçakoca", "lat": 41.0867, "lon": 31.1167},
        {"name": "Gümüşova", "lat": 40.8500, "lon": 30.9333}
    ]}
}
