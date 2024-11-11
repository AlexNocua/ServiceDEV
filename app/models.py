from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import CASCADE
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import authenticate, login


class CustomUserManager(BaseUserManager):
    def create_user(self, correo, nombre_completo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")
        correo = self.normalize_email(correo)
        user = self.model(
            correo=correo, nombre_completo=nombre_completo, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre_completo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(correo, nombre_completo, password, **extra_fields)


class ModelUsuarios(AbstractBaseUser, PermissionsMixin):
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre_completo"]

    def __str__(self):
        return self.correo


class ModelMensajes(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    servicios = models.CharField(max_length=200, blank=True, null=True)
    mensaje = models.CharField(max_length=1000, blank=True, null=True)


class ModelProductos(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    descripcion = models.CharField(max_length=1000, blank=True)
    imagen = models.BinaryField(blank=True, null=True)
    precio = models.FloatField(null=False)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class ModelDetalleVenta(models.Model):
    comprador = models.ForeignKey(
        ModelUsuarios, on_delete=CASCADE, related_name="detalles_producto"
    )
    producto = models.ForeignKey(
        ModelProductos, on_delete=CASCADE, related_name="detalles_producto"
    )
    subtotal = models.FloatField(default=0.0)
    vendido = models.BooleanField(default=False)

    def __str__(self):
        return f"Detalle venta {self.id} - Producto {self.producto.nombre}"


class ModelVentas(models.Model):
    comprador = models.ForeignKey(
        ModelUsuarios, on_delete=CASCADE, related_name="ventas"
    )
    productos_vendidos = models.CharField(max_length=100, blank=True, null=True)
    monto_total = models.CharField(max_length=50)
    fecha_venta = models.DateTimeField()

    def __str__(self):
        return f"Venta {self.id} - {self.comprador.nombre_completo}"
