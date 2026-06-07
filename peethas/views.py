from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Peetha, TravelPlan, PeethaHandler, PeethaMedia, Pooja, PoojaBooking, PeethaPaymentConfig
from .forms import TravelPlanForm, PeethaMediaAddForm, PeethaMediaEditForm

import datetime
import json
import razorpay
from firebase_admin import auth as firebase_auth
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .heritage_content import HERITAGE_CONTENT
from .veerashaiva_content import VEERASHAIVA_CONTENT
from .feature_flags import USE_OTP_LOGIN, USE_RECTANGULAR_PORTRAITS

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
        'current_swamiji_label': 'Current Jagathguru',
        'history_label': 'History',
        'about_label': 'About',
        'copyright': '© Veerashaiva Pancha Peethas',
        'login_btn': 'Handler Login',
        'logout_btn': 'Logout',
        'dashboard_btn': 'Dashboard',
        'travel_plans_title': 'Swamiji Travel Plans',
        'media_gallery_title': 'Photos & Videos',
        'no_travel_plans': 'No travel plans scheduled for this month.',
        'no_media': 'No photos or videos uploaded yet.',
        'divine_heritage_title': 'Panchapeetas',
        'veerashaiva_title': 'Veerashaiva-Lingayat'
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
        'login_btn': 'ನಿರ್ವಾಹಕರ ಲಾಗಿನ್',
        'logout_btn': 'ಲಾಗ್ ಔಟ್',
        'dashboard_btn': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'travel_plans_title': 'ಶ್ರೀಗಳ ಪ್ರವಾಸ ವಿವರಗಳು',
        'media_gallery_title': 'ಚಿತ್ರಗಳು ಮತ್ತು ವಿಡಿಯೋಗಳು',
        'no_travel_plans': 'ಈ ತಿಂಗಳಲ್ಲಿ ಯಾವುದೇ ಪ್ರವಾಸ ಯೋಜನೆಗಳಿಲ್ಲ.',
        'no_media': 'ಇನ್ನೂ ಯಾವುದೇ ಚಿತ್ರಗಳು ಅಥವಾ ವಿಡಿಯೋಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾಗಿಲ್ಲ.',
        'divine_heritage_title': 'ಪಂಚಪೀಠಗಳು',
        'veerashaiva_title': 'ವೀರಶೈವ-ಲಿಂಗಾಯತ'
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
        'login_btn': 'लॉगिन',
        'logout_btn': 'लॉग आउट',
        'dashboard_btn': 'डॅशबोर्ड',
        'travel_plans_title': 'श्रींचे प्रवास वेळापत्रक',
        'media_gallery_title': 'छायाचित्रे आणि व्हिडिओ',
        'no_travel_plans': 'या महिन्यात कोणतेही प्रवास नियोजन नाही.',
        'no_media': 'अद्याप कोणतेही फोटो किंवा व्हिडिओ अपलोड केलेले नाहीत.',
        'divine_heritage_title': 'पंचपीठे',
        'veerashaiva_title': 'वीरशैव-लिंगायत'
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
        'about_p2': '<strong>सिद्धांत शिखामणि</strong> इस परंपरा का मुख्य धर्मग्रंथ है, जिसमें पंचाचार्यों के दर्शन और वीरशैव धर्म का प्रतिपादन है। मान्यता है कि शिव के होने वाले पांच मुखों — <span class="keyword">सद्योजात</span>, <span class="keyword">वामदेव</span>, <span class="keyword">अघोर</span>, <span class="keyword">तत्पुरुष</span> और <span class="keyword">ईशान</span> — से इन आचार्यों का प्राकट्य हुआ और उन्होंने संपूर्ण भारत में इन पांच पीठों की स्थापना की।',
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
        'login_btn': 'लॉगिन',
        'logout_btn': 'लॉग आउट',
        'dashboard_btn': 'डैशबोर्ड',
        'travel_plans_title': 'पूज्य महाराज श्री की यात्रा योजनाएं',
        'media_gallery_title': 'चित्र और वीडियो',
        'no_travel_plans': 'इस माह में कोई यात्रा कार्यक्रम निर्धारित नहीं है।',
        'no_media': 'अभी तक कोई फोटो या वीडियो अपलोड नहीं किया गया है.',
        'divine_heritage_title': 'पंचपीठ',
        'veerashaiva_title': 'वीरशैव-लिंगायत'
    }
}

