from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class ModelUsuarios(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

class ModelMensajes(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    servicios = models.CharField(max_length=200, blank=True, null=True)
    mensaje = models.CharField(max_length=1000, blank=True, null=True)
