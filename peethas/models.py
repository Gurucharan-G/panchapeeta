from django.db import models


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
