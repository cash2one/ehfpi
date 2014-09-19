from django.conf.urls import patterns, include, url
from settings import *
from about.sitemapModel import EhfpiSitemap
from filebrowser.sites import site

from django.views.generic import RedirectView

from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

sitemaps = {
    'sitemap': EhfpiSitemap(['rest:index',
                             'search:index',
                             'search:quickSearch',
                             'search:advancedSearch',
                             'browse:index',
                             'analysis:index',
                             'analysis:gea',
                             'analysis:overlap',
                             'analysis:overlapNetwork',
                             'analysis:overlapHeatMap',
                             'analysis:overlapHeatMapArticle',
                             'analysis:pip',
                             'analysis:drug',
                             'analysis:gwasIndex',
                             'download:download',
                             'download:custom',
                             'news:index',
                             'about:index',
                             'about:statistics',
                             'about:siteIndex',
                             'about:submit',
                             'about:submitHistory',
                             'about:contact',
                             'about:external',
                             'help:searchHelp',
                             'help:browseHelp',
                             'help:analysisHelp',
                             'help:restHelp',
                             'help:citeHelp'
    ]),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ehf.views.home', name='home'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT, 'show_indexes': True}),
    url(r'^sitemap\.xml$', RedirectView.as_view(url='/static/sitemap.xml')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
    url(r'^rest/', include('rest.urls', namespace='rest')),
    url(r'^$', 'ehf.views.index'),
    url(r'^versionUpdate/$', 'ehf.views.versionUpdate'),
    url(r'^error/$', 'ehf.views.error'),

    #tools
    url(r'^getJson/$', 'ehf.views.getJson'),
    url(r'^google32523cba53827540.html/$', 'ehf.views.google'),
    url(r'^generateHeatmap/$', 'ehf.views.generateHeatmap'),
    url(r'^calOverlap/$', 'ehf.views.calOverlap'),

    url(r'^search/', include('search.urls', namespace="search")),
    url(r'^browse/', include('browse.urls', namespace="browse")),
    url(r'^analysis/', include('analysis.urls', namespace="analysis")),
    url(r'^download/', include('download.urls', namespace="download")),
    url(r'^about/', include('about.urls', namespace="about")),
    url(r'^help/', include('help.urls', namespace="help")),
    url(r'^news/', include('news.urls', namespace="news")),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
