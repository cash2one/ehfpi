from django.forms import ModelForm,Textarea
from analysis.models import networkModel

class networkForm(ModelForm):
    class Meta:
        model = networkModel
        widgets = {
            'geneList': Textarea(attrs={'cols': 60, 'rows': 8}),
        }
