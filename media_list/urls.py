from django.urls import path

from media_list import views

app_name = 'media_list'
urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<str:username>/', views.BookListView.as_view(), name='book-list'),
    path('films/', views.FilmListView.as_view(), name='film-list'),
    path('films/<str:username>/', views.FilmListView.as_view(), name='film-list'),
    path('series/', views.SeriesListView.as_view(), name='series-list'),
    path('series/<str:username>/', views.SeriesListView.as_view(), name='series-list'),
]
