from django.contrib import admin, messages
from django.urls import reverse
from django.db.models import Count
from django.utils.html import urlencode, format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Movie, Rating, Review
from .filters import ReviewsCountFilter, AvgRatingFilter

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'cast', 'crew','reviews_count','votes','avg_rating']
    list_filter = [AvgRatingFilter,ReviewsCountFilter]
    search_fields = ['title', 'cast']
    actions = ['clear_reviews', 'clear_votes']

    @admin.display(ordering='reviews_count')
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

    @admin.action(description='Clear votes')
    def clear_votes(self, request, queryset):
        updated_count = 0
        for movie in queryset:
            num_ratings = movie.votes() 
            updated_count += num_ratings 
            Rating.objects.filter(movie=movie).delete()
        self.message_user(
            request,
            f'{updated_count} votes were successfully removed.',
            messages.SUCCESS
        )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'stars']
    autocomplete_fields = ['user', 'movie']
    search_fields = ['user__username']
    list_filter = ['user__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'content']
    autocomplete_fields = ['user', 'movie']
    search_fields = ['user__username','movie__title']
    list_filter = ['user__username','movie']    


admin.site.unregister(User)
user = get_user_model()


@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username','first_name','last_name','email','is_staff']