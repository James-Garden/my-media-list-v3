from django.urls import path
from search import views

app_name = 'search'
urlpatterns = [
    path('', views.search_handler, name='index'),
    path('users/', views.UserSearch.as_view(), name='users')
]
