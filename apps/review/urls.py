from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewSet,
    CommentView,
    RatingView
)


router = DefaultRouter()


router.register('favorite', FavoriteViewSet, 'favorite')
router.register('comment', CommentView, 'comment')
router.register('rating', RatingView, 'rating')


urlpatterns = [
    # path('favorite/', FavoriteView.as_view(), name='favorite'),
]
urlpatterns += router.urls