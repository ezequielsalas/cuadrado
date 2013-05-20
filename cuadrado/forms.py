from django import forms
from models import Cuenta
from django.forms import ModelForm

class CuentaForm(ModelForm):
	class Meta:
		model = Cuenta