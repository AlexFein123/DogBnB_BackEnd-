from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Reservation

class UserCreateSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(write_only=True)
    apellido = serializers.CharField(write_only=True)
    nombreUsuario = serializers.CharField(source="username")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "nombre", "apellido", "nombreUsuario", "password"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("El correo ya está registrado")
        return value

    def validate_nombreUsuario(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return value

    def create(self, validated_data):
        first_name = validated_data.pop("nombre")
        last_name = validated_data.pop("apellido")
        password = validated_data.pop("password")
        user: User = User(**validated_data)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        # perfil por defecto: rol tutor
        Profile.objects.create(user=user, roles=["tutor"], host_status="none", active_role="tutor")
        return user


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = ["email", "username", "roles", "host_status", "active_role"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "stay_slug", "check_in", "check_out", "created_at"]
        read_only_fields = ["id", "created_at"]