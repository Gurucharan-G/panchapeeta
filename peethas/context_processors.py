from .models import Peetha
from .feature_flags import DEVOTEE_REGISTRATION

def live_peethas_processor(request):
    """
    Returns a list of Peethas that currently have an active live stream.
    """
    active_live = Peetha.objects.filter(live_youtube_url__isnull=False).exclude(live_youtube_url='')
    return {
        'live_peethas': active_live,
        'devotee_registration_enabled': bool(DEVOTEE_REGISTRATION),
    }

