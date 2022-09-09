from django.contrib import messages
from django.db.models import Model, Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from accounts.models import User
from utils.url_helpers import url_with_get_params

SEARCH_PAGES = {
    'users': '/search/users/'
}
# TODO: Add other search types [MMl-2]


def invalid_search(request, message, alert_type="danger"):
    messages.add_message(request, messages.ERROR, f"!{alert_type} {message}.")
    # TODO: Replace default redirect with home page [MML-1]
    referer = request.GET.get('referer', reverse('profiles:profile'))
    return redirect(referer)


def search_handler(request):
    params = request.GET.copy()
    search_type = params.pop('type', " ")[0]
    query = params.get('query', "")

    if len(query) < 3:
        return invalid_search(request, "Search query must be at least 3 characters", 'warning')
    elif search_type not in SEARCH_PAGES.keys():
        return invalid_search(request, "Invalid search type")

    return redirect(url_with_get_params(SEARCH_PAGES[search_type], params))


class BaseSearch(ListView):

    model: Model
    paginate_by = 10
    default_page_title = "Search results"
    template_name = 'search/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.default_page_title
        context['query'] = self.request.GET.get('query', "")
        return context


class UserSearch(BaseSearch):

    model = User

    def get_queryset(self):
        query = self.request.GET.get("query")
        return self.model.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)).order_by('-last_login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
