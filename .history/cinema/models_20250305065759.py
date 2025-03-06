# Create your models here.

from django.contrib.auth.models import User
from django.db import models
import re

class Pelicula(models.Model):
    CATEGORIAS = [
        ('Romance y Drama', 'Romance y Drama'),
        ('Ciencia ficción y fantasía', 'Ciencia ficción y fantasía'),
        ('Acción', 'Acción'),
        ('Comedia', 'Comedia'),
        ('Terror', 'Terror'),
        ('Documentales', 'Documentales'),
    ]
    
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    trailer_url = models.URLField(help_text="URL de YouTube (se convertirá automáticamente a formato embed)")
    imagen = models.ImageField(upload_to='peliculas/')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    calificacion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fecha_estreno = models.DateField(null=True, blank=True)
    horario = models.CharField(max_length=255, null=True, blank=True)  # Permite valores nulos y vacíos

    
    def save(self, *args, **kwargs):
        # Convertir URL de YouTube a formato embed si es necesario
        if 'youtube.com/watch?v=' in self.trailer_url:
            video_id = self.trailer_url.split('v=')[1].split('&')[0] if '&' in self.trailer_url.split('v=')[1] else self.trailer_url.split('v=')[1]
            self.trailer_url = f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.trailer_url:
            video_id = self.trailer_url.split('youtu.be/')[1]
            self.trailer_url = f'https://www.youtube.com/embed/{video_id}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"

from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Reserva(models.Model):
     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
     fecha = models.DateField()
     hora = models.TimeField()
     personas = models.IntegerField()
     productos = models.ManyToManyField(Pelicula, blank=True)
     estado = models.CharField(max_length=20, choices=[
         ('pendiente', 'Pendiente'),
         ('confirmada', 'Confirmada'),
         ('cancelada', 'Cancelada')
     ], default='pendiente')
    mensaje = models.TextField(blank=True, null=True)fecha_creacion = models.DateTimeField(auto_now_add=True)

class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    estado = models.CharField(max_length=20, default='pendiente', 
                             choices=[('pendiente', 'Pendiente'), 
                                     ('completado', 'Completado'), 
                                     ('cancelado', 'Cancelado')])

    def _str_(self):
        return f"Pedido de {self.nombre} - {self.fecha_compra}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    def _str_(self):
        return f"{self.cantidad} x {self.producto.nombre}"   

from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

# class Reserva(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     cantidad_personas = models.PositiveIntegerField()
#     total_boletos = models.PositiveIntegerField()
#     fecha_reserva = models.DateTimeField(auto_now_add=True)

    def calcular_boletos(self):
        return self.cantidad_personas * 1  # Por cada persona, un boleto

    def save(self, *args, **kwargs):
        self.total_boletos = self.calcular_boletos()
        super().save(*args, **kwargs)





  
