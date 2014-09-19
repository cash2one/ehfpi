from django.contrib import admin
from models import news
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class newsResource(resources.ModelResource):
    class Meta:
        model = news

class newsAdmin(ImportExportModelAdmin):
    list_display = ('newsId','title', 'author','time','content')
    list_filter = ['time','author']
    search_fields = ['title','content']
    class Media:
        css = {
            "all": ("/static/tinymce/tinymce.css",)
        }
        js = ["/static/tinymce/tinymce.min.js",
              "/static/tinymce/textareas.js",]

    change_list_template = 'smuggler/change_list.html'

    resource_class = newsResource
    pass

# register the admin class
admin.site.register(news,newsAdmin)