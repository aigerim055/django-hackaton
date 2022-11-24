from rest_framework import serializers

from .models import UserFollowing


class FollowingSerializer(serializers.ModelSerializer):
    user  = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserFollowing
        fields = ('user', 'following_user')


class FollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ('user', 'following_user')      