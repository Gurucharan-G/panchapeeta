import io
import re

filepath = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\views.py"
with io.open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_keys = {
    'en': {
        'login_prompt': 'Enter your mobile number to get an OTP.',
        'mobile_number_label': 'Mobile Number',
        'send_otp_btn': 'Send OTP',
        'enter_otp_label': 'Enter OTP',
        'verify_login_btn': 'Verify & Login',
    },
    'kn': {
        'login_prompt': 'OTP ಪಡೆಯಲು ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.',
        'mobile_number_label': 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
        'send_otp_btn': 'OTP ಕಳುಹಿಸಿ',
        'enter_otp_label': 'OTP ನಮೂದಿಸಿ',
        'verify_login_btn': 'ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಲಾಗಿನ್ ಮಾಡಿ',
    },
    'mr': {
        'login_prompt': 'OTP मिळवण्यासाठी तुमचा मोबाईल नंबर टाका.',
        'mobile_number_label': 'मोबाईल नंबर',
        'send_otp_btn': 'OTP पाठवा',
        'enter_otp_label': 'OTP टाका',
        'verify_login_btn': 'पडताळणी करा आणि लॉगिन करा',
    },
    'hi': {
        'login_prompt': 'OTP प्राप्त करने के लिए अपना मोबाइल नंबर दर्ज करें।',
        'mobile_number_label': 'मोबाइल नंबर',
        'send_otp_btn': 'OTP भेजें',
        'enter_otp_label': 'OTP दर्ज करें',
        'verify_login_btn': 'सत्यापित करें और लॉगिन करें',
    },
    'te': {
        'login_prompt': 'OTP పొందడానికి మీ మొబైల్ నంబర్‌ను నమోదు చేయండి.',
        'mobile_number_label': 'మొబైల్ నంబర్',
        'send_otp_btn': 'OTP పంపండి',
        'enter_otp_label': 'OTP నమోదు చేయండి',
        'verify_login_btn': 'ధృవీకరించి లాగిన్ అవ్వండి',
    },
    'ta': {
        'login_prompt': 'OTP ஐ பெற உங்கள் மொபைல் எண்ணை உள்ளிடவும்.',
        'mobile_number_label': 'மொபைல் எண்',
        'send_otp_btn': 'OTP அனுப்பு',
        'enter_otp_label': 'OTP ஐ உள்ளிடவும்',
        'verify_login_btn': 'சரிபார்த்து உள்நுழையவும்',
    },
    'ml': {
        'login_prompt': 'OTP ലഭിക്കുന്നതിന് നിങ്ങളുടെ മൊബൈൽ നമ്പർ നൽകുക.',
        'mobile_number_label': 'മൊബൈൽ നമ്പർ',
        'send_otp_btn': 'OTP അയയ്ക്കുക',
        'enter_otp_label': 'OTP നൽകുക',
        'verify_login_btn': 'സ്ഥിരീകരിച്ച് ലോഗിൻ ചെയ്യുക',
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

print("Translations for login page added.")
