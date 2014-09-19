from django.db import models

# Create your models here.
class news(models.Model):
    newsId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    time = models.DateTimeField()
    content = models.TextField()
    #content = HTMLField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.newsId)+" "+self.title;
    class Meta:
        ordering = ['-time']