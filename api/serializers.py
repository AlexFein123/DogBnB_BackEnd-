from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nombre', 'apellido', 'email', 'password', 'tipo', 'descripcion')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, v):
        if Usuario.objects.filter(email=v).exists():
            raise serializers.ValidationError("El email ya está registrado.")
        return v

    def create(self, validated_data):
        # bcrypt vía Django
        validated_data['password'] = make_password(validated_data['password'], hasher='bcrypt_sha256')
        return Usuario.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        pwd = attrs['password']
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")

        if not check_password(pwd, user.password):
            raise serializers.ValidationError("Credenciales inválidas")

        attrs['user'] = user
        return attrs
