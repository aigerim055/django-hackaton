from django.contrib import admin
from .models import Favorite, Comment, Rating


admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Rating)