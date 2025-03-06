from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from .models import Pelicula, Reserva, Pedido, ItemCarrito, Carrito, Producto
from django.contrib import messages


# Vista para la lista de películas
def lista_peliculas(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'peliculas/lista_peliculas.html', {'peliculas': peliculas})


# Vista para el detalle de una película
def detalle_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    return render(request, 'peliculas/detalle_pelicula.html', {'pelicula': pelicula})


# Vista para hacer una reserva
@login_required
def reserva(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    
    if request.method == 'POST':
        personas = int(request.POST.get('personas', 1))
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        reserva = Reserva.objects.create(
            usuario=request.user,
            personas=personas,
            fecha=fecha,
            hora=hora,
            estado='pendiente'
        )

        messages.success(request, 'Reserva creada exitosamente.')
        return redirect('detalle_pelicula', pelicula_id=pelicula.id)

    return render(request, 'reservas/crear_reserva.html', {'pelicula': pelicula})


# Vista para listar reservas de un usuario
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'reservas/lista_reservas.html', {'reservas': reservas})


# Vista para el carrito de compras
@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito})


# Agregar producto al carrito
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    item.cantidad += 1
    item.save()

    return JsonResponse({'mensaje': 'Producto agregado al carrito'})


# Eliminar producto del carrito
@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if item.carrito.usuario == request.user:
        item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')


# Vista para procesar el pedido
@login_required
def procesar_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    if not carrito.items.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('ver_carrito')

    pedido = Pedido.objects.create(
        nombre=request.user.username,
        correo=request.user.email,
        telefono=request.user.perfil.phone if hasattr(request.user, 'perfil') else '',
        total=carrito.total(),
        estado='pendiente'
    )

    for item in carrito.items.all():
        pedido.detalles.create(
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio,
            subtotal=item.subtotal()
        )

    carrito.items.all().delete()  # Vaciar el carrito tras la compra
    messages.success(request, "Pedido realizado con éxito.")
    return redirect('lista_pedidos')


# Vista para listar pedidos del usuario
@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(correo=request.user.email)
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})
