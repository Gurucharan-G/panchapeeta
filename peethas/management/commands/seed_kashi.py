from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHA_DATA = {
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
    "name_kn": "ಕಾಶಿ ಪೀಠ",
    "acharya_kn": "ಜಗದ್ಗುರು ವಿಶ್ವಾರಾಧ್ಯ",
    "simhasana_kn": "ಜ್ಞಾನ ಸಿಂಹಾಸನ",
    "location_kn": "ವಾರಣಾಸಿ (ಕಾಶಿ)",
    "current_swamiji_kn": "ಜಗದ್ಗುರು ಡಾ. ಮಲ್ಲಿಕಾರ್ಜುನ ವಿಶ್ವಾರಾಧ್ಯ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮೀಜಿ",
    "associated_linga_kn": "ವಿಶ್ವೇಶ್ವರ ಲಿಂಗ",
    "description_kn": "ಕಾಶಿ ಪೀಠವು ವಾರಣಾಸಿಯ ಜಂಗಮವಾಡಿ ಮಠ ಎಂದು ಪ್ರಸಿದ್ಧವಾಗಿದೆ. ಇದು ವೀರಶೈವ ಪಂಚಪೀಠಗಳಲ್ಲಿ ಪ್ರಮುಖವಾಗಿದ್ದು, ಲಕ್ಷಾಂತರ ಶಿವಲಿಂಗಗಳನ್ನು ಹೊಂದಿರುವ ಮಠವಾಗಿದೆ.",
    "history_kn": "ಮಹಾಶಿವರಾತ್ರಿಯಂದು ಕಾಶಿ ವಿಶ್ವೇಶ್ವರ ಜ್ಯೋತಿರ್ಲಿಂಗದಿಂದ ಜಗದ್ಗುರು ವಿಶ್ವಾರಾಧ್ಯರು ಪ್ರಕಟಗೊಂಡು ಜ್ಞಾನ ಪೀಠವನ್ನು ಸ್ಥಾಪಿಸಿದರು. ಈ ಮಠವು ಸಾವಿರ ವರ್ಷಗಳಿಗಿಂತಲೂ ಹೆಚ್ಚು ಇತಿಹಾಸ ಹೊಂದಿದ್ದು, ಕ್ರಿ.ಶ ೫೭೪ರ ತಾಮ್ರಶಾಸನವು ರಾಜ ಜಯನಂದ ದೇವರ ಭೂದಾನವನ್ನು ಉಲ್ಲೇಖಿಸುತ್ತದೆ.",
    "name_mr": "काशी पीठ",
    "acharya_mr": "जगद्गुरु विश्वाराध्य",
    "simhasana_mr": "ज्ञान सिंहासन",
    "location_mr": "वाराणसी (काशी)",
    "current_swamiji_mr": "जगद्गुरु डॉ. मल्लिकार्जुन विश्वाराध्य शिवाचार्य महास्वामीजी",
    "associated_linga_mr": "विश्वेश्वर लिंग",
    "description_mr": "काशी पीठ (जंगमवाडी मठ) हे वाराणसी (काशी) मधील सर्वात जुने आणि महत्त्वपूर्ण वीरशैव पीठ आहे, जिथे लाखो शिवलिंगांचा संग्रह आहे।",
    "history_mr": "शिवरात्रीला काशी विश्वेश्वर ज्योतिर्लिंगातून प्रकट झालेल्या जगद्गुरु विश्वाराध्यांनी या पीठाची स्थापना केली. इसवी सन ५७४ मधील राजा जयानंद देव यांच्या ताम्रपटावरून या मठाची प्राचीनता सिद्ध होते.",
    "name_hi": "काशी पीठ",
    "acharya_hi": "जगद्गुरु विश्वाराध्य",
    "simhasana_hi": "ज्ञान सिंहासन",
    "location_hi": "वाराणसी (काशी)",
    "current_swamiji_hi": "जगद्गुरु डॉ. मल्लिकार्जुन विश्वाराध्य शिवाचार्य महास्वामीजी",
    "associated_linga_hi": "विश्वेश्वर लिंग",
    "description_hi": "काशी पीठ, जिसे जंगमवाड़ी मठ के रूप में जाना जाता है, वाराणसी का एक प्रसिद्ध आध्यात्मिक और ऐतिहासिक वीरशैव महापीठ है, जो अपने अनगिनत शिवलिंगों के लिए प्रसिद्ध है।",
    "history_hi": "इस ज्ञान पीठ की स्थापना जगद्गुरु विश्वाराध्य जी ने की थी। इतिहास के अनुसार, इस मठ का अस्तित्व सदियों पुराना है। ५७४ ईस्वी का एक तांबे का दानपत्र इस मठ की प्राचीनता का ऐतिहासिक प्रमाण है।"
}

class Command(BaseCommand):
    help = "Seeds/updates the database record for Kashi Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {status}: {obj.name}"))
