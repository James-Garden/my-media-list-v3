from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from accounts.models import User


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"
    extra_context = {}
    profile_user = None

    def get_page_title(self):
        return f"{self.profile_user}' profile" \
            if self.profile_user.username[-1] == 's' \
            else f"{self.profile_user.username}'s profile"

    def set_profile_user(self, request, **kwargs):
        if 'username' in kwargs:
            self.profile_user = get_object_or_404(User, username=kwargs['username'])
        else:
            if request.user.is_authenticated:
                self.profile_user = request.user
            else:
                messages.add_message(request, messages.ERROR, "!danger You must be logged in to view your profile.")
                raise PermissionError

    def get(self, request, *args, **kwargs):
        try:
            self.set_profile_user(request, **kwargs)
        except PermissionError:
            return redirect_to_login(next=request.path)
        self.extra_context['page_title'] = self.get_page_title()
        return super().get(self, request, *args, **kwargs)
