from utils.views import BaseTemplateView


class Home(BaseTemplateView):
    page_title = "Home"
    template_name = "home/index.html"
