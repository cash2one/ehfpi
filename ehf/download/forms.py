from download.models import registerModel
from django.forms import ModelForm

class registerForm(ModelForm):
    class Meta:
        model = registerModel