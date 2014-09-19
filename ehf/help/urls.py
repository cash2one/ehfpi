from django.conf.urls import patterns, url

from help import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ehfHelp/$',views.ehfHelp,name='ehfHelp'),
    url(r'^searchHelp/$', views.searchHelp, name='searchHelp'),
    url(r'^browseHelp/$', views.browseHelp, name='browseHelp'),
    url(r'^analysisHelp/$', views.analysisHelp, name='analysisHelp'),
    url(r'^restHelp/$', views.restHelp, name='restHelp'),
    url(r'^citeHelp/$', views.citeHelp, name='citeHelp'),
)