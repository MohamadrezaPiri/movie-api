from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import MovieViewSet, import_movies, ReviewViewSet, RatingViewset

router = SimpleRouter()
router.register('', MovieViewSet)
router.register('ratings', RatingViewset)


movies_router = NestedSimpleRouter(router, '', lookup='movie')
movies_router.register('reviews', ReviewViewSet, basename='movie-reviews')

urlpatterns = [
    path('import_movies/', import_movies, name='import_movies'),
    path('', include(router.urls)),
    path('', include(movies_router.urls)),
]
