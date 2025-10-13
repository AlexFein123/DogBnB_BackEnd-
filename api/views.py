from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            user = s.save()
            return Response({"id": user.id, "email": user.email, "nombre": user.nombre, "apellido": user.apellido}, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        s = LoginSerializer(data=request.data)
        if s.is_valid():
            user = s.validated_data['user']
            # Por ahora devolvemos un "token" simple de ejemplo.
            # En producción: usar JWT (djangorestframework-simplejwt).
            return Response({"ok": True, "user": {"id": user.id, "email": user.email, "nombre": user.nombre, "apellido": user.apellido}})
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)