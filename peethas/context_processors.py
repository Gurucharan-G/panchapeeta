from .models import Peetha
from .feature_flags import DEVOTEE_REGISTRATION, DEVOTIONAL_CHANTING, DEVOTIONAL_CHANTING_AUTOPLAY

def live_peethas_processor(request):
    """
    Returns a list of Peethas that currently have an active live stream, all Peethas, and feature flags.
    """
    active_live = Peetha.objects.filter(live_youtube_url__isnull=False).exclude(live_youtube_url='')
    all_peethas = Peetha.objects.all().order_by('id')
    return {
        'live_peethas': active_live,
        'all_peethas': all_peethas,
        'devotee_registration_enabled': bool(DEVOTEE_REGISTRATION),
        'devotional_chanting_enabled': bool(DEVOTIONAL_CHANTING),
        'devotional_chanting_autoplay': bool(DEVOTIONAL_CHANTING_AUTOPLAY),
    }

