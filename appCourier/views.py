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
        
        print(request.POST.get('codigo'),request.POST.get('nombre'),request.POST.get('direccion_origen'),request.POST.get('direccion_destino'),request.POST.get('estado'))

        mi_modelo = SolicitudForm(codigo=codigo, nombre=nombre, direccion_origen=direccion_origen, direccion_destino=direccion_destino, estado=estado)
        mi_modelo.save()
        
        return redirect('appCourier/lista_solicitudes.html')  # Redirige a la página deseada después de guardar los valores

    return render(request, 'editar_Solicitud.html')  # Renderiza el formulario con los inputs y combobox

#-----------------------------------Integracion--------------------------------

def api_solicitud(request):
    form = SolicitudForm()

    if request.method == 'POST':
        form = SolicitudForm(request.POST)

        if form.is_valid():
            data = {
                'nombre_origen': form.cleaned_data['nombre_origen'],
                'direccion_origen': form.cleaned_data['direccion_origen'],
                'nombre_destino': form.cleaned_data['nombre_destino'],
                'direccion_destino': form.cleaned_data['direccion_destino'],
                'comentario': form.cleaned_data['comentario'],
                'informacion': form.cleaned_data['informacion'],
                'estado': form.cleaned_data['estado'],
                # Agrega más campos según corresponda
            }

            response = requests.get('https://musicpro.bemtorres.win/api/v1/transporte/solicitud', params=data)
            data = response.json()

            for item in data:
                solicitud = form.save(commit=False)
                solicitud.nombre_origen = item['nombre_origen']
                solicitud.direccion_origen = item['direccion_origen']
                solicitud.nombre_destino = item['nombre_destino']
                solicitud.direccion_destino = item['direccion_destino']
                solicitud.comentario = item['comentario']
                solicitud.informacion = item['informacion']
                solicitud.estado = item['estado']
                # Asigna valores a otros campos según corresponda

                solicitud.save()  # Guarda el objeto en la base de datos

            return redirect('appCourier/lista_solicitudes.html')  # Redirige a la página deseada después de guardar los datos

    return render(request, 'appCourier/solicitud.html', {'form': form})