from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from .models import Pelicula, Perfil, Reserva  # Asegúrate de que Reserva esté bien definida

def home(request):
    return render(request, "home.html")

def password_changed(request):
    return render(request, "password_changed.html")

def inicio(request):
    return render(request, "inicio.html")

def puestos(request):
    return render(request, 'puestos.html')

def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, "cartelera.html", {"peliculas": peliculas})

def pasarela(request):
    return render(request, 'pasarela.html')

from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Reserva, Pelicula


def reserva(request):
    peliculas = Pelicula.objects.all()  # Obtener todas las películas para mostrar en el formulario

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        personas = request.POST.get("personas")
        pelicula_id = request.POST.getlist("peliculas")  # Puede ser una lista de películas

        if nombre and email and fecha and hora and personas:
            try:
                reserva = Reserva.objects.create(
                    usuario=request.user,  # Asignamos el usuario autenticado
                    fecha=datetime.strptime(fecha, "%Y-%m-%d").date(),
                    hora=datetime.strptime(hora, "%H:%M").time(),
                    personas=int(personas),
                    estado="pendiente",
                )
                reserva.productos.set(Pelicula.objects.filter(id__in=pelicula_id))  # Asignamos las películas seleccionadas

                messages.success(request, "Reserva realizada con éxito.")
                return redirect("reserva")
            except Exception as e:
                messages.error(request, f"Error al crear la reserva: {str(e)}")
        else:
            messages.error(request, "Todos los campos son obligatorios.")

    return render(request, "reserva.html", {"peliculas": peliculas})


def peliculas(request):
    return render(request, "peliculas.html")

def peliculas_2(request):
    return render(request, "peliculas_2.html")

def contactenos(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje = request.POST.get("mensaje")

        if nombre and email and mensaje:
            mensaje_completo = f"Nombre: {nombre}\nCorreo: {email}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}"
            send_mail(
                subject="Nuevo mensaje de contacto",
                message=mensaje_completo,
                from_email="andrescediel070625@gmail.com",
                recipient_list=["andrescediel070625@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
            return redirect("contactenos")
        else:
            messages.error(request, "Todos los campos son obligatorios.")
    
    return render(request, "contactenos.html")

def somos(request):
    return render(request, "somos.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
        elif password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido.")
            return redirect("login")

    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("inicio")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")


def perfil(request):
    user_profile, created = Perfil.objects.get_or_create(user=request.user)
    return render(request, "perfil.html", {"user_profile": user_profile})


def user_info(request):
    user_profile, created = Perfil.objects.get_or_create(user=request.user)
    
    data = {
        "username": request.user.username,
        "email": request.user.email,
        "date_joined": request.user.date_joined.strftime("%d/%m/%Y"),
        "phone": user_profile.phone if user_profile.phone else "No registrado",
        "profile_picture": user_profile.profile_picture.url if user_profile.profile_picture else "/static/imagenes/perfil.jpg"
    }
    
    return JsonResponse(data)

def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/cambiar_contraseña/{uid}/{token}/")

            send_mail(
                "Restablecimiento de contraseña",
                f"Haz clic en el siguiente enlace para cambiar tu contraseña: {enlace}",
                "jalmpa77@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Se ha enviado un enlace de restablecimiento a su correo.")
            return redirect("home")
        else:
            messages.error(request, "No se encontró un usuario con ese correo electrónico.")
    
    return render(request, "restablecer.html")

def cambiar_contraseña(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contraseña = request.POST.get("password")
            if nueva_contraseña:
                user.set_password(nueva_contraseña)
                user.save()
                messages.success(request, "Contraseña cambiada con éxito.")
                return redirect("password_changed")
            else:
                messages.error(request, "La nueva contraseña no puede estar vacía.")

        return render(request, "cambiar_contraseña.html")

    messages.error(request, "El enlace de restablecimiento es inválido o ha expirado.")
    return redirect("login")

from django.shortcuts import render, redirect
from django.http import JsonResponse

def procesar_reserva(request):
    if request.method == 'POST':
        asientos = request.POST.get('asientos_seleccionados')
        # Aquí procesas los asientos seleccionados y los guardas en la base de datos
        return JsonResponse({'mensaje': 'Reserva procesada con éxito'})

    return redirect('pasarela') 



from django.http import JsonResponse
from django.core.cache import cache
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import  DetallePedido, Pelicula
from .forms import PedidoForm
import json

def finalizar_compra(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

    transaction_token = request.POST.get('transaction_token')
    cache_key = f'order_token_{transaction_token}'
    
    if cache.get(cache_key):
        return JsonResponse({'success': True, 'message': 'Reserva ya procesada'})
    
    cache.set(cache_key, True, 30)
    form = PedidoForm(request.POST, request.FILES)
    
    if not form.is_valid():
        cache.delete(cache_key)
        return JsonResponse({'success': False, 'errors': form.errors})
    
    pedido = form.save(commit=False)
    pedido.total = request.POST.get('total', 0)
    
    if 'comprobante' in request.FILES:
        pedido.comprobante = request.FILES['comprobante']
    
    pedido.save()
    items = json.loads(request.POST.get('items', '[]'))
    detalles_correo = []
    html_items = ""
    
    for item in items:
        pelicula_id = item.get('id')
        cantidad = item.get('cantidad', 1)
        precio = item.get('precio', 0)
        subtotal = item.get('subtotal', 0)
        
        pelicula = Pelicula.objects.get(id=pelicula_id)
        DetallePedido.objects.create(
            pedido=pedido,
            pelicula=pelicula,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=subtotal
        )
        
        detalle = f"Película: {pelicula.nombre}, Cantidad: {cantidad}, Precio: ${precio}."
        
        detalles_correo.append(detalle)
        html_items += f'<li>{detalle}</li>'
    
    asunto = "Confirmación de Reserva - Cinema Los Andes"
    destinatario = pedido.correo
    mensaje = f"""
    Hola {pedido.nombre},
    ¡Gracias por tu reserva en Cinema Los Andes!
    
    Detalles de tu reserva:
    {''.join([f'\n- {detalle}' for detalle in detalles_correo])}
    
    Total: ${pedido.total}
    Tu reserva será procesada a la brevedad.
    
    Saludos,
    El equipo de Cinema Los Andes
    """
    
    html_content = render_to_string('email_confirmacion.html', {
        'pedido': pedido,
        'html_items': html_items
    })
    
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        asunto,
        text_content,
        settings.EMAIL_HOST_USER,
        [destinatario, 'andrescediel070625@gmail.com']
    )
    email.attach_alternative(html_content, "text/html")
    
    if hasattr(pedido, 'comprobante') and pedido.comprobante:
        email.attach_file(pedido.comprobante.path)
    
    email.send()
    cache.set(cache_key, True, 60 * 30)
    
    return JsonResponse({'success': True, 'message': 'Reserva creada correctamente y confirmación enviada por correo'})



