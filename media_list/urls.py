from django.urls import path

from media_list import views

app_name = 'media_list'
urlpatterns = [
    path('book-list/', views.BookListView.as_view(), name='book-list'),
    path('book-list/<str:username>/', views.BookListView.as_view(), name='book-list'),
    path('film-list/', views.FilmListView.as_view(), name='film-list'),
    path('film-list/<str:username>/', views.FilmListView.as_view(), name='film-list'),
    path('series-list/', views.SeriesListView.as_view(), name='series-list'),
    path('series-list/<str:username>/', views.SeriesListView.as_view(), name='series-list'),
]
