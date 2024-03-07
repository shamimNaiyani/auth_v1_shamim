from django.urls import path
from .views import (
    UserRegisterView, 
    VerifyUserEmailView, 
    UserLoginView, 
    UserLogoutApiView,
    PasswordResetRequestApiView,
    PasswordResetConfirmApiView,
    SetNewPasswordApiView,
    UserProfile,
)
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('verify-email/', VerifyUserEmailView.as_view(), name="verify-email"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', TokenBlacklistView.as_view(), name="logout"),
    path('password-reset/', PasswordResetRequestApiView.as_view(), name="password-reset"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmApiView.as_view(), name="password-reset-confirm"),
    path('set-new-password/', SetNewPasswordApiView.as_view(), name="set-new-password"),
    path("profile/", UserProfile.as_view(), name="profile"),
]
