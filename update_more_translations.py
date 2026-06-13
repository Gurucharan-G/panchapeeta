import io
import re

filepath = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\views.py"
with io.open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_keys = {
    'en': {
        'nav_sign_in': 'Sign In / Sign Up',
        'nav_my_bookings': 'My Bookings',
    },
    'kn': {
        'nav_sign_in': 'ಸೈನ್ ಇನ್ / ಸೈನ್ ಅಪ್',
        'nav_my_bookings': 'ನನ್ನ ಬುಕಿಂಗ್‌ಗಳು',
    },
    'mr': {
        'nav_sign_in': 'साइन इन / साइन अप',
        'nav_my_bookings': 'माझे बुकिंग्स',
    },
    'hi': {
        'nav_sign_in': 'साइन इन / साइन अप',
        'nav_my_bookings': 'मेरी बुकिंग्स',
    },
    'te': {
        'nav_sign_in': 'సైన్ ఇన్ / సైన్ అప్',
        'nav_my_bookings': 'నా బుకింగ్‌లు',
    },
    'ta': {
        'nav_sign_in': 'உள்நுழைய / பதிவு செய்ய',
        'nav_my_bookings': 'எனது முன்பதிவுகள்',
    },
    'ml': {
        'nav_sign_in': 'സൈൻ ഇൻ / സൈൻ അപ്പ്',
        'nav_my_bookings': 'എൻ്റെ ബുക്കിംഗുകൾ',
    }
}

for lang, keys in new_keys.items():
    lang_pattern = f"('{lang}': {{.*?}})"
    match_lang = re.search(lang_pattern, content, re.DOTALL)
    if match_lang:
        lang_block = match_lang.group(1)
        insertion = ",\n"
        for k, v in keys.items():
            insertion += f"        '{k}': '{v}',\n"
        
        new_lang_block = lang_block.rsplit('\n    }', 1)[0] + insertion + "    }"
        content = content.replace(lang_block, new_lang_block)

with io.open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Translations for sign in / my bookings added.")
