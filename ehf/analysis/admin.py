from django.contrib import admin
from analysis.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

#for taxonomy
class taxonomyResource(resources.ModelResource):
    class Meta:
        model = taxonomy

# Register your models here.
class taxonomyAdmin(ImportExportModelAdmin):
    list_display = ('kingdom','kingdomTaxonomy', 'family','familyTaxonomy','genus','genusTaxonomy', 'species','speciesTaxonomy','pubmedId')
    list_filter = ['kingdom','family','genus','species']
    search_fields = ['kingdom','family','genus','species']
    change_list_template = 'smuggler/change_list.html'
    resource_class = taxonomyResource
    pass


#for heatmap
class heatmapModelResource(resources.ModelResource):
    class Meta:
        model = heatmapModel


class heatmapModelAdmin(ImportExportModelAdmin):
    list_display = ('a','b','level','commonGeneNumber','commonGeneList')
    list_filter = ['a','level']
    search_fields = ['a','level']
    change_list_template = 'smuggler/change_list.html'
    resource_class = heatmapModelResource
    pass

#for idNameMap
class idNameMapResource(resources.ModelResource):
    class Meta:
        model = idNameMap

class idNameMapAdmin(ImportExportModelAdmin):
    list_display = ('acc','type', 'name')
    list_filter = ['acc','type']
    search_fields = ['acc','type', 'name']
    change_list_template = 'smuggler/change_list.html'
    resource_class = idNameMapResource
    pass

#for vtpModel
class vtpModelResource(resources.ModelResource):
    class Meta:
        model = vtpModel

class vtpModelAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol', 'proteinName','uniprotId','virusTaxid','virusName','resources','note')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','resources']
    change_list_template = 'smuggler/change_list.html'
    resource_class = vtpModelResource
    pass

#for network
class networkModelResource(resources.ModelResource):
    class Meta:
        model = networkModel

class networkModelAdmin(ImportExportModelAdmin):
    list_display = ('geneList', 'file')
    search_fields = ['geneList']
    change_list_template = 'smuggler/change_list.html'
    resource_class = networkModelResource
    pass

#for gwas
class gwasResource(resources.ModelResource):
    class Meta:
        model = gwas

class gwasAdmin(ImportExportModelAdmin):
    list_display = ('pubmedId','disease','reportedGene','mappedGene')
    search_fields = ['disease','reportedGene']
    change_list_template = 'smuggler/change_list.html'
    resource_class = gwasResource
    pass

#for drug
class drugModelResource(resources.ModelResource):
    class Meta:
        model = drugModel

class drugModelAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','hgncId','uniprotId','proteinName','drugbankId','drugName','drugType')
    list_filter = ['drugType']
    search_fields = ['geneSymbol','drugName']
    change_list_template = 'smuggler/change_list.html'
    resource_class = drugModelResource
    pass

#for drug
class drugModelWithIntResource(resources.ModelResource):
    class Meta:
        model = drugModelWithInt

class drugModelWithIntAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','species','speciesTaxonomy','hgncId','uniprotId','proteinName','drugbankId','drugName','drugType')
    list_filter = ['drugType']
    search_fields = ['geneSymbol','drugName']
    change_list_template = 'smuggler/change_list.html'
    resource_class = drugModelWithIntResource
    pass

#for ppi
class ppiResource(resources.ModelResource):
    class Meta:
        model = ppi

class ppiAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol1','hprdId1','refseqId1','geneSymbol2','hprdId2','refseqId2','expType','pubmedId')
    list_filter = ['pubmedId']
    search_fields = ['geneSymbol1','geneSymbol2','hprdId1','hprdId2']
    change_list_template = 'smuggler/change_list.html'
    resource_class = ppiResource
    pass

#for overlapStatistics
class overlapStatisticsResource(resources.ModelResource):
    class Meta:
        model = overlapStatistics

class overlapStatisticsAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','speciesNumber','speciesList')
    list_filter = ['speciesNumber']
    search_fields = ['geneSymbol']
    change_list_template = 'smuggler/change_list.html'
    resource_class = overlapStatisticsResource
    pass

#for overlapDistribution
class overlapDistributionResource(resources.ModelResource):
    class Meta:
        model = overlapDistribution

class overlapDistributionAdmin(ImportExportModelAdmin):
    list_display = ('pathogenNumber','geneNumber','geneList','type')
    list_filter = ['pathogenNumber']
    search_fields = ['geneList']
    change_list_template = 'smuggler/change_list.html'
    resource_class = overlapDistributionResource
    pass

# register the admin class
admin.site.register(taxonomy,taxonomyAdmin)
admin.site.register(heatmapModel,heatmapModelAdmin)
admin.site.register(idNameMap,idNameMapAdmin)
admin.site.register(vtpModel,vtpModelAdmin)
admin.site.register(networkModel,networkModelAdmin)
admin.site.register(gwas,gwasAdmin)
admin.site.register(drugModel,drugModelAdmin)
admin.site.register(drugModelWithInt,drugModelWithIntAdmin)
admin.site.register(ppi,ppiAdmin)
admin.site.register(overlapStatistics,overlapStatisticsAdmin)
admin.site.register(overlapDistribution,overlapDistributionAdmin)