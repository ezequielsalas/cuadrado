from django.shortcuts import render_to_response, render
from django.http import HttpResponse ,HttpResponseRedirect
from forms import CuentaForm,FinancialAccForm,TransactionForm
from models import Cuenta,Equipo,Alianza,FinancialAcc,Transaction
from django.core import serializers
# Create your views here.
def validateSignin(usuario, email, password):
	result = True
	if usuario =='' or email =='' or password =='':
		result = False

	return result 

def getLogin(request):
	try:
		request.session['account']
	except NameError, KeyError:
		request.session['account'] = ''
	
	return 	request.session['account'].usuario

def getCurrentAccount(request):
	try:
		request.session['account']
	except NameError, KeyError:
		request.session['account'] = ''

	return request.session['account']	

def saveInSession(request,name,value):
	try:
		request.session[name] = value
	except NameError, KeyError:
		raise nameError
	
def getSavedInSession(request,name):
	try:
		request.session[name]
	except NameError, KeyError:
		request.session[name] = ''

	return request.session[name]
	
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
	cuenta = Cuenta.objects.filter(email= pusuario, password=ppassword)
	if cuenta:
		request.session['account'] = cuenta[0]
		grupos = cuenta[0].equipo_set.all()
		page = 'grupos.html'
		if(grupos):
			page = 'home.html'
		
		return render(request,page,{'user':getLogin(request),'grupos':grupos})
	else:
		return render(request,'index.html',{'msje':msje})

def viewhome(request):
	acc = getCurrentAccount(request)
	grupos = acc.equipo_set.all()
	return render(request,'home.html',{'user':getLogin(request),'grupos':grupos})

def viewcreategroup(request):
	return render(request,'creategroup.html',{'user':getLogin(request)})

def viewfinancialinterest(request):
	#TODO: restriction for get only the account in my team
	teamName = request.GET.get('search','')
	if not teamName:
		return HttpResponseRedirect('/homeview/')
	
	team = Equipo.objects.get(nombre=teamName)
	
	saveInSession(request, 'team', team)
	
	accFina = team.financialacc_set.all()
	return render(request,'financialInterest.html',{'user':getLogin(request),'accFina':accFina})


def grupo(request):
	return render(request,'grupos.html',{'user':getLogin(request)})

def viewsearchgroup(request):
	return render(request,'searchgroup.html',{'user':getLogin(request)})

def searchgroup(request):
	teamName = request.GET.get('search','')
	teams = Equipo.objects.filter(nombre=teamName)
	
	return render(request,'searchgroup.html',{'user':getLogin(request),'teams':teams})

def serchNameGroup(request):
	
	
	data = serializers.serialize('json', Equipo.objects.all(), fields=('nombre'))
	return HttpResponse(data, mimetype='application/json')


def logout(request):
	request.session.flush()
	return render(request, "index.html")

def creategroup(request):
	nombregrupo = request.POST.get('equipoparam')
	interesfinanciero = request.POST.get('finanzaparam')
	cuenta = getCurrentAccount(request)
	equipo = Equipo(nombre=nombregrupo,interesFinanciero=interesfinanciero,propietario=cuenta.usuario)

	equipo.save()
	alianza = Alianza(equipo=equipo,cuenta=cuenta)
	alianza.save()
	return render(request,'creategroup.html',{'user':getLogin(request)})

def createFinancialAcc(request):
	accFina = ''
	accFinaName = ''
	trxs = ''
	balance = 0.0
	if request.method == 'POST':
		faf = FinancialAccForm(request.POST)
     	
     	if faf.is_valid():
	 		faft = faf.save(commit = False)
	 		acc = getCurrentAccount(request)
		 	team = getSavedInSession(request, 'team')
		 	grupo = acc.equipo_set.filter(nombre = team.nombre)
		 	accFinaName = faft.name
		 	faft.teamowner = grupo[0]
		 	faft.save()
			accFina = team.financialacc_set.all()
			saveInSession(request, 'currentAccFina', faft)
	
	return render(request,'financialAcctnx.html',{'user':getLogin(request),'accFina':accFina,'currentAccFina':accFinaName,'trans':trxs,'balance':balance}) 

def financialAccByName(request):
	team = getSavedInSession(request, 'team')
	accFina = team.financialacc_set.all()
	
	currentAccFinaName = request.GET.get('search','')
	if not currentAccFinaName:
		return HttpResponseRedirect('/homeview/')
	
	for acc in accFina:
		if acc.name == currentAccFinaName:
			saveInSession(request, 'currentAccFina', acc)
	currentAccFina = getSavedInSession(request, 'currentAccFina')		
	trxs = 	currentAccFina.transaction_set.all()
	balance = 0 
	for t in trxs:
		balance += t.amount
	return render(request,'financialAcctnx.html',{'user':getLogin(request),'accFina':accFina,'currentAccFina':currentAccFinaName,'trans':trxs,'balance':balance})

def createFinancialTranx(request):
	acc = getCurrentAccount(request)
	currentAccFina = getSavedInSession(request, 'currentAccFina')
	team = getSavedInSession(request, 'team')
	accFina = team.financialacc_set.all()
	
	if request.method == 'POST':
		trx = TransactionForm(request.POST)
		if trx.is_valid():
			typeTrx = request.POST.get('transTypeParam' , '')
			trxt = trx.save(commit = False)
			trxt.creator = acc
			trxt.accounttrans =  currentAccFina
			if typeTrx == 'isSpending':
				trxt.amount = trxt.amount * -1
			
			
			trxt.save()
	trxs = 	currentAccFina.transaction_set.all()
	
	balance = 0 
	for t in trxs:
		balance += t.amount
		
	return render(request,'financialAcctnx.html',{'user':getLogin(request),'accFina':accFina,'currentAccFina':currentAccFina.name,'trans':trxs,'balance':balance})