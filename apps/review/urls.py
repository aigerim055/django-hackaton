from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteView,
    CommentView,
    RatingView
)


router = DefaultRouter()


router.register('favorite', FavoriteView, 'favorite')
router.register('comment', CommentView, 'comment')
router.register('rating', RatingView, 'rating')


urlpatterns = [

]
urlpatterns += router.urls