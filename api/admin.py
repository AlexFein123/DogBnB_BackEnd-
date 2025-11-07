from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "es_hospedador")
    list_filter = ("es_hospedador",)
    search_fields = ("user__username", "user__email")
