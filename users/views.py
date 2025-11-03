from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import (
    UserCreateSerializer,
    ProfileSerializer,
    ReservationSerializer,
)
from .models import Profile, Reservation

class UsuarioCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "nombreUsuario": user.username,
                    "roles": user.profile.roles if hasattr(user, "profile") else ["tutor"],
                    "hostStatus": user.profile.host_status if hasattr(user, "profile") else "none",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response({"message": "Error al registrarse", "errors": serializer.errors}, status=400)


class MeView(APIView):
    def get(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        profile = user.profile
        data = {
            "id": user.id,
            "email": user.email,
            "nombreUsuario": user.username,
            "roles": profile.roles,
            "hostStatus": profile.host_status,
            "activeRole": profile.active_role,
        }
        return Response(data)


class ActivateHostView(APIView):
    def post(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        profile: Profile = user.profile
        if "host" not in profile.roles:
            profile.roles.append("host")
        profile.host_status = "active"
        profile.active_role = "host"
        profile.save(update_fields=["roles", "host_status", "active_role"])
        return Response({"roles": profile.roles, "hostStatus": profile.host_status})


class ReservationsView(APIView):
    def get(self, request):
        user_id = request.query_params.get("userId")
        if not user_id:
            return Response({"message": "userId requerido"}, status=400)
        user = get_object_or_404(User, pk=user_id)
        qs = Reservation.objects.filter(user=user)
        return Response(ReservationSerializer(qs, many=True).data)

    def post(self, request):
        user_id = request.data.get("userId")
        if not user_id:
            return Response({"message": "userId requerido"}, status=400)
        user = get_object_or_404(User, pk=user_id)
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            Reservation.objects.create(
                user=user,
                stay_slug=serializer.validated_data["stay_slug"],
                check_in=serializer.validated_data["check_in"],
                check_out=serializer.validated_data["check_out"],
            )
            return Response({"message": "Reserva creada"}, status=201)
        return Response(serializer.errors, status=400)