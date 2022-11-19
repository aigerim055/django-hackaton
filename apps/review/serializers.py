from rest_framework import serializers

from .models import (
    Favorite,
    Comment,
    Rating,
)



class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('books')
        favorite = Favorite.objects.filter(user=user, book=book).first()
        if favorite:
            raise serializers.ValidationError('!!!')

        return super().create(validated_data)

    def del_favorites(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('books')
        favorite = Favorite.objects.filter(user=user, book=book).first()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('this book is not favorite')


class FavoritesListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='account.username')

    class Meta:
        model = Favorite
        fields = ['user', 'book']


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs