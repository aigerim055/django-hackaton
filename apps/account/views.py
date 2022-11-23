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


class ActivationView(APIView):
    def post(self, request: Request): 
        serilizer = PhoneActivationSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.activate_account()
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
    def post(self, request):  
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code was sent to your phone',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):  
    def post(self, request: Request): 
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'password restored successfuly',
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