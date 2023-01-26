import requests
from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Movie, Review, Rating, Movie
from .serializers import MoviewSerializer, ReviewSerializer, RatingSerializer
from .permissions import IsAuthorOrReadOnly

# Create your views here.


def import_movies(request):
    api_key = '8483343c'
    movie_title = request.GET.get('title')
    response = requests.get(
        f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}")
    movie_data = response.json()
    if movie_data['Response'] == 'True':
        release_date = datetime.strptime(
            movie_data['Released'], '%d %b %Y').date()
        (movie, created) = Movie.objects.get_or_create(title=movie_data['Title'], defaults={
            'release_date': release_date,
            'cast': movie_data['Actors'],
            'crew': movie_data['Director'],
            'plot': movie_data['Plot'],
            'poster': movie_data['Poster'],
            'imdb_rating': movie_data['imdbRating'],
            'imdb_votes': movie_data['imdbVotes'],
            'imdb_id': movie_data['imdbID'],
        })
        if created:
            message = 'Movie imported successfully'
        else:
            message = 'Movie already exists in database'
    else:
        message = 'Movie not found'

    return JsonResponse({'message': message})


class MovieViewSet(ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviewSerializer
    pagination_class = PageNumberPagination


class RatingViewset(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(movie=self.kwargs['movie_pk'])

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'movie_id': self.kwargs['movie_pk']}
