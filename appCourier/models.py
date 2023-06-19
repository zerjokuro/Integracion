from django.db import models

class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    nombre_origen = models.CharField(max_length=100, blank=True)
    direccion_origen = models.CharField(max_length=100)
    nombre_destino = models.CharField(max_length=100, blank=True)
    direccion_destino = models.CharField(max_length=100)
    comentario = models.CharField(max_length=100, null=True)
    informacion = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=100, default= 'por enviar')


