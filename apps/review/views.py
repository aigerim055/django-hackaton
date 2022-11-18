from crypt import methods
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import(
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.bio.permissions import IsOwner
from .models import Favorite
from .serializers import (
    FavoriteSerializer,
    FavoritesListSerializer
)



class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def perform_create(self, serializer): # для чего эта функция, чтобы не рописыать юзера в запрроме
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            self.permission_classes = [IsOwner, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        book = self.get_object()
        serializer = FavoriteSerializer(
            data=request.data, 
            context={
                'request':request,
                'book':book
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('successfully added to favorites!')
            if request.method == 'DELETE':
                serializer.del_favorites()
                return Response('successfully removed from favorites!')
