from django.db import models

class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=100)
    direccion_destino = models.CharField(max_length=100)
    estado = models.CharField(max_length=100, default= 'Preparacion')
    precio= models.IntegerField(default=0)

class Usuario(models.Model):
    correo = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=100)



