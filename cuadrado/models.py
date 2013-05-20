from django.db import models

# Create your models here.
class Cuenta(models.Model):
	usuario = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	password = models.CharField(max_length=200)

class Equipo(models.Model):
	nombre = models.CharField(max_length=200)
	creado = models.DateField(auto_now=True)
	interesFinanciero = models.BooleanField()
	interesConocimiento = models.BooleanField()
	interesCultura = models.BooleanField()
	interesAlianza = models.BooleanField()
	asociados = models.ForeignKey(Cuenta)
    