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
                  'poster', 'imdb_rating', 'imdb_votes', 'imdb_id', 'votes', 'avg_rating']


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
