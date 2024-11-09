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
    ##############################################################################
    #    end_points
    path("crear_usuario", views.crear_usuario, name="crear_usuario"),
    path("enviar_mensajes", views.enviar_mensajes, name="enviar_mensajes"),
    ##############################################################################
]
