from rest_framework import serializers
from books.models import (
    Book,
    Rate,
    Author,
    Genre
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.db import models

class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer of Genre for Book Model
    """
    class Meta:
        model = Genre
        fields = (
            "id",
            "title"
        )


class AuthorSerailizer(serializers.ModelSerializer):
    """
    Serializer of Author for Book Model
    """
    class Meta:
        model = Author
        fields = (
            "id",
            "fullname"
        )


class BookListSerailizer(serializers.ModelSerializer):
    """
    Serializer of Book Model for list of books
    """
    genre = GenreSerializer(read_only = True)
    author = AuthorSerailizer(read_only = True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "author",
            "genre",
            "published_date",
            "average_score"
        )

    def get_average_score(self, obj):
        return round(obj.reviews.aggregate(avg_score=models.Avg('score'))['avg_score'], 1)


class RateCreateSerializer(serializers.ModelSerializer):
    """
    Rate Serializer for creating Rate object
    """
    class Meta:
        model = Rate
        fields = '__all__'


class RateListSerializer(serializers.ModelSerializer):
    """
    Rate list Serializer for Book detail
    """
    class Meta:
        model = Rate
        fields = (
            "text",
            "score"
        )


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Book detail with reviews list
    """
    reviews = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only = True)
    author = AuthorSerailizer(read_only = True)
    average_score = serializers.SerializerMethodField()


    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "author",
            "genre",
            "published_date",
            "average_score",
            "reviews"
        )
    
    def get_average_score(self, obj):
        """
        Calculating average rating of book
        """
        return round(obj.reviews.aggregate(avg_score=models.Avg('score'))['avg_score'], 1)

    def get_reviews(self, obj):
        """
        Reviews list
        """
        return RateListSerializer(obj.reviews, many = True).data