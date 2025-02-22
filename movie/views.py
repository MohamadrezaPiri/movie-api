import requests
from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework.backends import DjangoFilterBackend
from .models import Movie, Review, Rating, Movie
from .serializers import MovieSerializer, ReviewSerializer, RatingSerializer, SearchMovieSerializer
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


class MovieViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    def get_object(self):
        obj = super().get_object()
        ip = self.request.ip_address
        if ip not in obj.hits.all():
            obj.hits.add(ip)
        return obj    
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ['imdb_rating', 'avg_rating']
    search_fields = ['title', 'cast', 'crew']
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]


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
        review = Review.objects.filter(movie=self.kwargs['movie_pk'])
        if review.exists():
            return review
        raise NotFound()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'movie_id': self.kwargs['movie_pk']}
