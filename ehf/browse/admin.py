from django.contrib import admin
from browse.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

#for import_export
class geneResource(resources.ModelResource):
    class Meta:
        model = gene

# class gene admin
class geneAdmin(ImportExportModelAdmin):
    list_display = ('geneAcc','geneSymbol', 'geneDescription','synonyms','uniprotId','targetOrganism')
    list_filter = ['targetOrganism']
    search_fields = ['geneSymbol']
    change_list_template = 'smuggler/change_list.html'
    resource_class = geneResource
    pass


#for import_export
class pathogenResource(resources.ModelResource):
    class Meta:
        model = pathogen

# class pathogen admin
class pathogenAdmin(ImportExportModelAdmin):
    list_display = ('pathogenAcc','strain', 'species','genus','family','group','kingdom')
    list_filter = ['species']
    search_fields = ['strain']
    change_list_template = 'smuggler/change_list.html'
    resource_class = pathogenResource
    pass

#for import_export
class publicationResource(resources.ModelResource):
    class Meta:
        model = publication

# class publication admin
class publicationAdmin(ImportExportModelAdmin):
    list_display = ('pubmedId','title', 'author','year','journal','articleFile')
    list_filter = ['title','journal','year']
    search_fields = ['title']
    change_list_template = 'smuggler/change_list.html'
    resource_class = publicationResource
    pass


#for import_export
class screenResource(resources.ModelResource):
    class Meta:
        model = screen

# class screen admin
class screenAdmin(ImportExportModelAdmin):
    list_display = ('screenAcc','scope', 'assayType','phenotype','reagent')
    list_filter = ['phenotype']
    search_fields = ['phenotype']
    change_list_template = 'smuggler/change_list.html'
    resource_class = screenResource
    pass


#for import_export
class interactionResource(resources.ModelResource):
    class Meta:
        model = interaction

class InteractionAdmin(ImportExportModelAdmin):
    list_display = ('ehfpiAcc','geneAcc', 'pathogenAcc','publicationAcc','screenAcc')  #in change list
    change_list_template = 'smuggler/change_list.html'
    resource_class = interactionResource
    pass

#for preview
class previewResource(resources.ModelResource):
    class Meta:
        model = previewModel

# class preview admin
class previewAdmin(ImportExportModelAdmin):
    list_display = ('title','pubmedId', 'phenotype','species','speciesTaxonomy')
    list_filter = ['phenotype']
    search_fields = ['phenotype']
    change_list_template = 'smuggler/change_list.html'
    resource_class = previewResource
    pass

#for preview
class previewSpeciesResource(resources.ModelResource):
    class Meta:
        model = previewSpeciesModel

# class preview admin
class previewSpeciesAdmin(ImportExportModelAdmin):
    list_display = ('title','pubmedId', 'phenotype','strain')
    list_filter = ['phenotype']
    search_fields = ['phenotype']
    change_list_template = 'smuggler/change_list.html'
    resource_class = previewSpeciesResource
    pass


# register the admin class
admin.site.register(gene,geneAdmin)
admin.site.register(pathogen,pathogenAdmin)
admin.site.register(publication,publicationAdmin)
admin.site.register(screen,screenAdmin)
admin.site.register(interaction,InteractionAdmin)
admin.site.register(previewModel,previewAdmin)
admin.site.register(previewSpeciesModel,previewSpeciesAdmin)


