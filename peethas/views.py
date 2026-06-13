from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
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
        'veerashaiva_title': 'Veerashaiva-Lingayat',
        'nav_home': 'Home',
        'nav_jagathguru': 'Jagathguru',
        'nav_pooja_booking': 'Pooja Booking',
        'nav_contact_us': 'Contact Us',
        'nav_sign_in': 'Sign In / Sign Up',
        'nav_my_bookings': 'My Bookings',
        'login_prompt': 'Enter your mobile number to get an OTP.',
        'mobile_number_label': 'Mobile Number',
        'send_otp_btn': 'Send OTP',
        'enter_otp_label': 'Enter OTP',
        'verify_login_btn': 'Verify & Login',
    
        'login_welcome': 'Welcome back to Pancha Peethas',
        'username_label': 'Username',
        'password_label': 'Password',
        'sign_in_only': 'Sign In',
        'no_account_prompt': "Don't have an account?",
        'sign_up_btn': 'Sign Up',
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
        'veerashaiva_title': 'ವೀರಶೈವ-ಲಿಂಗಾಯತ',
        'nav_home': 'ಮುಖಪುಟ',
        'nav_jagathguru': 'ಜಗದ್ಗುರು',
        'nav_pooja_booking': 'ಪೂಜೆ ಬುಕಿಂಗ್',
        'nav_contact_us': 'ಸಂಪರ್ಕಿಸಿ',
        'nav_sign_in': 'ಸೈನ್ ಇನ್ / ಸೈನ್ ಅಪ್',
        'nav_my_bookings': 'ನನ್ನ ಬುಕಿಂಗ್‌ಗಳು',
        'login_prompt': 'OTP ಪಡೆಯಲು ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.',
        'mobile_number_label': 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
        'send_otp_btn': 'OTP ಕಳುಹಿಸಿ',
        'enter_otp_label': 'OTP ನಮೂದಿಸಿ',
        'verify_login_btn': 'ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಲಾಗಿನ್ ಮಾಡಿ',
    
        'login_welcome': 'ಪಂಚ ಪೀಠಗಳಿಗೆ ಮರಳಿ ಸ್ವಾಗತ',
        'username_label': 'ಬಳಕೆದಾರರ ಹೆಸರು',
        'password_label': 'ಗುಪ್ತಪದ',
        'sign_in_only': 'ಸೈನ್ ಇನ್',
        'no_account_prompt': 'ಖಾತೆ ಇಲ್ಲವೇ?',
        'sign_up_btn': 'ಸೈನ್ ಅಪ್ ಮಾಡಿ',
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
        'veerashaiva_title': 'वीरशैव-लिंगायत',
        'nav_home': 'मुख्यपृष्ठ',
        'nav_jagathguru': 'जगद्गुरु',
        'nav_pooja_booking': 'पूजा बुकिंग',
        'nav_contact_us': 'संपर्क करा',
        'nav_sign_in': 'साइन इन / साइन अप',
        'nav_my_bookings': 'माझे बुकिंग्स',
        'login_prompt': 'OTP मिळवण्यासाठी तुमचा मोबाईल नंबर टाका.',
        'mobile_number_label': 'मोबाईल नंबर',
        'send_otp_btn': 'OTP पाठवा',
        'enter_otp_label': 'OTP टाका',
        'verify_login_btn': 'पडताळणी करा आणि लॉगिन करा',
    
        'login_welcome': 'पंचपीठात पुन्हा स्वागत आहे',
        'username_label': 'वापरकर्ता नाव',
        'password_label': 'पासवर्ड',
        'sign_in_only': 'लॉगिन करा',
        'no_account_prompt': 'खाते नाही का?',
        'sign_up_btn': 'साइन अप करा',
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
        'veerashaiva_title': 'वीरशैव-लिंगायत',
        'nav_home': 'होम',
        'nav_jagathguru': 'जगद्गुरु',
        'nav_pooja_booking': 'पूजा बुकिंग',
        'nav_contact_us': 'संपर्क करें',
        'nav_sign_in': 'साइन इन / साइन अप',
        'nav_my_bookings': 'मेरी बुकिंग्स',
        'login_prompt': 'OTP प्राप्त करने के लिए अपना मोबाइल नंबर दर्ज करें।',
        'mobile_number_label': 'मोबाइल नंबर',
        'send_otp_btn': 'OTP भेजें',
        'enter_otp_label': 'OTP दर्ज करें',
        'verify_login_btn': 'सत्यापित करें और लॉगिन करें',
    
        'login_welcome': 'पंच पीठों में आपका फिर से स्वागत है',
        'username_label': 'उपयोगकर्ता नाम',
        'password_label': 'पासवर्ड',
        'sign_in_only': 'साइन इन करें',
        'no_account_prompt': 'क्या आपका खाता नहीं है?',
        'sign_up_btn': 'साइन अप करें',
    },
    'te': {
        'site_title': 'వీరశైవ పంచ పీఠాలు',
        'site_subtitle': 'వీరశైవ పంచ పీఠాలు',
        'hero_title': 'వీరశైవ ధర్మంలోని <span class="keyword">ఐదు పవిత్ర పీఠాలు</span>',
        'hero_subtitle': '<span class="keyword">పంచ పీఠాలు</span> అనగా వీరశైవ ధర్మ ప్రచారం కోసం పరమశివుని <span class="keyword">ఐదు ముఖాల</span> నుండి ఉద్భవించిన <span class="keyword">పంచాచార్యులు</span> స్థాపించిన ఐదు పురాతన మఠాలు.',
        'explore_peetha': 'పీఠం వివరాలు →',
        'founded_by': 'స్థాపకులు:',
        'peeta_suffix': 'పీఠం',
        'about_title': '<span class="keyword">వీరశైవం</span> గురించి',
        'about_p1': '<span class="keyword">వీరశైవం</span> ఒక ప్రాచీన శైవ సంప్రదాయం. ఇది పరమశివుని పట్ల భక్తి, శరీరముపై <span class="keyword">ఇష్టలింగ ధారణ</span> మరియు <span class="keyword">పంచాచారాల</span> (లింగాచారం, సదాచారం, శివాచారం, భృత్యచారం మరియు గణాచారం) ఆచరణను ఉద్ఘాటిస్తుంది.',
        'about_p2': '<strong>సిద్ధాంత శిఖామణి</strong> వీరశైవ ధర్మంలో ప్రధాన పవిత్ర గ్రంథం. పరమశివుని ఐదు ముఖాలైన <span class="keyword">సద్యోజాత</span>, <span class="keyword">వామదేవ</span>, <span class="keyword">అఘోర</span>, <span class="keyword">తత్పురుష</span> మరియు <span class="keyword">ఈశాన</span> ముఖాల నుండి పంచాచార్యులు అవతరించి భారతదేశమంతటా ఈ ఐదు పీఠాలను స్థాపించారని నమ్ముతారు.',
        'back_link': '← అన్ని పీఠాల పేజీకి వెళ్లండి',
        'key_details': 'ముఖ్య వివరాలు',
        'founding_acharya': 'స్థాపక జగద్గురువులు',
        'simhasana_label': 'సింహాసనం',
        'associated_linga_label': 'సంబంధిత లింగం',
        'location_label': 'స్థానం',
        'current_swamiji_label': 'ప్రస్తుత జగద్గురువులు',
        'history_label': 'చరిత్ర',
        'about_label': 'పీఠం గురించి',
        'copyright': '© వీరశైవ పంచ పీఠాలు',
        'login_btn': 'లాగిన్',
        'logout_btn': 'లాగ్ అవుట్',
        'dashboard_btn': 'డాష్‌బోర్డ్',
        'travel_plans_title': 'శ్రీలవారి ప్రయాణ ప్రణాళికలు',
        'media_gallery_title': 'ఫోటోలు & వీడియోలు',
        'no_travel_plans': 'ఈ నెలకు ప్రయాణ ప్రణాళికలు లేవు.',
        'no_media': 'ఇంకా ఎలాంటి ఫోటోలు లేదా వీడియోలు అప్‌లోడ్ చేయబడలేదు.',
        'divine_heritage_title': 'పంచపీఠాలు',
        'veerashaiva_title': 'వీరశైవ-లింగాయత్',
        'nav_home': 'హోమ్',
        'nav_jagathguru': 'జగద్గురు',
        'nav_pooja_booking': 'పూజా బుకింగ్',
        'nav_contact_us': 'మమ్మల్ని సంప్రదించండి',
        'nav_sign_in': 'సైన్ ఇన్ / సైన్ అప్',
        'nav_my_bookings': 'నా బుకింగ్‌లు',
        'login_prompt': 'OTP పొందడానికి మీ మొబైల్ నంబర్‌ను నమోదు చేయండి.',
        'mobile_number_label': 'మొబైల్ నంబర్',
        'send_otp_btn': 'OTP పంపండి',
        'enter_otp_label': 'OTP నమోదు చేయండి',
        'verify_login_btn': 'ధృవీకరించి లాగిన్ అవ్వండి',
    
        'login_welcome': 'పంచ పీఠాలకు తిరిగి స్వాగతం',
        'username_label': 'వాడుకరి పేరు',
        'password_label': 'పాస్వర్డ్',
        'sign_in_only': 'సైన్ ఇన్',
        'no_account_prompt': 'ఖాతా లేదా?',
        'sign_up_btn': 'సైన్ అప్ చేయండి',
    },
    'ta': {
        'site_title': 'வீரசைவ பஞ்ச பீடங்கள்',
        'site_subtitle': 'வீரசைவ பஞ்ச பீடங்கள்',
        'hero_title': 'வீரசைவ மரபின் <span class="keyword">ஐந்து புனித பீடங்கள்</span>',
        'hero_subtitle': '<span class="keyword">பஞ்ச பீடங்கள்</span> என்பது வீரசைவத்தை பரப்ப சிவபெருமானின் <span class="keyword">ஐந்து முகங்களில்</span> இருந்து தோன்றிய <span class="keyword">பஞ்சாச்சார்யர்களால்</span> நிறுவப்பட்ட ஐந்து பழமையான மடங்களாகும்.',
        'explore_peetha': 'பீடத்தின் விவரங்கள் →',
        'founded_by': 'நிறுவியவர்:',
        'peeta_suffix': 'பீடம்',
        'about_title': '<span class="keyword">வீரசைவம்</span> பற்றி',
        'about_p1': '<span class="keyword">வீரசைவம்</span> ஒரு பழமையான சைவ மரபு. சிவபெருமான் மீதான பக்தி, <span class="keyword">இஷ்டலிங்க தாரணை</span> மற்றும் <span class="keyword">பஞ்சாச்சாரம்</span> (லிங்காச்சாரம், சதாச்சாரம், சிவாச்சாரம், பிருத்யாச்சாரம், கணாச்சாரம்) ஆகியவற்றை இது வலியுறுத்துகிறது.',
        'about_p2': '<strong>சித்தாந்த சிகாமணி</strong> வீரசைவத்தின் முக்கிய புனித நூலாகும். சிவபெருமானின் ஐந்து முகங்களான <span class="keyword">சத்யோஜாதம்</span>, <span class="keyword">வாமதேவம்</span>, <span class="keyword">அகோரம்</span>, <span class="keyword">தத்புருஷம்</span>, <span class="keyword">ஈசானம்</span> ஆகியவற்றிலிருந்து அவதரித்த பஞ்சாச்சார்யர்கள் இந்தியா முழுவதும் இந்த ஐந்து பீடங்களை நிறுவினர்.',
        'back_link': '← அனைத்து பீடங்களுக்கும் திரும்புக',
        'key_details': 'முக்கிய விவரங்கள்',
        'founding_acharya': 'நிறுவிய ஜகத்குரு',
        'simhasana_label': 'சிம்மாசனம்',
        'associated_linga_label': 'தொடர்புடைய லிங்கம்',
        'location_label': 'இடம்',
        'current_swamiji_label': 'தற்போதைய ஜகத்குரு',
        'history_label': 'வரலாறு',
        'about_label': 'பீடத்தைப் பற்றி',
        'copyright': '© வீரசைவ பஞ்ச பீடங்கள்',
        'login_btn': 'உள்நுழைக',
        'logout_btn': 'வெளியேறு',
        'dashboard_btn': 'கட்டுப்பாட்டு அறை',
        'travel_plans_title': 'சுவாமிகளின் பயணத் திட்டங்கள்',
        'media_gallery_title': 'புகைப்படங்கள் & காணொளிகள்',
        'no_travel_plans': 'இந்த மாதத்தில் பயணத் திட்டங்கள் எதுவும் இல்லை.',
        'no_media': 'இதுவரை புகைப்படங்களோ காணொளிகளோ பதிவேற்றப்படவில்லை.',
        'divine_heritage_title': 'பஞ்சபீடங்கள்',
        'veerashaiva_title': 'வீரசைவ-லிங்காயத்',
        'nav_home': 'முகப்பு',
        'nav_jagathguru': 'ஜகத்குரு',
        'nav_pooja_booking': 'பூஜை முன்பதிவு',
        'nav_contact_us': 'தொடர்பு கொள்ள',
        'nav_sign_in': 'உள்நுழைய / பதிவு செய்ய',
        'nav_my_bookings': 'எனது முன்பதிவுகள்',
        'login_prompt': 'OTP ஐ பெற உங்கள் மொபைல் எண்ணை உள்ளிடவும்.',
        'mobile_number_label': 'மொபைல் எண்',
        'send_otp_btn': 'OTP அனுப்பு',
        'enter_otp_label': 'OTP ஐ உள்ளிடவும்',
        'verify_login_btn': 'சரிபார்த்து உள்நுழையவும்',
    
        'login_welcome': 'பஞ்ச பீடங்களுக்கு மீண்டும் வரவேற்கிறோம்',
        'username_label': 'பயனர் பெயர்',
        'password_label': 'கடவுச்சொல்',
        'sign_in_only': 'உள்நுழைக',
        'no_account_prompt': 'கணக்கு இல்லையா?',
        'sign_up_btn': 'பதிவு செய்யவும்',
    },
    'ml': {
        'site_title': 'വീരശൈവ പഞ്ചപീഠങ്ങൾ',
        'site_subtitle': 'വീരശൈവ പഞ്ചപീഠങ്ങൾ',
        'hero_title': 'വീരശൈവ പാരമ്പര്യത്തിലെ <span class="keyword">അഞ്ച് പുണ്യപീഠങ്ങൾ</span>',
        'hero_subtitle': 'വീരശൈവ ധർമ്മം പ്രചരിപ്പിക്കുന്നതിനായി പരമശിവൻ്റെ <span class="keyword">അഞ്ച് മുഖങ്ങളിൽ</span> നിന്ന് അവതരിച്ച <span class="keyword">പഞ്ചാചാര്യന്മാർ</span> സ്ഥാപിച്ച അഞ്ച് പ്രാചീന മഠങ്ങളാണ് <span class="keyword">പഞ്ചപീഠങ്ങൾ</span>.',
        'explore_peetha': 'പീഠത്തെക്കുറിച്ച് അറിയുക →',
        'founded_by': 'സ്ഥാപകൻ:',
        'peeta_suffix': 'പീഠം',
        'about_title': '<span class="keyword">വീരശൈവ ധർമ്മത്തെക്കുറിച്ച്</span>',
        'about_p1': 'പരമശിവനോടുള്ള ഭക്തി, ശരീരത്തിൽ <span class="keyword">ഇഷ്ടലിംഗധാരണം</span>, <span class="keyword">പഞ്ചാചാരങ്ങൾ</span> (ലിംഗാചാരം, സദാചാരം, ശിവാചാരം, ഭൃത്യാചാരം, ഗണാചാരം) എന്നിവയ്ക്ക് പ്രാധാന്യം നൽകുന്ന ഒരു പ്രാചീന ശൈവ പാരമ്പര്യമാണ് <span class="keyword">വീരശൈവം</span>.',
        'about_p2': '<strong>സിദ്ധാന്ത ശിഖാമണി</strong> ആണ് ഈ പാരമ്പര്യത്തിലെ മുഖ്യ ഗ്രന്ഥം. പരമശിവൻ്റെ അഞ്ച് മുഖങ്ങളായ <span class="keyword">സദ്യോജാതം</span>, <span class="keyword">വാമദേവം</span>, <span class="keyword">അഘോരം</span>, <span class="keyword">തത്പുരുഷം</span>, <span class="keyword">ഈശാനം</span> എന്നിവയിൽ നിന്നും അവതരിച്ച പഞ്ചാചാര്യന്മാർ ഭാരതത്തിലുടനീളം ഈ അഞ്ച് പീഠങ്ങൾ സ്ഥാപിച്ചുവെന്ന് വിശ്വസിക്കപ്പെടുന്നു.',
        'back_link': '← പ്രധാന പേജിലേക്ക് മടങ്ങുക',
        'key_details': 'പ്രധാന വിവരങ്ങൾ',
        'founding_acharya': 'സ്ഥാപക ജഗദ്ഗുരു',
        'simhasana_label': 'സിംഹാസനം',
        'associated_linga_label': 'ബന്ധപ്പെട്ട ലിംഗം',
        'location_label': 'സ്ഥലം',
        'current_swamiji_label': 'നിലവിലെ ജഗദ്ഗുരു',
        'history_label': 'ചരിത്രം',
        'about_label': 'പീഠത്തെക്കുറിച്ച്',
        'copyright': '© വീരശൈവ പഞ്ചപീഠങ്ങൾ',
        'login_btn': 'ലോഗിൻ',
        'logout_btn': 'ലോഗൗട്ട്',
        'dashboard_btn': 'ഡാഷ്‌ബോർഡ്',
        'travel_plans_title': 'സ്വാമിജിയുടെ യാത്രാ വിവരങ്ങൾ',
        'media_gallery_title': 'ചിത്രങ്ങളും വീഡിയോകളും',
        'no_travel_plans': 'ഈ മാസത്തിൽ യാത്രാ പരിപാടികളില്ല.',
        'no_media': 'ചിത്രങ്ങളോ വീഡിയോകളോ ഇതുവരെ അപ്‌ലോഡ് ചെയ്തിട്ടില്ല.',
        'divine_heritage_title': 'പഞ്ചപീഠങ്ങൾ',
        'veerashaiva_title': 'വീരശൈവ-ലിംഗായത്ത്',
        'nav_home': 'ഹോം',
        'nav_jagathguru': 'ജഗദ്ഗുരു',
        'nav_pooja_booking': 'പൂജ ബുക്കിംഗ്',
        'nav_contact_us': 'ബന്ധപ്പെടുക',
        'nav_sign_in': 'സൈൻ ഇൻ / സൈൻ അപ്പ്',
        'nav_my_bookings': 'എൻ്റെ ബുക്കിംഗുകൾ',
        'login_prompt': 'OTP ലഭിക്കുന്നതിന് നിങ്ങളുടെ മൊബൈൽ നമ്പർ നൽകുക.',
        'mobile_number_label': 'മൊബൈൽ നമ്പർ',
        'send_otp_btn': 'OTP അയയ്ക്കുക',
        'enter_otp_label': 'OTP നൽകുക',
        'verify_login_btn': 'സ്ഥിരീകരിച്ച് ലോഗിൻ ചെയ്യുക',
    
        'login_welcome': 'പഞ്ച പീഠങ്ങളിലേക്ക് വീണ്ടും സ്വാഗതം',
        'username_label': 'ഉപയോക്തൃനാമം',
        'password_label': 'പാസ്‌വേഡ്',
        'sign_in_only': 'സൈൻ ഇൻ ചെയ്യുക',
        'no_account_prompt': 'അക്കൗണ്ട് ഇല്ലേ?',
        'sign_up_btn': 'സൈൻ അപ്പ് ചെയ്യുക',
    }
}

MONTH_NAMES = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'kn': ['ಜನವರಿ', 'ಫೆಬ್ರವರಿ', 'ಮಾರ್ಚ್', 'ಏಪ್ರಿಲ್', 'ಮೇ', 'ಜೂನ್', 'ಜುಲೈ', 'ಆಗಸ್ಟ್', 'ಸೆಪ್ಟೆಂಬರ್', 'ಅಕ್ಟೋಬರ್', 'ನವೆಂಬರ್', 'ಡಿಸೆಂಬರ್'],
    'mr': ['जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर'],
    'hi': ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'],
    'te': ['జనవరి', 'ఫిబ్రవరి', 'మార్చి', 'ఏప్రిల్', 'మే', 'జూన్', 'జూలై', 'ఆగస్టు', 'సెప్టెంబర్', 'అక్టోబర్', 'నవంబర్', 'డిసెంబర్'],
    'ta': ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்', 'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'],
    'ml': ['ജനുവരി', 'ഫെബ്രുവരി', 'മാർച്ച്', 'ഏപ്രിൽ', 'മെയ്', 'ജൂൺ', 'ജൂലൈ', 'ആഗസ്റ്റ്', 'സെപ്റ്റംബർ', 'ഒക്ടോബർ', 'നവംബർ', 'ഡിസംബർ'],
}


