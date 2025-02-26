from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Pelicula, Perfil

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'inicio.html')

def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'cartelera.html', {'peliculas': peliculas})

def peliculas(request):
    return render(request, 'peliculas.html')

def peliculas_2(request):
    return render(request, 'peliculas_2.html')

def contactenos(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje = request.POST.get("mensaje")

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

    return render(request, "contactenos.html")

def somos(request):
    return render(request, 'somos.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "¡Registro exitoso! Te has registrado.")
                return redirect('inicio')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("inicio")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")

@login_required
def perfil(request):
    user_profile, created = Perfil.objects.get_or_create(user=request.user)
    return render(request, "perfil.html", {"user_profile": user_profile, "user": request.user})

@login_required
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
