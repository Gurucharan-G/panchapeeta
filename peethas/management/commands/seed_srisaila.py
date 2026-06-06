from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHA_DATA = {
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
    "name_kn": "ಶ್ರೀಶೈಲ ಪೀಠ",
    "acharya_kn": "ಜಗದ್ಗುರು ಪಂಡಿತಾರಾಧ್ಯ",
    "simhasana_kn": "ಸೂರ್ಯ ಸಿಂಹಾಸನ",
    "location_kn": "ಶ್ರೀಶೈಲಂ, ಆಂಧ್ರಪ್ರದೇಶ",
    "current_swamiji_kn": "ಶ್ರೀ ಚನ್ನಸಿದ್ಧರಾಮ ಪಂಡಿತಾರಾಧ್ಯ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮಿಗಳು (೩೨ನೇ ಪೀಠಾಧಿಪತಿ)",
    "associated_linga_kn": "ಮಲ್ಲಿಕಾರ್ಜುನ ಲಿಂಗ",
    "description_kn": "ಶ್ರೀಶೈಲ ಪೀಠವು ಆಂಧ್ರಪ್ರದೇಶದ ಶ್ರೀಶೈಲಂನ ಮಲ್ಲಿಕಾರ್ಜುನ ಜ್ಯೋತಿರ್ಲಿಂಗ ಕ್ಷೇತ್ರದಲ್ಲಿ ಸ್ಥಾಪಿತವಾಗಿರುವ ವೀರಶೈವ ಧರ್ಮದ ಪುರಾತನ ಸೂರ್ಯ ಸಿಂಹಾಸನ ಪೀಠವಾಗಿದೆ.",
    "history_kn": "ಈ ಪೀಠವು ಜಗದ್ಗುರು ಪಂಡಿತಾರಾಧ್ಯರಿಂದ ಸ್ಥಾಪಿಸಲ್ಪಟ್ಟಿತು. ಶ್ರೀಶೈಲ ಕ್ಷೇತ್ರವು ಇತಿಹಾಸದಲ್ಲಿ ಕದಂಬರು, ಚಾಲುಕ್ಯರು, ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯದ ಹರಿಹರ ರಾಜರು ಮತ್ತು ಛತ್ರಪತಿ ಶಿವಾಜಿ ಮಹಾರಾಜರಿಂದ ಪೋಷಿಸಲ್ಪಟ್ಟಿದೆ.",
    "name_mr": "श्रीशैल पीठ",
    "acharya_mr": "जगद्गुरु पंडिताराध्य",
    "simhasana_mr": "सूर्य सिंहासन",
    "location_mr": "श्रीशैलम, आंध्र प्रदेश",
    "current_swamiji_mr": "श्री चन्नसिद्धराम पंडिताराध्य शिवाचार्य महास्वामी (३२ वे पीठाधिपती)",
    "associated_linga_mr": "मल्लिकार्जुन लिंग",
    "description_mr": "श्रीशैल पीठ (सूर्य सिंहासन) हे आंध्र प्रदेशातील मल्लिकार्जुन ज्योतिर्लिंग क्षेत्रात असलेले एक अत्यंत पवित्र आणि प्राचीन पीठ आहे।",
    "history_mr": "या पीठाचा संबंध जगद्गुरु पंडिताराध्यांशी आहे. छत्रपती शिवाजी महाराज, हरिहर राजा आणि अनेक ऐतिहासिक राजवंशांनी या पवित्र मंदिराचे संवर्धन व संरक्षण केले होते.",
    "name_hi": "श्रीशैल पीठ",
    "acharya_hi": "जगद्गुरु पंडिताराध्य",
    "simhasana_hi": "सूर्य सिंहासन",
    "location_hi": "श्रीशैलम, आंध्र प्रदेश",
    "current_swamiji_hi": "श्री चन्नसिद्धराम पंडिताराध्य शिवाचार्य महास्वामी (३२वें पीठाधिपति)",
    "associated_linga_hi": "मल्लिकार्जुन लिंग",
    "description_hi": "श्रीशैल पीठ, जिसे सूर्य सिंहासन भी कहा जाता है, आंध्र प्रदेश के श्रीशैलम में मल्लिकार्जुन ज्योतिर्लिंग और शक्तिपीठ क्षेत्र में स्थित है।",
    "history_hi": "यह पीठ जगद्गुरु पंडिताराध्य जी से जुड़ी हुई है। ऐतिहासिक रूप से इसे विजयनगर साम्राज्य, चालुक्य और मराठा शासक छत्रपति शिवाजी महाराज द्वारा संरक्षण दिया गया था।"
}

class Command(BaseCommand):
    help = "Seeds/updates the database record for Srisaila Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {status}: {obj.name}"))
