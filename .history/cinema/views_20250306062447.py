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
def inicio(request):
    return render(request, "inicio.html")

def password_changed(request):
    return render(request, "password_changed.html")


def puestos(request):
    return render(request, 'puestos.html')

def cartelera(request):
    peliculas = Pelicula.objects.all()
    return render(request, "cartelera.html", {"peliculas": peliculas})


from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Reserva, Pelicula, CarritoItem

@login_required
def reserva(request):
    peliculas = Pelicula.objects.all()

    if request.method == "POST":
        if 'nombre' in request.POST:
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            fecha = request.POST.get("fecha")
            hora = request.POST.get("hora")
            personas = request.POST.get("personas")
            pelicula_id = request.POST.get("peliculas")

            if nombre and email and fecha and hora and personas:
                try:

                    personas_int = int(personas)

                    reserva = Reserva.objects.create(
                        usuario=request.user,
                        fecha=datetime.strptime(fecha, "%Y-%m-%d").date(),
                        hora=datetime.strptime(hora, "%H:%M").time(),
                        personas=personas_int, 
                        estado="pendiente",
                    )

                    reserva.productos.set(Pelicula.objects.filter(id=pelicula_id))

                    CarritoItem.objects.create(
                        usuario=request.user if request.user.is_authenticated else None,
                        reserva=reserva,
                        cantidad=1,  
                        sesion_id=request.session.session_key if not request.user.is_authenticated else None
                    )
                    
                    messages.success(request, "Reserva creada y añadida al carrito con éxito")
                    return redirect('ver_carrito')
                except ValueError:
                    messages.error(request, "El número de personas debe ser un valor numérico válido")
                except Exception as e:
                    messages.error(request, f"Error al crear la reserva: {str(e)}")
        
        elif 'pelicula_id' in request.POST:
            pelicula_id = request.POST.get('pelicula_id')
            try:
                pelicula = Pelicula.objects.get(id=pelicula_id)
                messages.error(request, "Función no implementada correctamente")
            except Pelicula.DoesNotExist:
                messages.error(request, "Película no encontrada")
    
    return render(request, 'reserva.html', {'peliculas': peliculas})


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
    form_data = {}
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        form_data = {
            'username': username,
            'email': email
        }
        
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

    return render(request, "register.html", {'form': form_data})

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
from .models import Pelicula
import json




from .models import CarritoItem
def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)

    for item in carrito_items:
        total += item.subtotal()
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Item eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoItem, Orden, OrdenItem, Datos
from .forms import OrdenForm
def pasarela(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')
    
    for item in carrito_items:
        total += item.subtotal()
    
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            
            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key
            
            orden.total = total
            orden.save()
            
            for item in carrito_items:
                OrdenItem.objects.create(
                    orden=orden,
                    reserva=item.reserva,
                    precio=15000,  # Precio base por persona
                    cantidad=item.cantidad
                )
            
            carrito_items.delete()
            
            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmacion', orden_id=orden.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos = Datos.objects.get(usuario=request.user)
                initial_data = {
                    'nombre': f"{datos.nombre} {datos.apellido}",
                    'email': request.user.email,
                    'telefono': ''
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email,
                    'telefono': ''
                }
        
        form = OrdenForm(initial=initial_data)
    
    return render(request, 'pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })

def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        else:
            orden = Orden.objects.get(id=orden_id, sesion_id=request.session.session_key)
        
        items = OrdenItem.objects.filter(orden=orden)
        
        return render(request, 'confirmacion.html', {
            'orden': orden,
            'items': items
        })
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('cartelera')