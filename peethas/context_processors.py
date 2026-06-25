from .models import Peetha

def live_peethas_processor(request):
    """
    Returns a list of Peethas that currently have an active live stream.
    """
    active_live = Peetha.objects.filter(live_youtube_url__isnull=False).exclude(live_youtube_url='')
    return {
        'live_peethas': active_live
    }
