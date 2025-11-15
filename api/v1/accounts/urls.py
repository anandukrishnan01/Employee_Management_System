from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenBlacklistView,)
from .views import SignupView
from api.v1.accounts.views import CustomTokenRefreshView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignupView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
