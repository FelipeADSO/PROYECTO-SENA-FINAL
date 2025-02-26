from django.contrib import admin


from .models import Pelicula

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'calificacion')
    list_filter = ('categoria', 'calificacion')
    search_fields = ('titulo', 'descripcion')

admin.site.register(Pelicula, PeliculaAdmin)
