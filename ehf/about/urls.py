from django.conf.urls import patterns, url

from about import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^siteIndex/$', views.siteIndex, name='siteIndex'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^submitHistory/$', views.submitHistory, name='submitHistory'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^copyright/$', views.copyright, name='copyright'),
    url(r'^externalLinks/$', views.external, name='external'),
    url(r'^thanks/$', views.thanks, name='thanks'),
)