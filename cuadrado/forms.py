from django import forms
from models import Cuenta,FinancialAcc,Transaction
from django.forms import ModelForm

class CuentaForm(ModelForm):
	class Meta:
		model = Cuenta
		
class FinancialAccForm(ModelForm):
	class Meta:
		model = FinancialAcc
		
class TransactionForm(ModelForm):
	class Meta:
		model = Transaction