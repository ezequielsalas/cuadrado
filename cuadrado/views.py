from django.shortcuts import render_to_response, render
from django.http import HttpResponse ,HttpResponseRedirect
from forms import CuentaForm,FinancialAccForm,TransactionForm, TransactionBudgetForm
from models import Cuenta,Equipo,Alianza,FinancialAcc,Transaction , Budget
from django.core import serializers
from django.db.models import Q
from django.db import IntegrityError
# Create your views here.
def validateSignin(usuario, email, password,repassword):
	result = True
	if usuario =='' or email =='' or password =='' or password !=repassword:
		result = False

	return result 

def getLogin(request):
	if 'account' not in request.session:
		return ''
	
	return 	request.session['account'].usuario

def getCurrentAccount(request):
	if 'account' not in request.session:
		return ''	
	return request.session['account']	

def isLoged(request):
	if 'account' not in request.session:
		return HttpResponseRedirect('/')	
	return True	

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
		prepassword = request.POST.get('repassword', '')
		if validateSignin(pusuario,pemail,ppassword,prepassword):
			reg = Cuenta(usuario=pusuario.strip(), email=pemail.strip(), password=ppassword)
			try:
				reg.save()
				msj = 'Gracias por registrarte. Ya puedes acceder a tu cuenta!'
			except (NameError,IntegrityError):
				msje = 'Usuario no disponible'
			 
		else:
			msje = 'Datos incorrectos'
	
	#if isLoged(request):
	#	return HttpResponseRedirect('/homeview/')
	
	return render(request,'index.html',{'msj':msj, 'msje':msje,'user':getLogin(request)})

def login(request):
	pusuario = request.POST.get('usuarioLogin', '')
	ppassword = request.POST.get('passwordLogin', '')
	msje = 'Verifica tu password y usuario'
	cuenta = Cuenta.objects.filter(email= pusuario.strip(), password=ppassword)
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
	isLoged(request)
	grupos = Alianza.objects.filter(cuenta__usuario=getLogin(request)).filter(Q(estado__isnull=True)|Q(estado='Aliado'))
	return render(request,'home.html',{'user':getLogin(request),'grupos':grupos})

def viewcreategroup(request):
	isLoged(request)
	print 'paso el isLoged'
	return render(request,'creategroup.html',{'user':getLogin(request)})

def viewfinancialinterest(request):
	#TODO: restriction for get only the account in my team
	isLoged(request)
	teamName = request.GET.get('search','')
	if not teamName:
		return HttpResponseRedirect('/homeview/')
	
	team = Equipo.objects.get(nombre=teamName)
	
	saveInSession(request, 'team', team)
	
	accFina = team.financialacc_set.all()
	return render(request,'financialInterest.html',{'user':getLogin(request),'accFina':accFina})


def grupo(request):
	isLoged(request)
	return render(request,'grupos.html',{'user':getLogin(request)})

def viewsearchgroup(request):
	isLoged(request)
	return render(request,'searchgroup.html',{'user':getLogin(request)})

def searchgroup(request):
	isLoged(request)
	teamName = request.GET.get('searchGroup','')
	user = getLogin(request)
	
	teams = Alianza.objects.filter(equipo__nombre__icontains=teamName.strip(),estado__isnull=True).exclude(equipo__propietario=user)
	
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
	isLoged(request)
	teamName = request.GET.get('requestGroup','')
	alliance = request.GET.get('alliance','')
	
	cuenta = getCurrentAccount(request)
	equipo = Equipo.objects.get(nombre=teamName.strip())
	
	if equipo:
		t = Alianza.objects.filter(equipo__nombre=teamName.strip(),cuenta__usuario=cuenta.usuario)
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
	isLoged(request)
	teams = Alianza.objects.filter(equipo__propietario=getLogin(request), estado = 'Pendiente')
	result = ''
	
	for v in teams:
		result = result + ""+ v.cuenta.usuario+" quiere formar parte de <span>"+v.equipo.nombre+"</span>,"
	
	return HttpResponse(result)

def serchNameGroup(request):
	isLoged(request)
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
	isLoged(request)
	nombregrupo = request.POST.get('equipoparam')
	interesfinanciero = request.POST.get('finanzaparam','True')
	cuenta = getCurrentAccount(request)
	msj = ''
	if cuenta:
		
		if not Equipo.objects.filter(nombre=nombregrupo.strip()):
			equipo = Equipo(nombre=nombregrupo.strip(),interesFinanciero=interesfinanciero.strip(),propietario=cuenta.usuario)
		
			equipo.save()
			alianza = Alianza(equipo=equipo,cuenta=cuenta)
			alianza.save()
			return HttpResponseRedirect('/homeview/')
		else:
			msj = 'Ya existe este equipo.'

	return render(request,'creategroup.html',{'user':getLogin(request),'msj':msj})

