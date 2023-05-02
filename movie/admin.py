from django.contrib import admin, messages
from django.urls import reverse
from django.db.models import Count,Avg,Q
from django.utils.html import urlencode, format_html
from .models import Movie, Rating, Review

# Register your models here.


class AvgRatingFilter(admin.SimpleListFilter):
    title = 'avg rating'
    parameter_name = 'avg_rating'

    def lookups(self, request, model_admin):
        return [
            ('<5', 'Under 5'),
            ('>5', 'Above 5')

        ]

    def queryset(self, request, queryset):
        if self.value() == '<5':
            annotated_value=queryset.annotate(avg_rating=Avg('rating__stars'))
            return annotated_value.filter(avg_rating__lt=5)
        elif self.value() == '>5':
            return annotated_value.filter(Q(avg_rating__gt=5) | Q(avg_rating=5))
        


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'cast', 'crew','reviews_count','votes','avg_rating']
    list_filter = [AvgRatingFilter]
    search_fields = ['title', 'cast']
    actions = ['clear_reviews', 'clear_votes']

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
