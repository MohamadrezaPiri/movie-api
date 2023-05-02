from django.contrib import admin
from django.db.models import Count, Avg, Q


class AvgRatingFilter(admin.SimpleListFilter):
    title = 'avg rating'
    parameter_name = 'avg_rating'

    def lookups(self, request, model_admin):
        return [
            ('<5', 'Under 5'),
            ('>5', 'Above 5')

        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(avg_rating=Avg('rating__stars'))
        if self.value() == '<5':
            return annotated_value.filter(avg_rating__lt=5)
        elif self.value() == '>5':
            return annotated_value.filter(Q(avg_rating__gt=5) | Q(avg_rating=5))
        

class ReviewsCountFilter(admin.SimpleListFilter):
    title = 'Reviews'
    parameter_name = 'reviews_count'

    def lookups(self, request, model_admin):
        return [
            ('=0', 'Without review'),
            ('0<', 'With review')

        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(reviews_count=Count('reviews'))
        if self.value() == '=0':
            return annotated_value.filter(reviews_count=0)
        elif self.value() == '0<':
            return annotated_value.filter(reviews_count__gt=0)
