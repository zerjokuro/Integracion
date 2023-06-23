from django import forms
from .models import Solicitud, Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['codigo', 'nombre', 'direccion_origen', 'direccion_destino', 'estado','precio']



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {k:"" for k in fields }