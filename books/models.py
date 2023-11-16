from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    """
    Genro Model for books
    fields: title
    """
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Author(models.Model):
    """
    Author of books
    fields: fullname
    """
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname


class Book(models.Model):
    """
    Book Model
    fields: title, description, author, genre, published_date
    """

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, models.SET_NULL, null=True, blank=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title


class Rate(models.Model):
    """
    Rate Model of books
    fields: user, text, score
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='reviews')