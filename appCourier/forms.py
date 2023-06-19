from django import forms
from .models import Solicitud
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre_origen','direccion_origen','nombre_destino', 'direccion_destino','comentario','informacion','estado']