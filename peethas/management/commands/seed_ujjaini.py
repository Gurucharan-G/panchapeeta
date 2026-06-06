from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHA_DATA = {
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
    "name_kn": "ಉಜ್ಜಯಿನಿ ಪೀಠ",
    "acharya_kn": "ಜಗದ್ಗುರು ಮರುಳಸಿದ್ದೇಶ್ವರ (ದಾರುಕಾಚಾರ್ಯ)",
    "simhasana_kn": "ಸದ್ಧರ್ಮ ಸಿಂಹಾಸನ",
    "location_kn": "ಉಜ್ಜಯಿನಿ, ಕುಡ್ಲಿಗಿ, ವಿಜಯನಗರ",
    "current_swamiji_kn": "ಜಗದ್ಗುರು ಶ್ರೀ ಸಿದ್ಧಲಿಂಗ ರಾಜದೇಶಿಕೇಂದ್ರ ಶಿವಾಚಾರ್ಯ ಭಗವತ್ಪಾದ ಸ್ವಾಮೀಜಿ",
    "associated_linga_kn": "ಸಿದ್ದೇಶ್ವರ ಲಿಂಗ",
    "description_kn": "ಉಜ್ಜಯಿನಿ ಸದ್ಧರ್ಮ ಸಿಂಹಾಸನ ಮಹಾಪೀಠವು ವೀರಶೈವ ಧರ್ಮದ ಪಂಚಪೀಠಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ. ಇದು ಕರ್ನಾಟಕದ ವಿಜಯನಗರ ಜಿಲ್ಲೆಯ ಉಜ್ಜಯಿನಿಯಲ್ಲಿದೆ.",
    "history_kn": "ಈ ಪೀಠವು ಶ್ರೀ ಮರುಳಸಿದ್ದೇಶ್ವರರಿಗೆ ಸಂಬಂಧಿಸಿದೆ. ಈ ಪೀಠದ ಪರಂಪರೆಯು ಅತ್ಯಂತ ಪುರಾತನವಾಗಿದ್ದು, ಮಧ್ಯಪ್ರದೇಶದ ಉಜ್ಜಯಿನಿಯ ಮೂಲ ಪೀಠದೊಂದಿಗೆ ಆಧ್ಯಾತ್ಮಿಕ ಸಂಪರ್ಕ ಹೊಂದಿದೆ. ನಂತರ ೧೫ನೇ ಶತಮಾನದಲ್ಲಿ ಇದನ್ನು ಕರ್ನಾಟಕದ ಪ್ರಸ್ತುತ ಸ್ಥಳಕ್ಕೆ ವರ್ಗಾಯಿಸಲಾಯಿತು ಎಂದು ನಂಬಲಾಗಿದೆ.",
    "name_mr": "उज्जैनी पीठ",
    "acharya_mr": "जगद्गुरु मरुळसिद्धेश्वर (दारुकाचार्य)",
    "simhasana_mr": "सद्धर्म सिंहासन",
    "location_mr": "उज्जैनी, विजयनगर",
    "current_swamiji_mr": "जगद्गुरु श्री सिद्धलिंग राजदेशिकेंद्र शिवाचार्य भगवत्पाद स्वामीजी",
    "associated_linga_mr": "सिद्धेश्वर लिंग",
    "description_mr": "उज्जैनी सद्धर्म सिंहासन महापीठ वीरशैव संप्रदाय के पांच प्राचीन पीठों में से एक है। यह कर्नाटक के विजयनगर जिले में स्थित है।",
    "history_mr": "यह पीठ श्री मरुळसिद्धेश्वर महाराज से संबंधित है। परंपरा के अनुसार, इस पीठ का आध्यात्मिक संबंध मध्य प्रदेश के उज्जैन से है, जिसे बाद में कर्नाटक में स्थानांतरित किया गया। यहाँ का मरुळसिद्धेश्वर मंदिर अपनी सुंदर वास्तुकला के लिए प्रसिद्ध है।",
    "name_hi": "उज्जैनी पीठ",
    "acharya_hi": "जगद्गुरु मरुळसिद्धेश्वर (दारुकाचार्य)",
    "simhasana_hi": "सद्धर्म सिंहासन",
    "location_hi": "उज्जैनी, विजयनगर",
    "current_swamiji_hi": "जगद्गुरु श्री सिद्धलिंग राजदेशिकेंद्र शिवाचार्य भगवत्पाद स्वामीजी",
    "associated_linga_hi": "सिद्धेश्वर लिंग",
    "description_hi": "उज्जैनी सद्धर्म सिंहासन महापीठ वीरशैव संप्रदाय के प्राचीन पांच पीठों में से एक है। यह ऐतिहासिक शहर उज्जैनी, कर्नाटक में स्थित है।",
    "history_hi": "यह पीठ श्री मरुळसिद्धेश्वर को समर्पित है। इसका इतिहास प्राचीन काल से जुड़ा हुआ है। माना जाता है कि १५वीं शताब्दी में इसे मध्य प्रदेश से कर्नाटक के वर्तमान स्थान पर स्थानांतरित किया गया था।"
}

class Command(BaseCommand):
    help = "Seeds/updates the database record for Ujjaini Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {status}: {obj.name}"))
