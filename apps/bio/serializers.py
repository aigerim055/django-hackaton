from rest_framework import serializers

from .models import (
    UserProfile, 
    ProfileImage
)

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
    avatar = serializers.ImageField()   #######
    birthday = serializers.DateField()                         # settings include format   # формат как проверяется, выпдает ли календарь
    phone = serializers.CharField(max_length=14) 
 

    def create(self, validated_data):
        avatar_carousel = validated_data.pop('avatar_carousel')
        profile = UserProfile.objects.create(**validated_data)
        images = []
        for image in avatar_carousel:
            images.append(ProfileImage(profile=profile, avatar=image))
        ProfileImage.objects.bulk_create(images)
        return profile

    
      

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

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['avatar'] = ProfileImageSerializer(
    #         instance.profile_images.all()
    #     ).data 
    #     return rep

    


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = 'avatar',