def get_language(request):
    lang = request.GET.get('lang')
    if lang in ['en', 'kn', 'mr', 'hi', 'te', 'ta', 'ml']:
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
        elif lang == 'te':
            obj.short_name = obj.name.replace(" పీఠం", "")
        elif lang == 'ta':
            obj.short_name = obj.name.replace(" பீடம்", "")
        elif lang == 'ml':
            obj.short_name = obj.name.replace(" പീഠം", "")
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
            'firebase_config': json.dumps(settings.FIREBASE_WEB_CONFIG)
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
            title_te = form.cleaned_data.get('title_te', '').strip()
            description_te = form.cleaned_data.get('description_te', '').strip()
            title_ta = form.cleaned_data.get('title_ta', '').strip()
            description_ta = form.cleaned_data.get('description_ta', '').strip()
            title_ml = form.cleaned_data.get('title_ml', '').strip()
            description_ml = form.cleaned_data.get('description_ml', '').strip()

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
                            title_te=title_te,
                            description_te=description_te,
                            title_ta=title_ta,
                            description_ta=description_ta,
                            title_ml=title_ml,
                            description_ml=description_ml,
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
                                title_te=title_te,
                                description_te=description_te,
                                title_ta=title_ta,
                                description_ta=description_ta,
                                title_ml=title_ml,
                                description_ml=description_ml,
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
