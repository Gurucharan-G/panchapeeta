import io

filepath = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\veerashaiva_content.py"
with io.open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('""వాక్కు', '"\\"వాక్కు')
content = content.replace('నమస్కరిస్తున్నాను.""', 'నమస్కరిస్తున్నాను.\\""')
content = content.replace('""కామికాగమంలో', '"\\"కామికాగమంలో')
content = content.replace('వివరించబడింది.""', 'వివరించబడింది.\\""')

content = content.replace('""வார்த்தையும்', '"\\"வார்த்தையும்')
content = content.replace('வணங்குகிறேன்.""', 'வணங்குகிறேன்.\\""')
content = content.replace('""காமிகாகமத்தில்', '"\\"காமிகாகமத்தில்')
content = content.replace('விளக்கப்பட்டுள்ளது.""', 'விளக்கப்பட்டுள்ளது.\\""')

content = content.replace('""വാക്കും', '"\\"വാക്കും')
content = content.replace('വണങ്ങുന്നു.""', 'വണങ്ങുന്നു.\\""')
content = content.replace('""കാമികാഗമത്തിൽ', '"\\"കാമികാഗമത്തിൽ')
content = content.replace('വിശദീകരിച്ചിരിക്കുന്നു.""', 'വിശദീകരിച്ചിരിക്കുന്നു.\\""')

with io.open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Syntax fixed!")
