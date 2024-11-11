from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    ##############################################################################
    # vistas
    path("", views.principal, name="principal"),
    path("conocenos", views.conocenos, name="conocenos"),
    path("servicios", views.servicios, name="servicios"),
    path("contacto", views.contacto, name="contacto"),
    path("productos", views.productos, name="productos"),
    path("compras", views.compras, name="compras"),
    ##############################################################################
    #    end_points
    path("iniciar_sesion", views.iniciar_sesion, name="iniciar_sesion"),
    path("editar_perfil", views.editar_perfil, name="editar_perfil"),
    path("cerrar_sesion", views.cerrar_sesion, name="cerrar_sesion"),
    path("crear_usuario", views.crear_usuario, name="crear_usuario"),
    path("enviarnueva_venta_mensajes", views.enviar_mensajes, name="enviar_mensajes"),
    path("nueva_venta", views.nueva_venta, name="nueva_venta"),
    path(
        "anadir_producto_carrito/<int:id_producto>/<int:id_user>",
        views.anadir_producto_carrito,
        name="anadir_producto_carrito",
    ),
    path(
        "eliminar_producto/<int:id_producto>",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    ##############################################################################
]
