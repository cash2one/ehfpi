from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.encoding import smart_str

# Create your models here.
# this class is for the field description in download
class fieldDescription(models.Model):
    databaseId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

# the model for register form
class registerModel(models.Model):
    # unicode too
    name = models.CharField(max_length=100)
    institute = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=255)
    email = models.EmailField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)

# legacy data
class legacyModel(models.Model):
    verId = models.CharField(max_length=100)  #version id
    name = models.CharField(max_length=100)  #version name
    releaseDate = models.DateTimeField()  #release date
    description = models.TextField()  #version summary