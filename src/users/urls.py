from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from .views import UserCreate, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user_create'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
