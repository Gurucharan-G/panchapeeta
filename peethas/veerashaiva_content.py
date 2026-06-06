# -*- coding: utf-8 -*-
"""
Veerashaiva-Lingayat section content in all 4 languages.
Faithfully reproduced from the user-provided translation files.

Structure per language:
  - title: Section heading
  - opening_shloka: { verse, translation (optional), reference }
  - intro_paragraphs: Paragraphs before the Siddhanta Shikhamani verse
  - siddhanta: { intro, verse, translation_label (optional), translation (optional) }
  - body_paragraphs: Paragraphs after the Siddhanta verse
  - teachings: List of teaching points (English only; others have them inline)
  - teachings_note: Closing note after teachings (English only)
  - conclusion: Final paragraph
"""

VEERASHAIVA_CONTENT = {
    # ─────────────────────── ENGLISH ───────────────────────
    'en': {
        'title': 'Veerashaiva-Lingayat',

        'opening_shloka': {
            'verse': (
                "Vāgarthāviva saṁpṛktau vāgartha-pratipattaye |\n"
                "Jagataḥ pitarau vande Pārvatī Parameśvarau ||"
            ),
            'translation': (
                "\u201cLike word and meaning, inseparably united for the "
                "realization of both word and meaning, I bow to Parvati and "
                "Parameshwara, the parents of the universe.\u201d"
            ),
            'reference': 'Kalidasa'
        },

        'intro_paragraphs': [
            (
                "The Veerashaiva Dharma is extremely ancient. Its history and "
                "tradition are unique and unparalleled. It is a religion that "
                "has always desired the welfare of all living beings. It does "
                "not accommodate selfish and narrow-minded attitudes that seek "
                "only one\u2019s own survival and prosperity. It proclaims that "
                "conduct is superior to caste, practice is superior to mere "
                "philosophy, action is superior to words, spiritual discipline "
                "is superior to preaching, selfless service (Dasoha) is "
                "superior to charity, and character is superior to mere "
                "biography or reputation. The credit for imparting religious "
                "values and noble thoughts equally to all, without "
                "discrimination based on gender, social status, wealth, or "
                "rank, belongs to the Veerashaiva Dharma."
            ),
            (
                "Veerashaiva Dharma possesses its own constitution, code of "
                "conduct, and philosophical principles. The cultural "
                "foundation of Veerashaiva Dharma, in which Ashtavarana (the "
                "Eight Protective Coverings) forms the body, Panchachara (the "
                "Five Codes of Conduct) serves as the life-force, and "
                "Shatsthala (the Six Stages of Spiritual Attainment) "
                "constitutes the soul, can be found in the Shiva Agamas."
            ),
        ],

        'siddhanta': {
            'intro': 'The religious text Siddhanta Shikhamani declares:',
            'verse': (
                "\u201cSiddhānta Mahātantre Kāmikā Śivodite\n"
                "Nirdiṣṭam Uttare Bhāge Vīraśaiva Mataṁ Param.\u201d"
            ),
            'translation_label': 'Translation:',
            'translation': (
                "\u201cIn the great Siddhanta Tantra, revealed by Shiva in the "
                "Kamika Agama, the supreme doctrine of Veerashaivism is "
                "expounded in the latter section.\u201d"
            ),
        },

        'body_paragraphs': [
            (
                "The glory and greatness of Veerashaiva Dharma can be seen in "
                "the latter portions of the twenty-eight Shiva Agamas, "
                "beginning with Kamika and ending with Vatula. Possessing a "
                "history of more than five thousand years, Veerashaiva Dharma "
                "has upheld social justice by rejecting caste discrimination, "
                "gender inequality, superstition, and harmful customs, while "
                "advocating universal equality."
            ),
            (
                "Great sages such as Agastya, Dadhichi, Vyasa, Sananda, and "
                "Durvasa became spiritually exalted by practicing and "
                "preserving the principles of Shivadvaita Philosophy. Numerous "
                "invaluable texts, including the Shiva Agamas, Siddhanta "
                "Shikhamani, Kriyasara, Shrikara Bhashya, and Shivatamanjari, "
                "have enhanced the sanctity and glory of Veerashaiva Dharma."
            ),
            (
                "The distinction of nurturing the ideals of Kayaka (dignity of "
                "labor) and Dasoha (selfless service) belongs to Veerashaiva "
                "Dharma. It is credited with removing the defects and "
                "weaknesses of the individual self (Anga) and transforming "
                "devotees into those endowed with the virtues of the Linga. "
                "Veerashaiva Dharma regards the human body itself as a temple "
                "and worships the Ishtalinga, bestowed by the Guru, as the "
                "personal and supreme deity."
            ),
        ],

        'teachings_intro': (
            "Veerashaiva Dharma has uprooted the barriers of caste and "
            "delivered a message of harmony and social unity. It teaches that:"
        ),
        'teachings': [
            "The individual soul (Jiva) can become one with Shiva.",
            "The devotee (Anga) can become united with the Linga.",
            "A worldly person (Bhavi) can transform into a devotee (Bhakta).",
            "Material substances can become sacred offerings (Prasada).",
            "Work (Karma) can become Dharma.",
            "Water and land themselves can become sacred places of pilgrimage.",
        ],
        'teachings_note': "These are among the unique teachings found within this tradition.",

        'conclusion': (
            "In Veerashaiva Dharma, which harmoniously combines knowledge "
            "(Jnana) and action (Karma), greater importance is given to "
            "commitment to principles rather than attachment to individuals, "
            "to moral character rather than personal history, and to the "
            "living spiritual guide (Jangama) rather than immovable objects "
            "(Sthavara)."
        ),
    },

    # ─────────────────────── KANNADA ───────────────────────
    'kn': {
        'title': 'ವೀರಶೈವ-ಲಿಂಗಾಯತ',

        'opening_shloka': {
            'verse': (
                "ವಾಗರ್ಥಾವಿವ ಸಂತೃಕ ವಾಗರ್ಥಪ್ರತಿಪತ್ತಯೇ।\n"
                "ಜಗತಃ ಪಿತರೌ‍ ವಂದೇ ಪಾರ್ವತೀ ಪರಮೇಶ್ವರ್‍॥"
            ),
            'translation': None,
            'reference': 'ಕಾಳಿದಾಸ'
        },

        'intro_paragraphs': [
            (
                "ವೀರಶೈವ ಧರ್ಮ ಅತ್ಯಂತ ಪ್ರಾಚೀನ. ಇದರ ಇತಿಹಾಸ ಮತ್ತು ಪರಂಪರೆ "
                "ಅಪೂರ್ವ, ಸಕಲ ಜೀವಾತ್ಮರಿಗೆ ಸದಾ ಲೇಸನ್ನೇ ಬಯಸಿದ ಧರ್ಮ "
                "ತಾನೊಬ್ಬನೇ ಬದುಕಿ ಬಾಳಬೇಕೆಂಬ ಸ್ವಾರ್ಥ ಸಂಕುಚಿತ ಮನೋಭಾವನೆಗಳು "
                "ಇಲ್ಲಿಲ್ಲ. ಜಾತಿಗಿಂತ ನೀತಿ, ತತ್ವಕ್ಕಿಂತ ಆಚರಣೆ, ಮಾತಿಗಿಂತ ಕೃತಿ, "
                "ಬೋಧನೆಗಿಂತ ಸಾಧನೆ, ದಾನಕ್ಕಿಂತ ದಾಸೋಹ, ಚರಿತ್ರೆಗಿಂತ ಚಾರಿತ್ರ್ಯ "
                "ಶ್ರೇಷ್ಠವೆಂದು ಸಾರಿದೆ. ಗಂಡು ಹೆಣ್ಣು, ಉಚ್ಚನೀಚ, ಬಡವ ಬಲ್ಲಿದ "
                "ಎಂಬ ಭೇದವಿಲ್ಲದೇ ಎಲ್ಲರಿಗೂ ಧಾರ್ಮಿಕ ಸಂಸ್ಕಾರ ಸದ್ವಿಚಾರಗಳನ್ನು "
                "ಕೊಟ್ಟ ಕೀರ್ತಿ ವೀರಶೈವ ಧರ್ಮಕ್ಕೆ ಸಲ್ಲುತ್ತದೆ."
            ),
        ],

        'siddhanta': {
            'intro': (
                "ವೀರಶೈವ ಧರ್ಮಕ್ಕೆ ಸಂವಿಧಾನ, ಆಚಾರ ಸಂಹಿತೆ ಮತ್ತು "
                "ಸಿದ್ಧಾಂತಗಳಿವೆ. ಅಷ್ಟಾವರಣದೇ ಅಂಗವಾಗಿ ಪಂಚಾಚಾರವೇ ಪ್ರಾಣವಾಗಿ "
                "ಷಟ್\u200c ಸ್ಥಲಗಳೇ ಆತ್ಮವಾಗಿರುವ ವೀರಶೈವ ಧರ್ಮ ಸಂಸ್ಕೃತಿಯನ್ನು "
                "ಶಿವಾಗಮಗಳಲ್ಲಿ ಕಾಣಬಹುದು. ಸಿದ್ಧಾಂತ ಶಿಖಾಮಣಿ ಧರ್ಮ ಗ್ರಂಥದಲ್ಲಿ"
            ),
            'verse': (
                "ಸಿದ್ಧಾಂತಾ ಮಹಾತಂತೇ ಕಾಮಿಕಾ ಶಿವೋದಿತೇ\n"
                "ನಿರ್ದಿಷ್ಟಮುತ್ತರೇ ಭಾಗೇ ವೀರಶೈವ ಮತಂ ಪರಂ"
            ),
            'translation_label': None,
            'translation': None,
        },

        'body_paragraphs': [
            (
                "ಎಂದು ಸಾರಿದೆ. ಕಾಮಿಕಾದಿ ವಾತುಲಾಂತವಾದ ಇಪತ್ತೆಂಟು "
                "ಶಿವಾಗಮಗಳ ಉತ್ತರ ಭಾಗದಲ್ಲಿ ವೀರಶೈವ ಧರ್ಮದ ಹಿರಿಮೆಯನ್ನು "
                "ಕಾಣಬಹುದು. ಐದು ಸಾವಿರ ವರುಷಗಳ ಇತಿಹಾಸವುಳ್ಳ ವೀರಶೈವ "
                "ಧರ್ಮದಲ್ಲಿ ಜಾತಿಯತೆ, ಸ್ತ್ರೀ ಪುರುಷ ಅಸಮಾನತೆ, ಮೂಢನಂಬಿಕೆ "
                "ಕಂದಾಚಾರಗಳನ್ನು ನಿರಾಕರಿಸಿ, ಸರ್ವ ಸಮಾನತೆಯನ್ನು ಸಾರುವ "
                "ಮೂಲಕ ಸಾಮಾಜಿಕ ನ್ಯಾಯವನ್ನು ಎತ್ತಿ ಹಿಡಿದಿದೆ."
            ),
            (
                "ಅಗಸ್ಯ, ದಧೀಚಿ, ವ್ಯಾಸ, ಸಾನಂದ, ದೂರ್ವಾಸ ಮಹರ್ಷಿಗಳು "
                "ಶಿವಾದೈತ ತತ್ವ ಸಿದ್ಧಾಂತಗಳನ್ನು ಪರಿಪಾಲಿಸಿ ಪಾವನರಾದರು. "
                "ಶಿವಾಗಮಗಳು, ಸಿದ್ಧಾಂತ ಶಿಖಾಮಣಿ, ಕ್ರಿಯಾಸಾರ, ಶ್ರೀಕರಭಾಷ್ಯ, "
                "ಶಿವಾ ತಮಂಜರಿ ಮೊದಲ್ಗೊಂಡು ಹಲವಾರು ಅಮೂಲ್ಯ ಗ್ರಂಥಗಳು "
                "ವೀರಶೈವ ಧರ್ಮದ ಪಾವಿತ್ರ್ಯತೆಯನ್ನು ಹೆಚ್ಚಿಸಿವೆ. ಕಾಯಕ ಮತ್ತು "
                "ದಾಸೋಹ ಭಾವನೆಗಳನ್ನು ಬೆಳೆಸಿದ ಶ್ರೇಯಸ್ಸು ವೀರಶೈವ ಧರ್ಮಕ್ಕಿದೆ. "
                "ಅಂಗ ಅವಗುಣಗಳನ್ನು ನೀಗಿ ಲಿಂಗಗುಣ ಸಂಪನ್ನರನ್ನಾಗಿ ಮಾಡಿದ "
                "ಕೀರ್ತಿ ಇದರದು. ದೇಹವನ್ನೇ ದೇವಾಲಯ ಮಾಡಿ ಗುರುಕೊಟ್ಟ "
                "ಇಷ್ಟಲಿಂಗವೇ ಆರಾಧ್ಯ ದೈವವೆಂದು ಪೂಜಿಸಿದ ಧರ್ಮ ವೀರಶೈವವಾಗಿದೆ."
            ),
        ],

        'teachings_intro': None,
        'teachings': [],
        'teachings_note': None,

        'conclusion': (
            "ವೀರಶೈವ ಧರ್ಮವು ಜಾತಿ ಜಂಜಡಗಳ ಬೇರು ಕಿತ್ತು ಸಾಮರಸ್ಯದ ಸಂದೇಶ "
            "ನೀಡಿದೆ. ಜೀವ ಶಿವನಾಗುವ, ಅಂಗ ಲಿಂಗವಾಗುವ, ಭವಿ ಭಕ್ತನಾಗುವ "
            "ಪದಾರ್ಥ ಪ್ರಸಾದವನ್ನಾಗಿಸುವ, ಕರ್ಮ ಧರ್ಮವನ್ನಾಗಿಸುವ, ಜಲನೆಲ "
            "ತೀರ್ಥಕ್ಷೇತ್ರಗಳೆಂದು ಸಾರಿದ ವಿಶೇಷತೆಯನ್ನು ಈ ಧರ್ಮದಲ್ಲಿ "
            "ಕಾಣಬಹುದು. ಜ್ಞಾನ ಕರ್ಮ ಸಮುಚ್ಛಯದಿಂದ ಕೂಡಿದ ವೀರಶೈವ ಧರ್ಮದಲ್ಲಿ "
            "ವ್ಯಕ್ತಿ ನಿಷ್ಠೆಗಿಂತ ತತ್ವ ನಿಷ್ಠೆಗೆ, ಚರಿತ್ರೆಗಿಂತ ಚಾರಿತ್ರ್ಯಕ್ಕೆ, "
            "ಸ್ಥಾವರಕ್ಕಿಂತ ಜಂಗಮಕ್ಕೆ ಹೆಚ್ಚು ಮಹತ್ವವನ್ನು ಕೊಟ್ಟಿದೆ."
        ),
    },

    # ─────────────────────── HINDI ───────────────────────
    'hi': {
        'title': 'वीरशैव-लिंगायत',

        'opening_shloka': {
            'verse': (
                "वागर्थाविव सम्पृक्तौ वागर्थप्रतिपत्तये।\n"
                "जगतः पितरौ वन्दे पार्वती परमेश्वरौ॥"
            ),
            'translation': (
                "\u201cजैसे वाणी और उसका अर्थ अभिन्न रूप से जुड़े हुए हैं, "
                "वैसे ही वाणी और अर्थ की प्राप्ति के लिए मैं जगत के "
                "माता-पिता पार्वती और परमेश्वर को प्रणाम करता हूँ।\u201d"
            ),
            'reference': 'कालिदास'
        },

        'intro_paragraphs': [
            (
                "वीरशैव धर्म अत्यंत प्राचीन है। इसका इतिहास और परंपरा "
                "अद्वितीय एवं अनुपम है। यह ऐसा धर्म है जिसने सदैव समस्त "
                "जीवात्माओं के कल्याण की कामना की है। केवल स्वयं जीवित "
                "रहकर सुखपूर्वक जीवन बिताने की स्वार्थपूर्ण और संकुचित "
                "मानसिकता को इसमें कोई स्थान नहीं है। यह धर्म प्रतिपादित "
                "करता है कि जाति से नीति श्रेष्ठ है, तत्त्वज्ञान से आचरण "
                "श्रेष्ठ है, वचन से कर्म श्रेष्ठ है, उपदेश से साधना श्रेष्ठ "
                "है, दान से दासोह श्रेष्ठ है तथा चरित से चरित्र श्रेष्ठ है। "
                "स्त्री-पुरुष, ऊँच-नीच, धनवान-निर्धन आदि किसी भी प्रकार "
                "का भेद किए बिना सभी को धार्मिक संस्कार और सद्विचार प्रदान "
                "करने का श्रेय वीरशैव धर्म को प्राप्त है।"
            ),
            (
                "वीरशैव धर्म का अपना संविधान, आचार-संहिता और सिद्धांत हैं। "
                "शिवागमों में वर्णित वीरशैव संस्कृति में अष्टावरण उसके अंग, "
                "पंचाचार उसका प्राण और षट्स्थल उसकी आत्मा माने गए हैं।"
            ),
        ],

        'siddhanta': {
            'intro': 'सिद्धांत शिखामणि में कहा गया है—',
            'verse': (
                "\u201cसिद्धान्त महातन्त्रे कामिका शिवोदिते ।\n"
                "निर्दिष्टमुत्तरे भागे वीरशैव मतं परम् ॥\u201d"
            ),
            'translation_label': 'अर्थात्—',
            'translation': (
                "\u201cभगवान शिव द्वारा प्रतिपादित कामिकागम के उत्तर भाग में "
                "वीरशैव मत के परम सिद्धांतों का निरूपण किया गया है।\u201d"
            ),
        },

        'body_paragraphs': [
            (
                "कामिक से लेकर वातुल तक के अट्ठाईस शिवागमों के उत्तर भागों "
                "में वीरशैव धर्म की महिमा का वर्णन मिलता है। पाँच हजार "
                "वर्षों से अधिक प्राचीन इस धर्म ने जातिवाद, स्त्री-पुरुष "
                "असमानता, अंधविश्वास और कुप्रथाओं का विरोध करते हुए "
                "सामाजिक न्याय और सार्वभौमिक समानता का समर्थन किया है।"
            ),
            (
                "ऋषि अगस्त्य, दधीचि, व्यास, सनन्द तथा दुर्वासा आदि "
                "महर्षियों ने शिवाद्वैत सिद्धांतों का पालन कर आध्यात्मिक "
                "पवित्रता प्राप्त की। शिवागम, सिद्धांत शिखामणि, क्रियासार, "
                "श्रीकरभाष्य, शिवातमंजरी आदि अनेक अमूल्य ग्रंथों ने "
                "वीरशैव धर्म की पवित्रता और गौरव को बढ़ाया है।"
            ),
            (
                "कायक (परिश्रमपूर्ण कर्म) और दासोह (निःस्वार्थ सेवा) की "
                "भावना को विकसित करने का श्रेय भी वीरशैव धर्म को प्राप्त "
                "है। इसने मनुष्य के अंगगत दोषों को दूर कर उसे लिंगगुणों "
                "से सम्पन्न बनाया। शरीर को ही मंदिर मानकर गुरु द्वारा "
                "प्रदत्त इष्टलिंग को आराध्य देवता के रूप में पूजना वीरशैव "
                "धर्म की विशेषता है।"
            ),
            (
                "वीरशैव धर्म ने जातिगत बंधनों की जड़ों को उखाड़कर सामाजिक "
                "समरसता का संदेश दिया। यह सिखाता है कि जीव शिव बन सकता "
                "है, अंग लिंग बन सकता है, भवि भक्त बन सकता है, पदार्थ "
                "प्रसाद बन सकता है, कर्म धर्म बन सकता है तथा जल और भूमि "
                "भी तीर्थक्षेत्र बन सकते हैं।"
            ),
        ],

        'teachings_intro': None,
        'teachings': [],
        'teachings_note': None,

        'conclusion': (
            "ज्ञान और कर्म के समन्वय से युक्त वीरशैव धर्म में "
            "व्यक्ति-निष्ठा की अपेक्षा तत्त्व-निष्ठा को, चरित की अपेक्षा "
            "चरित्र को तथा स्थावर की अपेक्षा जंगम को अधिक महत्व दिया "
            "गया है।"
        ),
    },

    # ─────────────────────── MARATHI ───────────────────────
    'mr': {
        'title': 'वीरशैव-लिंगायत',

        'opening_shloka': {
            'verse': (
                "वागर्थाविव सम्पृक्तौ वागर्थप्रतिपत्तये।\n"
                "जगतः पितरौ वन्दे पार्वती परमेश्वरौ॥"
            ),
            'translation': (
                "\u201cजसा शब्द आणि त्याचा अर्थ हे एकमेकांशी अविभाज्यरीत्या "
                "जोडलेले आहेत, तसाच शब्द आणि अर्थ यांची प्राप्ती व्हावी "
                "म्हणून मी जगताचे माता-पिता पार्वती आणि परमेश्वर यांना "
                "वंदन करतो.\u201d"
            ),
            'reference': 'कालिदास'
        },

        'intro_paragraphs': [
            (
                "वीरशैव धर्म अत्यंत प्राचीन आहे. त्याचा इतिहास आणि "
                "परंपरा अद्वितीय आहेत. सर्व जीवात्म्यांच्या कल्याणाची "
                "कामना करणारा हा धर्म आहे. फक्त स्वतःचे हित साधण्याच्या "
                "संकुचित आणि स्वार्थी विचारसरणीला येथे स्थान नाही. हा धर्म "
                "सांगतो की जातीपेक्षा नीती श्रेष्ठ आहे, तत्त्वज्ञानापेक्षा "
                "आचरण श्रेष्ठ आहे, शब्दांपेक्षा कृती श्रेष्ठ आहे, "
                "उपदेशापेक्षा साधना श्रेष्ठ आहे, दानापेक्षा दासोह श्रेष्ठ "
                "आहे आणि चरित्रकथनापेक्षा चारित्र्य श्रेष्ठ आहे. "
                "स्त्री-पुरुष, उच्च-नीच, श्रीमंत-गरीब असा कोणताही भेदभाव "
                "न करता सर्वांना धार्मिक संस्कार आणि सद्विचार देण्याचे श्रेय "
                "वीरशैव धर्माला जाते."
            ),
            (
                "वीरशैव धर्माला स्वतःची आचारसंहिता, तत्त्वप्रणाली आणि "
                "धार्मिक व्यवस्था आहे. शिवागमांमध्ये वर्णन केलेल्या "
                "वीरशैव संस्कृतीत अष्टावरण हे शरीर, पंचाचार हा प्राण "
                "आणि षट्स्थल हा आत्मा मानला जातो."
            ),
        ],

        'siddhanta': {
            'intro': 'सिद्धांत शिखामणी ग्रंथात असे म्हटले आहे:',
            'verse': (
                "\u201cसिद्धान्त महातन्त्रे कामिका शिवोदिते ।\n"
                "निर्दिष्टमुत्तरे भागे वीरशैव मतं परम् ॥\u201d"
            ),
            'translation_label': 'याचा अर्थ:',
            'translation': (
                "\u201cभगवान शिवांनी प्रतिपादित केलेल्या कामिकागमाच्या "
                "उत्तर भागात वीरशैव मताचे परम तत्त्वज्ञान स्पष्ट "
                "केलेले आहे.\u201d"
            ),
        },

        'body_paragraphs': [
            (
                "कामिक ते वातुल या अठ्ठावीस शिवागमांच्या उत्तर भागांमध्ये "
                "वीरशैव धर्माचे महत्त्व वर्णिलेले आहे. पाच हजार वर्षांहून "
                "अधिक इतिहास असलेल्या या धर्माने जातिभेद, स्त्री-पुरुष "
                "असमानता, अंधश्रद्धा आणि कुप्रथांना नाकारून सामाजिक न्याय "
                "व सर्वसमावेशक समानतेचा पुरस्कार केला आहे."
            ),
            (
                "अगस्त्य, दधीची, व्यास, सनंद, आणि दुर्वासा यांसारख्या "
                "महर्षींनी शिवाद्वैत तत्त्वांचे पालन करून आध्यात्मिक "
                "पावित्र्य प्राप्त केले. शिवागम, सिद्धांत शिखामणी, "
                "क्रियासार, श्रीकरभाष्य, शिवातमंजरी इत्यादी ग्रंथांनी "
                "वीरशैव धर्माची प्रतिष्ठा वाढवली आहे."
            ),
            (
                "कायक (परिश्रमपूर्वक कार्य) आणि दासोह (निःस्वार्थ सेवा) "
                "यांची भावना विकसित करण्याचे मोठे श्रेय या धर्माला जाते. "
                "मानवातील दोष दूर करून त्याला लिंगगुणांनी संपन्न करण्याचे "
                "कार्य या धर्माने केले. शरीरालाच देवालय मानून गुरुने "
                "दिलेल्या इष्टलिंगाची आराधना करणे ही त्याची वैशिष्ट्यपूर्ण "
                "परंपरा आहे."
            ),
            (
                "वीरशैव धर्माने जातिभेदांच्या मुळांवर प्रहार करून सामाजिक "
                "ऐक्याचा संदेश दिला आहे. जीव शिव होऊ शकतो, अंग लिंग होऊ "
                "शकते, भवि भक्त होऊ शकतो, पदार्थ प्रसाद होऊ शकतो, कर्म "
                "धर्म होऊ शकते आणि जल-भूमी तीर्थक्षेत्र होऊ शकतात, अशी "
                "या धर्माची शिकवण आहे."
            ),
        ],

        'teachings_intro': None,
        'teachings': [],
        'teachings_note': None,

        'conclusion': (
            "ज्ञान आणि कर्म यांच्या समन्वयाने युक्त असलेल्या वीरशैव "
            "धर्मात व्यक्तिपूजेपेक्षा तत्त्वनिष्ठेला, इतिहासापेक्षा "
            "चारित्र्याला आणि स्थावरापेक्षा जंगमाला अधिक महत्त्व "
            "दिले जाते."
        ),
    },
}
