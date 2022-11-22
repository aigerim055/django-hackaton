from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, mixins
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .serializers import (
    RegistrationSerializer,
    PhoneActivationSerializer,
    ChangePasswordSerializer,
    RestorePasswordSerializer,
    SetRestoredPasswordSerializer,
    )

User = get_user_model()

class RegistrationView(APIView):
    def post(self, request: Request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Thanks for registration! Activate your account', 
                status=status.HTTP_201_CREATED
            )


class ActivationView(APIView): # Phone Activation View
    def post(self, request: Request): # sms
        serilizer = PhoneActivationSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.activate_account()
            return Response(
                'Account activated. You can login now.',
                status=status.HTTP_200_OK
            )


# class 
    def get(self, request, activation_code): # email
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated. You can login now.',
            status=status.HTTP_200_OK
            )


class ActivationViewSet(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'phone':
            return ...
        if self.action == 'phone':
            return ...


    @action(detail=True, methods=['POST'])
    def activate_via_email(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated. You can login now.',
            status=status.HTTP_200_OK
            )



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password changed succesfully',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView):
    def post(self, request):  # sms
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code was sent to your phone',
                status=status.HTTP_200_OK
            )
 
    def post(self, request: Request):  # email
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code for restoring your password has been sent ot your email.',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):
    def post(self, request: Request): # sms
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'password restored successfuly',
                status=status.HTTP_200_OK
            )

    def post(self, request: Request): # email
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Your password has been restored.',
                status=status.HTTP_200_OK
            )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Your account has been deleted.',
            status=status.HTTP_204_NO_CONTENT
        )