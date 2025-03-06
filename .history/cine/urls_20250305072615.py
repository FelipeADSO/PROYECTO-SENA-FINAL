from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cinema import views
from django.contrib.auth.views import LogoutView
from cinema.views import agregar_al_carrito, reserva

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inicio', views.inicio, name='inicio'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('reserva/', hacer_reserva, name='reserva'),
    path('pasarela/', views.pasarela, name='pasarela'),
    path('carrito/', views.carrito, name='carrito'),
    path('cartelera', views.cartelera, name='cartelera'),
    path('peliculas', views.peliculas, name='peliculas'),
    path('puestos/', views.puestos, name='puestos'),
    path('procesar-reserva/', views.procesar_reserva, name='procesar_reserva'),
    path('peliculas_2', views.peliculas_2, name='peliculas_2'),
    path('contactenos', views.contactenos, name='contactenos'),
    path('login', views.login, name='login'),
    path('somos', views.somos, name='somos'),
    path('perfil/', views.perfil, name="perfil"),
    path('reserva/', views.reserva, name="reserva"),
    path('api/user-info/', views.user_info, name="user_info"),
    path('register', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path("cambiar_contraseña/<uidb64>/<token>/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("password_changed/", views.password_changed, name="password_changed"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
