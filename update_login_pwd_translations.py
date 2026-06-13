import io
import re

filepath = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\views.py"
with io.open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_keys = {
    'en': {
        'login_welcome': 'Welcome back to Pancha Peethas',
        'username_label': 'Username',
        'password_label': 'Password',
        'sign_in_only': 'Sign In',
        'no_account_prompt': "Don't have an account?",
        'sign_up_btn': 'Sign Up',
    },
    'kn': {
        'login_welcome': 'ಪಂಚ ಪೀಠಗಳಿಗೆ ಮರಳಿ ಸ್ವಾಗತ',
        'username_label': 'ಬಳಕೆದಾರರ ಹೆಸರು',
        'password_label': 'ಗುಪ್ತಪದ',
        'sign_in_only': 'ಸೈನ್ ಇನ್',
        'no_account_prompt': "ಖಾತೆ ಇಲ್ಲವೇ?",
        'sign_up_btn': 'ಸೈನ್ ಅಪ್ ಮಾಡಿ',
    },
    'mr': {
        'login_welcome': 'पंचपीठात पुन्हा स्वागत आहे',
        'username_label': 'वापरकर्ता नाव',
        'password_label': 'पासवर्ड',
        'sign_in_only': 'लॉगिन करा',
        'no_account_prompt': "खाते नाही का?",
        'sign_up_btn': 'साइन अप करा',
    },
    'hi': {
        'login_welcome': 'पंच पीठों में आपका फिर से स्वागत है',
        'username_label': 'उपयोगकर्ता नाम',
        'password_label': 'पासवर्ड',
        'sign_in_only': 'साइन इन करें',
        'no_account_prompt': "क्या आपका खाता नहीं है?",
        'sign_up_btn': 'साइन अप करें',
    },
    'te': {
        'login_welcome': 'పంచ పీఠాలకు తిరిగి స్వాగతం',
        'username_label': 'వాడుకరి పేరు',
        'password_label': 'పాస్వర్డ్',
        'sign_in_only': 'సైన్ ఇన్',
        'no_account_prompt': "ఖాతా లేదా?",
        'sign_up_btn': 'సైన్ అప్ చేయండి',
    },
    'ta': {
        'login_welcome': 'பஞ்ச பீடங்களுக்கு மீண்டும் வரவேற்கிறோம்',
        'username_label': 'பயனர் பெயர்',
        'password_label': 'கடவுச்சொல்',
        'sign_in_only': 'உள்நுழைக',
        'no_account_prompt': "கணக்கு இல்லையா?",
        'sign_up_btn': 'பதிவு செய்யவும்',
    },
    'ml': {
        'login_welcome': 'പഞ്ച പീഠങ്ങളിലേക്ക് വീണ്ടും സ്വാഗതം',
        'username_label': 'ഉപയോക്തൃനാമം',
        'password_label': 'പാസ്‌വേഡ്',
        'sign_in_only': 'സൈൻ ഇൻ ചെയ്യുക',
        'no_account_prompt': "അക്കൗണ്ട് ഇല്ലേ?",
        'sign_up_btn': 'സൈൻ അപ്പ് ചെയ്യുക',
    }
}

for lang, keys in new_keys.items():
    lang_pattern = f"('{lang}': {{.*?}})"
    match_lang = re.search(lang_pattern, content, re.DOTALL)
    if match_lang:
        lang_block = match_lang.group(1)
        insertion = ",\n"
        # Avoid creating double comma if the last line already ends with a comma
        # Actually it's safer to just insert the keys right before the final '}'
        # Let's do it carefully:
        
        inner_content = lang_block.rstrip().rstrip('}')
        if not inner_content.strip().endswith(','):
            inner_content += ",\n"
        else:
            inner_content += "\n"
            
        for k, v in keys.items():
            inner_content += f"        '{k}': '{v}',\n"
        
        new_lang_block = inner_content + "    }"
        content = content.replace(lang_block, new_lang_block)

with io.open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Translations for login_password.html added.")
