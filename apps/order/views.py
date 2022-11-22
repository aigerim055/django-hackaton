from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]   # IsOwner    filtration
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'year_published', 'in_stock', 'genre', 'price', 'author']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
       

# create - authenticated 
# retrieve - is owner
# list - is owner
# update - is owner - убрать
# delete - is owner

# менять статус с 