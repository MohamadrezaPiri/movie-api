from django.contrib.auth.models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer
from .models import Movie, Review


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password']


class MoviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'cast', 'crew', 'plot',
                  'poster', 'imdb_rating', 'imdb_votes', 'imdb_id']


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


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
