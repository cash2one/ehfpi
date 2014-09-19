from django.contrib import admin
from about.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

#for submitModel app
class submitModelResource(resources.ModelResource):
    class Meta:
        model = submitModel

# Register your models here.
class submitModelAdmin(ImportExportModelAdmin):
    list_display = ('name','institute', 'email','content')
    list_filter = ['institute','name']
    search_fields = ['content']
    change_list_template = 'smuggler/change_list.html'
    resource_class = submitModelResource
    pass

class submitFileModelResource(resources.ModelResource):
    class Meta:
        model = submitFileModel

# Register your models here.
class submitFileModelAdmin(ImportExportModelAdmin):
    list_display = ('file')
    change_list_template = 'smuggler/change_list.html'
    resource_class = submitFileModelResource
    pass

#for contactModel app
class contactModelResource(resources.ModelResource):
    class Meta:
        model = contactModel

class contactModelAdmin(ImportExportModelAdmin):
    list_display = ('title','email','content')
    list_filter = ['email']
    search_fields = ['content']
    class Media:
        css = {
            "all": ("/static/tinymce/tinymce.css",)
        }
        js = ["/static/tinymce/tinymce.min.js",
              "/static/tinymce/textareas.js",]
    change_list_template = 'smuggler/change_list.html'
    resource_class = contactModelResource
    pass

# register the admin class
admin.site.register(submitModel,submitModelAdmin)
admin.site.register(contactModel,contactModelAdmin)