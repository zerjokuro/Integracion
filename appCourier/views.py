from django.shortcuts import render, get_object_or_404, redirect
from .models import Solicitud
from .forms import SolicitudForm
import requests
from django.http import HttpResponse, JsonResponse
from .serializers import SolicitudSerializer
from rest_framework import generics

#---------------------------------Metodos crud---------------------------------------

def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'appCourier/lista_solicitudes.html', {'solicitudes': solicitudes})

def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    return render(request, 'appCourier/detalle_solicitud.html', {'solicitud': solicitud})


def nuevo_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save()
            return redirect('detalle_solicitud', pk=solicitud.pk)
    else:
        form = SolicitudForm()
    return render(request, 'appCourier/editar_solicitud.html', {'form': form})

def editar_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('detalle_solicitud', pk=solicitud.pk)
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'appCourier/editar_solicitud.html', {'form': form})

def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.delete()
    return redirect('lista_solicitudes')


#-----------------------------Metodos cliente vista--------------------------------------------

def buscar (request):
    
    return render(request,"appCourier/buscar.html")


def datos(reques):
    
    if reques.GET["codigo"]:
        
        auxCodigo= reques.GET["codigo"]
        
        datos= get_object_or_404(Solicitud,codigo=auxCodigo)

    return render(reques,"appCourier/datos_codigo.html",{"datos": datos})


#----------------------------------Metodos rest-----------------------------------------------

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
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        direccion_origen = request.POST.get('direccion_origen')
        direccion_destino = request.POST.get('direccion_destino')
        estado = request.POST.get('estado')
        
        mi_modelo = SolicitudForm(codigo=codigo, nombre=nombre, direccion_origen=direccion_origen, direccion_destino=direccion_destino, estado=estado)
        mi_modelo.save()
        
        return redirect('appCourier/lista_solicitudes.html')  # Redirige a la página deseada después de guardar los valores

    return render(request, 'editar_Solicitud.html')  # Renderiza el formulario con los inputs y combobox
