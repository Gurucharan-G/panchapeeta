import io
import re

filepath = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\views.py"
with io.open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_keys = {
    'en': {
        'nav_home': 'Home',
        'nav_jagathguru': 'Jagathguru',
        'nav_pooja_booking': 'Pooja Booking',
        'nav_contact_us': 'Contact Us',
    },
    'kn': {
        'nav_home': 'ಮುಖಪುಟ',
        'nav_jagathguru': 'ಜಗದ್ಗುರು',
        'nav_pooja_booking': 'ಪೂಜೆ ಬುಕಿಂಗ್',
        'nav_contact_us': 'ಸಂಪರ್ಕಿಸಿ',
    },
    'mr': {
        'nav_home': 'मुख्यपृष्ठ',
        'nav_jagathguru': 'जगद्गुरु',
        'nav_pooja_booking': 'पूजा बुकिंग',
        'nav_contact_us': 'संपर्क करा',
    },
    'hi': {
        'nav_home': 'होम',
        'nav_jagathguru': 'जगद्गुरु',
        'nav_pooja_booking': 'पूजा बुकिंग',
        'nav_contact_us': 'संपर्क करें',
    },
    'te': {
        'nav_home': 'హోమ్',
        'nav_jagathguru': 'జగద్గురు',
        'nav_pooja_booking': 'పూజా బుకింగ్',
        'nav_contact_us': 'మమ్మల్ని సంప్రదించండి',
    },
    'ta': {
        'nav_home': 'முகப்பு',
        'nav_jagathguru': 'ஜகத்குரு',
        'nav_pooja_booking': 'பூஜை முன்பதிவு',
        'nav_contact_us': 'தொடர்பு கொள்ள',
    },
    'ml': {
        'nav_home': 'ഹോം',
        'nav_jagathguru': 'ജഗദ്ഗുരു',
        'nav_pooja_booking': 'പൂജ ബുക്കിംഗ്',
        'nav_contact_us': 'ബന്ധപ്പെടുക',
    }
}

for lang, keys in new_keys.items():
    # Find the end of the dictionary for each language
    # 'lang': { ... }
    # we'll look for:
    #         'veerashaiva_title': '...'
    #     },
    pattern = r"(\s*)'veerashaiva_title':\s*'(.*?)'\n(\s*)\},"
    
    match = re.search(pattern, content)
    
    # We need to specifically target the one for 'lang'
    # Actually, let's just insert after 'veerashaiva_title': '...', for each language respectively.
    # A safer way is to find the block for the language.
    lang_pattern = f"('{lang}': {{.*?}})"
    
    match_lang = re.search(lang_pattern, content, re.DOTALL)
    if match_lang:
        lang_block = match_lang.group(1)
        # Add new keys before the closing brace of the language block
        insertion = ",\n"
        for k, v in keys.items():
            insertion += f"        '{k}': '{v}',\n"
        
        # Replace the last newline and brace in the block
        # The block ends with \n    }
        new_lang_block = lang_block.rsplit('\n    }', 1)[0] + insertion + "    }"
        content = content.replace(lang_block, new_lang_block)

with io.open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Translations added to views.py successfully.")
