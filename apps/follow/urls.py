from rest_framework.routers import DefaultRouter
from .views import UserFollowingViewSet


router = DefaultRouter()

router.register('', UserFollowingViewSet, 'follow')

urlpatterns = [

]
urlpatterns += router.urls