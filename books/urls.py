from django.urls import path
from books.views import (
    BooksView,
    RateView,
    GenreView,
    BookDetailView,
    AuthorView
)

urlpatterns = [
    path('leave-rate/', RateView.as_view()),
    path('list/', BooksView.as_view()),
    path('genre-list/', GenreView.as_view()),
    path('author-list/', AuthorView.as_view()),
    path('detail/<int:pk>/', BookDetailView.as_view()),
]