from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Peetha, TravelPlan, PeethaHandler, PeethaMedia, Pooja, PoojaBooking, PeethaPaymentConfig, FeatureFlag, Building, Room, AccommodationBooking
from .forms import TravelPlanForm, PeethaMediaAddForm, PeethaMediaEditForm, PeethaHandlerForm, PeethaPaymentConfigForm, PoojaForm, BuildingForm
from django.db import models

import datetime
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .heritage_content import HERITAGE_CONTENT
from .veerashaiva_content import VEERASHAIVA_CONTENT
from .feature_flags import USE_RECTANGULAR_PORTRAITS

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
        'veerashaiva_title': 'Srimad Veerashiva',
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
        'birthday_title': 'Happy Birthday',
        'birthday_message': 'May the divine blessings of Lord Shiva and the holy Jagadgurus of the Pancha Peethas be with you on this auspicious day.',
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
        'veerashaiva_title': 'ಶ್ರೀಮದ್ ವೀರಶೈವ',
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
        'birthday_title': 'ಜನ್ಮದಿನದ ಶುಭಾಶಯಗಳು',
        'birthday_message': 'ಈ ಪವಿತ್ರ ದಿನದಂದು ಭಗವಾನ್ ಶಿವ ಮತ್ತು ಪಂಚಪೀಠಗಳ ಜಗದ್ಗುರುಗಳ ದಿವ್ಯ ಆಶೀರ್ವಾದವು ನಿಮ್ಮ ಮೇಲಿರಲಿ. ✨🕉️',
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
        'veerashaiva_title': 'श्रीमद् वीरशैव',
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
        'birthday_title': 'वाढदिवसाच्या हार्दिक शुभेच्छा',
        'birthday_message': 'या मंगलदिनी भगवान शिव आणि पंचपीठांच्या जगद्गुरूंचे दिव्य आशीर्वाद आपल्या पाठीशी राहोत.',
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
        'veerashaiva_title': 'श्रीमद् वीरशैव',
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
        'birthday_title': 'जन्मदिन की हार्दिक शुभकामनाएं',
        'birthday_message': 'इस पावन अवसर पर भगवान शिव और पंचपीठों के जगद्गुरुओं का दिव्य आशीर्वाद आपको प्राप्त हो।',
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
        'veerashaiva_title': 'శ్రీమద్ వీరశైవ',
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
        'birthday_title': 'పుట్టినరోజు శుభాకాంక్షలు',
        'birthday_message': 'ఈ పవిత్ర దినమున శివుని మరియు పంచపీఠాల జగద్గురువుల దివ్య ఆశీస్సులు మీకు లభించాలని కోరుకుంటున్నాము.',
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
        'veerashaiva_title': 'ஸ்ரீமத் வீரசைவ',
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
        'birthday_title': 'இனிய பிறந்தநாள் நல்வாழ்த்துகள்',
        'birthday_message': 'இந்த நன்னாளில் சிவபெருமானின் மற்றும் பஞ்ச பீடங்களின் ஜകத்குருக்களின் தெய்வீக அருள் உங்களுக்கு கிடைக்கட்டும். ✨🕉️',
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
        'veerashaiva_title': 'ശ്രീമദ് വീരശൈവ',
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
        'birthday_title': 'ജന്മദിനാശംസകൾ',
        'birthday_message': 'ഈ മംഗളദിനത്തിൽ പരമശിവന്റെയും പഞ്ചപീഠങ്ങളുടെ ജഗദ്ഗുരുക്കളുടെയും ദിവ്യാനുഗ്രഹം നിങ്ങൾക്ക് ഉണ്ടാകട്ടെ.',
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
    elif isinstance(obj, Pooja):
        fields = ['name', 'description']
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
    
    is_birthday = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.date_of_birth:
                today = datetime.date.today()
                if profile.date_of_birth.month == today.month and profile.date_of_birth.day == today.day:
                    is_birthday = True
        except Exception:
            pass
    if request.GET.get('test_birthday') == 'true':
        is_birthday = True

    return render(request, 'peethas/home.html', {
        'peethas': peethas,
        'use_rectangular_portraits': USE_RECTANGULAR_PORTRAITS,
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'heritage_content': HERITAGE_CONTENT[lang],
        'veerashaiva_content': VEERASHAIVA_CONTENT[lang],
        'is_birthday': is_birthday,
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

    # Feature Flags check — all peetha-level features
    flag_keys = [
        'overall', 'pooja_booking', 'accommodation', 'media_gallery',
        'travel_plans', 'live_stream', 'contact_section'
    ]
    flags = {}
    for key in flag_keys:
        flag_obj, _ = FeatureFlag.objects.get_or_create(
            name=f"{slug}_{key}",
            defaults={'is_enabled': True, 'description': f"{key.replace('_', ' ').title()} flag ({peetha.name})"}
        )
        flags[key] = flag_obj.is_enabled
    
    overall_enabled = flags['overall']
    pooja_booking_enabled = overall_enabled and flags['pooja_booking']
    accommodation_enabled = overall_enabled and flags['accommodation']
    media_gallery_enabled = overall_enabled and flags['media_gallery']
    travel_plans_enabled = overall_enabled and flags['travel_plans']
    live_stream_enabled = overall_enabled and flags['live_stream']
    contact_section_enabled = overall_enabled and flags['contact_section']

    return render(request, 'peethas/peetha_detail.html', {
        'peetha': peetha,
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'travel_plans_grouped': grouped_plans,
        'media_gallery': media_list,
        'poojas': poojas,
        'show_admin_button': show_admin_button,
        'pooja_booking_enabled': pooja_booking_enabled,
        'accommodation_enabled': accommodation_enabled,
        'media_gallery_enabled': media_gallery_enabled,
        'travel_plans_enabled': travel_plans_enabled,
        'live_stream_enabled': live_stream_enabled,
        'contact_section_enabled': contact_section_enabled,
    })


# ===== Authentication Views =====

def login_view(request):
    lang = get_language(request)
    next_url = request.GET.get('next', 'peethas:home')
    
    if request.user.is_authenticated:
        if request.user.is_superuser or hasattr(request.user, 'handler_profile'):
            return redirect('peethas:dashboard_home')
        return redirect(next_url)
        
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


def register_view(request):
    lang = get_language(request)
    next_url = request.GET.get('next', 'peethas:home')
    
    if request.user.is_authenticated:
        return redirect('peethas:home')
        
    from .feature_flags import DEVOTEE_REGISTRATION
    if not bool(DEVOTEE_REGISTRATION):
        messages.error(request, 'Devotee registration is currently disabled.')
        return redirect('peethas:login')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
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

def check_peetha_authorization(user, peetha, readonly=False, allow_staff_write=False):
    """
    Checks if the logged-in user is a superuser or the assigned handler/staff for the Peetha.
    For staff users (is_staff=True and not is_superuser), their access is strictly read-only.
    Raises PermissionDenied if not authorized or if staff tries to perform a write action.
    """
    if user.is_superuser:
        return True
    try:
        handler = user.handler_profile
        if handler.peetha == peetha:
            # Locked to this Peetha. If it's a write action (readonly=False) and they are staff, deny access
            if not readonly and user.is_staff and not allow_staff_write:
                raise PermissionDenied("Staff accounts have read-only access to this Peetha.")
            return True
    except PeethaHandler.DoesNotExist:
        pass
    raise PermissionDenied("You do not have permission to manage this Peetha.")


@login_required(login_url='peethas:login')
def dashboard_home(request):
    lang = get_language(request)
    
    # Check if user is a Peetha Handler first
    try:
        handler = request.user.handler_profile
        return redirect('peethas:dashboard_peetha', slug=handler.peetha.slug)
    except PeethaHandler.DoesNotExist:
        pass

    # If superuser: show the portal where they can manage any Peetha or view reports
    if request.user.is_superuser:
        peethas = Peetha.objects.all()
        
        # Tech and non-tech stats/reports
        total_users = User.objects.count()
        total_bookings = PoojaBooking.objects.filter(payment_status='success').count()
        
        # Total revenue
        total_revenue_val = PoojaBooking.objects.filter(payment_status='success').aggregate(total=models.Sum('amount'))['total']
        total_revenue = total_revenue_val if total_revenue_val is not None else 0.00
        
        active_payments = PeethaPaymentConfig.objects.filter(is_active=True).count()
        
        # Recent Bookings
        recent_bookings = PoojaBooking.objects.select_related('pooja', 'pooja__peetha').order_by('-created_at')[:10]
        
        # Handlers list
        handlers = PeethaHandler.objects.select_related('user', 'peetha').filter(user__is_staff=False, user__is_superuser=False)
        
        # Users list for dropdown (exclude staff/superusers)
        users = User.objects.filter(is_superuser=False, is_staff=False).order_by('username')

        # Staff and Super Admin users list
        staff_users = User.objects.filter(models.Q(is_staff=True) | models.Q(is_superuser=True)).distinct().order_by('username')
        
        # Payment Configs
        payment_configs = PeethaPaymentConfig.objects.select_related('peetha').all()
        
        # Feature Flags
        peethas_list = Peetha.objects.all().order_by('id')
        features_meta = [
            {'key': 'overall', 'name': 'Overall Status', 'desc': 'Master toggle for all features of this Peetha'},
            {'key': 'pooja_booking', 'name': 'Pooja Booking', 'desc': 'Enable or disable online Pooja/Seva booking'},
            {'key': 'accommodation', 'name': 'Accommodation', 'desc': 'Enable or disable Accommodation section'},
            {'key': 'media_gallery', 'name': 'Media Gallery', 'desc': 'Show or hide the Photo & Video gallery'},
            {'key': 'travel_plans', 'name': 'Swamiji Travel Plans', 'desc': 'Show or hide the Travel Plans timeline'},
            {'key': 'live_stream', 'name': 'YouTube Live Stream', 'desc': 'Show or hide the Live Stream embed'},
            {'key': 'contact_section', 'name': 'Contact Us', 'desc': 'Show or hide the Contact Us section'},
        ]
        
        feature_board = []
        for feat in features_meta:
            row_cells = []
            for p in peethas_list:
                flag_name = f"{p.slug}_{feat['key']}"
                flag_obj, created = FeatureFlag.objects.get_or_create(
                    name=flag_name,
                    defaults={
                        'is_enabled': True,
                        'description': f"{feat['desc']} ({p.name})"
                    }
                )
                row_cells.append({
                    'peetha': p,
                    'flag': flag_obj
                })
            feature_board.append({
                'key': feat['key'],
                'name': feat['name'],
                'desc': feat['desc'],
                'cells': row_cells
            })

        # All peetha-level feature keys (used to exclude from global settings list)
        peetha_feature_keys = [f['key'] for f in features_meta]
        peetha_flag_q = models.Q()
        for key in peetha_feature_keys:
            peetha_flag_q |= models.Q(name__endswith=f'_{key}')
        feature_flags = FeatureFlag.objects.exclude(peetha_flag_q).order_by('name')

        # Ensure global system flags exist
        FeatureFlag.objects.get_or_create(
            name='DEVOTEE_REGISTRATION',
            defaults={'is_enabled': True, 'description': 'Allow new devotees to register on the platform'}
        )
        
        # Forms for action panels
        handler_form = PeethaHandlerForm()
        handler_form.fields['user'].queryset = User.objects.filter(
            models.Q(is_staff=True) | models.Q(is_superuser=True) | models.Q(handler_profile__isnull=False)
        ).distinct().order_by('username')
        
        payment_form = PeethaPaymentConfigForm()
        
        all_poojas = Pooja.objects.select_related('peetha').filter(is_active=True).order_by('peetha__name', 'name')
        
        return render(request, 'peethas/dashboard.html', {
            'is_admin': True,
            'is_superuser': request.user.is_superuser,
            'is_staff': request.user.is_staff and not request.user.is_superuser,
            'peethas': peethas,
            'total_users': total_users,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
            'active_payments': active_payments,
            'recent_bookings': recent_bookings,
            'handlers': handlers,
            'users': users,
            'staff_users': staff_users,
            'payment_configs': payment_configs,
            'feature_flags': feature_flags,
            'feature_board': feature_board,
            'handler_form': handler_form,
            'payment_form': payment_form,
            'all_poojas': all_poojas,
            'labels': TRANSLATIONS['en'],  # Admin panel uses English
            'lang': lang,
        })
    
    logout(request)
    messages.error(request, "This account is not associated with any Peetha. Logging out.")
    return redirect('peethas:login')


@login_required(login_url='peethas:login')
def assign_handler(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
        
    if request.method == 'POST':
        action = request.POST.get('action', 'assign')
        
        msg = ""
        success = True
        
        if action == 'delete':
            handler_id = request.POST.get('handler_id')
            if handler_id:
                handler = get_object_or_404(PeethaHandler, pk=handler_id)
                username = handler.user.username
                peetha_name = handler.peetha.name
                user = handler.user
                user.is_staff = False
                user.save()
                handler.delete()
                msg = f"Removed {username} as handler for {peetha_name}."
                messages.success(request, msg)
        elif action == 'revoke_staff':
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(User, pk=user_id)
                PeethaHandler.objects.filter(user=user).delete()
                user.is_staff = False
                user.is_superuser = False
                user.save()
                msg = f"Revoked staff/admin access for {user.username}."
                messages.success(request, msg)
        else:
            user_id = request.POST.get('user')
            role = request.POST.get('role', 'handler')
            user = get_object_or_404(User, pk=user_id)
            
            if role == 'superuser':
                # Since they are becoming Super Admin, remove handler mapping if any
                PeethaHandler.objects.filter(user=user).delete()
                user.is_staff = True
                user.is_superuser = True
                user.save()
                msg = f"Assigned {user.username} as Super Admin."
                messages.success(request, msg)
            elif role == 'staff':
                peetha_id = request.POST.get('peetha')
                if not peetha_id:
                    msg = "Please select a Peetha for the staff."
                    success = False
                    messages.error(request, msg)
                else:
                    peetha = get_object_or_404(Peetha, pk=peetha_id)
                    PeethaHandler.objects.filter(user=user).delete()
                    user.is_staff = True
                    user.is_superuser = False
                    user.save()
                    PeethaHandler.objects.create(user=user, peetha=peetha)
                    msg = f"Assigned {user.username} as Staff (Read-Only admin) for {peetha.name}."
                    messages.success(request, msg)
            elif role == 'handler':
                peetha_id = request.POST.get('peetha')
                if not peetha_id:
                    msg = "Please select a Peetha for the handler."
                    success = False
                    messages.error(request, msg)
                else:
                    peetha = get_object_or_404(Peetha, pk=peetha_id)
                    # Since user is OneToOne, check if they are already a handler elsewhere and delete that
                    PeethaHandler.objects.filter(user=user).delete()
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    PeethaHandler.objects.create(user=user, peetha=peetha)
                    msg = f"Assigned {user.username} as handler for {peetha.name}."
                    messages.success(request, msg)
            else:  # devotee
                PeethaHandler.objects.filter(user=user).delete()
                user.is_staff = False
                user.is_superuser = False
                user.save()
                msg = f"Changed {user.username}'s role to regular Devotee."
                messages.success(request, msg)
                
        # AJAX response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': success,
                'message': msg
            })
            
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_home') + '#roles-section:active-handlers-view')


@login_required(login_url='peethas:login')
def create_user_account(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
        
    redirect_hash = '#roles-section:create-account-view'
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', 'devotee')
        peetha_id = request.POST.get('peetha', '')
        
        from django.urls import reverse
        
        if not username:
            messages.error(request, "Username is required.")
        elif not email:
            messages.error(request, "Email is required.")
        elif not password:
            messages.error(request, "Password is required.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email address already exists.")
        else:
            try:
                if role == 'superuser':
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name
                    )
                    messages.success(request, f"Super Admin account '{username}' successfully created.")
                elif role == 'staff':
                    if not peetha_id:
                        messages.error(request, "Please select a Peetha for the staff.")
                        return redirect(reverse('peethas:dashboard_home') + '#roles-section:create-account-view')
                    
                    peetha = get_object_or_404(Peetha, pk=peetha_id)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name
                    )
                    user.is_staff = True
                    user.save()
                    PeethaHandler.objects.create(user=user, peetha=peetha)
                    messages.success(request, f"Staff account '{username}' successfully created and assigned to {peetha.name}.")
                    redirect_hash = '#roles-section:active-handlers-view'
                elif role == 'handler':
                    if not peetha_id:
                        messages.error(request, "Please select a Peetha for the handler.")
                        return redirect(reverse('peethas:dashboard_home') + '#roles-section:create-account-view')
                    
                    peetha = get_object_or_404(Peetha, pk=peetha_id)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name
                    )
                    # Create handler mapping
                    PeethaHandler.objects.create(user=user, peetha=peetha)
                    messages.success(request, f"Peetha Handler account '{username}' successfully created and assigned to {peetha.name}.")
                    redirect_hash = '#roles-section:active-handlers-view'
                else: # devotee
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name
                    )
                    messages.success(request, f"Devotee account '{username}' successfully created.")
            except Exception as e:
                messages.error(request, f"An error occurred while creating the account: {str(e)}")
                
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_home') + redirect_hash)


