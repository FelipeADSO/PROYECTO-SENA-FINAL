from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


from .models import Producto, Carrito, ItemCarrito, Reserva

admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Reserva)

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'calificacion')
    list_filter = ('categoria', 'calificacion')
    search_fields = ('titulo', 'descripcion')

admin.site.register(PeliculaAdmin, PeliculaAdmin)

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
    admin.site.register(PeliculaAdmin)
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

from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'total', 'fecha_compra', 'estado')
    list_filter = ('estado', 'fecha_compra')
    search_fields = ('nombre', 'correo')
    readonly_fields = ('total',)
    inlines = [DetallePedidoInline]    
