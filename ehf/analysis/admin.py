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


'''
for DAVID annotations
'''
#for geneSymbolToDavidGeneName
class geneSymbolToDavidGeneNameResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToDavidGeneName

class geneSymbolToDavidGeneNameAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','davidGeneName')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','davidGeneName']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToDavidGeneNameResource
    pass

#for geneSymbolToGOBP
class geneSymbolToGOBPResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToGOBP

class geneSymbolToGOBPAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','gobp','gobpAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','gobp','gobpAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToGOBPResource
    pass

#for geneSymbolToGOCC
class geneSymbolToGOCCResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToGOCC

class geneSymbolToGOCCAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','gocc','goccAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','gocc','goccAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToGOCCResource
    pass

#for geneSymbolToGOMF
class geneSymbolToGOMFResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToGOMF

class geneSymbolToGOMFAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','gomf','gomfAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','gomf','gomfAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToGOMFResource
    pass


#for geneSymbolToPathwayBBID
class geneSymbolToPathwayBBIDResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToPathwayBBID

class geneSymbolToPathwayBBIDAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','BBID')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','BBID']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToPathwayBBIDResource
    pass

#for geneSymbolToPathwayBBID
class geneSymbolToPathwayBBIDResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToPathwayBBID

class geneSymbolToPathwayBBIDAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','BBID')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','BBID']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToPathwayBBIDResource
    pass

#for geneSymbolToPathwayKEGG
class geneSymbolToPathwayKEGGResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToPathwayKEGG

class geneSymbolToPathwayKEGGAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','KEGG','KEGGAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','KEGG','KEGGAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToPathwayKEGGResource
    pass

#for geneSymbolToPathwayPANTHER
class geneSymbolToPathwayPANTHERResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToPathwayPANTHER

class geneSymbolToPathwayPANTHERAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','PANTHER','PANTHERAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','PANTHER','PANTHERAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToPathwayPANTHERResource
    pass

#for geneSymbolToPathwayREACTOME
class geneSymbolToPathwayREACTOMEResource(resources.ModelResource):
    class Meta:
        model = geneSymbolToPathwayREACTOME

class geneSymbolToPathwayREACTOMEAdmin(ImportExportModelAdmin):
    list_display = ('geneSymbol','REACTOME','REACTOMEAnnotation')
    list_filter = ['geneSymbol']
    search_fields = ['geneSymbol','REACTOME','REACTOMEAnnotation']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneSymbolToPathwayREACTOMEResource
    pass

admin.site.register(geneSymbolToDavidGeneName,geneSymbolToDavidGeneNameAdmin)
admin.site.register(geneSymbolToGOBP,geneSymbolToGOBPAdmin)
admin.site.register(geneSymbolToGOCC,geneSymbolToGOCCAdmin)
admin.site.register(geneSymbolToGOMF,geneSymbolToGOMFAdmin)
admin.site.register(geneSymbolToPathwayBBID,geneSymbolToPathwayBBIDAdmin)
admin.site.register(geneSymbolToPathwayKEGG,geneSymbolToPathwayKEGGAdmin)
admin.site.register(geneSymbolToPathwayPANTHER,geneSymbolToPathwayPANTHERAdmin)
admin.site.register(geneSymbolToPathwayREACTOME,geneSymbolToPathwayREACTOMEAdmin)