from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from browse.browse_view_models import allEHFPI


class EhfpiSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def location(self, obj):
        return reverse(obj)