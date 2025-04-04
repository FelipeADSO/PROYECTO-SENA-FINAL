from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cinema import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path("", views.home, name="home"),
    path('pasarela/', views.pasarela, name='pasarela'),
    path('cartelera', views.cartelera, name='cartelera'),
    path('peliculas', views.peliculas, name='peliculas'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('puestos/', views.puestos, name='puestos'),
    path('historial/', views.historial_compras, name='historial'),
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
    path("cambiar_contrasena/<uidb64>/<token>/", views.cambiar_contrasena, name="cambiar_contrasena"),
    path("password_changed/", views.password_changed, name="password_changed"),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('confirmacion/<int:orden_id>/', views.confirmacion, name='confirmacion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
