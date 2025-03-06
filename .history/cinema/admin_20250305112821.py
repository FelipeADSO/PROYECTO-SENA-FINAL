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


