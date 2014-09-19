from models import *
from django.db import models

# this is the model view of all the EHFPI data, we integrate the data for convenience
class allEHFPI(models.Model):
    ehfpiAcc = models.CharField(max_length=255,primary_key=True)
    #gene
    geneSymbol = models.CharField(max_length=255)
    geneDescription = models.CharField(max_length=255)  #!!added
    previousName = models.CharField(max_length=255)
    synonyms = models.CharField(max_length=255)
    entrezId = models.CharField(max_length=255)
    uniprotId = models.CharField(max_length=255)
    proteinName = models.CharField(max_length=255)
    ensemblGeneId = models.CharField(max_length=255)
    targetOrganism = models.CharField(max_length=255)
    drosophilaGene = models.CharField(max_length=255)
    humanHomolog = models.CharField(max_length=255)
    go = models.TextField()
    pathway = models.CharField(max_length=255)
    # chromosomeName = models.CharField(max_length=255)
    # geneStart = models.IntegerField()
    # geneEnd = models.IntegerField()
    isVTP = models.IntegerField()
    resources = models.CharField(max_length=255)
    geneNote = models.CharField(max_length=255)

    #pathogen
    fullName = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    aliases = models.CharField(max_length=255)
    strain = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    speciesTaxonomy = models.CharField(max_length=255)
    genus = models.CharField(max_length=255)
    genusTaxonomy = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    familyTaxonomy = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    kingdom = models.CharField(max_length=255)
    kingdomTaxonomy = models.IntegerField()

    #publication
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pubmedId = models.CharField(max_length=255)
    firstAuthor = models.CharField(max_length=255)
    year = models.IntegerField()
    journal = models.CharField(max_length=255)
    abstract = models.TextField()
    articleFile = models.FileField(upload_to='files/')
    doi = models.CharField(max_length=255)

    #screen
    scope = models.CharField(max_length=255)
    assayType = models.CharField(max_length=255)  #change from type
    reagent = models.CharField(max_length=255)
    targetOrganism = models.CharField(max_length=255)
    phenotype = models.CharField(max_length=255)
    #level = models.CharField(max_length=255)  #remove to gene note
    bioModelDescription = models.CharField(max_length=255)  #change from
    confirmatoryScreenDescription = models.CharField(max_length=255)
    primaryScreenDescription = models.CharField(max_length=255)
    hitsNumber = models.CharField(max_length=255)
    confirmedHitsNumber = models.CharField(max_length=255)
    primaryHitsNumber = models.CharField(max_length=255)
    screenNote = models.CharField(max_length=255);

    # display the class
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.ehfpiAcc)+" "+self.geneSymbol+" "+self.strain+" "+self.title;

    #this is the view in the mysql database
    class Meta:
        db_table = 'mainView'