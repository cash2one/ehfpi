from django.conf.urls import patterns, url

from download import views

urlpatterns = patterns('',
    url(r'^$', views.custom, name='download'),
    url(r'^legacy/$', views.legacy, name='legacy'),
    url(r'^custom/$', views.custom, name='custom'),
    url(r'^register/$', views.register, name='register'),
    url(r'^downloadAll/$', views.downloadAll, name='downloadAll'),
    url(r'^gencsv/$', views.gencsv, name='gencsv'),
)