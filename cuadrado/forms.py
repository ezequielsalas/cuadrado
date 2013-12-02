from django import forms
from models import Cuenta,FinancialAcc,Transaction,TransactionBudget
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

class TransactionBudgetForm(ModelForm):
	class Meta:
		model = TransactionBudget