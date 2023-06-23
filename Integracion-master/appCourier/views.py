from django.shortcuts import render, get_object_or_404, redirect
from .models import Solicitud, Usuario
from .forms import SolicitudForm , UserRegisterForm
import requests
from django.http import HttpResponse, JsonResponse
from .serializers import SolicitudSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#---------------------------------Metodos crud---------------------------------------
@login_required
def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'appCourier/lista_solicitudes.html', {'solicitudes': solicitudes})
@login_required
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    return render(request, 'appCourier/detalle_solicitud.html', {'solicitud': solicitud})

@login_required
def nuevo_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save()
            return redirect('detalle_solicitud', pk=solicitud.pk)
    else:
        form = SolicitudForm()
    return render(request, 'appCourier/nueva_solicitud.html', {'form': form})
@login_required
def editar_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.delete()
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            solicitud = form.save()# Actualiza la instancia existente en lugar de crear una nueva
            return redirect('detalle_solicitud', pk=solicitud.pk)
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'appCourier/editar_solicitud.html', {'form': form, 'solicitud': solicitud})


@login_required
def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.delete()
    return redirect('lista_solicitudes')


#-----------------------------Metodos cliente vista--------------------------------------------

def buscar (request):
    
    return render(request,"appCourier/buscar.html")


def datos(request):
    codigo = request.GET.get("codigo")
    datos = None
    mensaje = None
    
    if codigo:
        try:
            datos = Solicitud.objects.get(codigo=codigo)
        except Solicitud.DoesNotExist:
            mensaje = "No se encontró la solicitud con el código proporcionado"

    return render(request, "appCourier/datos_codigo.html", {"datos": datos, "mensaje": mensaje})


#----------------------------------Metodos rest-----------------------------------------------
@login_required
def api_saldo(request):
    url = 'https://musicpro.bemtorres.win/api/v1/test/saldo'  # Reemplaza con la URL de la API que deseas consumir

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Si la respuesta es en formato JSON
        # Realiza las operaciones que necesites con los datos obtenidos
        return JsonResponse(data)
    else:
        # La solicitud no fue exitosa, mostrar el código de estado
        error_message = 'Error: ' + str(response.status_code)
        # Mostrar el mensaje de error de la respuesta (si está disponible)
        error_message += ' - ' + response.text
        return HttpResponse(error_message, status=response.status_code)
@login_required
def api_saludo(request):
    url = 'https://musicpro.bemtorres.win/api/v1/test/saludo'  # Reemplaza con la URL de la API que deseas consumir

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Si la respuesta es en formato JSON
        # Realiza las operaciones que necesites con los datos obtenidos
        return JsonResponse(data)
    else:
        # La solicitud no fue exitosa, mostrar el código de estado
        error_message = 'Error: ' + str(response.status_code)
        # Mostrar el mensaje de error de la respuesta (si está disponible)
        error_message += ' - ' + response.text
        return HttpResponse(error_message, status=response.status_code)
    

class SolicitudListView(generics.ListCreateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class SolicitudDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    
"""INTENTO COMBO BOX EDITAR"""
def guardar_valores(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_solicitudes')  # Redirige a la página deseada después de guardar los valores
    else:
        form = SolicitudForm()
        

    return render(request, 'editar_Solicitud.html')  # Renderiza el formulario con los inputs y combobox

    

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('../solicitudes/')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'appcourier/register.html', context)
