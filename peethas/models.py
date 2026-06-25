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
    live_youtube_url = models.URLField(blank=True, null=True, help_text="YouTube Live stream URL (leave blank if not active)")
    live_youtube_title = models.CharField(max_length=200, blank=True, null=True, help_text="Custom title for the live stream (defaults to 'Swamiji Divine Live Stream' if blank)")

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

    # Telugu translations
    name_te = models.CharField(max_length=200, blank=True)
    acharya_te = models.CharField(max_length=200, blank=True)
    simhasana_te = models.CharField(max_length=200, blank=True)
    location_te = models.CharField(max_length=300, blank=True)
    current_swamiji_te = models.CharField(max_length=400, blank=True)
    associated_linga_te = models.CharField(max_length=200, blank=True)
    description_te = models.TextField(blank=True)
    history_te = models.TextField(blank=True)

    # Tamil translations
    name_ta = models.CharField(max_length=200, blank=True)
    acharya_ta = models.CharField(max_length=200, blank=True)
    simhasana_ta = models.CharField(max_length=200, blank=True)
    location_ta = models.CharField(max_length=300, blank=True)
    current_swamiji_ta = models.CharField(max_length=400, blank=True)
    associated_linga_ta = models.CharField(max_length=200, blank=True)
    description_ta = models.TextField(blank=True)
    history_ta = models.TextField(blank=True)

    # Malayalam translations
    name_ml = models.CharField(max_length=200, blank=True)
    acharya_ml = models.CharField(max_length=200, blank=True)
    simhasana_ml = models.CharField(max_length=200, blank=True)
    location_ml = models.CharField(max_length=300, blank=True)
    current_swamiji_ml = models.CharField(max_length=400, blank=True)
    associated_linga_ml = models.CharField(max_length=200, blank=True)
    description_ml = models.TextField(blank=True)
    history_ml = models.TextField(blank=True)


    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_live_youtube_id(self):
        if not self.live_youtube_url:
            return None
        import re
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, self.live_youtube_url)
        return match.group(1) if match else None


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

    # Telugu translations
    title_te = models.CharField(max_length=200, blank=True)
    description_te = models.TextField(blank=True)

    # Tamil translations
    title_ta = models.CharField(max_length=200, blank=True)
    description_ta = models.TextField(blank=True)

    # Malayalam translations
    title_ml = models.CharField(max_length=200, blank=True)
    description_ml = models.TextField(blank=True)


    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.peetha.name} - {self.media_type} - {self.title}"

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

    # Telugu translations
    title_te = models.CharField(max_length=200, blank=True)
    location_te = models.CharField(max_length=300, blank=True)
    description_te = models.TextField(blank=True)

    # Tamil translations
    title_ta = models.CharField(max_length=200, blank=True)
    location_ta = models.CharField(max_length=300, blank=True)
    description_ta = models.TextField(blank=True)

    # Malayalam translations
    title_ml = models.CharField(max_length=200, blank=True)
    location_ml = models.CharField(max_length=300, blank=True)
    description_ml = models.TextField(blank=True)


    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.peetha.name} - {self.title} ({self.start_date})"


# ===== POOJA BOOKING MODELS =====

class PeethaPaymentConfig(models.Model):
    peetha = models.OneToOneField(Peetha, on_delete=models.CASCADE, related_name='payment_config')
    razorpay_key_id = models.CharField(max_length=100, help_text="Razorpay Key ID for this Peetha")
    razorpay_key_secret = models.CharField(max_length=100, help_text="Razorpay Key Secret for this Peetha")
    is_active = models.BooleanField(default=True, help_text="Enable/Disable online payments for this Peetha")

    def __str__(self):
        return f"Payment Config - {self.peetha.name}"


class Pooja(models.Model):
    peetha = models.ForeignKey(Peetha, on_delete=models.CASCADE, related_name='poojas')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Rupees")
    category = models.CharField(
        max_length=50,
        default='special',
        choices=(
            ('daily', 'Daily Seva'),
            ('special', 'Special Pooja'),
            ('homa', 'Homa & Havan'),
            ('utsava', 'Utsava / Festival Seva'),
        )
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    total_slots = models.PositiveIntegerField(default=10, help_text="Total available slots per day")
    available_days = models.CharField(max_length=200, default='all', help_text="Comma-separated weekdays or 'all'")

    # Translations
    name_kn = models.CharField(max_length=200, blank=True)
    description_kn = models.TextField(blank=True)
    name_mr = models.CharField(max_length=200, blank=True)
    description_mr = models.TextField(blank=True)
    name_hi = models.CharField(max_length=200, blank=True)
    description_hi = models.TextField(blank=True)
    name_te = models.CharField(max_length=200, blank=True)
    description_te = models.TextField(blank=True)
    name_ta = models.CharField(max_length=200, blank=True)
    description_ta = models.TextField(blank=True)
    name_ml = models.CharField(max_length=200, blank=True)
    description_ml = models.TextField(blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.peetha.name}"


class PoojaBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    pooja = models.ForeignKey(Pooja, on_delete=models.PROTECT, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    devotee_name = models.CharField(max_length=200)
    devotee_phone = models.CharField(max_length=20)
    devotee_email = models.EmailField(blank=True)
    gotra = models.CharField(max_length=100, blank=True)
    nakshatra = models.CharField(max_length=100, blank=True)
    rashi = models.CharField(max_length=100, blank=True)
    family_members = models.TextField(blank=True, help_text="Names of family members to include in sankalpa")
    date_of_pooja = models.DateField()
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.devotee_name} - {self.pooja.name} ({self.get_payment_status_display()})"

    @property
    def formatted_family_members(self):
        if not self.family_members:
            return ""
        import json
        try:
            members = json.loads(self.family_members)
            if isinstance(members, list):
                parts = []
                for m in members:
                    details = []
                    if m.get('gotra'): details.append(f"G: {m['gotra']}")
                    if m.get('nakshatra'): details.append(f"N: {m['nakshatra']}")
                    if m.get('rashi'): details.append(f"R: {m['rashi']}")
                    detail_str = f" ({', '.join(details)})" if details else ""
                    parts.append(f"{m['name']}{detail_str}")
                return ", ".join(parts)
        except Exception:
            pass
        return self.family_members


class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}: {'Enabled' if self.is_enabled else 'Disabled'}"


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    gotra = models.CharField(max_length=100, blank=True)
    nakshatra = models.CharField(max_length=100, blank=True)
    rashi = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile - {self.user.username}"

    def completion_percentage(self):
        fields = [
            self.user.first_name,
            self.user.email,
            self.phone_number,
            self.address,
            self.profile_pic,
            self.gender,
            self.gotra,
            self.nakshatra,
            self.rashi
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)


def get_user_profile(self):
    profile, created = UserProfile.objects.get_or_create(user=self)
    return profile

User.profile = property(get_user_profile)

