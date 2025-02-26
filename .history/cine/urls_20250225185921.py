"""
URL configuration for cine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cinema import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('inicio',views.inicio, name='inicio'),
    path('cartelera',views.cartelera, name='cartelera'),
    path('peliculas',views.peliculas, name='peliculas'),
    path('peliculas_2',views.peliculas_2, name='peliculas_2'),
    path('contactenos',views.contactenos, name='contactenos'),
    path('login',views.login, name='login'),
    path('somos',views.somos, name='somos'),
    path('register',views.register, name='register'),]
    # path('logout/', cerrar_sesion, name='logout'),
    # path('estrenos/', views.estrenos, name='estrenos'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 # Asegúrate de tener esta línea
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)