MONTH_NAMES = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'kn': ['ಜನವರಿ', 'ಫೆಬ್ರವರಿ', 'ಮಾರ್ಚ್', 'ಏಪ್ರಿಲ್', 'ಮೇ', 'ಜೂನ್', 'ಜುಲೈ', 'ಆಗಸ್ಟ್', 'ಸೆಪ್ಟೆಂಬರ್', 'ಅಕ್ಟೋಬರ್', 'ನವೆಂಬರ್', 'ಡಿಸೆಂಬರ್'],
    'mr': ['जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर'],
    'hi': ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'],
}


def get_language(request):
    lang = request.GET.get('lang')
    if lang in ['en', 'kn', 'mr', 'hi']:
        request.session['lang'] = lang
    return request.session.get('lang', 'en')


def translate_object(obj, lang):
    if lang == 'en':
        if hasattr(obj, 'name') and obj.name:
            obj.short_name = obj.name.replace(" Peetha", "")
        return obj

    if isinstance(obj, Peetha):
        fields = ['name', 'acharya', 'simhasana', 'location', 'current_swamiji', 'associated_linga', 'description', 'history']
    elif isinstance(obj, PeethaMedia):
        fields = ['title', 'description']
    elif isinstance(obj, TravelPlan):
        fields = ['title', 'location', 'description']
    else:
        fields = []

    for field in fields:
        localized_val = getattr(obj, f"{field}_{lang}", None)
        if localized_val:
            setattr(obj, field, localized_val)
    
    if isinstance(obj, Peetha):
        if lang == 'kn':
            obj.short_name = obj.name.replace(" ಪೀಠ", "")
        elif lang == 'mr' or lang == 'hi':
            obj.short_name = obj.name.replace(" पीठ", "")
        else:
            obj.short_name = obj.name.replace(" Peetha", "")

    return obj


# ===== Public Frontend Views =====

def home(request):
    lang = get_language(request)
    peethas = [translate_object(p, lang) for p in Peetha.objects.all()]
    return render(request, 'peethas/home.html', {
        'peethas': peethas,
        'use_rectangular_portraits': USE_RECTANGULAR_PORTRAITS,
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'heritage_content': HERITAGE_CONTENT[lang],
        'veerashaiva_content': VEERASHAIVA_CONTENT[lang],
    })


def peetha_detail(request, slug):
    lang = get_language(request)
    peetha = get_object_or_404(Peetha, slug=slug)
    peetha = translate_object(peetha, lang)

    # 1. Fetch Travel Plans from current month onwards
    today = datetime.date.today()
    start_of_current_month = datetime.date(today.year, today.month, 1)
    
    # Query database
    travel_plans_qs = TravelPlan.objects.filter(
        peetha=peetha, 
        start_date__gte=start_of_current_month
    ).order_by('start_date')

    # Group Travel Plans by Month
    grouped_plans = []
    current_group = None
    
    for plan in travel_plans_qs:
        # Translate plan content
        plan = translate_object(plan, lang)
        
        # Localize month name
        month_idx = plan.start_date.month - 1
        month_name = MONTH_NAMES.get(lang, MONTH_NAMES['en'])[month_idx]
        year = plan.start_date.year
        month_str = f"{month_name} {year}"
        
        if not current_group or current_group['month_str'] != month_str:
            current_group = {
                'month_str': month_str,
                'plans': []
            }
            grouped_plans.append(current_group)
        current_group['plans'].append(plan)

    # 2. Fetch Media Gallery (Photos and videos)
    media_list = [translate_object(m, lang) for m in PeethaMedia.objects.filter(peetha=peetha)]

    # 3. Fetch Active Poojas
    poojas = [translate_object(p, lang) for p in Pooja.objects.filter(peetha=peetha, is_active=True)]

    # Dynamic styling variable
    show_admin_button = request.user.is_authenticated

    return render(request, 'peethas/peetha_detail.html', {
        'peetha': peetha,
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'travel_plans_grouped': grouped_plans,
        'media_gallery': media_list,
        'poojas': poojas,
        'show_admin_button': show_admin_button,
    })


# ===== Authentication Views =====

