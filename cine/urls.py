from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cinema import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inicio', views.inicio, name='inicio'),
    path('cartelera', views.cartelera, name='cartelera'),
    path('peliculas', views.peliculas, name='peliculas'),
    path('peliculas_2', views.peliculas_2, name='peliculas_2'),
    path('contactenos', views.contactenos, name='contactenos'),
    path('login', views.login, name='login'),
    path('somos', views.somos, name='somos'),
    path('perfil/', views.perfil, name="perfil"),
    path('api/user-info/', views.user_info, name="user_info"),
    path('register', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path("cambiar_contraseña/<uidb64>/<token>/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("password_changed/", views.password_changed, name="password_changed"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
