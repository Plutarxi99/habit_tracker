from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        user = User(email=validated_data["email"], chat_id_tg=validated_data["chat_id_tg"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["email", "password", "chat_id_tg"]
        extra_kwargs = {"password": {"write_only": True}}
