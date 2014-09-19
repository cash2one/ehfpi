from django.db import models

class gene(models.Model):
    geneAcc = models.CharField(max_length=255,primary_key=True)
    geneSymbol = models.CharField(max_length=255)
    geneDescription = models.CharField(max_length=255)
    previousName = models.CharField(max_length=255)
    synonyms = models.CharField(max_length=255)
    entrezId = models.CharField(max_length=255)
    uniprotId = models.CharField(max_length=255)
    proteinName = models.CharField(max_length=255)
    ensemblGeneId = models.CharField(max_length=255)
    targetOrganism = models.CharField(max_length=255)  #same as in screen, can be remove
    drosophilaGene = models.CharField(max_length=255)
    humanHomolog = models.CharField(max_length=255)  #changed
    go = models.TextField()
    pathway = models.CharField(max_length=255)
    # put into search.das
    # chromosomeName = models.CharField(max_length=255)
    # geneStart = models.IntegerField()
    # geneEnd = models.IntegerField()
    isVTP = models.IntegerField()
    resources = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.geneAcc)+" "+self.geneSymbol;


class pathogen(models.Model):
    pathogenAcc = models.CharField(max_length=255,primary_key=True)
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
    kingdomTaxonomy = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.pathogenAcc)+" "+self.strain;


# Create your models here.
class publication(models.Model):
    publicationAcc = models.CharField(max_length=255,primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pubmedId = models.CharField(max_length=255)
    firstAuthor = models.CharField(max_length=255)
    year = models.IntegerField()
    journal = models.CharField(max_length=255)
    abstract = models.TextField()
    articleFile = models.FileField(upload_to='files/')
    doi = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.pubmedId)+" "+self.title;

class screen(models.Model):
    screenAcc = models.CharField(max_length=255,primary_key=True)
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
    note = models.CharField(max_length=255);
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.screenAcc)+" "+self.scope+" "+self.assayType;

class interaction(models.Model):
    ehfpiAcc = models.CharField(max_length=255,primary_key=True)
    geneAcc = models.ForeignKey(gene)
    pathogenAcc = models.ForeignKey(pathogen)
    publicationAcc = models.ForeignKey(publication)
    screenAcc = models.ForeignKey(screen)
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.ehfpiAcc)+" "+str(self.geneAcc)+" "+str(self.pathogenAcc)+" "+str(self.publicationAcc)+" "+str(self.screenAcc);

#browse preview
class previewModel(models.Model):
    title = models.CharField(max_length=255)
    pubmedId = models.CharField(max_length=255)
    phenotype = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    speciesTaxonomy = models.CharField(max_length=255)

#browse preview for species
class previewSpeciesModel(models.Model):
    title = models.CharField(max_length=255)
    pubmedId = models.CharField(max_length=255)
    phenotype = models.CharField(max_length=255)
    strain = models.CharField(max_length=255)