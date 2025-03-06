from django.contrib.auth.models import User
from django.db import models


# Modelo de Película
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
    horario = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Convertir URL de YouTube a formato embed
        if 'youtube.com/watch?v=' in self.trailer_url:
            video_id = self.trailer_url.split('v=')[1].split('&')[0]
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


# Modelo de Perfil de Usuario
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


# Modelo de Reserva
class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=20, 
        choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]
    )
    mensaje = models.TextField(blank=True, null=True)
    personas = models.IntegerField(default=1)  # Asegúrate de que este campo existe
    productos = models.ManyToManyField(Producto, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def total_boletos(self):
        return self.personas * 12000

    def __str__(self):
        return f"Reserva de {self.usuario} - {self.personas} personas el {self.fecha}"


# Modelo de Pedido
class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    estado = models.CharField(
        max_length=20, 
        default='pendiente', 
        choices=[
            ('pendiente', 'Pendiente'), 
            ('completado', 'Completado'), 
            ('cancelado', 'Cancelado')
        ]
    )

    def __str__(self):
        return f"Pedido de {self.nombre} - {self.fecha_compra}"


# Modelo de Detalle de Pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.titulo}"


# Modelo de Carrito de Compras
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario}"


# Modelo de Ítem del Carrito
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
