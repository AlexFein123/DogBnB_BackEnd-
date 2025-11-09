from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name  = serializers.CharField(max_length=150)
    username   = serializers.CharField(max_length=150)
    email      = serializers.EmailField()
    password   = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, v):
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe.")
        return v

    def validate_email(self, v):
        if User.objects.filter(email=v).exists():
            raise serializers.ValidationError("Ese email ya está registrado.")
        return v

    def create(self, validated_data):
        user = User.objects.create_user(
            username   = validated_data["username"],
            email      = validated_data["email"],
            password   = validated_data["password"],   # -> Django la hashea
            first_name = validated_data["first_name"],
            last_name  = validated_data["last_name"],
        )
        # perfil asociado
        Usuario.objects.create(user=user, es_hospedador=False)

        # emitir tokens
        refresh = RefreshToken.for_user(user)
        return {
            "user_id": user.id,
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }