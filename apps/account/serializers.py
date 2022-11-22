from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .tasks import send_activation_sms, send_activation_email
from .utils import normalize_phone


User = get_user_model()


def email_validator(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with such email is not found.'
            )
        return email


class RegistrationSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password_confirm')

    def validate_phone(self, phone):
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format!')
        return phone

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data): # sms
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_sms(user.phone, user.activation_code)
        return user

    def create(self, validated_data):  # email
        user = User.objects.create_user(**validated_data)
        user.create_activation_email()
        send_activation_email.delay(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True)
    code = serializers.CharField(max_length=10, required=True)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('No user found with this phone number')
        return phone

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Invalid activation code')

    def activate_account(self): # sms
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.is_active = True
        user.activation_code = ''
        user.save()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=150, required=True)
    new_password = serializers.CharField(max_length=150, required=True)
    new_password_confirm = serializers.CharField(max_length=150, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('wrong password!'.upper())
        return old_password

    def validate(self, attrs: dict):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'password do not match'
            )
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class RestorePasswordSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=13, required=True)

    def send_code(self): # sms
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone) 
        user.create_activation_code()
        send_activation_sms(user.phone, user.activation_code)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        return phone

    def send_code(self): # email
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Password restoration',
            message=f'Your code for password restoration {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )


class SetRestoredPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True)
    code = serializers.CharField(min_length=1, max_length=10, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_password_confirm = serializers.CharField(max_length=128, required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError(
                'wrong code'
            )
        return code 

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'passwords code do not match'
            )
        return attrs

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        return phone

    def set_new_password(self): # sms
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()

    def set_new_password(self): # email
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()