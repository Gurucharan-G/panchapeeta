from django.shortcuts import render, get_object_or_404
from .models import Peetha

# UI Static Labels Translations
TRANSLATIONS = {
    'en': {
        'site_title': 'Veerashaiva Pancha Peethas',
        'site_subtitle': 'ವೀರಶೈವ ಪಂಚಪೀಠಗಳು',
        'hero_title': 'The <span class="keyword">Five Sacred Seats</span> of <span class="keyword">Veerashaivism</span>',
        'hero_subtitle': 'The <span class="keyword">Pancha Peethas</span> are the five ancient monasteries established by the <span class="keyword">Panchacharyas</span> — the five founding sages who emerged from the <span class="keyword">five faces of Lord Shiva</span> to propagate the <span class="keyword">Veerashaiva</span> faith.',
        'explore_peetha': 'Explore Peetha →',
        'founded_by': 'Founded by',
        'peeta_suffix': 'Peeta',
        'about_title': 'About <span class="keyword">Veerashaivism</span>',
        'about_p1': '<span class="keyword">Veerashaivism</span> is an ancient Shaivite tradition that emphasizes devotion to <span class="keyword">Lord Shiva</span>, the practice of <em>Lingadharana</em> (wearing the <span class="keyword">Ishtalinga</span> on the body), and adherence to the <em>Panchachara</em> — the five codes of conduct: <span class="keyword">Lingachara</span>, <span class="keyword">Sadachara</span>, <span class="keyword">Shivachara</span>, <span class="keyword">Bhrityachara</span>, and <span class="keyword">Ganachara</span>.',
        'about_p2': 'The <strong>Siddhanta Shikhamani</strong> is considered the primary holy text of the tradition, detailing the philosophy of the <span class="keyword">Panchacharyas</span> and the <span class="keyword">Veerashaiva dharma</span>. The tradition holds that these five <span class="keyword">Acharyas</span> incarnated from the five faces of <span class="keyword">Lord Shiva</span> — <span class="keyword">Sadyojata</span>, <span class="keyword">Vamadeva</span>, <span class="keyword">Aghora</span>, <span class="keyword">Tatpurusha</span>, and <span class="keyword">Ishana</span> — to establish the five <span class="keyword">Peethas</span> across India.',
        'back_link': '← Back to All Peethas',
        'key_details': 'Key Details',
        'founding_acharya': 'Founding Acharya',
        'simhasana_label': 'Simhasana',
        'associated_linga_label': 'Associated Linga',
        'location_label': 'Location',
        'current_swamiji_label': 'Current Swamiji',
        'history_label': 'History',
        'about_label': 'About',
        'copyright': '© Veerashaiva Pancha Peethas',
    },
    'kn': {
        'site_title': 'ವೀರಶೈವ ಪಂಚಪೀಠಗಳು',
        'site_subtitle': 'ವೀರಶೈವ ಪಂಚಪೀಠಗಳು',
        'hero_title': 'ವೀರಶೈವ ಧರ್ಮದ <span class="keyword">ಪಂಚ ಮಹಾಪೀಠಗಳು</span>',
        'hero_subtitle': '<span class="keyword">ಪಂಚಪೀಠಗಳು</span> ವೀರಶೈವ ಧರ್ಮದ ಪ್ರಚಾರಕ್ಕಾಗಿ ಶಿವನ <span class="keyword">ಐದು ಮುಖಗಳಿಂದ</span> ಉದ್ಭವಿಸಿದ <span class="keyword">ಪಂಚಾಚಾರ್ಯರು</span> ಸ್ಥಾಪಿಸಿದ ಐದು ಪುರಾತನ ಮಠಗಳಾಗಿವೆ.',
        'explore_peetha': 'ಪೀಠದ ವಿವರಗಳು →',
        'founded_by': 'ಸ್ಥಾಪನೆ:',
        'peeta_suffix': 'ಪೀಠ',
        'about_title': '<span class="keyword">ವೀರಶೈವ ಧರ್ಮದ</span> ಪರಿಚಯ',
        'about_p1': '<span class="keyword">ವೀರಶೈವ ಧರ್ಮವು</span> ಪರಶಿವನಲ್ಲಿ ಭಕ್ತಿ, ದೇಹದ ಮೇಲೆ <span class="keyword">ಇಷ್ಟಲಿಂಗ ಧರಿಸುವಿಕೆ</span> (ಲಿಂಗಧಾರಣ), ಮತ್ತು <span class="keyword">ಪಂಚಾಚಾರಗಳ</span> (ಲಿಂಗಾಚಾರ, ಸದಾಚಾರ, ಶಿವಾಚಾರ, ಭೃತ್ಯಾಚಾರ ಮತ್ತು ಗಣಾಚಾರ) ಪಾಲನೆಗೆ ಒತ್ತು ನೀಡುವ ಅತ್ಯಂತ ಪುರಾತನ ಶೈವ ಪರಂಪರೆಯಾಗಿದೆ.',
        'about_p2': 'ಶ್ರೀ ಜಗದ್ಗುರು ಪಂಚಾಚಾರ್ಯರ ತತ್ವಜ್ಞಾನ ಮತ್ತು <span class="keyword">ವೀರಶೈವ ಧರ್ಮದ</span> ಸಾರವನ್ನು ವಿವರಿಸುವ <strong>ಸಿದ್ಧಾಂತ ಶಿಖಾಮಣಿ</strong> ವೀರಶೈವರ ಪರಮ ಪವಿತ್ರ ಗ್ರಂಥವಾಗಿದೆ. ಶಿವನ ಐದು ಮುಖಗಳಾದ <span class="keyword">ಸದ್ಯೋಜಾತ</span>, <span class="keyword">ವಾಮದೇವ</span>, <span class="keyword">ಅಘೋರ</span>, <span class="keyword">ತತ್ಪುರುಷ</span> ಮತ್ತು <span class="keyword">ಈಶಾನ</span> ಮುಖಗಳಿಂದ ಜಗದ್ಗುರುಗಳು ಅವತರಿಸಿ ಭಾರತದಾದ್ಯಂತ ಈ ಪಂಚಪೀಠಗಳನ್ನು ಸ್ಥಾಪಿಸಿದರು ಎಂಬ ನಂಬಿಕೆ ಇದೆ.',
        'back_link': '← ಪೀಠಗಳ ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'key_details': 'ಪ್ರಮುಖ ವಿವರಗಳು',
        'founding_acharya': 'ಸ್ಥಾಪಕ ಜಗದ್ಗುರುಗಳು',
        'simhasana_label': 'ಸಿಂಹಾಸನ',
        'associated_linga_label': 'ಸಂಬಂಧಿತ ಲಿಂಗ',
        'location_label': 'ಸ್ಥಳ',
        'current_swamiji_label': 'ಪ್ರಸ್ತುತ ಜಗದ್ಗುರುಗಳು',
        'history_label': 'ಇತಿಹಾಸ',
        'about_label': 'ಪೀಠದ ವಿವರಣೆ',
        'copyright': '© ವೀರಶೈವ ಪಂಚ ಮಹಾಪೀಠಗಳು',
    },
    'mr': {
        'site_title': 'वीरशैव पंचपीठ',
        'site_subtitle': 'वीरशैव पंचपीठ',
        'hero_title': 'वीरशैव संप्रदायाचे <span class="keyword">पाच पावन पीठ</span>',
        'hero_subtitle': '<span class="keyword">पंचपीठ</span> ही वीरशैव च्या प्रसारासाठी भगवान शिवाच्या <span class="keyword">पाच मुखांतून</span> प्रकट झालेल्या <span class="keyword">पंचाचार्यांनी</span> स्थापन केलेली पाच प्राचीन मठे आहेत.',
        'explore_peetha': 'पीठाचे सविस्तर वर्णन →',
        'founded_by': 'संस्थापक:',
        'peeta_suffix': 'पीठ',
        'about_title': '<span class="keyword">वीरशैव संप्रदायाविषयी</span>',
        'about_p1': '<span class="keyword">वीरशैव संप्रदाय</span> हा एक प्राचीन शैव पंथ आहे जो भगवान शिवाची भक्ती, शरीरावर <span class="keyword">इष्टलिंग धारण</span> (लिंगधारण) करणे आणि <span class="keyword">पंचाचार</span> (लिंगाचार, सदाचार, शिवाचार, भृत्याचार आणि गणाचार) या पाच आचारसंहितांचे पालन करण्यावर भर देतो.',
        'about_p2': '<strong>सिद्धांत शिखामणी</strong> हा वीरशैव धर्माचा मूळ ग्रंथ मानला जातो, ज्यामध्ये पंचाचार्यांचे तत्त्वज्ञान आणि वीरशैव धर्माचे सविस्तर वर्णन आहे. भगवान शिवाच्या <span class="keyword">सद्योजात</span>, <span class="keyword">वामदेव</span>, <span class="keyword">अघोर</span>, <span class="keyword">तत्पुरुष</span> आणि <span class="keyword">ईशान</span> या पाच मुखांमधून पंचाचार्य अवतरले आणि त्यांनी भारतामध्ये या पाच पीठांची स्थापना केली.',
        'back_link': '← सर्व पीठांच्या पानावर मागे जा',
        'key_details': 'महत्त्वाचे तपशील',
        'founding_acharya': 'संस्थापक जगद्गुरु',
        'simhasana_label': 'सिंहासन',
        'associated_linga_label': 'संबंधित लिंग',
        'location_label': 'स्थान',
        'current_swamiji_label': 'सध्याचे जगद्गुरु',
        'history_label': 'इतिहास',
        'about_label': 'माहिती',
        'copyright': '© वीरशैव पंच महापीठ',
    },
    'hi': {
        'site_title': 'वीरशैव पंचपीठ',
        'site_subtitle': 'वीरशैव पंचपीठ',
        'hero_title': 'वीरशैव संप्रदाय के <span class="keyword">पांच पावन महापीठ</span>',
        'hero_subtitle': '<span class="keyword">पंचपीठ</span> वीरशैव धर्म के प्रचार-प्रसार के लिए भगवान शिव के <span class="keyword">पांच मुखों</span> से प्रकट हुए <span class="keyword">पंचाचार्यों</span> द्वारा स्थापित पांच अत्यंत प्राचीन मठ हैं।',
        'explore_peetha': 'पीठ की खोज करें →',
        'founded_by': 'संस्थापक:',
        'peeta_suffix': 'पीठ',
        'about_title': '<span class="keyword">वीरशैव संप्रदाय</span> के बारे में',
        'about_p1': '<span class="keyword">वीरशैव संप्रदाय</span> एक अत्यंत प्राचीन शैव परंपरा है जो भगवान शिव के प्रति अटूट भक्ति, शरीर पर <span class="keyword">इष्टलिंग धारण</span> (लिंगधारण) और <span class="keyword">पंचाचार</span> (लिंगाचार, सदाचार, शिवाचार, भृत्याचार और गणाचार) के पालन पर बल देती है।',
        'about_p2': '<strong>सिद्धांत शिखामणि</strong> इस परंपरा का मुख्य धर्मग्रंथ है, जिसमें पंचाचार्यों के दर्शन और वीरशैव धर्म का प्रतिपादन है। मान्यता है कि शिव के पांच मुखों — <span class="keyword">सद्योजात</span>, <span class="keyword">वामदेव</span>, <span class="keyword">अघोर</span>, <span class="keyword">तत्पुरुष</span> और <span class="keyword">ईशान</span> — से इन पांच आचार्यों का प्राकट्य हुआ और उन्होंने संपूर्ण भारत में इन पांच पीठों की स्थापना की।',
        'back_link': '← मुख्य पृष्ठ पर वापस जाएँ',
        'key_details': 'मुख्य विवरण',
        'founding_acharya': 'संस्थापक जगद्गुरु',
        'simhasana_label': 'सिंहासन',
        'associated_linga_label': 'संबद्ध शिवलिंग',
        'location_label': 'स्थान',
        'current_swamiji_label': 'वर्तमान जगद्गुरु',
        'history_label': 'इतिहास',
        'about_label': 'विवरण',
        'copyright': '© वीरशैव पंच महापीठ',
    }
}


