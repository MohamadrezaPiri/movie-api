from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import MovieViewSet, import_movies, ReviewViewSet

router = SimpleRouter()
router.register('movies', MovieViewSet)

movies_router = NestedSimpleRouter(router, 'movies', lookup='movie')
movies_router.register('reviews', ReviewViewSet, basename='movie-reviews')

urlpatterns = [
    path('import_movies/', import_movies, name='import_movies'),
    path('', include(router.urls)),
    path('', include(movies_router.urls)),
]
