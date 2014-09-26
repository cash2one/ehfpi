from django.conf.urls import patterns, url

from analysis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^gea/$', views.gea, name='gea'),
    url(r'^gea/getGeneList$', views.getGeneList, name='getGeneList'),
    url(r'^gea/davidResult', views.davidResult, name='davidResult'),
    url(r'^gea/downAnnotationReport', views.downAnnotationReport, name='downAnnotationReport'),

    url(r'^overlap/$', views.overlapIndex, name='overlap'),
    url(r'^overlap/overlapNetwork$', views.overlapNetwork, name='overlapNetwork'),
    url(r'^overlap/displayNetwork$', views.displayNetwork, name='displayNetwork'),
    url(r'^overlap/downloadCSV', views.downloadCSV, name='downloadCSV'),
    url(r'^overlap/overlapHeatMap$', views.overlapHeatMap, name='overlapHeatMap'),
    url(r'^overlap/overlapHeatMapArticle$', views.overlapHeatMapArticle, name='overlapHeatMapArticle'),

    url(r'^overlap/displayHeatMap$', views.displayHeatMap, name='displayHeatMap'),
    url(r'^overlap/displayHeatMapArticle$', views.displayHeatMapArticle, name='displayHeatMapArticle'),

    url(r'^overlap/heatMapResult', views.heatMapResult, name='heatMapResult'),
    url(r'^overlap/statistics', views.statistics, name='statistics'),
    url(r'^overlap/downloadStatistics', views.downloadStatistics, name='downloadStatistics'),
    url(r'^overlap/distribution', views.distribution, name='distribution'),


    url(r'^pip/$', views.pip, name='pip'),
    url(r'^pip/getVTPList/$', views.getVTPList, name='getVTPList'),
    url(r'^pip/download/$', views.download, name='download'),
    url(r'^pip/network/$', views.network, name='network'),
    url(r'^pip/ppi/$', views.ppiOthers, name='ppiOthers'),
    url(r'^pip/displayPPI/$', views.displayPPI, name='displayPPI'),
    url(r'^gwas/$', views.gwasIndex, name='gwasIndex'),
    url(r'^gwas/download/$', views.gwasDownload, name='gwasDownload'),
    url(r'^gwas/gwasResults$', views.gwasResults, name='gwasResults'),
    url(r'^drug/$', views.drug, name='drug'),
    url(r'^drugResults/$', views.drugResults, name='drugResults'),
    url(r'^drug/download/$', views.drugDownload, name='drugDownload'),
    url(r'^drug/network/$', views.drugNetwork, name='drugNetwork'),
    url(r'^drug/displayNetwork/$', views.drugDisplayNetwork, name='drugDisplayNetwork'),
)