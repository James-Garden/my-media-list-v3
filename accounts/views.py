from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    extra_context = {
        'page_title': "Login"
    }


class LogoutView(auth_views.LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, '!success Logged out successfully!')
        return super().dispatch(request, *args, **kwargs)
