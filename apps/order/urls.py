from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from .views import (
    OrderViewSet, 
    OrderHistoryView,
)



router = DefaultRouter()
router.register('orders', OrderViewSet, 'orders')

urlpatterns = [
    path('history/', OrderHistoryView.as_view(), name='orer-history')
]

urlpatterns += router.urls