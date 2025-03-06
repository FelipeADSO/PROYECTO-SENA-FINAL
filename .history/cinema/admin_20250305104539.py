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

try:
    admin.site.register(Pelicula)
except AlreadyRegistered:
    pass

# try:
#     admin.site.register(Datos)
# except AlreadyRegistered:
#     pass

try:
    admin.site.register(Reserva, ReservaAdmin)
except AlreadyRegistered:
    admin.site.unregister(Reserva)
    admin.site.register(Reserva, ReservaAdmin)

from .models import CarritoItem

class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'usuario', 'sesion_id', 'fecha_creacion')
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
    readonly_fields = ('producto', 'precio', 'cantidad')

class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'total', 'pagado', 'fecha_creacion')
    list_filter = ('pagado', 'fecha_creacion')
    search_fields = ('nombre', 'email')

try:
    admin.site.register(Orden, OrdenAdmin)
except AlreadyRegistered:
    pass
