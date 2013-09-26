from django.shortcuts import render_to_response, render
from django.http import HttpResponse ,HttpResponseRedirect
from forms import CuentaForm,FinancialAccForm,TransactionForm
from models import Cuenta,Equipo,Alianza,FinancialAcc,Transaction
from django.core import serializers
from django.db.models import Q
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
		grupos = Alianza.objects.filter(cuenta__usuario=cuenta[0].usuario).filter(Q(estado__isnull=True)|Q(estado='Aliado'))
		page = 'grupos.html'
		if(grupos):
			page = 'home.html'
		
		return render(request,page,{'user':getLogin(request),'grupos':grupos})
	else:
		return render(request,'index.html',{'msje':msje})

def viewhome(request):
	acc = getCurrentAccount(request)
	grupos = Alianza.objects.filter(cuenta__usuario=acc.usuario).filter(Q(estado__isnull=True)|Q(estado='Aliado'))
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
	teamName = request.GET.get('searchGroup','')
	user = getLogin(request)
	
	teams = Alianza.objects.filter(equipo__nombre__icontains=teamName,estado__isnull=True).exclude(equipo__propietario=user)
	
	currentTeams = []
	for team in teams:
		a = Alianza.objects.filter(equipo__nombre=team.equipo.nombre,cuenta__usuario=user ,estado__in=['Pendiente','Aliado']) 
		if a:
			currentTeams.append(a[0])
		else:
			currentTeams.append(team)
			
	return render(request,'searchgroup.html',{'user':user,'teams':currentTeams})

#Cambiar esto de get a post
def requestAlliance(request):
	teamName = request.GET.get('requestGroup','')
	alliance = request.GET.get('alliance','')
	
	cuenta = getCurrentAccount(request)
	equipo = Equipo.objects.get(nombre=teamName)
	
	if equipo:
		t = Alianza.objects.filter(equipo__nombre=teamName,cuenta__usuario=cuenta.usuario)
		if not t:
			ali = Alianza(equipo=equipo,cuenta=cuenta,estado='Pendiente')	
			ali.save()
	teams = Alianza.objects.filter(estado__isnull=True).exclude(equipo__propietario=cuenta.usuario)
	
	currentTeams = []
	for team in teams:
		a = Alianza.objects.filter(equipo__nombre=team.equipo.nombre,cuenta__usuario=cuenta.usuario,estado__in=['Pendiente','Aliado']) 
		if a:
			currentTeams.append(a[0])
		else:
			currentTeams.append(team)
							
	return render(request,'searchgroup.html',{'user':getLogin(request),'teams':currentTeams})

def getMeGroupMessage(request):
	teams = Alianza.objects.filter(equipo__propietario=getLogin(request), estado = 'Pendiente')
	result = ''
	
	for v in teams:
		result = result + ""+ v.cuenta.usuario+" quiere formar parte de <span>"+v.equipo.nombre+"</span>,"
	return HttpResponse(result)

def serchNameGroup(request):
	result = ''
	data = Equipo.objects.values('nombre').distinct()
	for v in data:
		if v['nombre']:
			result = result + ''+ v['nombre']+','
	
	return HttpResponse(result)


def logout(request):
	request.session.flush()
	return render(request, "index.html")

def creategroup(request):
	nombregrupo = request.POST.get('equipoparam')
	interesfinanciero = request.POST.get('finanzaparam','True')
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
     	faftname = request.POST.get('name','')
     	team = getSavedInSession(request, 'team')
     	exist = team.financialacc_set.filter(nombre = faftname)
     	if not exist:
	     	if faf.is_valid():
	     		faftname = faf.name
	     		team = getSavedInSession(request, 'team')
	     		exist = team.financialacc_set.filter(nombre = faftname)
	     		if not exist:
		     		faft = faf.save(commit = False)
		     		acc = getCurrentAccount(request)
		     		
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

def processAllianceRequest(request):
	action = request.GET.get('msjParam','')
	groupParam = request.GET.get('groupParam','')
	print 'en el metodo probando'
	a = Alianza.objects.get(equipo__nombre=groupParam,estado='Pendiente')
	print a
	print action
	if action =='Accept':
		a.estado = 'Aliado'
	elif action == 'Rejected':
		a.estado = 'Rota'
	print a	
	a.save()
	return HttpResponse('/')