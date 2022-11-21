from rest_framework import serializers

from .models import (
    Favorite,
    Comment,
    Rating,
)
from apps.account.serializers import UserListSerializer


# class CurrentBookDefault:
#     requires_context = True

#     def __call__(self, context):
#         return context['book']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Favorite
        # exclude = ['id']
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('books')
        favorite = Favorite.objects.filter(user=user, book=book).exists()
        if not favorite:
            return super().create(validated_data)
        raise serializers.ValidationError('This book has been added to favorites')

    def del_favorite(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('books')
        favorite = Favorite.objects.filter(user=user, book=book).exists()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('This book is not in favorites')


# class FavoriteListSerializer(serializers.ModelSerializer):
#     # user = serializers.ReadOnlyField(source='account.username')

#     user = UserListSerializer(read_only=True, many=True)  
#     class Meta:
#         model = Favorite
#         fields = ['user', 'book']

    # def to_representation(self, instance: Genre):
    #     books = instance.books.all()
    #     representation = super().to_representation(instance)  
    #     representation['books'] = BookListSerializer(
    #         instance=books, many=True).data
    #     return representation


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs