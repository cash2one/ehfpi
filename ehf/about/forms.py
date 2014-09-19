from about.models import submitModel,contactModel,submitFileModel
from django.forms import ModelForm,Textarea
from django.forms import TextInput

class submitForm(ModelForm):
    class Meta:
        model = submitModel
        widgets = {
            'content': Textarea(attrs={'cols': 100, 'rows': 8}),
        }

        error_messages = {
            'email': {
                'required':'email is required',
                'invalid': 'please input a valid email address'
            },
            'name':{
                'required':"name is required",
            },
            'institute':{
                'required':"institute is required",
            },
            'content':{
                'required': "content is required",
            }
        }

class submitFileForm(ModelForm):
    class Meta:
        model = submitFileModel

class contactForm(ModelForm):
    class Meta:
        model = contactModel
        widgets = {
            'content': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
        error_messages = {
            'email': {
                'required':'email is required',
                'invalid': 'please input a valid email address'
            },
            'title':{
                'required':"title is required",
            },
            'content':{
                'required': "content is required",
            }
        }
