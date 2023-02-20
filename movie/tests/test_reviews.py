import pytest
from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
from movie.models import *


# FIXTURES
@pytest.fixture
def create_review(api_client):
    def do_create_review(movie_id, review):
        return api_client.post(f'/movies/{movie_id}/reviews/', review)
    return do_create_review


@pytest.fixture
def update_review(api_client):
    def do_update_review(movie_id, review_id, review):
        return api_client.put(f'/movies/{movie_id}/reviews/{review_id}/', review)
    return do_update_review


@pytest.fixture
def delete_review(api_client):
    def do_delete_review(movie_id, review_id):
        return api_client.delete(f'/movies/{movie_id}/reviews/{review_id}/')
    return do_delete_review


# TESTS
@pytest.mark.django_db
class TestCreateReview:
    def test_if_user_is_anonymous_returns_401(self, create_review):
        response = create_review('1', {'text': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, create_review, authenticate):
        authenticate()
        response = create_review('1', {'text': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_review, authenticate):
        movie = baker.make(Movie)
        user = baker.make(User)
        review = baker.make(Review, user=user, movie=movie)

        authenticate(user=user)
        response = create_review(movie.id, {'text': 'a'})

        assert response.status_code == status.HTTP_201_CREATED


@ pytest.mark.django_db
class TestUpdateReview:
    def test_if_user_is_anonymous_returns_401(self,  update_review):
        response = update_review('1', '1', {'text': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, update_review, authenticate):
        movie = baker.make(Movie)
        user = baker.make(User)
        review = baker.make(Review, user=user, movie=movie)

        authenticate(user=user)
        response = update_review(movie.id, review.id, {'text': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_author_returns_403(self, update_review, authenticate):
        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        user = baker.make(User)
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=user)
        response = update_review(movie.id, review.id, {'text': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_200(self,  update_review, authenticate):

        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=author)
        response = update_review(movie.id, review.id, {'text': 'a'})

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, update_review, authenticate):
        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        user = baker.make(User, is_staff=True)
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=user)
        response = update_review(movie.id, review.id, {'text': 'a'})

        assert response.status_code == status.HTTP_200_OK


@ pytest.mark.django_db
class TestDeleteReview:
    def test_if_user_is_anonymous_returns_401(self,  delete_review):
        response = delete_review('1', '1')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(self,  delete_review, authenticate):
        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        user = baker.make(User)
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=user)
        response = delete_review(movie.id, review.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_204(self,  delete_review, authenticate):
        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=author)
        response = delete_review(movie.id, review.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self, delete_review, authenticate):
        movie = baker.make(Movie)
        author = baker.make(User, username='author')
        user = baker.make(User, is_staff=True)
        review = baker.make(Review, user=author, movie=movie)

        authenticate(user=user)
        response = delete_review(movie.id, review.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestGetReviewsList:
    def test_if_returns_200(self, api_client):
        review = baker.make(Review)

        response = api_client.get(f'/movies/{review.movie.id}/reviews/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_movie_or_any_reviews_does_not_exist_returns_404(self, api_client):

        response = api_client.get(f'/movies/1/reviews/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
