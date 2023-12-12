from users.apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from django.urls import path


from users.views import UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    # token_
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
]
