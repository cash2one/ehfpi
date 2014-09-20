from django.db import models

# FAQ for reviewers
class faqModel(models.Model):
    faqId = models.AutoField(primary_key=True)
    ctime = models.DateTimeField()
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.faqId)+' ' +self.question+' '+self.answer;
    class Meta:
        ordering = ['faqId']