def get_language(request):
    lang = request.GET.get('lang')
    if lang in ['en', 'kn', 'mr', 'hi']:
        request.session['lang'] = lang
    return request.session.get('lang', 'en')


def translate_object(obj, lang):
    if lang == 'en':
        obj.short_name = obj.name.replace(" Peetha", "")
        return obj
    fields = ['name', 'acharya', 'simhasana', 'location', 'current_swamiji', 'associated_linga', 'description', 'history']
    for field in fields:
        localized_val = getattr(obj, f"{field}_{lang}", None)
        if localized_val:
            setattr(obj, field, localized_val)
    
    if lang == 'kn':
        obj.short_name = obj.name.replace(" ಪೀಠ", "")
    elif lang == 'mr' or lang == 'hi':
        obj.short_name = obj.name.replace(" पीठ", "")
    else:
        obj.short_name = obj.name.replace(" Peetha", "")
    return obj


def home(request):
    lang = get_language(request)
    peethas = [translate_object(p, lang) for p in Peetha.objects.all()]
    return render(request, 'peethas/home.html', {
        'peethas': peethas,
        'use_rectangular_portraits': True,  # Set to True for Rectangle, False for Circle
        'lang': lang,
        'labels': TRANSLATIONS[lang],
    })


def peetha_detail(request, slug):
    lang = get_language(request)
    peetha = get_object_or_404(Peetha, slug=slug)
    peetha = translate_object(peetha, lang)
    return render(request, 'peethas/peetha_detail.html', {
        'peetha': peetha,
        'lang': lang,
        'labels': TRANSLATIONS[lang],
    })
