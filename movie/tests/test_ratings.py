import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from movie.models import *


@pytest.mark.django_db
class TestCreatRating:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/ratings/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_already_rated_a_movie_returns_400(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/ratings/', {'movie': movie.id, 'stars': 3})
        response2 = client.post('/ratings/', {'movie': movie.id, 'stars': 4})

        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_rate_is_not_between_1_and_10_returns_400(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/ratings/', {'movie': movie.id, 'stars': 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_rate_is_between_1_and_10_returns_201(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/ratings/', {'movie': movie.id, 'stars': 3})

        assert response.status_code == status.HTTP_201_CREATED
