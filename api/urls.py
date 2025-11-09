from django.urls import path
from .views import RegistrarView, PerfilView, HacerHospedadorView 

urlpatterns = [
    path("registrar/", RegistrarView.as_view(), name="registrar"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
    path("hacer-hospedador/", HacerHospedadorView.as_view(), name="hacer_hospedador"),
]