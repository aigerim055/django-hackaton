from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegistrationSerializer,
    ActivationSerializer,
    ChangePasswordSerializer,
     RestorePasswordSerializer,
     SetRestoredPasswordSerializer,
    )



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
        serilizer = ActivationSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.activate_account()
            return Response(
                'Аккаунт активирован!',
                status=status.HTTP_200_OK
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'password changed seccesfully!',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView):
    def post(self, request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'code was sent to your phone',
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