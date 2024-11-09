from django.contrib import messages
from django.shortcuts import render, redirect

from app.models import ModelUsuarios

# Create your views here.


###########################################################
# renderizacion de plantillas
def principal(request):
    return render(request, "principal.html")


def conocenos(request):
    return render(request, "conocenos.html")


def contacto(request):
    return render(request, "contacto.html")


def productos(request):
    return render(request, "productos.html")


def servicios(request):
    return render(request, "servicios.html")


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
