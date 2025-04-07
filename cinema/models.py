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
    orden = models.IntegerField(default=0)  # Campo para definir el orden de las películas

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
        ordering = ['orden']  # Ordenar por el campo "orden" de menor a mayor


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
    hora = models.TimeField(default="12:00")
    personas = models.IntegerField()
    productos = models.ManyToManyField(Pelicula, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')
    mensaje = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)



class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} x Reserva #{self.reserva.id}"
    
    def subtotal(self):
        return 12000 * self.cantidad * self.reserva.personas

class Datos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)

    def __str__(self):
        return self.usuario.username   
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.nombre}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.cantidad} x Reserva #{self.reserva.id}"
    
    def subtotal(self):
        return self.precio * self.cantidad

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contacto de {self.nombre}"
    


class EstrenoPelicula(models.Model):
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
    imagen = models.ImageField(upload_to='estrenos/')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    calificacion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fecha_estreno = models.DateField(null=True, blank=True)
    horario = models.CharField(max_length=255, null=True, blank=True)
    orden = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
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
        verbose_name = "estreno"
        verbose_name_plural = "estrenos"
        ordering = ['orden']
        
from django.db import models

class ContenidoCine(models.Model):
    GENEROS = [
        ('Romance y Drama', 'Romance y Drama'),
        ('Ciencia ficción y fantasía', 'Ciencia ficción y fantasía'),
        ('Acción', 'Acción'),
        ('Comedia', 'Comedia'),
        ('Terror', 'Terror'),
        ('Documentales', 'Documentales'),
    ]
    FORMATOS = [
        ('2D', '2D'),
        ('3D', '3D'),
        ('2D/3D', 'Disponible en ambos formatos'),
    ]
    
    nombre = models.CharField(max_length=100)
    sinopsis = models.TextField()
    video_promocional = models.URLField(help_text="URL de YouTube (se convertirá automáticamente a formato embed)")
    imagen_portada = models.ImageField(upload_to='contenidos/')
    genero = models.CharField(max_length=50, choices=GENEROS)
    puntuacion = models.FloatField(choices=[(x / 2, str(x / 2)) for x in range(1, 11)])  # Permite valores decimales
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    fecha_estreno = models.DateField(null=True, blank=True)  # Nuevo campo
    prioridad = models.IntegerField(default=0)
    formato = models.CharField(
        max_length=5,
        choices=FORMATOS,
        default='2D',
        verbose_name="Formato de proyección"
    )
    funcion_2d = models.BooleanField(
        default=False,
        verbose_name="Disponible en 2D"
    )
    funcion_3d = models.BooleanField(
        default=False,
        verbose_name="Disponible en 3D"
    )

    def save(self, *args, **kwargs):
        # Convertir URL de YouTube a formato embed
        if 'youtube.com/watch?v=' in self.video_promocional:
            video_id = self.video_promocional.split('v=')[1].split('&')[0] if '&' in self.video_promocional.split('v=')[1] else self.video_promocional.split('v=')[1]
            self.video_promocional = f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.video_promocional:
            video_id = self.video_promocional.split('youtu.be/')[1]
            self.video_promocional = f'https://www.youtube.com/embed/{video_id}'
        
    # Actualizar el campo formato basado en las funciones disponibles
        if self.funcion_2d and self.funcion_3d:
            self.formato = '2D/3D'
        elif self.funcion_2d:
            self.formato = '2D'
        elif self.funcion_3d:
            self.formato = '3D'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Contenido de Cine"
        verbose_name_plural = "Contenidos de Cine"
        ordering = ['prioridad']

from django.db import models

class Funcion(models.Model):
    titulo = models.CharField(max_length=255)
    horario = models.DateTimeField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.titulo} - {self.horario}"
    
from django.contrib.auth.models import User
from django.db import models

class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    pelicula = models.CharField(max_length=200)  # Puede ser una ForeignKey si tienes un modelo Pelicula
    cantidad_boletos = models.PositiveIntegerField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)  # Fecha automática

    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula} ({self.fecha_reserva})"




