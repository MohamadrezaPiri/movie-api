from django.contrib import admin, messages
from django.urls import reverse
from django.db.models import Count
from django.utils.html import urlencode, format_html
from .models import Movie, Rating, Review

# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'cast', 'crew','reviews_count','votes','avg_rating']
    search_fields = ['title', 'cast']

    def reviews_count(self, movie):
        url = (
            reverse('admin:movie_review_changelist')
            + '?'
            + urlencode({
                'movie__id': str(movie .id)
            }))
        return format_html('<a href="{}">{}</a>', url, movie.reviews_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            reviews_count=Count('reviews')
        )
    
    @admin.action(description='Clear reviews')
    def clear_reviews(self, request, queryset):
        total_reviews_count = sum(movie.reviews.count() for movie in queryset)
        
        for movie in queryset:
            movie.reviews.all().delete()
    
        self.message_user(
            request,
            f'{total_reviews_count} reviews cleared.',
            messages.SUCCESS
        )



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'stars']
    autocomplete_fields = ['user', 'movie']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text']
    autocomplete_fields = ['user', 'movie']
