import base64
from app.forms import UsuarioEditForm
from app.models import ModelUsuarios

from django.contrib.auth.decorators import login_required

from app.utils.busquedas import devolver_productos_pendientes



def convertir_imagen(imagen):
    print(type(imagen))
    imagen_codificada = imagen
    imagen_decodificada = (
        base64.b64encode(imagen_codificada).decode("utf-8")
        if imagen_codificada
        else None
    )
    return imagen_decodificada

def datos_usuario(request):
    if request.user.is_authenticated:
        usuario = (
            ModelUsuarios.objects.get(correo=request.user.correo)
            if ModelUsuarios.objects.filter(correo=request.user.correo)
            else None
        )
        datos = {
            'num_productos':devolver_productos_pendientes(usuario).count(),
            "id_user":usuario.id,
            "form": UsuarioEditForm,
            "nombre_completo": usuario.nombre_completo,
            "correo": usuario.correo,
        }
        print(request.user.nombre_completo)
        print(request.user.correo)
        return datos
    else:
        return {}
    
def correo_nueva_compra(nombre,correo,direccion,ciudad,departamento,total, str_productos):
    import os
    import resend

    resend.api_key = "re_QWSwNWba_9XkDEE4UBzVvaCDr8VMvG3fU"

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["nocua68@gmail.com"],
        "subject": f"Nueva solicitud de compra SERVICEDEV por el usuario {nombre}",
        "html": f"""
      
<html lang="es">
  <head>
    <meta charset="UTF-8">
  </head>
  <body style="font-family: Arial, sans-serif; background-color: #f8fafc; color: #1e293b; line-height: 1.6; margin: 0; padding: 40px 20px;">
     <div class="geometric-shapes" style="position: absolute; top: 20px; right: 20px; z-index: -1;">
        <div class="wave" style="width: 180px; height: 20px; background-color: #1d4ed8; position: absolute; bottom: -20px; left: 10px; border-radius: 10px;"></div>
        <div class="circle circle-2" style="width: 120px; height: 120px; background-color: #93c5fd; border-radius: 50%; position: absolute; top: -80px; left: -30px;"></div>
        <div class="circle circle-1" style="width: 100px; height: 100px; background-color: #2563eb; border-radius: 50%; position: absolute; top: -50px; left: -50px;"></div>
      </div>
    <div style="max-width: 800px; margin: 20px auto; background-color: white; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); position: relative;">
      <div style="position: relative; border-bottom: 2px solid #2563eb; padding-bottom: 20px; margin-bottom: 30px;">
        <div style="color: #2563eb; font-size: 1.8em; font-weight: bold; margin-bottom: 15px; padding-left: 15px;">Detalles de Compra Solicitados - {str_productos}</div>
      </div>
      <p>Estimado/a Asesor de Compras,</p>
      <p>Has recibido una solicitud para coordinar una compra a través de ServiceDEV. A continuación, encontrarás los detalles proporcionados por el comprador sobre el producto de su interés:</p>

      <div style="color: #1d4ed8; font-weight: bold; margin-top: 25px; margin-bottom: 15px; font-size: 1.2em; display: flex; align-items: center;">
        Detalles del Producto/s
      </div>
      <div style="background: linear-gradient(135deg, #f8fafc 0%, white 100%); padding: 20px; border-radius: 12px; margin: 15px 0; border: 1px solid rgba(37, 99, 235, 0.1); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);">
        <ul style="list-style-type: none; padding-left: 0;">
          <li style="margin-bottom: 12px; padding-left: 25px; position: relative;">
            <strong>Productos:</strong>  {str_productos}
          </li>
        </ul>
      </div>

      <div style="color: #1d4ed8; font-weight: bold; margin-top: 25px; margin-bottom: 15px; font-size: 1.2em; display: flex; align-items: center;">
        Información del Comprador
      </div>
      <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 12px; padding-left: 25px; position: relative;">
          <strong>Nombre completo:</strong> {nombre}
        </li>
        <li style="margin-bottom: 12px; padding-left: 25px; position: relative;">
          <strong>Correo electrónico:</strong> {correo}
        </li>
        <li style="margin-bottom: 12px; padding-left: 25px; position: relative;">
          <strong>Ubicación:</strong>
          </br>
          {direccion}-{ciudad}-{departamento}
        </li>
         <li style="margin-bottom: 12px; padding-left: 25px; position: relative;">
          <strong>Total a pagar:</strong>{total}
        
          
        </li>
      </ul>

      <p>Por favor, revisa la información y contáctate con el comprador para coordinar la compra, confirmando precios, disponibilidad, y métodos de pago. Recuerda también proporcionar detalles sobre tiempos de entrega, garantías, y cualquier otra documentación relevante.</p>
    </div>
     <div class="geometric-shapes" style="position: absolute; top: 20px; right: 20px; z-index: -1;">
        <div class="circle circle-1" style="width: 100px; height: 100px; background-color: #2563eb; border-radius: 50%; position: absolute; top: -50px; left: -50px;"></div>
        <div class="circle circle-2" style="width: 120px; height: 120px; background-color: #93c5fd; border-radius: 50%; position: absolute; top: -80px; left: -30px;"></div>
        <div class="wave" style="width: 180px; height: 20px; background-color: #1d4ed8; position: absolute; bottom: -20px; left: 10px; border-radius: 10px;"></div>
      </div>
  </body>
</html>
    
        """,
    }

    email = resend.Emails.send(params)
    print(email)

