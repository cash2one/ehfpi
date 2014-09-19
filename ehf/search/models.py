from django.db import models

# Create your models here.
# can be integrate into gene model
class das(models.Model):
    geneSymbol = models.CharField(max_length=255)
    chromN = models.CharField(max_length=255)
    startN = models.CharField(max_length=255)
    stopN = models.CharField(max_length=255)