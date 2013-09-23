from django.db import models

# Create your models here.
class Cuenta(models.Model):
	usuario = models.CharField(max_length=200)
	email = models.EmailField(max_length=200, unique=True)
	password = models.CharField(max_length=200)
	#equipo = models.ForeignKey('Equipo',blank=True, null=True)
	def __unicode__(self):
		return self.usuario

class Equipo(models.Model):
	nombre = models.CharField(max_length=200)
	creado = models.DateField(auto_now=True)
	interesFinanciero = models.BooleanField()
	interesConocimiento = models.BooleanField()
	interesCultura = models.BooleanField()
	interesAlianza = models.BooleanField()
	alianza = models.ManyToManyField(Cuenta,through='Alianza')
	propietario = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

class Alianza(models.Model):
	cuenta = models.ForeignKey(Cuenta, related_name='Cuenta')
	equipo = models.ForeignKey(Equipo, related_name='Equipo')
	creado = models.DateField(auto_now=True)
	#Aliado Rota Pendiente
	estado = models.CharField(max_length=200,blank=True, null=True)
	
class Category(models.Model):
	name = models.CharField(max_length=200)
	
class FinancialAcc(models.Model):
	balance = models.FloatField(blank=True, null=True)
	name = models.CharField(max_length=200, unique=True)
	created = models.DateField(auto_now=True)
#	transaction = models.ForeignKey(Transaction, related_name='Transaction',blank=True, null=True)
	porcent = models.IntegerField(max_length=200,blank=True, null=True)
	fee = models.IntegerField(max_length=200,blank=True, null=True)
	teamowner = models.ForeignKey(Equipo,blank=True, null=True)
	def __unicode__(self):
		return self.name 
	
class Transaction(models.Model):
	created = models.DateField(auto_now=True)
	amount =  models.FloatField()
	concept = models.CharField(max_length=200)
	creator = models.ForeignKey(Cuenta,blank=True, null=True)
	accounttrans = models.ForeignKey(FinancialAcc,blank=True, null=True)
	
	def __unicode__(self):
		return self.concept