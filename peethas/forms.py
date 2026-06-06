from django import forms
from .models import PeethaMedia, TravelPlan


class PeethaMediaForm(forms.ModelForm):
    class Meta:
        model = PeethaMedia
        fields = [
            'media_type', 'photo_file', 'youtube_url',
            'title', 'description',
            'title_kn', 'description_kn',
            'title_mr', 'description_mr',
            'title_hi', 'description_hi'
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
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        photo_file = cleaned_data.get('photo_file')
        youtube_url = cleaned_data.get('youtube_url')

        if media_type == 'photo':
            if not photo_file:
                self.add_error('photo_file', 'Please upload an image file.')
        elif media_type == 'video':
            if not youtube_url:
                self.add_error('youtube_url', 'Please provide a YouTube URL.')
            else:
                # Basic validation for YouTube ID parsing
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
            'title_hi', 'location_hi', 'description_hi'
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
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'End date cannot be before start date.')

        return cleaned_data
