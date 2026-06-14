import io

views_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\views.py"
content_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\veerashaiva_content.py"

translations = {
    'ವೀರಶೈವ-ಲಿಂಗಾಯತ': 'ಶ್ರೀಮದ್ ವೀರಶೈವ',
    'वीरशैव-लिंगायत': 'श्रीमद् वीरशैव',
    'వీరశైవ-లింగాయత్': 'శ్రీమద్ వీరశైవ',
    'வீரசைவ-லிங்காயத்': 'ஸ்ரீமத் வீரசைவ',
    'വീരശൈവ-ലിംഗായത്ത്': 'ശ്രീമദ് വീരശൈവ',
}

# Update views.py
with io.open(views_path, "r", encoding="utf-8") as f:
    views_content = f.read()

for old, new in translations.items():
    views_content = views_content.replace(f"'veerashaiva_title': '{old}'", f"'veerashaiva_title': '{new}'")

with io.open(views_path, "w", encoding="utf-8") as f:
    f.write(views_content)

# Update veerashaiva_content.py
with io.open(content_path, "r", encoding="utf-8") as f:
    vc_content = f.read()

for old, new in translations.items():
    vc_content = vc_content.replace(f"'title': '{old}'", f"'title': '{new}'")

with io.open(content_path, "w", encoding="utf-8") as f:
    f.write(vc_content)

print("All titles updated.")
