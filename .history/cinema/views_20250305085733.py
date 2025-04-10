from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from datetime import datetime
import json

from .models import Pelicula, Perfil, Reserva, Producto, Carrito, ItemCarrito, DetallePedido
from .forms import PedidoForm

# Vistas generales
def home(request):
    return render(request, "home.html")

def inicio(request):
    return render(request, "inicio.html")

def peliculas(request):
    return render(request, "peliculas.html")

def peliculas_2(request):
    return render(request, "peliculas_2.html")

def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, "cartelera.html", {"peliculas": peliculas})

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

# Autenticación y usuarios
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
    user_profile, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, "perfil.html", {"user_profile": user_profile})

# Recuperación de contraseña
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

# Funcionalidad de reservas y carrito
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, _ = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    item.cantidad += 1
    item.save()
    return redirect('ver_carrito')

@login_required
def reserva(request):
    if request.method == "POST":
        cantidad_personas = int(request.POST['cantidad_personas'])
        Reserva.objects.create(usuario=request.user, cantidad_personas=cantidad_personas)
        return redirect('reserva_exitosa')
    return render(request, 'hacer_reserva.html')
