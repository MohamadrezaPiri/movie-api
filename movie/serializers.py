from rest_framework import serializers
from .models import Movie


class MoviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'cast', 'crew', 'plot',
                  'poster', 'imdb_rating', 'imdb_votes', 'imdb_id']
