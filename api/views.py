from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, views
from .serializers import RegistroSerializer

class RegistrarUsuarioView(views.APIView):
    authentication_classes = []  # registro público
    permission_classes = []      # (tenés AllowAny por defecto)

    def post(self, request):
        s = RegistroSerializer(data=request.data)
        if s.is_valid():
            user = s.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "es_hospedador": user.perfil.es_hospedador,  # related_name="perfil"
            }, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)