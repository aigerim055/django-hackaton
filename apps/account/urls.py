from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegistrationView,
    ActivationView
)


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registartion'),
    path('activate/', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
]