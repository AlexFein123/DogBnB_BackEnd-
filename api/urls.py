from django.urls import path
from .views import RegistrarUsuarioView

urlpatterns = [
    path("registrar", RegistrarUsuarioView.as_view(), name="api-registrar"),
]