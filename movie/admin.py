from django.contrib import admin
from django.urls import reverse
from django.utils.html import urlencode, format_html
from .models import Movie, Rating, Review

# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'cast', 'crew']
    search_fields = ['title', 'cast']

    def reviews(self, movie):
        url = (
            reverse('admin:movie_movie_changelist')
            + '?'
            + urlencode({
                'movie__id': str(movie.id)
            }))
        return format_html('<a href="{}">{}</a>', url, movie.reviews)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'stars']
    autocomplete_fields = ['user', 'movie']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text']
    autocomplete_fields = ['user', 'movie']
