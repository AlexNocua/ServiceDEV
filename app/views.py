import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms import UsuarioEditForm
from django.db.models import Q
from app.models import ModelDetalleVenta, ModelProductos, ModelUsuarios, ModelVentas
from app.utils.busquedas import devolver_productos, devolver_productos_pendientes
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from app.utils.utilidades import correo_nueva_compra, datos_usuario, convertir_imagen

# Create your views here.


###########################################################
# renderizacion de plantillas
def principal(request):
    context = datos_usuario(request)
    print(type(context))
    return render(request, "principal.html", context)


def compras(request):
    context = datos_usuario(request)
    productos_pendientes = devolver_productos_pendientes(request.user)

    if productos_pendientes:
        dic_productos = {}
        for i, producto in enumerate(productos_pendientes):
            dic_productos[f"producto_{i}"] = {
                "id": producto.id,
                "producto": producto.producto,
                "imagen": convertir_imagen(producto.producto.imagen),
            }

        context["productos_pendientes"] = dic_productos

        messages.success(
            request,
            f"Tienes {len(productos_pendientes)} productos pendientes de compra.",
        )
        return render(request, "compras.html", context)
    else:
        messages.info(request, "No tienes productos pendientes de compra.")

        return redirect("app:productos")


def conocenos(request):
    context = datos_usuario(request)
    return render(request, "conocenos.html", context)


def contacto(request):
    context = datos_usuario(request)
    return render(request, "contacto.html", context)


def productos(request):
    context = datos_usuario(request)
    productos = devolver_productos()
    dic_productos = {}
    if productos:
        dic_productos = {}
        for i, producto in enumerate(productos):
            dic_productos[f"producto_{i}"] = {
                "id_producto": producto.id,
                "nombre_producto": producto.nombre,
                "descripcion": producto.descripcion,
                "imagen_producto": convertir_imagen(producto.imagen),
                "precio": producto.precio,
                "cantidad": producto.cantidad,
            }

        context["productos"] = dic_productos
    else:
        pass
    return render(request, "productos.html", context)


def servicios(request):
    context = datos_usuario(request)
    return render(request, "servicios.html", context)


def nueva_venta(request):
    if request.method == "POST":
        productos = ModelDetalleVenta.objects.filter(
            Q(comprador=request.user) & Q(vendido=False)
        )
        str_productos = ""
        for producto in productos:
            producto.producto.cantidad -= 1
            str_productos += producto.producto.nombre + "-"
            producto.producto.save()

        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        direccion = request.POST.get("direccion")
        ciudad = request.POST.get("ciudad")
        departamento = request.POST.get("departamento")
        total = request.POST.get("valortotal")
        print(total, "--------------------------------")
        new_venta = ModelVentas.objects.create(
            comprador=request.user,
            monto_total=total,
            productos_vendidos=str_productos,
            fecha_venta=datetime.datetime.now(),
        )
        new_venta.save()
        correo_nueva_compra(
            nombre, correo, direccion, ciudad, departamento, total, str_productos
        )
        productos.update(vendido=True)

        messages.success(
            request,
            "La venta se ha procesado correctamente y los productos han sido marcados como vendidos.",
        )

        return redirect("app:productos")
    else:
        messages.warning(
            request, "No se ha enviado ningún dato para procesar la venta."
        )
        return redirect("app:productos")


###########################################################
# end_point Inicio de sesion y cierre
def iniciar_sesion(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")

        usuario = authenticate(request, correo=correo, password=password)

        if usuario is not None:

            login(request, usuario)
            messages.success(
                request, "¡Inicio de sesión exitoso! Bienvenido a tu cuenta."
            )
            return redirect("app:principal")
        else:
            messages.error(
                request,
                "Correo electrónico o contraseña incorrectos. Por favor, intenta nuevamente.",
            )
            return redirect("app:principal")

    return redirect("app:principal")


@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = UsuarioEditForm(request.POST, instance=request.user)

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")

        if form.is_valid():
            user = authenticate(username=request.user.correo, password=current_password)
            if user is not None:
                if new_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)

                form.save()
                messages.success(request, "¡Perfil actualizado con éxito!")
                return redirect("app:principal")

            else:
                messages.error(request, "La contraseña actual no es correcta.")
                return redirect("app:editar_perfil")

        else:
            messages.error(
                request, "Hubo un error al actualizar tu perfil. Intenta nuevamente."
            )
            return redirect("app:editar_perfil")

    else:
        form = UsuarioEditForm(instance=request.user)

    return redirect("app:editar_perfil")


@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "¡Has cerrado sesión con éxito! Esperamos verte pronto.")
    return redirect("app:principal")


###########################################################


###########################################################
# end_point crear usuario
def crear_usuario(request):
    from django.contrib.auth.hashers import make_password

    if request.method == "POST":
        nombre_completo = request.POST.get("nombre_completo")
        correo = request.POST.get("correo")
        password = request.POST.get("password")

        password_encriptada = make_password(password)

        nuevo_usuario = ModelUsuarios.objects.create(
            nombre_completo=nombre_completo, correo=correo, password=password_encriptada
        )
        nuevo_usuario.save()

        messages.success(request, "Usuario creado con éxito.")
        return redirect("app:principal")

    return render(request, "principal.html")


# ###########################################################
# end_point mensajes
def enviar_mensajes(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")
        servicios = request.POST.get("servicios")
        mensaje = request.POST.get("mensaje")

        from app.models import ModelMensajes

        nuevo_mensaje = ModelMensajes.objects.create(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            servicios=servicios,
            mensaje=mensaje,
        )
        nuevo_mensaje.save()
        messages.success(request, "Mensaje creado con éxito.")
        return redirect("app:contacto")

    else:
        messages.error(request, "Error.")
        return redirect("app:contacto")


###########################################################
def anadir_producto_carrito(request, id_producto, id_user):
    comprador = ModelUsuarios.objects.get(id=id_user)
    producto = ModelProductos.objects.get(id=id_producto)
    new_detalles_venta = ModelDetalleVenta.objects.create(
        comprador=comprador,
        producto=producto,
    )

    new_detalles_venta.save()
    messages.success(request, f"{producto.nombre} ha sido añadido a tu carrito.")

    return redirect("app:productos")


def eliminar_producto(request, id_producto):
    try:
        producto = ModelDetalleVenta.objects.get(id=id_producto)
        producto.delete()
        messages.success(request, "Producto eliminado del carrito exitosamente.")
    except ModelDetalleVenta.DoesNotExist:
        messages.error(request, "El producto no se encontró en el carrito.")
    return redirect("app:compras")


###########################################################
