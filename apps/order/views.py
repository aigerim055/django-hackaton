from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as rest_filter
from rest_framework import filters

from .models import Order
from .serializers import (
    OrderSerializer,
    OrderHistorySerializer,
)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]   # IsOwner    filtration
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    filterset_fields = ['status']
    ordering_fields = ['created_at']
    search_fields = ['order_id', 'status']
    

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderHistoryView(ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
       

# create - authenticated 
# retrieve - is owner
# list - is owner
# update - is owner - убрать
# delete - is owner

# менять статус с 