from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^gea/$', views.gea, name='gea'),
    url(r'^network/$', views.network, name='network'),
    url(r'^networkAdvanced/$', views.networkAdvanced, name='networkAdvanced'),
    url(r'^geaAdvanced/$', views.geaAdvanced, name='geaAdvanced'),
    url(r'^pipAdvanced/$', views.pipAdvanced, name='pipAdvanced'),
    url(r'^downloadAdvanced/$', views.downloadAdvanced, name='downloadAdvanced'),
    url(r'^pipHeatmap/$', views.pipHeatmap, name='pipHeatmap'),
    url(r'^pipPreview/$', views.pipPreview, name='pipPreview'),
    url(r'^pip/$', views.pip, name='pip'),
    url(r'^download/$', views.download, name='download'),
    url(r'^quick/$', views.quickSearch, name='quickSearch'),
    url(r'^advanced/$', views.advancedSearch, name='advancedSearch'),
    url(r'^advanced/smartSubqueryParms/$', views.ajaxParms, name='ajaxParms'),
    url(r'^advanced/getSpecies/$', views.getSpecies, name='getSpecies'),
    url(r'^(?P<id>\w+)/$', views.searchDetail, name='searchDetail'),
)