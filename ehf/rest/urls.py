from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^select/$', views.select_entry.as_view()),
    #url(r'^ehfpi/$', views.EhfpiList.as_view()),
    #url(r'^ehfpi/(?P<pk>[0-9]+)/$', views.EhfpiDetail.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)