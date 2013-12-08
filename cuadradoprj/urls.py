from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cuadrado.views.index'),
    url(r'^login/', 'cuadrado.views.login'),
    url(r'^creategroupview/', 'cuadrado.views.viewcreategroup'),
    url(r'^searchgroupview/', 'cuadrado.views.viewsearchgroup'),
    url(r'^searchgroup/', 'cuadrado.views.searchgroup'),
      url(r'^requestalliance/', 'cuadrado.views.requestAlliance'),
    url(r'^financialview/', 'cuadrado.views.viewfinancialinterest'),
    url(r'^typeaheadGroup/', 'cuadrado.views.serchNameGroup'),
     url(r'^typeaheadBudget/', 'cuadrado.views.serchBudgetTranx'),
    url(r'^homeview/', 'cuadrado.views.viewhome'),
    url(r'^creategroup/', 'cuadrado.views.creategroup'),
    url(r'^logout/', 'cuadrado.views.logout'),
    url(r'^grupos/', 'cuadrado.views.grupo'),
    url(r'^createfinancialAcc/', 'cuadrado.views.createFinancialAcc'),
    url(r'^createfinancialTran/', 'cuadrado.views.createFinancialTranx'),
    url(r'^homefinancialTrans/', 'cuadrado.views.financialAccByName'),
    url(r'^budgetfinancialTrans/', 'cuadrado.views.budgetByFinantialAcc'),
    url(r'^getMeGroupMessage/', 'cuadrado.views.getMeGroupMessage'),
    url(r'^procedAllianceRequest/', 'cuadrado.views.processAllianceRequest'),
    url(r'^budgetview/', 'cuadrado.views.viewBudget'),
    url(r'^disableBudgetTrx/', 'cuadrado.views.removeBudgetTrx'),
    url(r'^createfinancialTranBudget/', 'cuadrado.views.createBudgetTranx'),
    # url(r'^cuadradoprj/', include('cuadradoprj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

)
