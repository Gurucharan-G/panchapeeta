from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHA_DATA = {
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
    "name_kn": "ಕೇದಾರ ಪೀಠ",
    "acharya_kn": "ಜಗದ್ಗುರು ಏಕೋರಾಮಾರಾಧ್ಯ",
    "simhasana_kn": "ವೈರಾಗ್ಯ ಸಿಂಹಾಸನ",
    "location_kn": "ಕೇದಾರನಾಥ್, ಉತ್ತರಾಖಂಡ",
    "current_swamiji_kn": "ಜಗದ್ಗುರು ಕೇದಾರ ಲಿಂಗ ಮಹಾರಾಜ್ (೩೨೫ನೇ ರಾವಲ್)",
    "associated_linga_kn": "ಕೇದಾರ ಲಿಂಗ",
    "description_kn": "ಕೇದಾರ ಪೀಠವು ಹಿಮಾಲಯದ ಪವಿತ್ರ ಕೇದಾರನಾಥ ಕ್ಷೇತ್ರದೊಂದಿಗೆ ನಿಕಟ ಸಂಪರ್ಕ ಹೊಂದಿರುವ ವೀರಶೈವ ಧರ್ಮದ ಪುರಾತನ ಪೀಠವಾಗಿದೆ.",
    "history_kn": "ಶ್ರೀ ಏಕೋರಾಮಾರಾಧ್ಯರು ಈ ಪೀಠವನ್ನು ಸ್ಥಾಪಿಸಿದರು. ಕೇದಾರನಾಥ ಜ್ಯೋತಿರ್ಲಿಂಗದ ಮುಖ್ಯ ಅರ್ಚಕರಾದ 'ರಾವಲ್' ಸಾಂಪ್ರದಾಯಿಕವಾಗಿ ವೀರಶೈವ ಸಮುದಾಯಕ್ಕೆ ಸೇರಿದವರಾಗಿರುತ್ತಾರೆ. ಚಳಿಗಾಲದಲ್ಲಿ ಕೇದಾರನಾಥ ದೇವರ ಪೂಜೆಯು ಉಖೀಮಠದ ಓಂಕಾರೇಶ್ವರ ದೇವಸ್ಥಾನದಲ್ಲಿ ನಡೆಯುತ್ತದೆ.",
    "name_mr": "केदार पीठ",
    "acharya_mr": "जगद्गुरु एकोरामाराध्य",
    "simhasana_mr": "वैराग्य सिंहासन",
    "location_mr": "केदारनाथ, उत्तराखंड",
    "current_swamiji_mr": "जगद्गुरु केदार लिंग महाराज (३२५ वे रावल)",
    "associated_linga_mr": "केदार लिंग",
    "description_mr": "केदार पीठ, जिसे हिमवत केदार वैराग्य पीठ भी कहा जाता है, हिमालयातील केदारनाथ मंदिराशी संबंधित वीरशैव धर्माचे एक पवित्र पीठ आहे।",
    "history_mr": "या पीठाची स्थापना जगद्गुरु एकोरामाराध्य यांनी केली होती. केदारनाथ मंदिराचे मुख्य पुजारी (रावल) हे ऐतिहासिक काळापासून कर्नाटकच्या वीरशैव संप्रदायातील असतात. हिवाळ्यात केदारनाथची पूजा उखीमठ येथे केली जाते.",
    "name_hi": "केदार पीठ",
    "acharya_hi": "जगद्गुरु एकोरामाराध्य",
    "simhasana_hi": "वैराग्य सिंहासन",
    "location_hi": "केदारनाथ, उत्तराखंड",
    "current_swamiji_hi": "जगद्गुरु केदार लिंग महाराज (३२५वें रावल)",
    "associated_linga_hi": "केदार लिंग",
    "description_hi": "केदार पीठ, जिसे हिमवत केदार वैराग्यपीठ भी कहा जाता है, हिमालय में पवित्र केदारनाथ मंदिर से जुड़ा एक अत्यंत प्राचीन वीरशैव महापीठ है।",
    "history_hi": "इस पीठ की स्थापना श्री एकोरामाराध्य जी द्वारा की गई थी। इस पीठ का केदारनाथ मंदिर के साथ एक विशेष संबंध है - मंदिर के मुख्य पुजारी (रावल) पारंपरिक रूप से कर्नाटक के वीरशैव समुदाय से होते हैं।"
}

class Command(BaseCommand):
    help = "Seeds/updates the database record for Kedara Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {status}: {obj.name}"))
