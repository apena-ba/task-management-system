from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

User = get_user_model()


def custom_password_validator(password, user):
    """
    Makes sure passwords contain:
    - 1 uppercase
    - 1 lowercase
    - 1 digit
    - 1 special character
    - no username in the password
    """
    if not re.search(r"[A-Z]", password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise serializers.ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise serializers.ValidationError("Password must contain at least one special character.")
    if user and user.username.lower() in password.lower():
        raise serializers.ValidationError("Password cannot contain your username.")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "team")
        read_only_fields = ("id",)

    def validate_password(self, value):
        # Temp user instance
        user = User(
            username=self.initial_data.get("username"),
            email=self.initial_data.get("email")
        )
        
        # Django validators + Custom validators
        validate_password(password=value, user=user)
        custom_password_validator(password=value, user=user)

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extends JWT login response to include user info"""
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data
