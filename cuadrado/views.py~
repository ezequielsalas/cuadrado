from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from forms import CuentaForm
from models import Cuenta

# Create your views here.
def validateSignin(usuario, email, password):
	result = True
	if usuario =='' or email =='' or password =='':
		result = False

	return result 

def getLogin(request):
	try:
		request.session['userSession']
	except NameError, KeyError:
		request.session['userSession'] = ''
	
	return 	request.session['userSession']

def index(request):
	msj = ''
	msje = ''
	if request.method == 'POST':
		pusuario = request.POST.get('usuario', '')
		pemail = request.POST.get('email', '')
		ppassword = request.POST.get('password', '')
		if validateSignin(pusuario,pemail,ppassword):
			reg = Cuenta(usuario=pusuario, email=pemail, password=ppassword)
			reg.save()
			msj = 'Gracias por registrarte. Ya puedes acceder a tu cuenta!'
		else:
			msje = 'Datos incorrectos'
	
	return render(request,'index.html',{'msj':msj, 'msje':msje})

def login(request):
	pusuario = request.POST.get('usuarioLogin', '')
	ppassword = request.POST.get('passwordLogin', '')
	msje = 'Verifica tu password y usuario'
	registro = Cuenta.objects.filter(email= pusuario, password=ppassword)
	if registro:
		request.session['userSession'] = registro[0].usuario

		return render(request,'home.html',{'user':getLogin(request)})
	else:
		return render(request,'index.html',{'msje':msje})

def viewcreategroup(request):

	return render(request,'creategroup.html',{'user':getLogin(request)})

def home(request):
	return render(request,'home.html',{'user':getLogin(request)})

def logout(request):
	request.session['userSession'] = ''
	return render(request, "index.html")

