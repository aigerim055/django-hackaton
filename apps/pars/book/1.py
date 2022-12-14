# from crypt import methods
# from rest_framework.viewsets import ModelViewSet, GenericViewSet
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import(
#     IsAdminUser,
#     IsAuthenticated,
#     AllowAny,
# )
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import mixins

# from apps.bio.permissions import IsOwner
# from .models import Favorite, Comment, Rating
# from .serializers import (
#     FavoriteSerializer,
#     FavoritesListSerializer,
#     CommentSerializer,
#     RatingSerializer,
# )




# class FavoriteViewSet(mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     GenericViewSet):


#     serializer_class = FavoriteSerializer
#     queryset = Favorite.objects.all()

#     def perform_create(self, serializer): # для чего эта функция, чтобы не рописыать юзера в запрроме
#         serializer.save(user=self.request.user)

#     def get_serializer_class(self):
#         if self.action == 'favorite' and self.request.method in ['POST', 'DELETE', 'LIST']:
#             return FavoriteSerializer
#         # if self.action == 'favorite' and self.request.method == 'LIST':
#         #     return Favorite
#         return super().get_serializer_class()

#     def get_permissions(self):
#         if self.action == 'favorite' and self.request.method in ['POST']:
#             self.permission_classes = [IsAuthenticated]
#         if self.action == 'favorite' and self.request.method =='DELETE':
#             self.permission_classes = [IsOwner]
#         return super().get_permissions()


#     @action(detail=True)#, methods=['POST', 'DELETE'])
#     def favorite(self, request, pk=None):
#         book = self.get_object()
#         serializer = FavoriteSerializer(
#             data=request.data, 
#             context={
#                 'request':request,
#                 'book':book
#             })
#         if serializer.is_valid(raise_exception=True):
#             if request.method == 'POST':
#                 serializer.save(user=request.user)
#                 return Response('Successfully added to favorites!')
#             if request.method == 'DELETE':
#                 serializer.del_favorite()
#                 return Response('Successfully removed from favorites!')

#     # def get_serializer_context(self):
#     # context = super().get_serializer_context()
#     # context['request'] = request
#     # return context

#     # def post(self, request):
#     #     serializer = FavoriteCreateSerializer(data=request.data)
#     #     if serializer.is_valid(raise_exception=True):
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # def delete(self, request, pk, format=None):
#     #     serializer = FavoriteDeleteSerializer(data=request.data)
#     #     pk = request.book
#     #     like = self.get_object(pk)
#     #     like.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)


# # class CommentView(
# #     mixins.CreateModelMixin,
# #     mixins.ListModelMixin,
# #     mixins.DestroyModelMixin,
# #     GenericViewSet
# #     ):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #     serializer.del_favorites()
# #     return Response('successfully removed from favorites!')


# # class CommentView(mixins.CreateModelMixin,
# #                 mixins.DestroyModelMixin,
# #                 mixins.ListModelMixin,
# #                 GenericViewSet):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #     permission_classes = [IsAuthenticated]

# #     def perform_create(self, serializer): 
# #         serializer.save(user=self.request.user)

# #     def get_serializer_context(self):
# #         context = super().get_serializer_context()
# #         context['request'] = self.request
# #         return context


# class RatingView(mixins.CreateModelMixin,
#                 mixins.DestroyModelMixin,
#                 mixins.ListModelMixin,
#                 GenericViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

#     # def perform_create(self, serializer): 
#     #     serializer.save(user=self.request.user)