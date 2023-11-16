from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from books.seralizers import (
    BookListSerailizer,
    AuthorSerailizer,
    GenreSerializer,
    RateCreateSerializer,
    BookDetailSerializer
)
from books.models import (
    Book,
    Rate,
    Author,
    Genre
)
from books.pagination import DeafultLimitOffsetPagination


class BooksView(APIView):
    """
    Book view included filter of books by genre and author
    """
    def get(self, request):
        """
        List and filter function of Book Model
        method: GET
        params: author, genre, start_date, end_date
        """
        paginator = DeafultLimitOffsetPagination()
        author = request.GET.get("author", None)
        genre = request.GET.get("genre", None)
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        filter_kwargs = {}

        if genre:
            filter_kwargs["genre__title"] = genre

        if author:
            filter_kwargs["author__fullname"] = author

        if start_date and end_date:
            filter_kwargs["published_date__range"] = [start_date, end_date]
        elif start_date:
            filter_kwargs["published_date__gte"] = start_date
        elif end_date:
            filter_kwargs["published_date__lte"] = end_date
        
        if filter_kwargs:
            books = Book.objects.filter(**filter_kwargs)
        else:
            books = Book.objects.all()
        return paginator.generate_response(books, BookListSerailizer, request)


class GenreView(APIView):
    """
    Genre List View
    """
    def get(self, request):
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many = True)
        return Response(serializer.data)


class AuthorView(APIView):
    """
    Author List View
    """
    def get(self, request):
        author = Author.objects.all()
        seralizer = AuthorSerailizer(author, many = True)
        return Response(seralizer.data)


class RateView(APIView):
    """
    Leave Rate to Book Authentication Requeired
    """
    def post(self, request):
        data = dict(request.data)
        data['user'] = request.user.id
        serializer = RateCreateSerializer(data = data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.error_messages, status=400)


class BookDetailView(APIView):
    """
    Detail of the book with reviews
    """
    def get(self, request, pk):
        book = Book.objects.get(id = pk)
        serializer = BookDetailSerializer(book, many = False)
        return Response(serializer.data)