@login_required(login_url='peethas:login')
def manage_payment_config(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
        
    if request.method == 'POST':
        peetha_id = request.POST.get('peetha')
        peetha = get_object_or_404(Peetha, pk=peetha_id)
        
        # Get or create payment config
        config, created = PeethaPaymentConfig.objects.get_or_create(peetha=peetha)
        
        form = PeethaPaymentConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated payment configuration for {peetha.name}.")
        else:
            messages.error(request, "Failed to update payment configuration. Please check your inputs.")
            
    return redirect('peethas:dashboard_home')


@login_required(login_url='peethas:login')
def delete_payment_config(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied()
        
    config = get_object_or_404(PeethaPaymentConfig, pk=pk)
    peetha_name = config.peetha.name
    config.delete()
    messages.success(request, f"Deleted payment configuration for {peetha_name}.")
    return redirect('peethas:dashboard_home')


@login_required(login_url='peethas:login')
def toggle_feature(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied()
        
    flag = get_object_or_404(FeatureFlag, pk=pk)
    flag.is_enabled = not flag.is_enabled
    flag.save()
    
    updated_flags = [flag]
    
    # All peetha-level feature keys (must match features_meta in dashboard_home)
    PEETHA_FEATURE_KEYS = [
        'overall', 'pooja_booking', 'accommodation', 'media_gallery',
        'travel_plans', 'live_stream', 'contact_section'
    ]
    CHILD_KEYS = [k for k in PEETHA_FEATURE_KEYS if k != 'overall']
    
    peetha_slug, feature_key = None, None
    for key in PEETHA_FEATURE_KEYS:
        suffix = f'_{key}'
        if flag.name.endswith(suffix):
            peetha_slug = flag.name[:-len(suffix)]
            feature_key = key
            break
        
    if peetha_slug and feature_key:
        # If overall is turned off, disable all child feature flags for this peetha
        if feature_key == 'overall' and not flag.is_enabled:
            for key in CHILD_KEYS:
                f_name = f"{peetha_slug}_{key}"
                try:
                    f_obj = FeatureFlag.objects.get(name=f_name)
                    if f_obj.is_enabled:
                        f_obj.is_enabled = False
                        f_obj.save()
                        updated_flags.append(f_obj)
                except FeatureFlag.DoesNotExist:
                    pass
        # If any child feature is turned on, auto-enable overall for this peetha
        elif feature_key in CHILD_KEYS and flag.is_enabled:
            overall_name = f"{peetha_slug}_overall"
            try:
                overall_obj = FeatureFlag.objects.get(name=overall_name)
                if not overall_obj.is_enabled:
                    overall_obj.is_enabled = True
                    overall_obj.save()
                    updated_flags.append(overall_obj)
            except FeatureFlag.DoesNotExist:
                pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', ''):
        return JsonResponse({
            'success': True,
            'updated': [
                {
                    'pk': uf.pk,
                    'name': uf.name,
                    'is_enabled': uf.is_enabled
                } for uf in updated_flags
            ]
        })
        
    messages.success(request, f"Feature flag '{flag.name}' set to {'Enabled' if flag.is_enabled else 'Disabled'}.")
    return redirect('peethas:dashboard_home')



@login_required(login_url='peethas:login')
def dashboard_peetha(request, slug):
    lang = get_language(request)
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha, readonly=True)

    media_list = PeethaMedia.objects.filter(peetha=peetha)
    travel_list = TravelPlan.objects.filter(peetha=peetha).order_by('start_date')
    pooja_list = Pooja.objects.filter(peetha=peetha).order_by('order', 'name')

    media_form = PeethaMediaAddForm()
    travel_form = TravelPlanForm()
    pooja_form = PoojaForm()
    building_form = BuildingForm()

    buildings = peetha.buildings.all()
    total_rooms_count = Room.objects.filter(building__peetha=peetha, building__is_active=True, is_active=True).count()
    accommodation_bookings = AccommodationBooking.objects.filter(peetha=peetha).select_related('room', 'room__building').order_by('-created_at')

    return render(request, 'peethas/dashboard.html', {
        'is_admin': request.user.is_superuser,
        'peetha': peetha,
        'media_list': media_list,
        'travel_list': travel_list,
        'pooja_list': pooja_list,
        'media_form': media_form,
        'travel_form': travel_form,
        'pooja_form': pooja_form,
        'building_form': building_form,
        'buildings': buildings,
        'total_rooms_count': total_rooms_count,
        'accommodation_bookings': accommodation_bookings,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def update_peetha_live(request, slug):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    
    if request.method == 'POST':
        live_url = request.POST.get('live_youtube_url', '').strip()
        live_title = request.POST.get('live_youtube_title', '').strip()
        
        if live_url:
            # Validate youtube url format
            import re
            pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
            match = re.search(pattern, live_url)
            if not match:
                messages.error(request, "Invalid YouTube URL format. Please provide a valid watch, share, or embed link.")
                from django.urls import reverse
                return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#live-section')
                
        peetha.live_youtube_url = live_url
        peetha.live_youtube_title = live_title if live_title else None
        peetha.save()
        if live_url:
            messages.success(request, f"YouTube Live Stream URL successfully updated for {peetha.name}.")
        else:
            messages.success(request, f"Live stream deactivated for {peetha.name}.")
            
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#live-section')


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


# --- Pooja CRUD Views ---

@login_required(login_url='peethas:login')
def pooja_add(request, slug):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)

    if request.method == 'POST':
        form = PoojaForm(request.POST)
        if form.is_valid():
            pooja = form.save(commit=False)
            pooja.peetha = peetha
            pooja.save()
            messages.success(request, "Pooja/Seva added successfully.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#pooja-section')


@login_required(login_url='peethas:login')
def pooja_edit(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    pooja_item = get_object_or_404(Pooja, pk=pk, peetha=peetha)

    if request.method == 'POST':
        form = PoojaForm(request.POST, instance=pooja_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Pooja/Seva updated successfully.")
            from django.urls import reverse
            return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#pooja-section')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PoojaForm(instance=pooja_item)

    lang = get_language(request)
    return render(request, 'peethas/dashboard_edit.html', {
        'peetha': peetha,
        'edit_type': 'pooja',
        'pooja_item': pooja_item,
        'form': form,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def pooja_delete(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha)
    pooja_item = get_object_or_404(Pooja, pk=pk, peetha=peetha)
    
    if request.method == 'POST':
        pooja_item.delete()
        messages.success(request, "Pooja/Seva deleted.")
        
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#pooja-section')


# --- Building CRUD Views ---

@login_required(login_url='peethas:login')
def building_add(request, slug):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha, allow_staff_write=True)

    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            try:
                building = form.save(commit=False)
                building.peetha = peetha
                building.save()
                messages.success(request, "Building and rooms added successfully.")
            except Exception as e:
                messages.error(request, f"Error creating building: {e}")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#accommodation-section')


@login_required(login_url='peethas:login')
def building_edit(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha, allow_staff_write=True)
    building_item = get_object_or_404(Building, pk=pk, peetha=peetha)

    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building_item)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Building and rooms updated successfully.")
                from django.urls import reverse
                return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#accommodation-section')
            except models.ProtectedError:
                messages.error(request, "Cannot update building layout: Some rooms that would be deleted have active devotee bookings.")
            except Exception as e:
                messages.error(request, f"Error updating building: {e}")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = BuildingForm(instance=building_item)

    lang = get_language(request)
    return render(request, 'peethas/dashboard_edit.html', {
        'peetha': peetha,
        'edit_type': 'building',
        'building_item': building_item,
        'form': form,
        'labels': TRANSLATIONS['en'],
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def building_delete(request, slug, pk):
    peetha = get_object_or_404(Peetha, slug=slug)
    check_peetha_authorization(request.user, peetha, allow_staff_write=True)
    building_item = get_object_or_404(Building, pk=pk, peetha=peetha)
    
    if request.method == 'POST':
        try:
            building_item.delete()
            messages.success(request, "Building and all associated rooms deleted successfully.")
        except models.ProtectedError:
            messages.error(request, "Cannot delete building: Some rooms in this building have active devotee bookings.")
        except Exception as e:
            messages.error(request, f"Error deleting building: {e}")
        
    from django.urls import reverse
    return redirect(reverse('peethas:dashboard_peetha', kwargs={'slug': peetha.slug}) + '#accommodation-section')


# ===== POOJA BOOKING VIEWS =====

@login_required(login_url='peethas:login')
def initiate_pooja_booking(request, peetha_slug):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser or hasattr(request.user, 'handler_profile'):
            raise PermissionDenied("Booking is not allowed for administrators, staff, or handlers.")
            
    peetha = get_object_or_404(Peetha, slug=peetha_slug)
    
    # Feature flag check
    overall_flag, _ = FeatureFlag.objects.get_or_create(
        name=f"{peetha_slug}_overall",
        defaults={'is_enabled': True, 'description': f"Overall Master toggle ({peetha.name})"}
    )
    pooja_flag, _ = FeatureFlag.objects.get_or_create(
        name=f"{peetha_slug}_pooja_booking",
        defaults={'is_enabled': True, 'description': f"Pooja Booking flag ({peetha.name})"}
    )
    if not (overall_flag.is_enabled and pooja_flag.is_enabled):
        messages.error(request, "Online Pooja Booking is currently unavailable for this Peetha.")
        return redirect('peethas:peetha_detail', slug=peetha.slug)
        
    if request.method == 'POST':
        pooja_id = request.POST.get('pooja_id')
        pooja = get_object_or_404(Pooja, pk=pooja_id, peetha=peetha)
        
        devotee_name = request.POST.get('devotee_name')
        devotee_phone = request.POST.get('devotee_phone')
        devotee_email = request.POST.get('devotee_email', '')
        gotra = request.POST.get('gotra', '')
        nakshatra = request.POST.get('nakshatra', '')
        rashi = request.POST.get('rashi', '')
        # Read dynamic family member arrays
        family_names = request.POST.getlist('family_member_name')
        family_gotras = request.POST.getlist('family_member_gotra')
        family_nakshatras = request.POST.getlist('family_member_nakshatra')
        family_rashis = request.POST.getlist('family_member_rashi')
        
        family_list = []
        for i in range(len(family_names)):
            if family_names[i].strip():
                family_list.append({
                    'name': family_names[i].strip(),
                    'gotra': family_gotras[i].strip() if i < len(family_gotras) else '',
                    'nakshatra': family_nakshatras[i].strip() if i < len(family_nakshatras) else '',
                    'rashi': family_rashis[i].strip() if i < len(family_rashis) else ''
                })
        family_members = json.dumps(family_list) if family_list else ''
        date_of_pooja = request.POST.get('date_of_pooja')
        
        # Validate date is not in the past
        try:
            booking_date = datetime.datetime.strptime(date_of_pooja, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format selected.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)

        if booking_date < datetime.date.today():
            messages.error(request, "Pooja/Seva booking cannot be made for a past date.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)

        # Validate weekday availability
        weekday_name = booking_date.strftime('%A')
        if pooja.available_days and pooja.available_days != 'all':
            available_list = [d.strip() for d in pooja.available_days.split(',') if d.strip()]
            if weekday_name not in available_list:
                messages.error(request, f"This Pooja/Seva ({pooja.name}) is not available on {weekday_name}s.")
                return redirect('peethas:peetha_detail', slug=peetha.slug)

        # Validate slot availability
        booked_count = PoojaBooking.objects.filter(
            pooja=pooja,
            date_of_pooja=booking_date,
            payment_status__in=['pending', 'success']
        ).count()
        if booked_count >= pooja.total_slots:
            messages.error(request, f"Sorry, all slots are fully booked for {pooja.name} on {booking_date}. Please choose another date.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)

        # Bypassing online payments: Save successful booking directly
        booking = PoojaBooking.objects.create(
            pooja=pooja,
            user=request.user,
            devotee_name=devotee_name,
            devotee_phone=devotee_phone,
            devotee_email=devotee_email,
            gotra=gotra,
            nakshatra=nakshatra,
            rashi=rashi,
            family_members=family_members,
            date_of_pooja=date_of_pooja,
            amount=pooja.price,
            razorpay_order_id=f"ORD-DUMMY-{int(datetime.datetime.now().timestamp())}",
            razorpay_payment_id=f"PAY-DUMMY-{int(datetime.datetime.now().timestamp())}",
            payment_status='success'
        )
        
        return redirect('peethas:booking_success', booking_id=booking.id)
        
    return redirect('peethas:peetha_detail', slug=peetha.slug)


def pooja_availability(request, peetha_slug, pooja_id):
    peetha = get_object_or_404(Peetha, slug=peetha_slug)
    
    # Feature flag check
    overall_flag, _ = FeatureFlag.objects.get_or_create(
        name=f"{peetha_slug}_overall",
        defaults={'is_enabled': True, 'description': f"Overall Master toggle ({peetha.name})"}
    )
    pooja_flag, _ = FeatureFlag.objects.get_or_create(
        name=f"{peetha_slug}_pooja_booking",
        defaults={'is_enabled': True, 'description': f"Pooja Booking flag ({peetha.name})"}
    )
    if not (overall_flag.is_enabled and pooja_flag.is_enabled):
        return JsonResponse({'error': 'Online Pooja Booking is currently disabled'}, status=403)
        
    pooja = get_object_or_404(Pooja, pk=pooja_id, peetha=peetha)
    
    today = datetime.date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
    except (ValueError, TypeError):
        year = today.year
        month = today.month

    import calendar
    try:
        num_days = calendar.monthrange(year, month)[1]
    except Exception:
        return JsonResponse({'error': 'Invalid month or year'}, status=400)
        
    availability = {}
    
    # Pre-fetch all bookings in this month for this pooja
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, num_days)
    bookings = PoojaBooking.objects.filter(
        pooja=pooja,
        date_of_pooja__range=(start_date, end_date),
        payment_status__in=['pending', 'success']
    ).values('date_of_pooja').annotate(count=models.Count('id'))
    
    booking_counts = {b['date_of_pooja']: b['count'] for b in bookings}
    
    for day in range(1, num_days + 1):
        day_date = datetime.date(year, month, day)
        date_str = day_date.strftime('%Y-%m-%d')
        
        # Check if in past
        if day_date < today:
            availability[date_str] = 'not_open'
            continue
            
        # Check if weekday is available
        weekday_name = day_date.strftime('%A')
        if pooja.available_days and pooja.available_days != 'all':
            available_list = [d.strip() for d in pooja.available_days.split(',') if d.strip()]
            if weekday_name not in available_list:
                availability[date_str] = 'not_open'
                continue
                
        # Check slots
        booked_count = booking_counts.get(day_date, 0)
        if booked_count >= pooja.total_slots:
            availability[date_str] = 'booked'
        elif pooja.total_slots - booked_count <= 2:
            availability[date_str] = 'fast'
        else:
            availability[date_str] = 'available'
            
    return JsonResponse({
        'pooja_id': pooja.id,
        'total_slots': pooja.total_slots,
        'year': year,
        'month': month,
        'availability': availability
    })


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
def booking_success(request, booking_id):
    booking = get_object_or_404(PoojaBooking, pk=booking_id)
    # Ensure they can only see their own booking, unless they are staff/superuser/handler
    if booking.user != request.user and not (request.user.is_superuser or request.user.is_staff or hasattr(request.user, 'handler_profile')):
        raise PermissionDenied("You do not have permission to view this receipt.")
        
    peetha = booking.pooja.peetha
    return render(request, 'peethas/pooja_success.html', {
        'booking': booking,
        'peetha': peetha,
    })

@login_required(login_url='peethas:login')
def my_bookings(request):
    lang = get_language(request)
    bookings = PoojaBooking.objects.filter(user=request.user).select_related('pooja', 'pooja__peetha').order_by('-created_at')
    stay_bookings = AccommodationBooking.objects.filter(user=request.user).select_related('peetha', 'room', 'room__building').order_by('-created_at')
    
    return render(request, 'peethas/my_bookings.html', {
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'bookings': bookings,
        'stay_bookings': stay_bookings,
    })


@login_required(login_url='peethas:login')
def profile_view(request):
    lang = get_language(request)
    profile = request.user.profile
    
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        
        # Update profile fields
        profile.phone_number = request.POST.get('phone_number', '').strip()
        profile.address = request.POST.get('address', '').strip()
        profile.gender = request.POST.get('gender', 'male')
        profile.gotra = request.POST.get('gotra', '').strip()
        profile.nakshatra = request.POST.get('nakshatra', '').strip()
        profile.rashi = request.POST.get('rashi', '').strip()
        
        dob_str = request.POST.get('date_of_birth', '').strip()
        if dob_str:
            try:
                # HTML5 date inputs format is YYYY-MM-DD
                profile.date_of_birth = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                profile.date_of_birth = None
        else:
            profile.date_of_birth = None
        
        # Handle profile pic removal
        if request.POST.get('remove_profile_pic') == 'true':
            if profile.profile_pic:
                profile.profile_pic.delete(save=False)
            profile.profile_pic = None
        # Handle profile pic upload
        elif 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('peethas:profile_view')
        
    completion = profile.completion_percentage()
    
    return render(request, 'peethas/profile.html', {
        'lang': lang,
        'labels': TRANSLATIONS[lang],
        'profile': profile,
        'completion': completion,
        'lang': lang,
    })


@login_required(login_url='peethas:login')
def dashboard_bookings_list(request):
    """AJAX API: Return bookings filtered by optional date, optional pooja_id, and optional peetha.
    Superusers/Admins can filter by peetha slug; Handlers/Staff are restricted to their assigned peetha.
    """
    if not (request.user.is_superuser or request.user.is_staff or hasattr(request.user, 'handler_profile')):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if not request.user.is_superuser:
        if not hasattr(request.user, 'handler_profile'):
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        handler = request.user.handler_profile
        peethas_qs = Peetha.objects.filter(pk=handler.peetha.pk)
    else:
        peetha_slug = request.GET.get('peetha', '')
        if peetha_slug:
            peethas_qs = Peetha.objects.filter(slug=peetha_slug)
        else:
            peethas_qs = Peetha.objects.all().order_by('id')

    is_staff_readonly = request.user.is_staff and not request.user.is_superuser
    range_str = request.GET.get('date_range', '').strip().lower()
    if is_staff_readonly:
        range_str = 'today'
    start_date = None
    end_date = None
    date_display_val = "All Dates"
    today = datetime.date.today()

    if range_str == '3m':
        start_date = today - datetime.timedelta(days=90)
        end_date = today
        date_display_val = "Previous 3 Months"
    elif range_str == '6m':
        start_date = today - datetime.timedelta(days=180)
        end_date = today
        date_display_val = "Previous 6 Months"
    elif range_str == '9m':
        start_date = today - datetime.timedelta(days=270)
        end_date = today
        date_display_val = "Previous 9 Months"
    elif range_str == '12m':
        start_date = today - datetime.timedelta(days=365)
        end_date = today
        date_display_val = "Previous 12 Months"
    elif range_str == 'today':
        start_date = today
        end_date = today
        date_display_val = today.strftime('%A, %d %B %Y')
    elif range_str == 'monthly':
        month_str = request.GET.get('month', '').strip()
        if month_str:
            try:
                parts = month_str.split('-')
                year = int(parts[0])
                month = int(parts[1])
                start_date = datetime.date(year, month, 1)
                if month == 12:
                    end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
                else:
                    end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
                date_display_val = start_date.strftime('%B %Y')
            except Exception:
                return JsonResponse({'error': 'Invalid month format. Use YYYY-MM.'}, status=400)
        else:
            start_date = datetime.date(today.year, today.month, 1)
            if today.month == 12:
                end_date = datetime.date(today.year + 1, 1, 1) - datetime.timedelta(days=1)
            else:
                end_date = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
            date_display_val = start_date.strftime('%B %Y')
    elif range_str == 'between':
        start_str = request.GET.get('start_date', '').strip()
        end_str = request.GET.get('end_date', '').strip()
        if start_str and end_str:
            try:
                start_date = datetime.date.fromisoformat(start_str)
                end_date = datetime.date.fromisoformat(end_str)
                date_display_val = f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"
            except ValueError:
                return JsonResponse({'error': 'Invalid start/end date format. Use YYYY-MM-DD.'}, status=400)
        else:
            start_date = today - datetime.timedelta(days=30)
            end_date = today
            date_display_val = f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"
    elif range_str == 'all':
        date_display_val = "All Dates"
    else:
        date_str = request.GET.get('date', '').strip()
        if date_str:
            try:
                target_date = datetime.date.fromisoformat(date_str)
                start_date = target_date
                end_date = target_date
                date_display_val = target_date.strftime('%A, %d %B %Y')
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        else:
            date_display_val = "All Dates"

    target_date = start_date if (start_date and start_date == end_date) else None

    pooja_id = request.GET.get('pooja_id', '').strip()
    pooja_filter = None
    if pooja_id:
        try:
            pooja_filter = Pooja.objects.get(pk=int(pooja_id))
            if not request.user.is_superuser:
                if pooja_filter.peetha != request.user.handler_profile.peetha:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
        except (ValueError, Pooja.DoesNotExist):
            return JsonResponse({'error': 'Invalid Pooja ID.'}, status=400)

    result = {
        'date': start_date.isoformat() if (start_date and start_date == end_date) else '',
        'date_range': range_str,
        'date_display': date_display_val,
        'peethas': [],
        'total_bookings': 0,
        'total_revenue': 0.0,
        'total_pending': 0,
    }

    for peetha in peethas_qs:
        bookings = PoojaBooking.objects.filter(pooja__peetha=peetha).select_related('pooja', 'user').order_by('-created_at')

        if start_date and end_date:
            bookings = bookings.filter(date_of_pooja__gte=start_date, date_of_pooja__lte=end_date)
        if pooja_filter:
            bookings = bookings.filter(pooja=pooja_filter)

        success_bookings = bookings.filter(payment_status='success')
        pending_bookings = bookings.filter(payment_status='pending')
        failed_bookings = bookings.filter(payment_status='failed')

        peetha_revenue = success_bookings.aggregate(total=models.Sum('amount'))['total'] or 0
        peetha_revenue = 0.0 if is_staff_readonly else float(peetha_revenue)

        bookings_data = []
        for b in bookings:
            bookings_data.append({
                'id': b.id,
                'devotee_name': b.devotee_name,
                'devotee_phone': b.devotee_phone,
                'devotee_email': b.devotee_email or '',
                'pooja_name': b.pooja.name,
                'pooja_category': b.pooja.get_category_display(),
                'date_of_pooja': b.date_of_pooja.strftime('%Y-%m-%d'),
                'gotra': b.gotra or '',
                'nakshatra': b.nakshatra or '',
                'rashi': b.rashi or '',
                'family_members': b.formatted_family_members or '',
                'amount': 0.0 if is_staff_readonly else float(b.amount),
                'payment_status': b.payment_status,
                'payment_status_display': b.get_payment_status_display(),
                'created_at': b.created_at.strftime('%d %b %Y, %I:%M %p') if b.created_at else '',
                'razorpay_payment_id': b.razorpay_payment_id or '',
                'transaction_id': b.razorpay_payment_id or '',
            })

        slot_info = []
        if target_date:
            poojas = Pooja.objects.filter(peetha=peetha, is_active=True).order_by('order', 'name')
            if pooja_filter and pooja_filter.peetha == peetha:
                poojas = poojas.filter(pk=pooja_filter.pk)

            for pooja in poojas:
                booked_count = PoojaBooking.objects.filter(
                    pooja=pooja,
                    date_of_pooja=target_date,
                    payment_status='success'
                ).count()
                slot_info.append({
                    'pooja_name': pooja.name,
                    'category': pooja.get_category_display(),
                    'total_slots': pooja.total_slots,
                    'booked_slots': booked_count,
                    'available_slots': max(0, pooja.total_slots - booked_count),
                    'utilization_pct': round((booked_count / pooja.total_slots) * 100, 1) if pooja.total_slots > 0 else 0,
                })

        peetha_data = {
            'name': peetha.name,
            'slug': peetha.slug,
            'color': peetha.color,
            'total_bookings': success_bookings.count(),
            'pending_bookings': pending_bookings.count(),
            'failed_bookings': failed_bookings.count(),
            'revenue': peetha_revenue,
            'bookings': bookings_data,
            'slot_info': slot_info,
        }

        result['peethas'].append(peetha_data)
        result['total_bookings'] += success_bookings.count()
        result['total_revenue'] += peetha_revenue
        result['total_pending'] += pending_bookings.count()

    result['total_revenue'] = round(result['total_revenue'], 2)

    return JsonResponse(result)


@login_required(login_url='peethas:login')
def dashboard_search_devotees(request):
    """AJAX API: Search devotees by name, phone, gender, gotra, etc. Superuser only."""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    from .models import UserProfile

    query = request.GET.get('q', '').strip()
    gender_filter = request.GET.get('gender', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = 20

    users = User.objects.all().order_by('-date_joined')

    # Exclude superusers, staff, and handlers from devotee listing (show only pure devotees)
    users = users.filter(is_superuser=False, is_staff=False, handler_profile__isnull=True)

    # Text search across multiple fields
    if query:
        users = users.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(username__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(profile_profile__phone_number__icontains=query) |
            models.Q(profile_profile__gotra__icontains=query) |
            models.Q(profile_profile__nakshatra__icontains=query) |
            models.Q(profile_profile__rashi__icontains=query)
        ).distinct()

    # Gender filter
    if gender_filter and gender_filter in ('male', 'female', 'other'):
        users = users.filter(profile_profile__gender=gender_filter)

    total_count = users.count()
    total_pages = max(1, (total_count + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * per_page
    users_page = users[offset:offset + per_page]

    devotees = []
    for u in users_page:
        try:
            profile = u.profile
        except Exception:
            profile = None

        # Booking summary for this devotee
        booking_count = PoojaBooking.objects.filter(user=u, payment_status='success').count()
        total_spent_val = PoojaBooking.objects.filter(user=u, payment_status='success').aggregate(
            total=models.Sum('amount')
        )['total']
        total_spent = float(total_spent_val) if total_spent_val else 0.0

        last_booking = PoojaBooking.objects.filter(user=u, payment_status='success').order_by('-created_at').first()

        # Determine current role metadata
        user_role = 'devotee'
        role_display = 'Devotee'
        assigned_peetha_id = None
        try:
            handler = u.handler_profile
            user_role = 'handler'
            role_display = f"Handler ({handler.peetha.name})"
            assigned_peetha_id = handler.peetha.id
        except Exception:
            if u.is_superuser:
                user_role = 'superuser'
                role_display = 'Super Admin'
            elif u.is_staff:
                user_role = 'staff'
                role_display = 'Staff (Read-Only)'

        devotees.append({
            'id': u.id,
            'username': u.username,
            'full_name': u.get_full_name() or u.username,
            'email': u.email or '',
            'phone': profile.phone_number if profile else '',
            'gender': profile.get_gender_display() if profile and profile.gender else '',
            'gender_raw': profile.gender if profile else '',
            'gotra': profile.gotra if profile else '',
            'nakshatra': profile.nakshatra if profile else '',
            'rashi': profile.rashi if profile else '',
            'address': profile.address if profile else '',
            'has_pic': bool(profile.profile_pic) if profile else False,
            'date_joined': u.date_joined.strftime('%d %b %Y') if u.date_joined else '',
            'last_login': u.last_login.strftime('%d %b %Y, %I:%M %p') if u.last_login else 'Never',
            'booking_count': booking_count,
            'total_spent': total_spent,
            'last_booking_date': last_booking.date_of_pooja.strftime('%d %b %Y') if last_booking else '',
            'last_booking_pooja': last_booking.pooja.name if last_booking else '',
            'completion': profile.completion_percentage() if profile else 0,
            'role': user_role,
            'role_display': role_display,
            'assigned_peetha_id': assigned_peetha_id,
        })

    return JsonResponse({
        'devotees': devotees,
        'total_count': total_count,
        'page': page,
        'total_pages': total_pages,
        'per_page': per_page,
        'query': query,
        'gender': gender_filter,
    })


# ===== ACCOMMODATION BOOKING VIEWS =====

def _get_available_rooms(peetha, room_type, check_in_date, check_out_date):
    rooms = Room.objects.filter(
        building__peetha=peetha,
        building__is_active=True,
        is_active=True,
        room_type=room_type
    )
    overlapping_booking_room_ids = AccommodationBooking.objects.filter(
        peetha=peetha,
        room_type=room_type,
        payment_status__in=['pending', 'success'],
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    ).exclude(room_id__isnull=True).values_list('room_id', flat=True)
    
    return rooms.exclude(id__in=overlapping_booking_room_ids)


def accommodation_availability(request, peetha_slug):
    peetha = get_object_or_404(Peetha, slug=peetha_slug)
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    
    if not check_in_str or not check_out_str:
        return JsonResponse({'error': 'Please select both check-in and check-out dates.'}, status=400)
        
    try:
        check_in_date = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out_date = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format.'}, status=400)
        
    if check_in_date >= check_out_date:
        return JsonResponse({'error': 'Check-out date must be after check-in date.'}, status=400)
        
    if check_in_date < datetime.date.today():
        return JsonResponse({'error': 'Dates cannot be in the past.'}, status=400)
        
    availability = {}
    for rtype in ['AC', 'Ordinary']:
        avail_rooms = _get_available_rooms(peetha, rtype, check_in_date, check_out_date)
        count = avail_rooms.count()
        first_room = Room.objects.filter(building__peetha=peetha, room_type=rtype, is_active=True).first()
        if first_room:
            price = first_room.price_per_night
        else:
            b = Building.objects.filter(peetha=peetha, is_active=True).first()
            if b:
                price = b.ac_room_price if rtype == 'AC' else b.ordinary_room_price
            else:
                price = 1000.00 if rtype == 'AC' else 500.00
                
        # Collect hot water info for this room type
        buildings_with_rooms = Building.objects.filter(rooms__in=avail_rooms).distinct()
        hot_water_available = any(b.has_hot_water for b in buildings_with_rooms)
        
        timings_list = [b.hot_water_timings for b in buildings_with_rooms if b.has_hot_water and b.hot_water_timings.strip()]
        hot_water_timings = timings_list[0] if timings_list else ("Available" if hot_water_available else "Not Available")
                
        availability[rtype] = {
            'available_count': count,
            'price_per_night': float(price),
            'hot_water_available': hot_water_available,
            'hot_water_timings': hot_water_timings if hot_water_available else 'Not Available',
        }
        
    return JsonResponse({'availability': availability})


@login_required(login_url='peethas:login')
def initiate_accommodation_booking(request, peetha_slug):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser or hasattr(request.user, 'handler_profile'):
            raise PermissionDenied("Booking is not allowed for administrators, staff, or handlers.")
            
    peetha = get_object_or_404(Peetha, slug=peetha_slug)
    
    if request.method == 'POST':
        devotee_name = request.POST.get('devotee_name')
        devotee_phone = request.POST.get('devotee_phone')
        devotee_email = request.POST.get('devotee_email', '')
        room_type = request.POST.get('room_type')
        check_in_str = request.POST.get('check_in_date')
        check_out_str = request.POST.get('check_out_date')
        
        if not all([devotee_name, devotee_phone, room_type, check_in_str, check_out_str]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        try:
            check_in_date = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date selection.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        if check_in_date >= check_out_date:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        if check_in_date < datetime.date.today():
            messages.error(request, "Stays cannot be booked for past dates.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        available_rooms = _get_available_rooms(peetha, room_type, check_in_date, check_out_date)
        if not available_rooms.exists():
            messages.error(request, f"Sorry, no {room_type} rooms are available for the selected dates.")
            return redirect('peethas:peetha_detail', slug=peetha.slug)
            
        assigned_room = available_rooms.first()
        nights = (check_out_date - check_in_date).days
        amount = assigned_room.price_per_night * nights
        
        booking = AccommodationBooking.objects.create(
            user=request.user,
            peetha=peetha,
            room=assigned_room,
            room_type=room_type,
            devotee_name=devotee_name,
            devotee_phone=devotee_phone,
            devotee_email=devotee_email,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            amount=amount,
            razorpay_order_id=f"ORD-ROOM-{int(datetime.datetime.now().timestamp())}",
            razorpay_payment_id=f"PAY-ROOM-{int(datetime.datetime.now().timestamp())}",
            payment_status='success'
        )
        
        return redirect('peethas:accommodation_booking_success', booking_id=booking.id)
        
    return redirect('peethas:peetha_detail', slug=peetha.slug)


@login_required(login_url='peethas:login')
def accommodation_booking_success(request, booking_id):
    booking = get_object_or_404(AccommodationBooking, pk=booking_id)
    if booking.user != request.user and not (request.user.is_superuser or request.user.is_staff or hasattr(request.user, 'handler_profile')):
        raise PermissionDenied("You do not have permission to view this receipt.")
        
    peetha = booking.peetha
    return render(request, 'peethas/accommodation_success.html', {
        'booking': booking,
        'peetha': peetha,
    })
