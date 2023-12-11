from rest_framework.generics import CreateAPIView

from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Для регистрации пользователя в приложении
    """
    serializer_class = UserSerializer
