import requests
from datetime import datetime
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Movie, Review, Rating


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'cast', 'crew', 'plot',
                  'poster', 'imdb_rating', 'imdb_votes', 'imdb_id', 'votes', 'avg_rating', 'hits']
        
        hits = serializers.SerializerMethodField(method_name='get_hits_count')

        def get_hits_count(self, movie:Movie):
            return movie.hits.count()
        
    def create(self, validated_data):
        api_key = '8483343c'
        movie_title = self.validated_data['title']
        response = requests.get(
            f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}")
        movie_data = response.json()
        if movie_data['Response'] == 'True':
            release_date = datetime.strptime(
                movie_data['Released'], '%d %b %Y').date()
            if not Movie.objects.filter(title=movie_data['Title']).exists():
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
                    return movie
            else:
                message = 'Movie already exists in database'
                return JsonResponse({'message': message})
        else:
            message = 'Movie not found'
            return JsonResponse({'message': message})

             
        

class SearchMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title']

    def create(self, validated_data):
        api_key = '8483343c'
        movie_title = self.validated_data['title']
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
                return {movie}  
            else:
                message = 'Movie already exists in database'
                return message
        else:
            message = 'Movie not found'
            return message



class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class RatingSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'stars']

    def create(self, validated_data):
        try:
            user_id = self.context['user_id']
            return Rating.objects.create(user_id=user_id, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'user': 'You have already rated this movie.'})


class ReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)
    movie = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'movie']

    def create(self, validated_data):
        user_id = self.context['user_id']
        movie_id = self.context['movie_id']
        return Review.objects.create(user_id=user_id, movie_id=movie_id, **validated_data)
