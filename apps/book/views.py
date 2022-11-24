from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import mixins, filters

from django_filters import rest_framework as rest_filter
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import (
    Author,
    Book,
    Genre
    )

from .serializers import (
    AuthorSerializer,
    AuthorListSerializer,
    AuthorRetrieveSerializer,

    BookSerializer,
    BookListSerializer,

    GenreSerializer,
    GenreListSerializer,
    GenreRetrieveSerializer
    )


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    filterset_fields = ['name']
    search_fields = ['first_name', 'last_name', 'last_name']


    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        elif self.action == 'retrieve':
            return AuthorRetrieveSerializer
        return AuthorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions() 

    @method_decorator(cache_page(60*2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend, 
        filters.OrderingFilter
        ]
    filterset_fields = ['title', 'year_published', 'in_stock', 'genre', 'price', 'author']
    search_fields = ['title', 'author', 'genre', 'author.last_name', 'author.first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions() 

    def retrieve(self, request, *args, **kwargs):
        instance: Book = self.get_object() 
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(60*2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
class GenreViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        elif self.action == 'retrieve':
            return GenreRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['destroy', 'create']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @method_decorator(cache_page(60*2))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)