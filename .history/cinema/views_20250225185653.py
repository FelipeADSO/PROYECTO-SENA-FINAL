from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.
 
def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'inicio.html')

# def cartelera(request):
#     return render(request, 'cartelera.html')
def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'cartelera.html', {'peliculas': peliculas})

def peliculas(request):
    return render(request, 'peliculas.html', )

def peliculas_2(request):
    return render(request, 'peliculas_2.html')

def contactenos(request):
    return render(request, 'contactenos.html')

def somos(request):
    return render(request, 'somos.html')

# def estrenos(request):
#     return render(request, 'estrenos.html')

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
                return redirect('login')  # Redirige a la página principal o dashboard

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Usa auth_login en lugar de login para evitar conflictos
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("inicio")  # Reemplaza "home" con la URL de tu página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")
