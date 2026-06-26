from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from django.contrib.auth import get_user_model


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_superuser or hasattr(user, 'handler_profile'):
            return reverse('peethas:dashboard_home')
        return '/'

    def login(self, request, user):
        # Clear or force next url to dashboard for superusers/handlers in normal login request parameters
        if user.is_superuser or hasattr(user, 'handler_profile'):
            if 'next' in request.GET:
                request.GET = request.GET.copy()
                request.GET['next'] = reverse('peethas:dashboard_home')
            if 'next' in request.POST:
                request.POST = request.POST.copy()
                request.POST['next'] = reverse('peethas:dashboard_home')
            if request.session.get('next'):
                request.session['next'] = reverse('peethas:dashboard_home')
        super().login(request, user)

    def add_message(self, request, level, message_template, message_context=None, extra_tags=None):
        # Suppress standard allauth login, logout, and signup success messages
        if message_template in [
            'account/messages/logged_in.txt',
            'account/messages/logged_out.txt',
            'account/messages/signup.txt',
        ] or (message_template and ('logged_in' in message_template or 'logged_out' in message_template or 'signup' in message_template)):
            return
        super().add_message(request, level, message_template, message_context, extra_tags)

    def is_open_for_signup(self, request):
        from .feature_flags import DEVOTEE_REGISTRATION
        return bool(DEVOTEE_REGISTRATION)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Enforce devotee registration block for new users
        from .feature_flags import DEVOTEE_REGISTRATION
        from django.contrib import messages
        
        # Determine if the returning social user matches a superuser or handler by email in the DB
        email = None
        if sociallogin.account and sociallogin.account.extra_data:
            email = sociallogin.account.extra_data.get('email')
        
        is_privileged = False
        user_exists = False
        User = get_user_model()
        
        if email:
            try:
                db_user = User.objects.get(email=email)
                user_exists = True
                if db_user.is_superuser or hasattr(db_user, 'handler_profile'):
                    is_privileged = True
            except User.DoesNotExist:
                pass
                
        if not user_exists and sociallogin.user.username:
            user_exists = User.objects.filter(username=sociallogin.user.username).exists()

        # If user does not exist (new signup) and devotee registration is disabled, block it
        if not user_exists and not bool(DEVOTEE_REGISTRATION):
            from allauth.exceptions import ImmediateHttpResponse
            from django.shortcuts import redirect
            messages.error(request, 'Devotee registration is currently disabled.')
            raise ImmediateHttpResponse(redirect('peethas:login'))

        # Force the redirect state to the dashboard for privileged users
        if is_privileged:
            sociallogin.state['next'] = reverse('peethas:dashboard_home')

    def is_open_for_signup(self, request, sociallogin):
        from .feature_flags import DEVOTEE_REGISTRATION
        return bool(DEVOTEE_REGISTRATION)



