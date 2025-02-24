from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, UserProfileView, UpdateProfileView, ChangePasswordView,
    PasswordResetView, LogoutView, CustomTokenObtainPairView
)

urlpatterns = [
    path('auth/', include([
        path('register/', RegisterView.as_view(), name='auth_register'),
        path('token/', CustomTokenObtainPairView.as_view(), name='auth_token'),
        path('token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
        path('logout/', LogoutView.as_view(), name='auth_logout'),
        path('password/reset/', PasswordResetView.as_view(), name='auth_password_reset'),
    ])),
    path('profile/', include([
        path('', UserProfileView.as_view(), name='profile'),
        path('update/', UpdateProfileView.as_view(), name='profile_update'),
        path('password/change/', ChangePasswordView.as_view(), name='profile_password_change'),
    ])),
]
