from django import forms
from .models import Solicitud
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['codigo', 'nombre','direccion_origen', 'direccion_destino','estado']