import requests
from datetime import datetime
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from .models import Movie
from .serializers import MoviewSerializer

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


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviewSerializer
