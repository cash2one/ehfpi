from django.contrib import admin
from download.models import fieldDescription,registerModel,legacyModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin


#for import_export
class fieldDescriptionResource(resources.ModelResource):
    class Meta:
        model = fieldDescription

# Register your models here.
class FiledDescriptionAdmin(ImportExportModelAdmin):
    list_display = ('name','description')
    list_filter = ['name']
    search_fields = ['description']
    change_list_template = 'smuggler/change_list.html'
    resource_class = fieldDescriptionResource
    pass

#for import_export
class registerModelResource(resources.ModelResource):
    class Meta:
        model = registerModel

# Register your models here.
class registerModelAdmin(ImportExportModelAdmin):
    list_display = ('name','institute','city','country','email','time')
    list_filter = ['institute']
    search_fields = ['institute']
    change_list_template = 'smuggler/change_list.html'
    resource_class = registerModelResource
    pass

class legacyResource(resources.ModelResource):
    class Meta:
        model = legacyModel

# Register your models here.
class legacyAdmin(ImportExportModelAdmin):
    list_display = ('verId','name','releaseDate','description')
    list_filter = ['name']
    search_fields = ['description']
    class Media:
        css = {
            "all": ("/static/tinymce/tinymce.css",)
        }
        js = ["/static/tinymce/tinymce.min.js",
              "/static/tinymce/textareas.js",]

    change_list_template = 'smuggler/change_list.html'
    resource_class = legacyResource
    pass


# register the admin class
admin.site.register(fieldDescription,FiledDescriptionAdmin)
# register the admin class
admin.site.register(registerModel,registerModelAdmin)

admin.site.register(legacyModel,legacyAdmin)