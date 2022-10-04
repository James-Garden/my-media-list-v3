from django.contrib.auth.views import redirect_to_login

from media_list.models import ListEntry
from utils.views import BaseTemplateView, get_user_from_url


class AbstractListView(BaseTemplateView):
    template_name = "media_list/list.html"
    page_user = None
    query_callback = None
    list_name = "Base List"

    def get_page_title(self):
        pluralise = "" if self.page_user.username[-1] == 's' else "s"
        return f"{self.page_user.username}'{pluralise} {self.list_name}"

    def get(self, request, *args, **kwargs):
        try:
            self.page_user = get_user_from_url(request, **kwargs)
        except PermissionError:
            return redirect_to_login(next=request.path)
        self.page_title = self.get_page_title()
        context = self.get_context_data(**kwargs)
        context['list_objects'] = self.query_callback(self.page_user)
        return self.render_to_response(context)


class BookListView(AbstractListView):
    query_callback = ListEntry.get_user_book_list
    list_name = "Book List"


class FilmListView(AbstractListView):
    query_callback = ListEntry.get_user_film_list
    list_name = "Film List"


class SeriesListView(AbstractListView):
    query_callback = ListEntry.get_user_series_list
    list_name = "Series List"
