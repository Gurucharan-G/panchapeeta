from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHAS_DATA = [
    {
        "name": "Rambhapuri Peetha",
        "slug": "rambhapuri",
        "acharya": "Jagadguru Renukacharya",
        "simhasana": "Veera Simhasana",
        "location": "Balehonnur, Chikkamagaluru",
        "state": "Karnataka",
        "current_swamiji": "Shree Shree Shree Jagadguru Prasanna Renuka Veera Someshwara Rajadeshikendra Shivacharya Mahaswamiji",
        "associated_linga": "Someshvara Linga",
        "associated_linga_map_url": "https://maps.google.com/?q=Someshwara+Temple+Kolanupaka+Telangana",
        "color": "#2e7d32",
        "description": "The Rambhapuri Peetha, also known as the Shri Jagadguru Rambhapuri Veerasimhasana Mahasamsthana Peetha, is considered the first among the five Pancha Mahapeethas of the Veerashaiva tradition. It is situated on the banks of the Bhadra River in the lush scenic town of Balehonnur, often called the 'Kashmir of Karnataka'.",
        "history": "The Peetha was established by Shri Jagadguru Renukacharyaji, who according to tradition emerged from the Someshwar Linga at Kollipaki (in present-day Andhra Pradesh). He traveled to Malayachala, the historical name for present-day Balehonnur, and established this sacred seat.\n\nThe lineage of the Peetha spans thousands of years, with the current Jagadguru being the 121st in the succession. The Peetha is central to the Veerashaiva faith and its history is deeply linked to the propagation of the Siddhanta Shikhamani, the religious text of Veerashaivism.\n\nThe Peetha is renowned for its annual Dasara Darbar and various social, cultural, and educational initiatives that serve the community.",
        "order": 1,
        
        # Kannada
        "name_kn": "ರಂಭಾಪುರಿ ಪೀಠ",
        "acharya_kn": "ಜಗದ್ಗುರು ರೇಣುಕಾಚಾರ್ಯ",
        "simhasana_kn": "ವೀರ ಸಿಂಹಾಸನ",
        "location_kn": "ಬಾಳೆಹೊನ್ನೂರು, ಚಿಕ್ಕಮಗಳೂರು",
        "current_swamiji_kn": "ಶ್ರೀ ಶ್ರೀ ಶ್ರೀ ಜಗದ್ಗುರು ಪ್ರಸನ್ನ ರೇಣುಕಾ ವೀರ ಸೋಮೇಶ್ವರ ರಾಜದೇಶಿಕೇಂದ್ರ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮೀಜಿ",
        "associated_linga_kn": "ಸೋಮೇಶ್ವರ ಲಿಂಗ",
        "description_kn": "ರಂಭಾಪುರಿ ಪೀಠವು ವೀರಶೈವ ಸಂಪ್ರದಾಯದ ಪಂಚ ಮಹಾಪೀಠಗಳಲ್ಲಿ ಮೊದಲನೆಯದಾಗಿದೆ. ಇದು ಭದ್ರಾ ನದಿಯ ದಂಡೆಯ ಮೇಲಿರುವ ಸುಂದರವಾದ ಬಾಳೆಹೊನ್ನೂರಿನಲ್ಲಿದೆ.",
        "history_kn": "ಈ ಪೀಠವನ್ನು ಶ್ರೀ ಜಗದ್ಗುರು ರೇಣುಕಾಚಾರ್ಯರು ಸ್ಥಾಪಿಸಿದರು. ಇವರು ಕೊಳ್ಳಿಪಾಕಿಯ ಸೋಮೇಶ್ವರ ಲಿಂಗದಿಂದ ಉದ್ಭವಿಸಿದವರು ಎಂದು ನಂಬಲಾಗಿದೆ. ರಂಭಾಪುರಿ ಪೀಠವು ವೀರಶೈವ ಧರ್ಮದ ಪ್ರಚಾರದಲ್ಲಿ ಪ್ರಮುಖ ಪಾತ್ರ ವಹಿಸಿದೆ.",

        # Marathi
        "name_mr": "रंभापुरी पीठ",
        "acharya_mr": "जगद्गुरु रेणुकाचार्य",
        "simhasana_mr": "वीर सिंहासन",
        "location_mr": "बालेहोन्नूर, चिकमगलूर",
        "current_swamiji_mr": "श्री श्री श्री जगद्गुरु प्रसन्न रेणुका वीर सोमेश्वर राजदेशिकेंद्र शिवाचार्य महास्वामीजी",
        "associated_linga_mr": "सोमेश्वर लिंग",
        "description_mr": "रंभापुरी पीठ वीरशैव परंपरा के पांच महापीठों में पहला है। यह भद्रा नदी के तट पर स्थित बालेहोन्नूर में स्थित है।",
        "history_mr": "इस पीठ की स्थापना श्री जगद्गुरु रेणुकाचार्यजी ने की थी। पौराणिक कथा के अनुसार, वे कोल्लीपाकी के सोमेश्वर लिंग से प्रकट हुए थे। वीरशैव धर्म के प्रचार और सिद्धांत शिखामणि के संरक्षण में इस पीठ का विशेष योगदान है।",

        # Hindi
        "name_hi": "रंभापुरी पीठ",
        "acharya_hi": "जगद्गुरु रेणुकाचार्य",
        "simhasana_hi": "वीर सिंहासन",
        "location_hi": "बालेहोन्नूर, चिकमगलूर",
        "current_swamiji_hi": "श्री श्री श्री जगद्गुरु प्रसन्न रेणुका वीर सोमेश्वर राजदेशिकेंद्र शिवाचार्य महास्वामीजी",
        "associated_linga_hi": "सोमेश्वर लिंग",
        "description_hi": "रंभापुरी पीठ वीरशैव परंपरा के पांच महापीठों में प्रथम है। यह कर्नाटक के चिकमगलूर जिले में भद्रा नदी के तट पर बालेहोन्नूर में स्थित है।",
        "history_hi": "इस पीठ की स्थापना श्री जगद्गुरु रेणुकाचार्य जी द्वारा की गई थी। परंपरा के अनुसार वे कोल्लीपाकी के सोमेश्वर लिंग से प्रकट हुए थे और मलेयाचल (बालेहोन्नूर) में इस पीठ की स्थापना की थी।"
    },
    {
        "name": "Ujjaini Peetha",
        "slug": "ujjaini",
        "acharya": "Jagadguru Marulasiddheshwara (Darukacharya)",
        "simhasana": "Saddharma Simhasana",
        "location": "Ujjaini, Kudligi Taluk, Vijayanagara District",
        "state": "Karnataka",
        "current_swamiji": "Jagadguru Sri Siddalinga Rajadeshikendra Shivacharya Bhagavatpada Swamiji",
        "associated_linga": "Siddheshvara Linga",
        "associated_linga_map_url": "https://maps.google.com/?q=Ujjain+Madhya+Pradesh",
        "color": "#c62828",
        "description": "The Ujjaini Saddharma Simhasana Mahapeetha is one of the five ancient Panchapeethas of Veerashaivism. It is located in the historic town of Ujjaini in Karnataka, known for its remarkable temple architecture and sculptures.",
        "history": "The Peetha is traditionally attributed to Sri Marulasiddheshwara, who is considered a contemporary of the 12th-century philosopher Basaveshwara. The lineage of the Peetha traces back to ancient times, with spiritual origins linked to the original Saddharma Peetha in Ujjain, Madhya Pradesh.\n\nAccording to tradition, the Peetha was moved from Madhya Pradesh to its current location in Karnataka around the 15th century during the time of Jagadguru Marulasiddha Shivacharya.\n\nThe site is home to the ancient Marulasiddheshwara Temple, famous for its architecture and the unique 'Shikara Thailabhisheka' tradition, where oil is offered to the temple's pinnacle annually. There is a famous saying: 'Ujjaini Olage nodu, Hampi Horage Nodu' — look at Ujjaini for its interior beauty, and look at Hampi for its exterior landscape.",
        "order": 2,

        # Kannada
        "name_kn": "ಉಜ್ಜಯಿನಿ ಪೀಠ",
        "acharya_kn": "ಜಗದ್ಗುರು ಮರುಳಸಿದ್ದೇಶ್ವರ (ದಾರುಕಾಚಾರ್ಯ)",
        "simhasana_kn": "ಸದ್ಧರ್ಮ ಸಿಂಹಾಸನ",
        "location_kn": "ಉಜ್ಜಯಿನಿ, ಕುಡ್ಲಿಗಿ, ವಿಜಯನಗರ",
        "current_swamiji_kn": "ಜಗದ್ಗುರು ಶ್ರೀ ಸಿದ್ಧಲಿಂಗ ರಾಜದೇಶಿಕೇಂದ್ರ ಶಿವಾಚಾರ್ಯ ಭಗವತ್ಪಾದ ಸ್ವಾಮೀಜಿ",
        "associated_linga_kn": "ಸಿದ್ದೇಶ್ವರ ಲಿಂಗ",
        "description_kn": "ಉಜ್ಜಯಿನಿ ಸದ್ಧರ್ಮ ಸಿಂಹಾಸನ ಮಹಾಪೀಠವು ವೀರಶೈವ ಧರ್ಮದ ಪಂಚಪೀಠಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ. ಇದು ಕರ್ನಾಟಕದ ವಿಜಯನಗರ ಜಿಲ್ಲೆಯ ಉಜ್ಜಯಿನಿಯಲ್ಲಿದೆ.",
        "history_kn": "ಈ ಪೀಠವು ಶ್ರೀ ಮರುಳಸಿದ್ದೇಶ್ವರರಿಗೆ ಸಂಬಂಧಿಸಿದೆ. ಈ ಪೀಠದ ಪರಂಪರೆಯು ಅತ್ಯಂತ ಪುರಾತನವಾಗಿದ್ದು, ಮಧ್ಯಪ್ರದೇಶದ ಉಜ್ಜಯಿನಿಯ ಮೂಲ ಪೀಠದೊಂದಿಗೆ ಆಧ್ಯಾತ್ಮಿಕ ಸಂಪರ್ಕ ಹೊಂದಿದೆ. ನಂತರ ೧೫ನೇ ಶತಮಾನದಲ್ಲಿ ಇದನ್ನು ಕರ್ನಾಟಕದ ಪ್ರಸ್ತುತ ಸ್ಥಳಕ್ಕೆ ವರ್ಗಾಯಿಸಲಾಯಿತು ಎಂದು ನಂಬಲಾಗಿದೆ.",

        # Marathi
        "name_mr": "उज्जैनी पीठ",
        "acharya_mr": "जगद्गुरु मरुळसिद्धेश्वर (दारुकाचार्य)",
        "simhasana_mr": "सद्धर्म सिंहासन",
        "location_mr": "उज्जैनी, विजयनगर",
        "current_swamiji_mr": "जगद्गुरु श्री सिद्धलिंग राजदेशिकेंद्र शिवाचार्य भगवत्पाद स्वामीजी",
        "associated_linga_mr": "सिद्धेश्वर लिंग",
        "description_mr": "उज्जैनी सद्धर्म सिंहासन महापीठ वीरशैव संप्रदाय के पांच प्राचीन पीठों में से एक है। यह कर्नाटक के विजयनगर जिले में स्थित है।",
        "history_mr": "यह पीठ श्री मरुळसिद्धेश्वर महाराज से संबंधित है। परंपरा के अनुसार, इस पीठ का आध्यात्मिक संबंध मध्य प्रदेश के उज्जैन से है, जिसे बाद में कर्नाटक में स्थानांतरित किया गया। यहाँ का मरुळसिद्धेश्वर मंदिर अपनी सुंदर वास्तुकला के लिए प्रसिद्ध है।",

        # Hindi
        "name_hi": "उज्जैनी पीठ",
        "acharya_hi": "जगद्गुरु मरुळसिद्धेश्वर (दारुकाचार्य)",
        "simhasana_hi": "सद्धर्म सिंहासन",
        "location_hi": "उज्जैनी, विजयनगर",
        "current_swamiji_hi": "जगद्गुरु श्री सिद्धलिंग राजदेशिकेंद्र शिवाचार्य भगवत्पाद स्वामीजी",
        "associated_linga_hi": "सिद्धेश्वर लिंग",
        "description_hi": "उज्जैनी सद्धर्म सिंहासन महापीठ वीरशैव संप्रदाय के प्राचीन पांच पीठों में से एक है। यह ऐतिहासिक शहर उज्जैनी, कर्नाटक में स्थित है।",
        "history_hi": "यह पीठ श्री मरुळसिद्धेश्वर को समर्पित है। इसका इतिहास प्राचीन काल से जुड़ा हुआ है। माना जाता है कि १५वीं शताब्दी में इसे मध्य प्रदेश से कर्नाटक के वर्तमान स्थान पर स्थानांतरित किया गया था।"
    },
    {
        "name": "Kedara Peetha",
        "slug": "kedara",
        "acharya": "Jagadguru Ekoramaradhya",
        "simhasana": "Vairagya Simhasana",
        "location": "Kedarnath, Uttarakhand",
        "state": "Uttarakhand",
        "current_swamiji": "Jagadguru Kedar Ling Maharaj (325th Jagadguru Rawal)",
        "associated_linga": "Kedara Linga",
        "associated_linga_map_url": "https://maps.google.com/?q=Kedarnath+Temple+Uttarakhand",
        "color": "#1565c0",
        "description": "The Kedara Peetha, also known as the Himavat Kedar Vairagyapeeth, is one of the five ancient Pancha Mahapeethas. It is associated with the sacred Kedarnath Temple in the Himalayas, one of the holiest shrines in Shaivism.",
        "history": "The Veerashaiva tradition identifies this Peetha as having been established by Ekoramaradhya, who emerged from one of the five heads of Lord Shiva. The Kedara Peetha holds a unique connection to the Kedarnath temple — the head priest (Raval) of the Kedarnath temple traditionally belongs to the Veerashaiva community from Karnataka.\n\nThe spiritual seat is centered at the Kedarnath Temple in Uttarakhand, while the administrative and monastic activities also involve the Omkareshwar Temple in Ukhimath, which serves as the winter seat of the Kedarnath deity.\n\nIn early 2026, the 324th Jagadguru, Bhimashankar Ling Shivacharya Mahaswamiji, announced his decision to step aside, and Kedar Ling Maharaj was named as the 325th Jagadguru Rawal.",
        "order": 3,

        # Kannada
        "name_kn": "ಕೇದಾರ ಪೀಠ",
        "acharya_kn": "ಜಗದ್ಗುರು ಏಕೋರಾಮಾರಾಧ್ಯ",
        "simhasana_kn": "ವೈರಾಗ್ಯ ಸಿಂಹಾಸನ",
        "location_kn": "ಕೇದಾರನಾಥ್, ಉತ್ತರಾಖಂಡ",
        "current_swamiji_kn": "ಜಗದ್ಗುರು ಕೇದಾರ ಲಿಂಗ ಮಹಾರಾಜ್ (೩೨೫ನೇ ರಾವಲ್)",
        "associated_linga_kn": "ಕೇದಾರ ಲಿಂಗ",
        "description_kn": "ಕೇದಾರ ಪೀಠವು ಹಿಮಾಲಯದ ಪವಿತ್ರ ಕೇದಾರನಾಥ ಕ್ಷೇತ್ರದೊಂದಿಗೆ ನಿಕಟ ಸಂಪರ್ಕ ಹೊಂದಿರುವ ವೀರಶೈವ ಧರ್ಮದ ಪುರಾತನ ಪೀಠವಾಗಿದೆ.",
        "history_kn": "ಶ್ರೀ ಏಕೋರಾಮಾರಾಧ್ಯರು ಈ ಪೀಠವನ್ನು ಸ್ಥಾಪಿಸಿದರು. ಕೇದಾರನಾಥ ಜ್ಯೋತಿರ್ಲಿಂಗದ ಮುಖ್ಯ ಅರ್ಚಕರಾದ 'ರಾವಲ್' ಸಾಂಪ್ರದಾಯಿಕವಾಗಿ ವೀರಶೈವ ಸಮುದಾಯಕ್ಕೆ ಸೇರಿದವರಾಗಿರುತ್ತಾರೆ. ಚಳಿಗಾಲದಲ್ಲಿ ಕೇದಾರನಾಥ ದೇವರ ಪೂಜೆಯು ಉಖೀಮಠದ ಓಂಕಾರೇಶ್ವರ ದೇವಸ್ಥಾನದಲ್ಲಿ ನಡೆಯುತ್ತದೆ.",

        # Marathi
        "name_mr": "केदार पीठ",
        "acharya_mr": "जगद्गुरु एकोरामाराध्य",
        "simhasana_mr": "वैराग्य सिंहासन",
        "location_mr": "केदारनाथ, उत्तराखंड",
        "current_swamiji_mr": "जगद्गुरु केदार लिंग महाराज (३२५ वे रावल)",
        "associated_linga_mr": "केदार लिंग",
        "description_mr": "केदार पीठ, जिसे हिमवत केदार वैराग्य पीठ भी कहा जाता है, हिमालयातील केदारनाथ मंदिराशी संबंधित वीरशैव धर्माचे एक पवित्र पीठ आहे।",
        "history_mr": "या पीठाची स्थापना जगद्गुरु एकोरामाराध्य यांनी केली होती. केदारनाथ मंदिराचे मुख्य पुजारी (रावल) हे ऐतिहासिक काळापासून कर्नाटकच्या वीरशैव संप्रदायातील असतात. हिवाळ्यात केदारनाथची पूजा उखीमठ येथे केली जाते.",

        # Hindi
        "name_hi": "केदार पीठ",
        "acharya_hi": "जगद्गुरु एकोरामाराध्य",
        "simhasana_hi": "वैराग्य सिंहासन",
        "location_hi": "केदारनाथ, उत्तराखंड",
        "current_swamiji_hi": "जगद्गुरु केदार लिंग महाराज (३२५वें रावल)",
        "associated_linga_hi": "केदार लिंग",
        "description_hi": "केदार पीठ, जिसे हिमवत केदार वैराग्यपीठ भी कहा जाता है, हिमालय में पवित्र केदारनाथ मंदिर से जुड़ा एक अत्यंत प्राचीन वीरशैव महापीठ है।",
        "history_hi": "इस पीठ की स्थापना श्री एकोरामाराध्य जी द्वारा की गई थी। इस पीठ का केदारनाथ मंदिर के साथ एक विशेष संबंध है - मंदिर के मुख्य पुजारी (रावल) पारंपरिक रूप से कर्नाटक के वीरशैव समुदाय से होते हैं।"
    },
    {
        "name": "Srisaila Peetha",
        "slug": "srisaila",
        "acharya": "Jagadguru Panditaradhya",
        "simhasana": "Surya Simhasana",
        "location": "Srisailam, Nallamala Hills, Nandyal District",
        "state": "Andhra Pradesh",
        "current_swamiji": "Sri Chinnasiddharama Panditaradhya Shivacharya Mahaswami (32nd Peethadhipathi)",
        "associated_linga": "Mallikarjuna Linga",
        "associated_linga_map_url": "https://maps.google.com/?q=Mallikarjuna+Temple+Srisailam+Andhra+Pradesh",
        "color": "#ffffff",
        "description": "The Srisaila Peetha, also known as the Surya Simhasana, is located at Srisailam in the Nallamala Hills of Andhra Pradesh. Srisailam is both one of the twelve Jyotirlingas and one of the eighteen Shakti Peethas, making it one of the holiest shrines in all of Hinduism.",
        "history": "Srisailam is deeply revered in the Veerashaiva tradition. It is associated with Panditaradhya, one of the Panchacharyas who originated from the five Sthavaralingas. The site has been a center for Veerashaiva scholars and saints, including the famous saint Palkuriki Somanatha.\n\nThe site has been venerated for centuries, with inscriptional evidence dating back to the Satavahana dynasty (2nd century CE). It has been patronized by numerous dynasties including the Kadambas, Chalukyas, Kakatiyas, the Vijayanagara Empire (notably Harihara II), and the Maratha ruler Chhatrapati Shivaji.\n\nThe main Mallikarjuna Swamy and Bhramaramba Devi temple is managed by the Srisaila Devasthanam under the government of Andhra Pradesh.",
        "order": 4,

        # Kannada
        "name_kn": "ಶ್ರೀಶೈಲ ಪೀಠ",
        "acharya_kn": "ಜಗದ್ಗುರು ಪಂಡಿತಾರಾಧ್ಯ",
        "simhasana_kn": "ಸೂರ್ಯ ಸಿಂಹಾಸನ",
        "location_kn": "ಶ್ರೀಶೈಲಂ, ಆಂಧ್ರಪ್ರದೇಶ",
        "current_swamiji_kn": "ಶ್ರೀ ಚನ್ನಸಿದ್ಧರಾಮ ಪಂಡಿತಾರಾಧ್ಯ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮಿಗಳು (೩೨ನೇ ಪೀಠಾಧಿಪತಿ)",
        "associated_linga_kn": "ಮಲ್ಲಿಕಾರ್ಜುನ ಲಿಂಗ",
        "description_kn": "ಶ್ರೀಶೈಲ ಪೀಠವು ಆಂಧ್ರಪ್ರದೇಶದ ಶ್ರೀಶೈಲಂನ ಮಲ್ಲಿಕಾರ್ಜುನ ಜ್ಯೋತಿರ್ಲಿಂಗ ಕ್ಷೇತ್ರದಲ್ಲಿ ಸ್ಥಾಪಿತವಾಗಿರುವ ವೀರಶೈವ ಧರ್ಮದ ಪುರಾತನ ಸೂರ್ಯ ಸಿಂಹಾಸನ ಪೀಠವಾಗಿದೆ.",
        "history_kn": "ಈ ಪೀಠವು ಜಗದ್ಗುರು ಪಂಡಿತಾರಾಧ್ಯರಿಂದ ಸ್ಥಾಪಿಸಲ್ಪಟ್ಟಿತು. ಶ್ರೀಶೈಲ ಕ್ಷೇತ್ರವು ಇತಿಹಾಸದಲ್ಲಿ ಕದಂಬರು, ಚಾಲುಕ್ಯರು, ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯದ ಹರಿಹರ ರಾಜರು ಮತ್ತು ಛತ್ರಪತಿ ಶಿವಾಜಿ ಮಹಾರಾಜರಿಂದ ಪೋಷಿಸಲ್ಪಟ್ಟಿದೆ.",

        # Marathi
        "name_mr": "श्रीशैल पीठ",
        "acharya_mr": "जगद्गुरु पंडिताराध्य",
        "simhasana_mr": "सूर्य सिंहासन",
        "location_mr": "श्रीशैलम, आंध्र प्रदेश",
        "current_swamiji_mr": "श्री चन्नसिद्धराम पंडिताराध्य शिवाचार्य महास्वामी (३२ वे पीठाधिपती)",
        "associated_linga_mr": "मल्लिकार्जुन लिंग",
        "description_mr": "श्रीशैल पीठ (सूर्य सिंहासन) हे आंध्र प्रदेशातील मल्लिकार्जुन ज्योतिर्लिंग क्षेत्रात असलेले एक अत्यंत पवित्र आणि प्राचीन पीठ आहे।",
        "history_mr": "या पीठाचा संबंध जगद्गुरु पंडिताराध्यांशी आहे. छत्रपती शिवाजी महाराज, हरिहर राजा आणि अनेक ऐतिहासिक राजवंशांनी या पवित्र मंदिराचे संवर्धन व संरक्षण केले होते.",

        # Hindi
        "name_hi": "श्रीशैल पीठ",
        "acharya_hi": "जगद्गुरु पंडिताराध्य",
        "simhasana_hi": "सूर्य सिंहासन",
        "location_hi": "श्रीशैलम, आंध्र प्रदेश",
        "current_swamiji_hi": "श्री चन्नसिद्धराम पंडिताराध्य शिवाचार्य महास्वामी (३२वें पीठाधिपति)",
        "associated_linga_hi": "मल्लिकार्जुन लिंग",
        "description_hi": "श्रीशैल पीठ, जिसे सूर्य सिंहासन भी कहा जाता है, आंध्र प्रदेश के श्रीशैलम में मल्लिकार्जुन ज्योतिर्लिंग और शक्तिपीठ क्षेत्र में स्थित है।",
        "history_hi": "यह पीठ जगद्गुरु पंडिताराध्य जी से जुड़ी हुई है। ऐतिहासिक रूप से इसे विजयनगर साम्राज्य, चालुक्य और मराठा शासक छत्रपति शिवाजी महाराज द्वारा संरक्षण दिया गया था।"
    },
    {
        "name": "Kashi Peetha",
        "slug": "kashi",
        "acharya": "Jagadguru Vishwaradhya",
        "simhasana": "Jnana Simhasana",
        "location": "Varanasi (Kashi)",
        "state": "Uttar Pradesh",
        "current_swamiji": "Jagadguru Dr. Mallikarjuna Vishwaradhya Shivacharya Mahaswamiji",
        "associated_linga": "Vishveshvara Linga",
        "associated_linga_map_url": "https://maps.google.com/?q=Kashi+Vishwanath+Temple+Varanasi+Uttar+Pradesh",
        "color": "#f9a825",
        "description": "The Kashi Peetha, widely known as the Jangamwadi Math, is one of the five major Veerashaiva Peethas. Located in the ancient holy city of Varanasi, it serves as a spiritual center and is renowned for its vast collection of Shivalingas.",
        "history": "According to tradition, Jagadguru Vishwaradhya Shivacharya Bhagavatpadji manifested from the Kashi Vishveshwar Jyotirlinga on Mahashivaratri and established this Jnana Peetha to propagate Veerashaiva philosophy.\n\nHistorical records indicate the math has existed for well over a millennium. A notable historical copper plate (danapatra) from 574 A.D. records a land grant made by King Jayananda Deo to the math, providing concrete evidence of its antiquity.\n\nThe Peetha serves as a spiritual center for followers of the Veerashaiva sect, particularly those from Karnataka and Maharashtra. It follows a traditional Guru-Shishya succession and is renowned for preserving and teaching the ancient Veerashaiva philosophy.",
        "order": 5,

        # Kannada
        "name_kn": "ಕಾಶಿ ಪೀಠ",
        "acharya_kn": "ಜಗದ್ಗುರು ವಿಶ್ವಾರಾಧ್ಯ",
        "simhasana_kn": "ಜ್ಞಾನ ಸಿಂಹಾಸನ",
        "location_kn": "ವಾರಣಾಸಿ (ಕಾಶಿ)",
        "current_swamiji_kn": "ಜಗದ್ಗುರು ಡಾ. ಮಲ್ಲಿಕಾರ್ಜುನ ವಿಶ್ವಾರಾಧ್ಯ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮೀಜಿ",
        "associated_linga_kn": "ವಿಶ್ವೇಶ್ವರ ಲಿಂಗ",
        "description_kn": "ಕಾಶಿ ಪೀಠವು ವಾರಣಾಸಿಯ ಜಂಗಮವಾಡಿ ಮಠ ಎಂದು ಪ್ರಸಿದ್ಧವಾಗಿದೆ. ಇದು ವೀರಶೈವ ಪಂಚಪೀಠಗಳಲ್ಲಿ ಪ್ರಮುಖವಾಗಿದ್ದು, ಲಕ್ಷಾಂತರ ಶಿವಲಿಂಗಗಳನ್ನು ಹೊಂದಿರುವ ಮಠವಾಗಿದೆ.",
        "history_kn": "ಮಹಾಶಿವರಾತ್ರಿಯಂದು ಕಾಶಿ ವಿಶ್ವೇಶ್ವರ ಜ್ಯೋತಿರ್ಲಿಂಗದಿಂದ ಜಗದ್ಗುರು ವಿಶ್ವಾರಾಧ್ಯರು ಪ್ರಕಟಗೊಂಡು ಜ್ಞಾನ ಪೀಠವನ್ನು ಸ್ಥಾಪಿಸಿದರು. ಈ ಮಠವು ಸಾವಿರ ವರ್ಷಗಳಿಗಿಂತಲೂ ಹೆಚ್ಚು ಇತಿಹಾಸ ಹೊಂದಿದ್ದು, ಕ್ರಿ.ಶ ೫೭೪ರ ತಾಮ್ರಶಾಸನವು ರಾಜ ಜಯನಂದ ದೇವರ ಭೂದಾನವನ್ನು ಉಲ್ಲೇಖಿಸುತ್ತದೆ.",

        # Marathi
        "name_mr": "काशी पीठ",
        "acharya_mr": "जगद्गुरु विश्वाराध्य",
        "simhasana_mr": "ज्ञान सिंहासन",
        "location_mr": "वाराणसी (काशी)",
        "current_swamiji_mr": "जगद्गुरु डॉ. मल्लिकार्जुन विश्वाराध्य शिवाचार्य महास्वामीजी",
        "associated_linga_mr": "विश्वेश्वर लिंग",
        "description_mr": "काशी पीठ (जंगमवाडी मठ) हे वाराणसी (काशी) मधील सर्वात जुने आणि महत्त्वपूर्ण वीरशैव पीठ आहे, जिथे लाखो शिवलिंगांचा संग्रह आहे।",
        "history_mr": "शिवरात्रीला काशी विश्वेश्वर ज्योतिर्लिंगातून प्रकट झालेल्या जगद्गुरु विश्वाराध्यांनी या पीठाची स्थापना केली. इसवी सन ५७४ मधील राजा जयानंद देव यांच्या ताम्रपटावरून या मठाची प्राचीनता सिद्ध होते.",

        # Hindi
        "name_hi": "काशी पीठ",
        "acharya_hi": "जगद्गुरु विश्वाराध्य",
        "simhasana_hi": "ज्ञान सिंहासन",
        "location_hi": "वाराणसी (काशी)",
        "current_swamiji_hi": "जगद्गुरु डॉ. मल्लिकार्जुन विश्वाराध्य शिवाचार्य महास्वामीजी",
        "associated_linga_hi": "विश्वेश्वर लिंग",
        "description_hi": "काशी पीठ, जिसे जंगमवाड़ी मठ के रूप में जाना जाता है, वाराणसी का एक प्रसिद्ध आध्यात्मिक और ऐतिहासिक वीरशैव महापीठ है, जो अपने अनगिनत शिवलिंगों के लिए प्रसिद्ध है।",
        "history_hi": "इस ज्ञान पीठ की स्थापना जगद्गुरु विश्वाराध्य जी ने की थी। इतिहास के अनुसार, इस मठ का अस्तित्व सदियों पुराना है। ५७४ ईस्वी का एक तांबे का दानपत्र इस मठ की प्राचीनता का ऐतिहासिक प्रमाण है।"
    },
]

class Command(BaseCommand):
    help = "Seeds the database with the 5 Pancha Peethas data and multi-lingual translations"

    def handle(self, *args, **options):
        for data in PEETHAS_DATA:
            obj, created = Peetha.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"  {status}: {obj.name}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! {Peetha.objects.count()} Peethas in database."))
