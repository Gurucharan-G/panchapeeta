from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse

class MobileAppRestrictionMiddleware:
    """
    Middleware to ensure that only privileged users (Handlers, Staff, Superadmins)
    can use the mobile application. Devotee accounts are completely blocked from 
    logging in via the mobile app.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine if the request originates from the Android WebView mobile app
        is_mobile_app = request.META.get('HTTP_X_REQUESTED_WITH') == 'com.panchapeetas.app'

        if is_mobile_app and request.user.is_authenticated:
            # Check if the user is privileged
            user = request.user
            is_privileged = user.is_superuser or user.is_staff or hasattr(user, 'handler_profile')
            
            if not is_privileged:
                # Log out the devotee user
                logout(request)
                # Display an error message
                messages.error(request, 'Devotee accounts are not permitted to use the mobile handler application.')
                
                # Redirect them to the login page
                return redirect(reverse('peethas:login'))

        response = self.get_response(request)
        return response
