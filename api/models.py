from django.db import models

# Create your models here.

class Usuario(models.Model): 
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)  # 'dueño' | 'anfitrion'
    descripcion = models.TextField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        managed = False  # ¡IMPORTANTE!