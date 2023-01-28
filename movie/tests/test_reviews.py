import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from movie.models import *


@pytest.mark.django_db
class TestCreateReview:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/movies/1/reviews/', {'text': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        client.force_authenticate(user=User())
        response = client.post('/movies/1/reviews/', {'text': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')
        review = Review.objects.create(
            text='This is a review', user=user, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/movies/1/reviews/', {'text': 'a'})

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateReview:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.put('/movies/1/reviews/1/', {'text': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self):

        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        user = User.objects.create(username='testuser')
        review = Review.objects.create(
            text='This is a review', user=user, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(
            f'/movies/{movie.id}/reviews/{review.id}/', {'text': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_author_returns_403(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        user = User.objects.create(username='testuser')
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(
            f'/movies/{movie.id}/reviews/{review.id}/', {'text': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_200(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=author)
        response = client.put(
            f'/movies/{movie.id}/reviews/{review.id}/', {'text': 'a'})

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        user = User.objects.create(username='testuser', is_staff=True)
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(
            f'/movies/{movie.id}/reviews/{review.id}/', {'text': 'a'})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteReview:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.delete('/movies/1/reviews/1/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        user = User.objects.create(username='testuser')
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            f'/movies/{movie.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_204(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=author)
        response = client.delete(
            f'/movies/{movie.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        author = User.objects.create(username='author')
        user = User.objects.create(username='testuser', is_staff=True)
        review = Review.objects.create(
            text='This is a review', user=author, movie=movie)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            f'/movies/{movie.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
