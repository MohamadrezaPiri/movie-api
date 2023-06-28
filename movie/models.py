from django.db import models
from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    cast = models.TextField()
    crew = models.TextField()
    plot = models.TextField()
    poster = models.URLField()
    imdb_rating = models.FloatField()
    imdb_votes = models.TextField()
    imdb_id = models.CharField(max_length=10)

    @admin.display(ordering='rating')
    def votes(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        ratings = Rating.objects.filter(movie=self)
        sum = 0
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum/len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title
    
    
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])

    class Meta:
        unique_together = [['user', 'movie']]
        index_together = [['user', 'movie']]

    def __str__(self) -> str:
        return self.movie.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()

    def __str__(self) -> str:
        return self.user.username
    
    @property
    def content(self):
        return truncatechars(self.text, 10)