def createFinancialAcc(request):
	isLoged(request)
	accFina = ''
	accFinaName = ''
	trxs = ''
	balance = 0.0
	msj = ''
	page = 'financialInterest.html'
	if request.method == 'POST':
		faf = FinancialAccForm(request.POST)
     	faftname = request.POST.get('name','')
     	team = getSavedInSession(request, 'team')
     	exist = team.financialacc_set.filter(name = faftname)
     	accFina = team.financialacc_set.all()
     	if not exist:
	     	if faf.is_valid():
     	
	     		faft = faf.save(commit = False)
	     		acc = getCurrentAccount(request)
	     		
	     		grupo = acc.equipo_set.filter(nombre = team.nombre)
	     		accFinaName = faft.name
	     		faft.teamowner = grupo[0]
	     		
	     		faft.save()
	     		budget =  Budget(name='Budget ',accOwner=faft)
	     		
	     		budget.save()
	     		saveInSession(request, 'currentAccFina', faft)
	
		else:	
			msj = 'Esta cuenta ya existe en este grupo.'
	     	page = 'financialInterest.html'
	return render(request,page,{'msj':msj,'user':getLogin(request),'accFina':accFina,'currentAccFina':accFinaName,'trans':trxs,'balance':balance}) 

def financialAccByName(request):
	isLoged(request)
	team = getSavedInSession(request, 'team')
	accFina = team.financialacc_set.all()
	
	currentAccFinaName = request.GET.get('search','')
	if not currentAccFinaName:
		return HttpResponseRedirect('/homeview/')
	
	for acc in accFina:
		if acc.name == currentAccFinaName.strip():
			saveInSession(request, 'currentAccFina', acc)
	currentAccFina = getSavedInSession(request, 'currentAccFina')		
	trxs = 	currentAccFina.transaction_set.all()
	balance = 0 
	for t in trxs:
		balance += t.amount
	return render(request,'financialAcctnx.html',{'user':getLogin(request),'accFina':accFina,'currentAccFina':currentAccFinaName,'trans':trxs,'balance':balance})

def createFinancialTranx(request):
	isLoged(request)
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
	isLoged(request)
	action = request.GET.get('msjParam','')
	groupParam = request.GET.get('groupParam','')
	a = Alianza.objects.get(equipo__nombre=groupParam.strip(),estado='Pendiente')
	print 'la accion', action
	if action =='Accept':
		a.estado = 'Aliado'
	elif action == 'Rejected':
		a.estado = 'Rota'
	a.save()
	return HttpResponse('/')

def viewBudget(request):
	return render(request,'accBudget.html')

def createBudget(request):
	isLoged(request)
	accFina = team.financialacc_set.all()
	
	currentAccFinaName = request.GET.get('search','')
	if not currentAccFinaName:
		return HttpResponseRedirect('/homeview/')
	
	for acc in accFina:
		if acc.name == currentAccFinaName.strip():
			budget =  Budget(name='Budget '.join(acc.name),hasBudget=True,teamowner= acc)
			budget.save()

	return budgetByFinantialAcc(request)


def budgetByFinantialAcc(request):
	isLoged(request)
	team = getSavedInSession(request, 'team')
	accFina = team.financialacc_set.all()
	
	currentAccFinaName = request.GET.get('search','')
	if not currentAccFinaName:
		return HttpResponseRedirect('/homeview/')
	
	for acc in accFina:
		if acc.name == currentAccFinaName.strip():
			saveInSession(request, 'currentAccFinaForBudget', acc)

	currentAccFina = getSavedInSession(request, 'currentAccFinaForBudget')
	trxs = None
	if currentAccFina.budget_set.all():
		trxs = 	currentAccFina.budget_set.all()[0].transactionbudget_set.all()
	balance = 0
	if not trxs is None:
		for t in trxs:
			balance += t.amount
			
	return render(request,'accBudget.html',{'user':getLogin(request),'currentAccFina':currentAccFinaName,'transBudget':trxs,'balance':balance})

def createBudgetTranx(request):
	isLoged(request)
	acc = getCurrentAccount(request)
	currentAccFina = getSavedInSession(request, 'currentAccFina')
	team = getSavedInSession(request, 'team')
	accFina = team.financialacc_set.all()
	
	if request.method == 'POST':
		trx = TransactionBudgetForm(request.POST)
		if trx.is_valid():
			typeTrx = request.POST.get('transTypeParam' , '')
			trxt = trx.save(commit = False)
			trxt.creator = acc
			trxt.budgetTrans =  currentAccFina.budget_set.all()[0]
			if typeTrx == 'isSpending':
				trxt.amount = trxt.amount * -1
			
			trxt.save()
	trxs = 	currentAccFina.budget_set.all()[0].transactionbudget_set.all()
	
	balance = 0 
	for t in trxs:
		balance += t.amount
		
	return render(request,'accBudget.html',{'user':getLogin(request),'currentAccFina':currentAccFina.name,'transBudget':trxs,'balance':balance})
