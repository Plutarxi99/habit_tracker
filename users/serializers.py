from rest_framework.serializers import ModelSerializer
# from rest_framework.authtoken.models import Token

from users.models import User


class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        # user = User(email=validated_data["email"], is_active=False)
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        # token = Token.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
