from django.db import models
from django.contrib.auth.models import User


class Peetha(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    acharya = models.CharField(max_length=200, help_text="Founding Acharya name")
    simhasana = models.CharField(max_length=200, help_text="Name of the Simhasana (throne)")
    location = models.CharField(max_length=300)
    state = models.CharField(max_length=100, blank=True)
    current_swamiji = models.CharField(max_length=400, blank=True)
    associated_linga = models.CharField(max_length=200)
    associated_linga_map_url = models.URLField(blank=True, help_text="Google Maps URL for the associated Linga location")
    color = models.CharField(max_length=50, help_text="CSS color for this Peetha")
    description = models.TextField(help_text="Brief summary")
    history = models.TextField(help_text="Detailed history and origin story")
    order = models.PositiveIntegerField(default=0)

    # Jagathguru details
    swamiji_photo = models.ImageField(upload_to='peetha_media/swamiji/', blank=True, null=True, help_text="Photo of the current Jagathguru")
    swamiji_bio = models.TextField(blank=True, help_text="Biography of the current Jagathguru")

    # Contact details
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)

    # Kannada translations
    name_kn = models.CharField(max_length=200, blank=True)
    acharya_kn = models.CharField(max_length=200, blank=True)
    simhasana_kn = models.CharField(max_length=200, blank=True)
    location_kn = models.CharField(max_length=300, blank=True)
    current_swamiji_kn = models.CharField(max_length=400, blank=True)
    associated_linga_kn = models.CharField(max_length=200, blank=True)
    description_kn = models.TextField(blank=True)
    history_kn = models.TextField(blank=True)

    # Marathi translations
    name_mr = models.CharField(max_length=200, blank=True)
    acharya_mr = models.CharField(max_length=200, blank=True)
    simhasana_mr = models.CharField(max_length=200, blank=True)
    location_mr = models.CharField(max_length=300, blank=True)
    current_swamiji_mr = models.CharField(max_length=400, blank=True)
    associated_linga_mr = models.CharField(max_length=200, blank=True)
    description_mr = models.TextField(blank=True)
    history_mr = models.TextField(blank=True)

    # Hindi translations
    name_hi = models.CharField(max_length=200, blank=True)
    acharya_hi = models.CharField(max_length=200, blank=True)
    simhasana_hi = models.CharField(max_length=200, blank=True)
    location_hi = models.CharField(max_length=300, blank=True)
    current_swamiji_hi = models.CharField(max_length=400, blank=True)
    associated_linga_hi = models.CharField(max_length=200, blank=True)
    description_hi = models.TextField(blank=True)
    history_hi = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PeethaHandler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='handler_profile')
    peetha = models.ForeignKey(Peetha, on_delete=models.CASCADE, related_name='handlers')

    def __str__(self):
        return f"{self.user.username} ({self.peetha.name})"


class PeethaMedia(models.Model):
    MEDIA_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    peetha = models.ForeignKey(Peetha, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='photo')
    photo_file = models.ImageField(upload_to='peetha_media/photos/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube Video URL")
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Kannada translations
    title_kn = models.CharField(max_length=200, blank=True)
    description_kn = models.TextField(blank=True)

    # Marathi translations
    title_mr = models.CharField(max_length=200, blank=True)
    description_mr = models.TextField(blank=True)

    # Hindi translations
    title_hi = models.CharField(max_length=200, blank=True)
    description_hi = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.peetha.name} - {self.title} ({self.media_type})"

    def get_youtube_id(self):
        if not self.youtube_url or self.media_type != 'video':
            return None
        import re
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, self.youtube_url)
        return match.group(1) if match else None


class TravelPlan(models.Model):
    peetha = models.ForeignKey(Peetha, on_delete=models.CASCADE, related_name='travel_plans')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Kannada translations
    title_kn = models.CharField(max_length=200, blank=True)
    location_kn = models.CharField(max_length=300, blank=True)
    description_kn = models.TextField(blank=True)

    # Marathi translations
    title_mr = models.CharField(max_length=200, blank=True)
    location_mr = models.CharField(max_length=300, blank=True)
    description_mr = models.TextField(blank=True)

    # Hindi translations
    title_hi = models.CharField(max_length=200, blank=True)
    location_hi = models.CharField(max_length=300, blank=True)
    description_hi = models.TextField(blank=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.peetha.name} - {self.title} ({self.start_date})"

