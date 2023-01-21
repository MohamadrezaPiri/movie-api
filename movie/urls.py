from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import MovieViewSet, import_movies

# router = SimpleRouter()
# router.register('movies', MovieViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('import_movies/', import_movies, name='import_movies')

]
