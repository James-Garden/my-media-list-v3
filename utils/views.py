from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):
    page_title = "Untitled page"
    template_name = "layout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
