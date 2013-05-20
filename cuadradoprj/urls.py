from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cuadrado.views.index'),
    url(r'^login/', 'cuadrado.views.login'),
    url(r'^creategroup/', 'cuadrado.views.viewcreategroup'),
    url(r'^logout/', 'cuadrado.views.logout'),
    url(r'^home/', 'cuadrado.views.home'),
    # url(r'^cuadradoprj/', include('cuadradoprj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

)
