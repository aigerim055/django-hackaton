from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet


router = DefaultRouter()


router.register('favorite', FavoriteViewSet, 'favorite')


urlpatterns = [
    # path('favorite/', FavoriteView.as_view(), name='favorite'),
]
urlpatterns += router.urls