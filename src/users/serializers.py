from django.conf import settings

import jwt
from rest_framework import serializers

from users.models import User


class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "token",
            "password",
        )

    def is_valid(self, raise_exception=False):
        is_valid = super(ResetPasswordSerializer, self).is_valid(raise_exception)

        token = self.validated_data.get("token")
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]

        try:
            decoded = jwt.decode(token, secret, algorithm)
            email = decoded.get("email")
            user = User.objects.get(email=email)
            self.instance = user
        except (User.DoesNotExist, jwt.InvalidTokenError):
            is_valid = False
            if raise_exception:
                raise serializers.ValidationError("Token inválido")

        return is_valid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = (
            "username",
            "is_superuser",
            "date_joined",
        )
        exclude = (
            "id",
            "groups",
            "password",
            "is_staff",
            "is_active",
            "last_login",
            "user_permissions",
        )
