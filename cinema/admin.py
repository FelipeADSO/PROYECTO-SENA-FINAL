from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered



from .models import Pelicula, Reserva

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'calificacion')
    list_filter = ('categoria', 'calificacion')
    search_fields = ('titulo', 'descripcion')

admin.site.register(Pelicula, PeliculaAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'hora', 'personas', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('fecha_creacion',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('usuario')

# Intentamos registrar cada modelo solo si no está ya registrado
try:
    admin.site.register(Pelicula)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Pelicula)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Reserva, ReservaAdmin)
except AlreadyRegistered:
    # Si ya está registrado, podemos actualizar la configuración
    admin.site.unregister(Reserva)
    admin.site.register(Reserva, ReservaAdmin)

from .models import CarritoItem

class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'cantidad', 'usuario', 'sesion_id', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('producto__nombre', 'usuario__username')

try:
    admin.site.register(CarritoItem, CarritoItemAdmin)
except AlreadyRegistered:
    pass

from .models import Orden, OrdenItem

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    readonly_fields = ('reserva', 'precio', 'cantidad')

class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'total', 'pagado', 'fecha_creacion')
    list_filter = ('pagado', 'fecha_creacion')
    search_fields = ('nombre', 'email')

try:
    admin.site.register(Orden, OrdenAdmin)
except AlreadyRegistered:
    pass

from .models import Contacto

class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_creacion')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion',)

try:
    admin.site.register(Contacto, ContactoAdmin)
except AlreadyRegistered:
    pass

from django.contrib import admin
from .models import EstrenoPelicula

@admin.register(EstrenoPelicula)
class EstrenoPeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'calificacion', 'fecha_estreno', 'orden')
    ordering = ('orden',)

from django.contrib import admin
from .models import ContenidoCine  # Asegúrate de importar el modelo

admin.site.register(ContenidoCine)  # Registra el modelo en el admin




