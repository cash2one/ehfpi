from django.contrib import admin
from models import faqModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class faqResource(resources.ModelResource):
    class Meta:
        model = faqModel

class faqAdmin(ImportExportModelAdmin):
    list_display = ('faqId','ctime','question', 'answer')
    list_filter = ['ctime']
    search_fields = ['question']
    class Media:
        css = {
            "all": ("/static/tinymce/tinymce.css",)
        }
        js = ["/static/tinymce/tinymce.min.js",
              "/static/tinymce/textareas.js",]

    change_list_template = 'smuggler/change_list.html'

    resource_class = faqResource
    pass

# register the admin class
admin.site.register(faqModel,faqAdmin)