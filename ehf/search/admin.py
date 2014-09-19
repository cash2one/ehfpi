from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from search.models import *

# Register your models here.
#for preview
class dasResource(resources.ModelResource):
    class Meta:
        model = das

# class preview admin
class dasAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','chromN', 'startN','stopN')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol']
    change_list_template = 'smuggler/change_list.html'
    resource_class = dasResource
    pass

admin.site.register(das,dasAdmin)