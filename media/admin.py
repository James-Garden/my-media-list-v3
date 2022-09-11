from django.contrib import admin

from media.models import Media, Film, Series, Book

admin.site.register(Media)
admin.site.register(Film)
admin.site.register(Series)
admin.site.register(Book)
