from .models import CustomUser
from rest_framework import serializers

from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        account = CustomUser(
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Password": "Passwords are not equal"})
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "id"]


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
        ]
