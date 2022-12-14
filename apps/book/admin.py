from django.contrib import admin
from .models import Author, Book, Genre

admin.site.register(Author)
# admin.site.register(Book)
admin.site.register(Genre)

# from django.apps import apps
# from django.contrib.admin.sites import AlreadyRegistered


# app_models = apps.get_app_config('book').get_models()
# for model in app_models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass

from .models import Book, BookImage

class TabularInlineImages(admin.TabularInline):
    model = BookImage
    extra = 5
    fields = ['image']

class BookAdmin(admin.ModelAdmin):
    model = Book
    inlines = [TabularInlineImages]

admin.site.register(Book, BookAdmin)
