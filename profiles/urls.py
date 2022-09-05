from django.urls import path
from profiles import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile')
]
