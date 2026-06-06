from django.core.management.base import BaseCommand
from peethas.models import Peetha

PEETHA_DATA = {
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
    "description": "The Rambhapuri Peetha, also known as the Shri Jagadguru Rambhapuri Veerasimhasana Mahasamsthana Peetha, is the first and oldest among the five sacred Pancha Mahapeethas of the Veerashaiva tradition. Nestled on the banks of the scenic Bhadra River in the lush green valley of Balehonnur (Chikkamagaluru district), a region widely celebrated as the 'Kashmir of Karnataka', this ancient spiritual seat has guided social, cultural, and educational fields for millennia.",
    "history": "The Peetha was established by the primal Guru, Shri Jagadguru Renukacharyaji, who emerged from the Someshwara Linga at Kollipaki (Kolanupaka in modern Nalgonda district, Telangana). Following divine command, he traveled to the picturesque region of Malayachala (the historical name for Balehonnur) and founded this sacred seat to propagate the eternal message of human welfare and devotion.\n\nAccording to scriptures, Renukacharyaji manifested across yugas: as Sri Jagadguru Ekakshara Shivacharya in Krita Yuga, Sri Jagadguru Ekavera Shivacharya in Treta Yuga, Sri Jagadguru Renuka Shivacharya in Dvapara Yuga, and Sri Jagadguru Revanasiddha Bhagavatpada (Revanasiddha Shivacharya) in Kali Yuga. In Treta Yuga, Renukacharya taught the sacred text of Veerashaivism, 'Siddhanta Shikhamani', to Sage Agastya on the peaks of Malayachala. In Kali Yuga, Revanasiddha Shivacharya traveled widely for 700 years, performing legendary deeds such as presenting the Chandramouleshvara Linga and Ratnagarbha Ganapathi to Adi Shankaracharya, rescuing 12,000 virgins in Kalyan, and humbling Gorakhnath.\n\nThe temple complex features the central shrine of the guardian deity, Sri Veerabhadra Swamy (the Gotrapurusha). Next to it is the Sri Someshwara Temple housing the holy Linga from which Renukacharya manifested. A unique highlight is the presence of the Jodu Nandi (twin Nandi statues) facing the main shrine. Sri Chowdeshwari Devi resides as the powerful protecting goddess of the kshetra. The current pontiff, Shree Shree Shree Jagadguru Prasanna Renuka Veera Someshwara Rajadeshikendra Shivacharya Mahaswamiji, succeeded Veera Rudramuni Shivacharya as the 121st Jagadguru on February 6, 1992, at the age of 36. Under his guidance, the Peetha initiated the landmark 'Eight Point Program' for comprehensive spiritual, social, and educational development.",
    "order": 1,
    "name_kn": "ರಂಭಾಪುರಿ ಪೀಠ",
    "acharya_kn": "ಜಗದ್ಗುರು ರೇಣುಕಾಚಾರ್ಯ",
    "simhasana_kn": "ವೀರ ಸಿಂಹಾಸನ",
    "location_kn": "ಬಾಳೆಹೊನ್ನೂರು, ಚಿಕ್ಕಮಗಳೂರು",
    "current_swamiji_kn": "ಶ್ರೀ ಶ್ರೀ ಶ್ರೀ ಜಗದ್ಗುರು ಪ್ರಸನ್ನ ರೇಣುಕಾ ವೀರ ಸೋಮೇಶ್ವರ ರಾಜದೇಶಿಕೇಂದ್ರ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮೀಜಿ",
    "associated_linga_kn": "ಸೋಮೇಶ್ವರ ಲಿಂಗ",
    "description_kn": "ವೀರಶೈವ ಮಹಾಪಂಚಪೀಠಗಳಲ್ಲಿ ಪ್ರಥಮ ಪೀಠವಾದ ಶ್ರೀ ಜಗದ್ಗುರು ರಂಭಾಪುರಿ ವೀರಸಿಂಹಾಸನ ಮಹಾಸಂಸ್ಥಾನ ಪೀಠವು ಅತ್ಯಂತ ಪ್ರಾಚೀನ ಇತಿಹಾಸ ಹೊಂದಿದೆ. ಚಿಕ್ಕಮಗಳೂರು ಜಿಲ್ಲೆಯ ಭದ್ರಾ ನದಿಯ ತಟದಲ್ಲಿರುವ, 'ಕರ್ನಾಟಕದ ಕಾಶ್ಮೀರ' ಎಂದೇ ಪ್ರಸಿದ್ಧವಾದ ಸುಂದರ ಬಾಳೆಹೊನ್ನೂರಿನಲ್ಲಿ ಈ ಪೀಠವು ಸ್ಥಾಪಿತವಾಗಿದ್ದು, ಧಾರ್ಮಿಕ, ಶೈಕ್ಷಣಿಕ ಮತ್ತು ಸಾಮಾಜಿಕ ಕ್ಷೇತ್ರಗಳಲ್ಲಿ ಆದರ್ಶ ಮಾರ್ಗದರ್ಶಿಯಾಗಿದೆ.",
    "history_kn": "ಈ ಪೀಠವನ್ನು ಆದಿ ಜಗದ್ಗುರು ಶ್ರೀ ರೇಣುಕಾಚಾರ್ಯರು ಸ್ಥಾಪಿಸಿದರು. ಇವರು ಆಂಧ್ರಪ್ರದೇಶದ ನಲಗೊಂಡ ಜಿಲ್ಲೆಯ ಕೊಲನುಪಾಕ ಕ್ಷೇತ್ರದ ಶ್ರೀ ಸೋಮೇಶ್ವರ ಶಿವಲಿಂಗದಿಂದ ಆವೀರ್ಭವಿಸಿದರು. ನಂತರ ಮಲಯಾಚಲದ (ಬಾಳೆಹೊನ್ನೂರು) ಭದ್ರಾ ನದಿ ದಂಡೆಯ ಪವಿತ್ರ ನೆಲೆಯಲ್ಲಿ ಈ ಧರ್ಮಪೀಠವನ್ನು ಸಂಸ್ಥಾಪಿಸಿದರು. ಮಲಯಾಚಲದಲ್ಲಿ ತಪಸ್ಸನ್ನಾಚರಿಸುತ್ತಿದ್ದ ಅಗಸ್ತ್ಯ ಮಹರ್ಷಿಗೆ ರೇಣುಕಾಚಾರ್ಯರು ವೀರಶೈವ ಧರ್ಮದ ಪವಿತ್ರ ಗ್ರಂಥವಾದ 'ಸಿದ್ಧಾಂತ ಶಿಖಾಮಣಿ'ಯನ್ನು ಬೋಧಿಸಿ ಶಿವದೀಕ್ಷೆಯನ್ನಿತ್ತರು.\n\nರೇಣುಕಾಚಾರ್ಯರು ಕೃತಯುಗದಲ್ಲಿ ಶ್ರೀ ಜಗದ್ಗುರು ಏಕಾಕ್ಷರ ಶಿವಾಚಾರ್ಯರಾಗಿ, ತ್ರೇತಾಯುಗದಲ್ಲಿ ಶ್ರೀ ಜಗದ್ಗುರು ಏಕವರ ಶಿವಾಚಾರ್ಯರಾಗಿ, ದ್ವಾಪರಯುಗದಲ್ಲಿ ಶ್ರೀ ಜಗದ್ಗುರು ರೇಣುಕ ಶಿವಾಚಾರ್ಯರಾಗಿ ಮತ್ತು ಕಲಿಯುಗದಲ್ಲಿ ಶ್ರೀ ಜಗದ್ಗುರು ರೇವಣಸಿದ್ಧ ಭಗವತ್ಪಾದರಾಗಿ ಅವತರಿಸಿದರು. ರೇವಣಸಿದ್ಧರು ಕಲಿಯುಗದಲ್ಲಿ ಶ್ರೀ ಆದಿ ಶಂಕರಾಚಾರ್ಯರಿಗೆ ಶ್ರೀ ಚಂದ್ರಮೌಳೀಶ್ವರ ಲಿಂಗ ಮತ್ತು ರತ್ನಗರ್ಭ ಗಣಪತಿಯನ್ನು ಅನುಗ್ರಹಿಸಿದರೆಂದು ಶೃಂಗೇರಿಯ ಗುರುವಂಶಕಾವ್ಯದಲ್ಲಿ ನಿರೂಪಿತವಾಗಿದೆ. ಅವರು ಚೋಳ ರಾಜನಿಗೆ ಆಶೀರ್ವದಿಸಿ, ಬಿಜ್ಜಳ ರಾಜನ ಕನ್ನಿಕೆಯರ ಬಲಿದಾನ ತಡೆದು, ಕೊಲ್ಲಾಪುರದ ಗೋರಕ್ಷನಾಥನ ಗರ್ವಭಂಗಿಸಿದರು.\n\nಕ್ಷೇತ್ರದ ಆರಾಧ್ಯ ಮತ್ತು ಗೋತ್ರಪುರುಷನಾಗಿ ಶ್ರೀ ವೀರಭದ್ರಸ್ವಾಮಿ ಪೂಜಿಸಲ್ಪಡುತ್ತಾನೆ. ಇಲ್ಲಿನ ವೀರಭದ್ರಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಬಲಭಾಗದಲ್ಲಿ ರೇಣುಕಾಚಾರ್ಯರು ಆವೀರ್ಭವಿಸಿದ ಶ್ರೀ ಸೋಮೇಶ್ವರ ಶಿವಲಿಂಗದ ಗುಡಿಯಿದೆ. ಎಡಭಾಗದಲ್ಲಿ ಚಂದ್ರಮೌಳೀಶ್ವರ ಲಿಂಗ ಪ್ರದಾನದ ಶಿಲಾಮೂರ್ತಿ ಮತ್ತು ಗಣಪತಿ ವಿಗ್ರಹವಿದೆ. ಈ ದೇವಸ್ಥಾನದಲ್ಲಿ ಜೋಡು ನಂದಿ (ಜೋಡಿ ನಂದಿ) ಇರುವುದು ಅಪೂರ್ವ ವಿಶೇಷ. ಕ್ಷೇತ್ರದ ಶಕ್ತಿದೇವತೆಯಾಗಿ ಶ್ರೀ ಚೌಡೇಶ್ವರಿ ದೇವಿ ನೆಲೆಸಿದ್ದಾಳೆ. ಪ್ರಸ್ತುತ ಪೀಠದಲ್ಲಿ ೧೨೧ನೇ ಜಗದ್ಗುರುಗಳಾಗಿ ಶ್ರೀ ಶ್ರೀ ಶ್ರೀ ಪ್ರಸನ್ನ ರೇಣುಕ ವೀರ ಸೋಮೇಶ್ವರ ರಾಜದೇಶಿಕೇಂದ್ರ ಶಿವಾಚಾರ್ಯ ಮಹಾಸ್ವಾಮೀಜಿಗಳು ಫೆಬ್ರವರಿ ೬, ೧೯೯೨ ರಂದು ತಮ್ಮ ೩೬ನೇ ವಯಸ್ಸಿನಲ್ಲಿ ಪೀಠಾರೋಹಣ ಮಾಡಿದರು. ವೀರ ರುದ್ರಾಮುನಿ ಶಿವಾಚಾರ್ಯರ ಉತ್ತರಾಧಿಕಾರಿಯಾದ ಇವರು ಪೀಠದ ಸರ್ವಾಂಗೀಣ ಅಭಿವೃದ್ಧಿಗಾಗಿ 'ಎಂಟು ಅಂಶಗಳ ಕಾರ್ಯಕ್ರಮ'ವನ್ನು ಜಾರಿಗೆ ತಂದಿದ್ದಾರೆ.",
    "name_mr": "रंभापुरी पीठ",
    "acharya_mr": "जगद्गुरु रेणुकाचार्य",
    "simhasana_mr": "वीर सिंहासन",
    "location_mr": "बालेहोन्नूर, चिकमगलूर",
    "current_swamiji_mr": "श्री श्री श्री जगद्गुरु प्रसन्न रेणुका वीर सोमेश्वर राजदेशिकेंद्र  शिवाचार्य महास्वामीजी",
    "associated_linga_mr": "सोमेश्वर लिंग",
    "description_mr": "रंभापुरी पीठ वीरशैव परंपरा के पांच महापीठों में पहला है। यह भद्रा नदी के तट पर स्थित बालेहोन्नूर में स्थित है।",
    "name_hi": "रंभापुरी पीठ",
    "acharya_hi": "जगद्गुरु रेणुकाचार्य",
    "simhasana_hi": "वीर सिंहासन",
    "location_hi": "बालेहोन्नूर, चिकमगलूर",
    "current_swamiji_hi": "श्री श्री श्री जगद्गुरु प्रसन्न रेणुका वीर सोमेश्वर राजदेशिकेंद्र शिवाचार्य महास्वामीजी",
    "associated_linga_hi": "सोमेश्वर लिंग",
    "description_hi": "रंभापुरी पीठ वीरशैव परंपरा के पांच महापीठों में प्रथम है। यह कर्नाटक के चिकमगलूर जिले में भद्रा नदी के तट पर बालेहोन्नूर में स्थित है।",
    "history_hi": "इस पीठ की स्थापना श्री जगद्गुरु रेणुकाचार्य जी द्वारा की गई थी। परंपरा के अनुसार वे कोल्लीपाकी के सोमेश्वर लिंग से प्रकट हुए थे और मलेयाचल (बालेहोन्नूर) में इस पीठ की स्थापना की थी।",
    "history_mr": "इस पीठ की स्थापना श्री जगद्गुरु रेणुकाचार्यजी ने की थी। पौराणिक कथा के अनुसार, वे कोल्लीपाकी के सोमेश्वर लिंग से प्रकट हुए थे। वीरशैव धर्म के प्रचार और सिद्धांत शिखामणि के संरक्षण में इस पीठ का विशेष योगदान है।"
}

class Command(BaseCommand):
    help = "Seeds/updates the database record for Rambhapuri Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {status}: {obj.name}"))
