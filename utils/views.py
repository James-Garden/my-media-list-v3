from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from accounts.models import User


def get_user_from_url(request, **kwargs):
    if 'username' in kwargs:
        return get_object_or_404(User, username=kwargs['username'])
    else:
        if request.user.is_authenticated:
            return request.user
        else:
            messages.add_message(request, messages.ERROR, "!danger You must be logged in to view your profile.")
            raise PermissionError


class BaseTemplateView(TemplateView):
    page_title = "Untitled page"
    template_name = "layout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
