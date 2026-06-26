from django import forms
from django.contrib.auth.models import User
from .models import PeethaMedia, TravelPlan, Peetha, PeethaHandler, PeethaPaymentConfig, Pooja, Building


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class PeethaMediaAddForm(forms.ModelForm):
    class Meta:
        model = PeethaMedia
        fields = [
            'media_type',
            'title', 'description',
            'title_kn', 'description_kn',
            'title_mr', 'description_mr',
            'title_hi', 'description_hi',
            'title_te', 'description_te',
            'title_ta', 'description_ta',
            'title_ml', 'description_ml'
        ]
        widgets = {
            'media_type': forms.Select(attrs={'class': 'form-input', 'id': 'media-type-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'English Title (optional, will default to filename)'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'English Description (optional)'}),
            
            'title_kn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ಕನ್ನಡ ಶೀರ್ಷಿಕೆ (ಐಚ್ಛಿಕ)'}),
            'description_kn': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'ಕನ್ನಡ ವಿವರಣೆ'}),
            
            'title_mr': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'मराठी शीर्षक (पर्यायी)'}),
            'description_mr': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'मराठी वर्णन'}),
            
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'हिन्दी शीर्षक (वैकल्पिक)'}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'हिन्दी विवरण'}),
            
            'title_te': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'తెలుగు శీర్షిక (ఐచ్ఛికం)'}),
            'description_te': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'తెలుగు వివరణ'}),
            
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'தமிழ் தலைப்பு (விரும்பினால்)'}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'தமிழ் விளக்கம்'}),
            
            'title_ml': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'മലയാളം ശീർഷകം (ഓപ്ഷണൽ)'}),
            'description_ml': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'മലയാളം വിവരണം'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class PeethaMediaEditForm(forms.ModelForm):
    class Meta:
        model = PeethaMedia
        fields = [
            'media_type', 'photo_file', 'youtube_url',
            'title', 'description',
            'title_kn', 'description_kn',
            'title_mr', 'description_mr',
            'title_hi', 'description_hi',
            'title_te', 'description_te',
            'title_ta', 'description_ta',
            'title_ml', 'description_ml'
        ]
        widgets = {
            'media_type': forms.Select(attrs={'class': 'form-input', 'id': 'media-type-select'}),
            'photo_file': forms.FileInput(attrs={'class': 'form-input', 'id': 'photo-file-input'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-input', 'id': 'youtube-url-input', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'English Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'English Description'}),
            
            'title_kn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ಕನ್ನಡ ಶೀರ್ಷಿಕೆ'}),
            'description_kn': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'ಕನ್ನಡ ವಿವರಣೆ'}),
            
            'title_mr': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'मराठी शीर्षक'}),
            'description_mr': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'मराठी वर्णन'}),
            
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'हिन्दी शीर्षक'}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'हिन्दी विवरण'}),
            
            'title_te': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'తెలుగు శీర్షిక'}),
            'description_te': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'తెలుగు వివరణ'}),
            
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'தமிழ் தலைப்பு'}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'தமிழ் விளக்கம்'}),
            
            'title_ml': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'മലയാളം ശീർഷകം'}),
            'description_ml': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'മലയാളം വിവരണം'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        photo_file = cleaned_data.get('photo_file')
        youtube_url = cleaned_data.get('youtube_url')

        if media_type == 'photo':
            if not photo_file and not self.instance.photo_file:
                self.add_error('photo_file', 'Please upload an image file.')
        elif media_type == 'video':
            if not youtube_url:
                self.add_error('youtube_url', 'Please provide a YouTube URL.')
            else:
                import re
                pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
                match = re.search(pattern, youtube_url)
                if not match:
                    self.add_error('youtube_url', 'Invalid YouTube URL. Please provide a valid watch, share, or embed link.')

        return cleaned_data


class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = [
            'title', 'start_date', 'end_date', 'location', 'description',
            'title_kn', 'location_kn', 'description_kn',
            'title_mr', 'location_mr', 'description_mr',
            'title_hi', 'location_hi', 'description_hi',
            'title_te', 'location_te', 'description_te',
            'title_ta', 'location_ta', 'description_ta',
            'title_ml', 'location_ml', 'description_ml'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'English Title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'English Location'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'English Description'}),

            'title_kn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ಕನ್ನಡ ಶೀರ್ಷಿಕೆ'}),
            'location_kn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ಕನ್ನಡ ಸ್ಥಳ'}),
            'description_kn': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'ಕನ್ನಡ ವಿವರಣೆ'}),

            'title_mr': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'मराठी शीर्षक'}),
            'location_mr': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'मराठी स्थान'}),
            'description_mr': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'मराठी वर्णन'}),

            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'हिन्दी शीर्षक'}),
            'location_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'हिन्दी स्थान'}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'हिन्दी विवरण'}),

            'title_te': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'తెలుగు శీర్షిక'}),
            'location_te': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'తెలుగు స్థానం'}),
            'description_te': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'తెలుగు వివరణ'}),

            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'தமிழ் தலைப்பு'}),
            'location_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'தமிழ் இடம்'}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'தமிழ் விளக்கம்'}),

            'title_ml': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'മലയാളം ശീർഷകം'}),
            'location_ml': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'മലയാളം സ്ഥാനം'}),
            'description_ml': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'മലയാളം വിവരണം'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'End date cannot be before start date.')

        return cleaned_data


class PeethaHandlerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label="Select User"
    )
    peetha = forms.ModelChoiceField(
        queryset=Peetha.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label="Select Peetha"
    )

    class Meta:
        model = PeethaHandler
        fields = ['user', 'peetha']


class PeethaPaymentConfigForm(forms.ModelForm):
    peetha = forms.ModelChoiceField(
        queryset=Peetha.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label="Peetha"
    )
    razorpay_key_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'rzp_live_...'}),
        label="Razorpay Key ID"
    )
    razorpay_key_secret = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Secret Key'}),
        label="Razorpay Key Secret"
    )
    is_active = forms.BooleanField(
        required=False,
        label="Enable Payments"
    )

    class Meta:
        model = PeethaPaymentConfig
        fields = ['peetha', 'razorpay_key_id', 'razorpay_key_secret', 'is_active']


WEEKDAYS_CHOICES = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)


class PoojaForm(forms.ModelForm):
    available_days_list = forms.MultipleChoiceField(
        choices=WEEKDAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'weekday-checkbox'}),
        required=False,
        label="Available Days",
        initial=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        help_text="Select weekdays when this pooja/seva is available."
    )

    class Meta:
        model = Pooja
        fields = [
            'name', 'description', 'price', 'category', 'total_slots',
            'is_active', 'order',
            'name_kn', 'description_kn',
            'name_mr', 'description_mr',
            'name_hi', 'description_hi',
            'name_te', 'description_te',
            'name_ta', 'description_ta',
            'name_ml', 'description_ml'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'English Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'English Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Price (INR)'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'total_slots': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Slots per day'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
            
            'name_kn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ಕನ್ನಡ ಹೆಸರು'}),
            'description_kn': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'ಕನ್ನಡ ವಿವರಣೆ'}),
            'name_mr': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'मराठी नाव'}),
            'description_mr': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'मराठी वर्णन'}),
            'name_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'हिन्दी नाम'}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'हिन्दी विवरण'}),
            'name_te': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'తెలుగు పేరు'}),
            'description_te': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'తెలుగు వివరణ'}),
            'name_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'தமிழ் பெயர்'}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'தமிழ் விளக்கம்'}),
            'name_ml': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'മലയാളം പേര്'}),
            'description_ml': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'മലയാളം വിവരണം'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_days = self.instance.available_days
            if current_days == 'all' or not current_days:
                self.fields['available_days_list'].initial = [day[0] for day in WEEKDAYS_CHOICES]
            else:
                self.fields['available_days_list'].initial = [d.strip() for d in current_days.split(',') if d.strip()]

    def clean(self):
        cleaned_data = super().clean()
        days_list = cleaned_data.get('available_days_list')
        if days_list is not None:
            if len(days_list) == 7:
                cleaned_data['available_days'] = 'all'
            else:
                cleaned_data['available_days'] = ','.join(days_list)
        else:
            cleaned_data['available_days'] = 'all'
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.available_days = self.cleaned_data.get('available_days', 'all')
        if commit:
            instance.save()
        return instance


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = [
            'name', 'description', 'total_floors', 'rooms_per_floor',
            'ac_floors_count', 'ac_room_numbers', 'ac_room_price', 'ordinary_room_price',
            'has_hot_water', 'hot_water_timings', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Building Name (e.g. Building A)'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Description'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'rooms_per_floor': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'ac_floors_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'ac_room_numbers': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Comma-separated specific AC rooms (e.g. G1, G2, 101). Overrides AC Floors.'}),
            'ac_room_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'ordinary_room_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'has_hot_water': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'hot_water_timings': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 6:00 AM - 9:00 AM'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_floors = cleaned_data.get('total_floors')
        ac_floors_count = cleaned_data.get('ac_floors_count')
        
        if total_floors is not None and ac_floors_count is not None:
            if ac_floors_count > total_floors:
                self.add_error('ac_floors_count', 'AC floors count cannot exceed total floors.')
        return cleaned_data


