from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import base64
from django.utils.html import format_html
from .forms import ModelProductosForm
from .models import (
    ModelUsuarios,
    ModelMensajes,
    ModelProductos,
    ModelVentas,
    ModelDetalleVenta,
)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = ModelUsuarios
        fields = "__all__"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return password
        return self.instance.password


@admin.register(ModelUsuarios)
class ModelUsuariosAdmin(UserAdmin):
    ordering = ["correo"]
    form = CustomUserChangeForm
    model = ModelUsuarios

    list_display = ("nombre_completo", "correo", "is_active", "is_staff")
    search_fields = ("nombre_completo", "correo")

    fieldsets = (
        (None, {"fields": ("nombre_completo", "correo", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("nombre_completo", "correo", "password1", "password2"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if "password" in form.cleaned_data:
            password = form.cleaned_data["password"]
            if password:
                obj.set_password(password)
        obj.save()


@admin.register(ModelMensajes)
class ModelMensajesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "correo", "servicios")
    search_fields = ("nombre", "correo", "servicios")
    list_filter = ("servicios",)


@admin.register(ModelProductos)
class ModelProductosAdmin(admin.ModelAdmin):
    form = ModelProductosForm
    list_display = ("nombre", "descripcion", "precio", "cantidad", "mostrar_imagen")
    search_fields = ("nombre", "descripcion")
    list_filter = ("precio",)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            imagen_64 = base64.b64encode(obj.imagen).decode("utf-8")
            return format_html(
                '<img src="data:image/jpeg;base64,{0}" width="50" height="50" />',
                imagen_64,
            )
        return "No hay imagen"

    mostrar_imagen.short_description = "Imagen"

    def save_model(self, request, obj, form, change):
        imagen_file = form.cleaned_data.get("imagen")
        if imagen_file:
            obj.imagen = imagen_file.read()
        super().save_model(request, obj, form, change)


@admin.register(ModelVentas)
class ModelVentasAdmin(admin.ModelAdmin):
    list_display = ("comprador", "productos_vendidos", "monto_total", "fecha_venta")
    search_fields = ("comprador__nombre_completo",)
    list_filter = ("fecha_venta",)


@admin.register(ModelDetalleVenta)
class ModelDetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("comprador", "producto",  "subtotal", "vendido")
    list_filter = ("vendido",)
