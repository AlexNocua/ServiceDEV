import base64
from app.models import *
from django.db.models import Q


def devolver_productos():
    productos = ModelProductos.objects.all()
    if productos:
        return productos
    else:
        return None


def devolver_productos_pendientes(comprador):
    productos = ModelDetalleVenta.objects.filter(Q(comprador=comprador) & Q(vendido=False))
    return productos

