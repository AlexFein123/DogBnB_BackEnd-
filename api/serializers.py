from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Usuario

class RegistroSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name  = serializers.CharField(max_length=150)
    username   = serializers.CharField(max_length=150)
    email      = serializers.EmailField()
    password   = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, v):
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError("Ese nombre de usuario ya existe.")
        return v

    def validate_email(self, v):
        if User.objects.filter(email=v).exists():
            raise serializers.ValidationError("Ese email ya está registrado.")
        return v

    def create(self, validated):
        user = User.objects.create_user(
            username   = validated["username"],
            email      = validated["email"],
            password   = validated["password"],     # ← Django la hashea con bcrypt
            first_name = validated["first_name"],
            last_name  = validated["last_name"],
        )
        Usuario.objects.create(user=user, es_hospedador=False)
        return user