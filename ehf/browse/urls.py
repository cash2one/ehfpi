from django.conf.urls import patterns, url

from browse import views

urlpatterns = patterns('',
    url(r'^guide$', views.guide, name='guide'),
	url(r'^$', views.index, name='index'),
    url(r'^updateTable/$', views.updateTable, name='updateTable'),
    url(r'^updateBadge/$', views.updateBadge, name='updateBadge'),
    url(r'^download/$', views.download, name='download'),
    url(r'^gea/$', views.gea, name='gea'),
    url(r'^pip/$', views.pip, name='pip'),
    url(r'^network/$', views.network, name='network'),
    url(r'^kingdom/(?P<id>[\w -]+)/$', views.kingdom, name='kingdom'),
    url(r'^group/(?P<id>[\w + -]+)/$', views.group, name='group'),
    url(r'^family/(?P<id>[\w -]+)/$', views.family, name='family'),
    url(r'^genus/(?P<id>[\w -]+)/$', views.genus, name='genus'),
    url(r'^species/(?P<id>[\w .()-]+)/$', views.species, name='species'),
    url(r'^previewResult/$', views.previewResult, name='previewResult'),
)