def login_view(request):
    lang = get_language(request)
    next_url = request.GET.get('next', 'peethas:home')
    
    if request.user.is_authenticated:
        if request.user.is_superuser or hasattr(request.user, 'handler_profile'):
            return redirect('peethas:dashboard_home')
        return redirect(next_url)
        
    if USE_OTP_LOGIN:
        return render(request, 'peethas/login_otp.html', {
            'lang': lang,
            'labels': TRANSLATIONS[lang],
            'next': next_url,
        })
    else:
        if request.method == 'POST':
            user_in = request.POST.get('username')
            pass_in = request.POST.get('password')
            user = authenticate(request, username=user_in, password=pass_in)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', 'peethas:home')
                if user.is_superuser or hasattr(user, 'handler_profile'):
                    return redirect('peethas:dashboard_home')
                
                # For safe redirect
                from django.utils.http import url_has_allowed_host_and_scheme
                if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('peethas:home')
            else:
                messages.error(request, 'Invalid username or password.')
                
        return render(request, 'peethas/login_password.html', {
            'lang': lang,
            'labels': TRANSLATIONS[lang],
            'next': next_url,
        })

@csrf_exempt
def verify_firebase_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')
            next_url = data.get('nextUrl', 'peethas:home')
            
            if not id_token:
                return JsonResponse({'success': False, 'error': 'No ID token provided'}, status=400)
                
            # Verify the token with Firebase Admin
            decoded_token = firebase_auth.verify_id_token(id_token)
            phone_number = decoded_token.get('phone_number')
            
            if not phone_number:
                return JsonResponse({'success': False, 'error': 'No phone number found in token'}, status=400)
                
            # Login or Register User
            # We use phone number as the username
            user, created = User.objects.get_or_create(username=phone_number)
            
            # Log the user in
            login(request, user)
            
            # Determine redirect URL
            redirect_url = next_url
            if user.is_superuser or hasattr(user, 'handler_profile'):
                from django.urls import reverse
                redirect_url = reverse('peethas:dashboard_home')
            elif redirect_url == 'peethas:home' or redirect_url.startswith('peethas:'):
                from django.urls import reverse
                try:
                    redirect_url = reverse(redirect_url)
                except:
                    redirect_url = '/'
            
            return JsonResponse({'success': True, 'redirectUrl': redirect_url})
            
        except Exception as e:
            print(f"Firebase verification error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def register_view(request):
    lang = get_language(request)
    next_url = request.GET.get('next', 'peethas:home')
    
    if USE_OTP_LOGIN:
        if next_url:
            return redirect(f"/login/?next={next_url}")
        return redirect('peethas:login')
    else:
        if request.user.is_authenticated:
            return redirect('peethas:home')
            
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name', '')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
                login(request, user)
                messages.success(request, 'Registration successful! Welcome.')
                
                next_url = request.POST.get('next', 'peethas:home')
                from django.utils.http import url_has_allowed_host_and_scheme
                if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('peethas:home')
                
        return render(request, 'peethas/register_password.html', {
            'lang': lang,
            'labels': TRANSLATIONS[lang],
            'next': next_url,
        })


def logout_view(request):
    logout(request)
    return redirect('peethas:home')


# ===== Dashboard & CRUD Views =====

def check_peetha_authorization(user, peetha):
    """
    Checks if the logged-in user is a superuser or the assigned handler for the Peetha.
    Raises PermissionDenied if not authorized.
    """
    if user.is_superuser:
        return True
    try:
        handler = user.handler_profile
        if handler.peetha == peetha:
            return True
    except PeethaHandler.DoesNotExist:
        pass
    raise PermissionDenied("You do not have permission to manage this Peetha.")


@login_required(login_url='peethas:login')
def dashboard_home(request):
    lang = get_language(request)
    # If superuser: show the portal where they can manage any Peetha
    if request.user.is_superuser:
        peethas = Peetha.objects.all()
        return render(request, 'peethas/dashboard.html', {
            'is_admin': True,
            'peethas': peethas,
            'labels': TRANSLATIONS['en'],  # Admin panel uses English
            'lang': lang,
        })
    
    # If normal user: check if handler profile exists
    try:
        handler = request.user.handler_profile
        return redirect('peethas:dashboard_peetha', slug=handler.peetha.slug)
    except PeethaHandler.DoesNotExist:
        logout(request)
        messages.error(request, "This account is not associated with any Peetha. Logging out.")
        return redirect('peethas:login')


@login_required(login_url='peethas:login')
def dashboard_peetha(request, slug):
    lang = get_language(request)
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)

    media_list = PeethaMedia.objects.filter(peetha=peetha)
    travel_list = TravelPlan.objects.filter(peetha=peetha).order_by('start_date')

    media_form = PeethaMediaAddForm()
    travel_form = TravelPlanForm()

    return render(request, 'peethas/dashboard.html', {
        'is_admin': request.user.is_superuser,
        'peetha': peetha,
        'media_list': media_list,
        'travel_list': travel_list,
        'media_form': media_form,
        'travel_form': travel_form,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


# --- Media CRUD Views ---

@login_required(login_url='peethas:login')
def media_add(request, slug):
    import os
    import re
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)

    if request.method == 'POST':
        form = PeethaMediaAddForm(request.POST, request.FILES)
        if form.is_valid():
            media_type = form.cleaned_data.get('media_type')
            title = form.cleaned_data.get('title', '').strip()
            description = form.cleaned_data.get('description', '').strip()
            
            # Retrieve translations
            title_kn = form.cleaned_data.get('title_kn', '').strip()
            description_kn = form.cleaned_data.get('description_kn', '').strip()
            title_mr = form.cleaned_data.get('title_mr', '').strip()
            description_mr = form.cleaned_data.get('description_mr', '').strip()
            title_hi = form.cleaned_data.get('title_hi', '').strip()
            description_hi = form.cleaned_data.get('description_hi', '').strip()

            if media_type == 'photo':
                # Handle multiple photos
                files = request.FILES.getlist('photo_file')
                if not files:
                    messages.error(request, "Please select at least one photo file to upload.")
                else:
                    success_count = 0
                    for i, file in enumerate(files):
                        # Determine title fallback
                        if not title:
                            # Use filename without extension
                            filename_only = os.path.splitext(file.name)[0]
                            # Clean filename
                            item_title = filename_only.replace('_', ' ').replace('-', ' ').title()
                        else:
                            if len(files) > 1:
                                item_title = f"{title} (Part {i + 1})"
                            else:
                                item_title = title

                        # Create and save PeethaMedia item
                        media = PeethaMedia(
                            peetha=peetha,
                            media_type='photo',
                            photo_file=file,
                            title=item_title,
                            description=description,
                            title_kn=title_kn,
                            description_kn=description_kn,
                            title_mr=title_mr,
                            description_mr=description_mr,
                            title_hi=title_hi,
                            description_hi=description_hi,
                        )
                        media.save()
                        success_count += 1
                    
                    messages.success(request, f"Successfully uploaded {success_count} photo(s).")

            elif media_type == 'video':
                # Handle multiple YouTube video URLs
                youtube_url_text = request.POST.get('youtube_url', '').strip()
                if not youtube_url_text:
                    messages.error(request, "Please enter at least one YouTube URL.")
                else:
                    # Split lines/commas and filter empty entries
                    urls = [u.strip() for u in youtube_url_text.replace(',', '\n').split('\n') if u.strip()]
                    if not urls:
                        messages.error(request, "Please enter valid YouTube URLs.")
                    else:
                        success_count = 0
                        yt_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
                        
                        for i, url in enumerate(urls):
                            match = re.search(yt_pattern, url)
                            if not match:
                                messages.error(request, f"Skipped invalid YouTube URL: {url}")
                                continue
                            
                            if not title:
                                item_title = f"Video - {match.group(1)}"
                            else:
                                if len(urls) > 1:
                                    item_title = f"{title} (Part {i + 1})"
                                else:
                                    item_title = title
                            
                            media = PeethaMedia(
                                peetha=peetha,
                                media_type='video',
                                youtube_url=url,
                                title=item_title,
                                description=description,
                                title_kn=title_kn,
                                description_kn=description_kn,
                                title_mr=title_mr,
                                description_mr=description_mr,
                                title_hi=title_hi,
                                description_hi=description_hi,
                            )
                            media.save()
                            success_count += 1
                        
                        if success_count > 0:
                            messages.success(request, f"Successfully added {success_count} video(s).")
                        else:
                            messages.error(request, "No valid videos were added.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
    return redirect('peethas:dashboard_peetha', slug=peetha.slug)


@login_required(login_url='peethas:login')
def media_edit(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    media_item = get_object_or_404(PeethaMedia, pk=pk, peetha=peetha)

    if request.method == 'POST':
        form = PeethaMediaEditForm(request.POST, request.FILES, instance=media_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Media item updated successfully.")
            return redirect('peethas:dashboard_peetha', slug=peetha.slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PeethaMediaEditForm(instance=media_item)

    lang = get_language(request)
    return render(request, 'peethas/dashboard_edit.html', {
        'peetha': peetha,
        'edit_type': 'media',
        'media_item': media_item,
        'form': form,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def media_delete(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    media_item = get_object_or_404(PeethaMedia, pk=pk, peetha=peetha)
    
    if request.method == 'POST':
        media_item.delete()
        messages.success(request, "Media item deleted.")
        
    return redirect('peethas:dashboard_peetha', slug=peetha.slug)


# --- Travel Plan CRUD Views ---

@login_required(login_url='peethas:login')
def travel_add(request, slug):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)

    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.peetha = peetha
            travel.save()
            messages.success(request, "Travel event added successfully.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
    return redirect('peethas:dashboard_peetha', slug=peetha.slug)


@login_required(login_url='peethas:login')
def travel_edit(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    travel_item = get_object_or_404(TravelPlan, pk=pk, peetha=peetha)

    if request.method == 'POST':
        form = TravelPlanForm(request.POST, instance=travel_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Travel event updated successfully.")
            return redirect('peethas:dashboard_peetha', slug=peetha.slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = TravelPlanForm(instance=travel_item)

    lang = get_language(request)
    return render(request, 'peethas/dashboard_edit.html', {
        'peetha': peetha,
        'edit_type': 'travel',
        'travel_item': travel_item,
        'form': form,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def travel_delete(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    travel_item = get_object_or_404(TravelPlan, pk=pk, peetha=peetha)
    
    if request.method == 'POST':
        travel_item.delete()
        messages.success(request, "Travel event deleted.")
        
    return redirect('peethas:dashboard_peetha', slug=peetha.slug)


# ===== POOJA BOOKING VIEWS =====

@login_required(login_url='peethas:login')
def initiate_pooja_booking(request, peetha_slug):
    peetha = get_object_or_404(Peetha, slug=peetha_slug)
    
    if request.method == 'POST':
        pooja_id = request.POST.get('pooja_id')
        pooja = get_object_or_404(Pooja, pk=pooja_id, peetha=peetha)
        
        devotee_name = request.POST.get('devotee_name')
        devotee_phone = request.POST.get('devotee_phone')
        devotee_email = request.POST.get('devotee_email', '')
        date_of_pooja = request.POST.get('date_of_pooja')
        
        # Payment config
        try:
            payment_config = peetha.payment_config
        except PeethaPaymentConfig.DoesNotExist:
            messages.error(request, "Online payments are currently unavailable for this Peetha.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        if not payment_config.is_active:
            messages.error(request, "Online payments are temporarily disabled for this Peetha.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        # Create Razorpay Order
        client = razorpay.Client(auth=(payment_config.razorpay_key_id, payment_config.razorpay_key_secret))
        
        amount_paise = int(pooja.price * 100) # Razorpay works in paise
        
        data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"pooja_receipt_{datetime.datetime.now().timestamp()}"
        }
        
        payment_order = client.order.create(data=data)
        
        # Save pending booking
        booking = PoojaBooking.objects.create(
            pooja=pooja,
            user=request.user,
            devotee_name=devotee_name,
            devotee_phone=devotee_phone,
            devotee_email=devotee_email,
            date_of_pooja=date_of_pooja,
            amount=pooja.price,
            razorpay_order_id=payment_order['id'],
            payment_status='pending'
        )
        
        return render(request, 'peethas/pooja_payment.html', {
            'booking': booking,
            'razorpay_order_id': payment_order['id'],
            'razorpay_merchant_key': payment_config.razorpay_key_id,
            'amount': amount_paise,
            'currency': 'INR',
            'peetha': peetha,
        })
        
    return redirect('peethas:peetha_detail', slug=peetha.slug)


@csrf_exempt
def verify_pooja_payment(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        booking = get_object_or_404(PoojaBooking, razorpay_order_id=razorpay_order_id)
        peetha = booking.pooja.peetha
        payment_config = peetha.payment_config
        
        client = razorpay.Client(auth=(payment_config.razorpay_key_id, payment_config.razorpay_key_secret))
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            
            # Payment successful
            booking.razorpay_payment_id = razorpay_payment_id
            booking.razorpay_signature = razorpay_signature
            booking.payment_status = 'success'
            booking.save()
            
            return render(request, 'peethas/pooja_success.html', {'booking': booking, 'peetha': peetha})
            
        except razorpay.errors.SignatureVerificationError:
            booking.payment_status = 'failed'
            booking.save()
            messages.error(request, "Payment verification failed. If money was deducted, it will be refunded.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
    return redirect('peethas:home')

@login_required(login_url='peethas:login')
def my_bookings(request):
    lang = get_language(request)
    bookings = PoojaBooking.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'peethas/my_bookings.html', {
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'bookings': bookings,
    })
