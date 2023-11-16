from django.contrib import admin
from books.models import (
    Book,
    Author,
    Rate,
    Genre
)

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Rate)
admin.site.register(Genre)