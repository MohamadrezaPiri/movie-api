from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import MovieViewSet, import_movies

router = SimpleRouter()
router.register('movies', MovieViewSet)

urlpatterns = [
    path('import_movies/', import_movies, name='import_movies'),
    path('', include(router.urls))
]
