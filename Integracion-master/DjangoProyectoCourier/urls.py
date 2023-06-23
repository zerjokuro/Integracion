"""
URL configuration for DjangoProyectoCourier project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path,include
from appCourier import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/nuevo/', views.nuevo_solicitud, name='nuevo_solicitud'),
    path('solicitudes/<int:pk>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitudes/<int:pk>/editar/', views.editar_solicitud, name='editar_solicitud'),
    path('solicitudes/<int:pk>/eliminar/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('buscar/', views.buscar ),
    path('datos/', views.datos),
    path('guardar_valores/', views.guardar_valores, name='guardar_valores'),
    path('api/', include('appCourier.urls')),
    path('api_saldo/', views.api_saldo),
    path('api_saludo/',views.api_saludo),
    path('registro/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='appcourier/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='appcourier/logout.html'), name='logout'),

    ]



