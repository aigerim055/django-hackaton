from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.account.utils import normalize_phone

from .models import (
    UserProfile, 
    ProfileImage
)



User = get_user_model()


class UserProfileCreateSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    avatar_carousel = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=40)
    bio = serializers.CharField(max_length=5000)
    avatar = serializers.ImageField()                          #######
    birthday = serializers.DateField()                         # settings include format   # формат как проверяется, выпдает ли календарь
    phone = serializers.CharField(max_length=14)    # normalize

    def create(self, validated_data):
        avatar_carousel = validated_data.pop('avatar_carousel')
        profile = UserProfile.objects.create(**validated_data)
        images = []
        for image in avatar_carousel:
            images.append(ProfileImage(profile=profile, avatar=image))
        ProfileImage.objects.bulk_create(images)
        return profile


    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format!')
        return phone      

    class Meta:
        model = UserProfile
        fields = ('__all__')


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = ProfileImageSerializer(
            instance.profile_images.all(),
            many=True
        ).data 
        return rep


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = 'avatar',


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserProfile