from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
import requests
from .models import Movie

# Create your views here.


def import_movie(request):
    api_key = '8483343c'
    movie_title = request.GET.get('title')
    response = request.get(f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"))
    movie_data-response.json()
    movie=Movie(title = movie_data['title'],
                release_date = movie_data['released'],
                cast = movie_data['actors'],
                crew = movie_data['director'],
                plot = movie_data['plot'],
                poster = movie_data['poster'],
                imdb_rating = movie_data['rating'],
                imdb_votes = movie_data['votes'],
                imdb_id = movie_data['id'])
