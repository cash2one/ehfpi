from django.db import models
from analysis.formatChecker import ContentTypeRestrictedFileField

# Create your models here.
# the model for statistics to display pie chart
class kingdomStatistics(models.Model):
    kingdom = models.CharField(max_length=50,primary_key=True)
    speciesCount = models.IntegerField()   #number of species for this kingdom

    # display the class
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.kingdom+" "+str(self.speciesCount);

    #this is the view in the mysql database
    class Meta:
        managed = False
        db_table = 'kingdomStatisticsView'

# the model for sumbit form
class submitModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    institute = models.CharField(max_length=200)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = (("name", "email","institute"),)

class submitFileModel(models.Model):
    file = ContentTypeRestrictedFileField(upload_to='template/upload/', content_types=['Microsoft Office Document','Zip archive data, at least v2.0 to extract'],max_upload_size=10485760,blank=False, null=False)

    # the model for contact form
class contactModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    email = models.EmailField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)