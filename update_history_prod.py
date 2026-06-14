import os
import django
from deep_translator import GoogleTranslator

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from peethas.models import Peetha

# English Histories mapped by Peetha name
histories_en = {
    "Rambhapuri": "The Rambhapuri Peetha, also known as the Veera Simhasana, is located in Balehonnur, Karnataka on the banks of the Bhadra river. According to Veerashaiva tradition, the Peetha was established by Jagadguru Sri Renukacharya, who emerged from the Someshwara Linga at Kollipaki. Historically, the Peetha has been a supreme center of the Veerashaiva tradition, heavily patronized by the rulers of the Vijayanagara Empire and the Keladi Nayakas. The central shrine features Sri Veerabhadra Swamy and the sacred Someshwara Linga.",
    "Ujjaini": "The Ujjaini Saddharma Simhasana Peetha traces its origins to Jagadguru Marulasiddheshwara, one of the Panchacharyas. Originally established in Ujjain, Madhya Pradesh, the Peetha was later relocated during the 15th century to its current location in Kudligi taluk, Karnataka. The site is famous for the ancient Marulasiddheshwar Temple and its unique annual 'Shikara Thailabhisheka' (oil anointing) ceremony.",
    "Kedara": "The Kedara Vairagya Simhasana Peetha is centered at the highly revered Kedarnath Temple in the Himalayas, Uttarakhand. Tradition holds that it was established by Jagadguru Ekoramaradhya. A unique historical aspect of this Peetha is its deep connection to the Kedarnath temple, where the head priest (the Rawal) traditionally belongs to the Veerashaiva community from Karnataka, maintaining the monastic and administrative activities during both summer (at Kedarnath) and winter (at Ukhimath).",
    "Srisaila": "The Srisaila Surya Simhasana Peetha is located in the sacred town of Srisailam, Andhra Pradesh, home to the Mallikarjuna Swamy Jyotirlinga. The Peetha is associated with Jagadguru Panditaradhya. Srisailam has been a flourishing center of Veerashaiva philosophy for centuries, patronized by ancient dynasties including the Satavahanas, Kakatiyas, and the Vijayanagara Empire. It served as a spiritual hub for renowned Veerashaiva saints and scholars like Palkuriki Somanatha.",
    "Kashi": "The Kashi Jnana Simhasana Peetha is situated in the holy city of Varanasi (Kashi), Uttar Pradesh. Tradition states it was founded by Jagadguru Vishwaradhya, who manifested from the Kashi Vishwanath Jyotirlinga. The Peetha boasts immense antiquity; a historical copper-plate grant (danapatra) dating back to 574 CE records a land donation by King Jayananda Deo, evidencing its long-standing presence. The Peetha remains a major center for preserving and teaching ancient Veerashaiva philosophy to this day."
}

# Supported languages
lang_mapping = {
    'kn': 'kannada',
    'hi': 'hindi',
    'mr': 'marathi',
    'te': 'telugu',
    'ta': 'tamil',
    'ml': 'malayalam'
}

def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation failed for {target_lang}: {e}")
        return text

print("Connecting to database and updating Peetha histories...")

for peetha in Peetha.objects.all():
    name = peetha.name
    key = None
    for k in histories_en.keys():
        if k in name:
            key = k
            break
            
    if key:
        print(f"Updating history for {name}...")
        en_text = histories_en[key]
        peetha.history_en = en_text
        peetha.history = en_text  # Default
        
        # Translate to other languages
        for lang_code, google_lang in lang_mapping.items():
            translated = translate_text(en_text, google_lang)
            setattr(peetha, f'history_{lang_code}', translated)
            
        peetha.save()
        print(f"Successfully updated and translated {name}")
    else:
        print(f"Skipping {name}, no matching key found.")

print("All history fields updated.")
