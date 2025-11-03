from django.urls import path
from .views import UsuarioCreateView, MeView, ActivateHostView, ReservationsView

urlpatterns = [
    path("usuarios", UsuarioCreateView.as_view(), name="usuarios-create"),
    path("usuarios/<int:user_id>", MeView.as_view(), name="usuarios-me"),
    path("usuarios/<int:user_id>/activar-host", ActivateHostView.as_view(), name="activar-host"),
    path("reservas", ReservationsView.as_view(), name="reservas"),
]