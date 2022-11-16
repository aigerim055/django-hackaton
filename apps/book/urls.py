from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookViewSet,
    GenreViewSet
    )


router = DefaultRouter()
router.register('author', AuthorViewSet)
router.register('book', BookViewSet)
router.register('genre', GenreViewSet)

urlpatterns = [

]

urlpatterns += router.urls