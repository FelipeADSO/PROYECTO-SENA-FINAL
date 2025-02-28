from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Pelicula, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def home(request):
    return render(request, 'home.html')

def password_changed(request):
    return render(request, "password_changed.html")


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
                return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session["bienvenida"] = f"¡Bienvenido, {user.username}!"
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

def restablecer(request):
    if request.method == "POST":
        email = request.POST["email"]
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
            return redirect("restablecer")  # Redirige de nuevo a la página de restablecimiento

    return render(request, "restablecer.html")

def cambiar_contraseña(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contraseña = request.POST["password"]
            user.set_password(nueva_contraseña)
            user.save()
            return redirect("password_changed")

        return render(request, "cambiar_contraseña.html")  # Página para cambiar contraseña

    return redirect("login")  # Si el enlace es inválido, redirige al login
