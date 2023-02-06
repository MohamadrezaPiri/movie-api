import pytest
from django.contrib.auth.models import User
from rest_framework import status
from movie.models import *


# FIXTURES
@pytest.fixture
def create_rating(api_client):
    def do_create_rating(rating):
        return api_client.post('/ratings/', rating)
    return do_create_rating


# TESTS
@pytest.mark.django_db
class TestCreatRating:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/ratings/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_already_rated_a_movie_returns_400(self,  create_rating, authenticate):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        authenticate(user=user)
        response = create_rating({'movie': movie.id, 'stars': 3})
        response2 = create_rating({'movie': movie.id, 'stars': 4})

        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_rate_is_not_between_1_and_10_returns_400(self,  create_rating, authenticate):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        authenticate(user=user)
        response = create_rating({'movie': movie.id, 'stars': 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_rate_is_between_1_and_10_returns_201(self,  create_rating, authenticate):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')

        authenticate(user=user)
        response = create_rating({'movie': movie.id, 'stars': 3})

        assert response.status_code == status.HTTP_201_CREATED
