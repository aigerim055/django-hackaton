from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)

from .serializers import (
    UserProfileSerializer,
    UserProfileListSerializer,
    UserProfile,
    UserProfileCreateSerializer,
)
from .permissions import IsOwner

class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            self.permission_classes = [IsOwner, IsAdminUser]
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()