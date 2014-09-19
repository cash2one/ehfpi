from django.db import models
from formatChecker import ContentTypeRestrictedFileField

class taxonomy(models.Model):
    kingdom = models.CharField(max_length=255)
    kingdomTaxonomy = models.IntegerField()

    group = models.CharField(max_length=255)  #fungi has no group info

    # virus has family, bacteria has genus
    family = models.CharField(max_length=255)
    familyTaxonomy = models.IntegerField()

    genus = models.CharField(max_length=255)
    genusTaxonomy = models.IntegerField()

    species = models.CharField(max_length=255)
    speciesTaxonomy = models.IntegerField()

    strain = models.CharField(max_length=255)  #used in preview

    pubmedId = models.CharField(max_length=255)  #used to generated the gea tree and heatmap article tree

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.species);


#used to precalculate the common gene list
class heatmapModel(models.Model):
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    commonGeneNumber = models.IntegerField()
    commonGeneList = models.TextField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.a)+":"+str(self.b);

#not necessary, but can be used to simplify the id field of tree
class idNameMap(models.Model):
    acc = models.CharField(max_length=255)  # taxonomy, pubmed, gram, baltimore id
    type = models.CharField(max_length=255)  # type, kingdom, species, gram, baltimore
    name = models.CharField(max_length=255)  # corresponding name

#used to store the network analysis user provided data
class networkModel(models.Model):
    geneList = models.TextField(blank=True)
    file = ContentTypeRestrictedFileField(upload_to='networkFiles/', content_types=['text/plain',''],max_upload_size=5242880,blank=True, null=True)


class vtpModel(models.Model):
    geneSymbol = models.CharField(max_length=255)
    proteinName = models.CharField(max_length=255)
    uniprotId = models.CharField(max_length=255)
    resources = models.CharField(max_length=255)
    virusTaxid = models.CharField(max_length=255)
    virusName = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.geneSymbol+' '+self.virusName);

class gwasOriginal(models.Model):
    acc = models.CharField(max_length=255)
    dataAdded = models.TimeField()
    pubmedId = models.CharField(max_length=255)
    firstAuthor = models.CharField(max_length=255)
    date = models.TimeField()
    journal = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    study = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    initialSampleSize = models.CharField(max_length=255)
    replicationSampleSize = models.CharField(max_length=255)
    cytogeneticLoc = models.CharField(max_length=255)
    chrId = models.CharField(max_length=255)
    charPos = models.CharField(max_length=255)
    reportedGene = models.CharField(max_length=255)
    mappedGene = models.CharField(max_length=255)
    upstreamGeneId = models.CharField(max_length=255)
    downstreamGeneId = models.CharField(max_length=255)
    snpGeneId = models.CharField(max_length=255)
    upstreamGeneDistance = models.FloatField()
    downstreamGeneDistance = models.FloatField()
    strongSnpAllele = models.CharField(max_length=255)
    snps = models.CharField(max_length=255)
    merged = models.IntegerField()
    snpIdCurrent = models.IntegerField()
    context = models.CharField(max_length=255)
    interGenetic = models.IntegerField()
    riskAlleleFreq = models.FloatField()
    pvalue = models.FloatField()
    pvalueMLog = models.FloatField()
    pvalueText = models.CharField(max_length=255)
    orOrBeta = models.CharField(max_length=255)
    ci = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    cnv = models.CharField(max_length=255)


    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.disease+' '+self.mappedGene);

#add species info in gwas
class gwas(models.Model):
    acc = models.IntegerField(primary_key=True)
    species = models.CharField(max_length=255)
    speciesTaxonomy = models.CharField(max_length=255)
    dataAdded = models.TimeField()
    pubmedId = models.CharField(max_length=255)
    firstAuthor = models.CharField(max_length=255)
    date = models.TimeField()
    journal = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    study = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    initialSampleSize = models.CharField(max_length=255)
    replicationSampleSize = models.CharField(max_length=255)
    cytogeneticLoc = models.CharField(max_length=255)
    chrId = models.CharField(max_length=255)
    charPos = models.CharField(max_length=255)
    reportedGene = models.CharField(max_length=255)
    mappedGene = models.CharField(max_length=255)
    upstreamGeneId = models.CharField(max_length=255)
    downstreamGeneId = models.CharField(max_length=255)
    snpGeneId = models.CharField(max_length=255)
    upstreamGeneDistance = models.FloatField()
    downstreamGeneDistance = models.FloatField()
    strongSnpAllele = models.CharField(max_length=255)
    snps = models.CharField(max_length=255)
    merged = models.IntegerField()
    snpIdCurrent = models.IntegerField()
    context = models.CharField(max_length=255)
    interGenetic = models.IntegerField()
    riskAlleleFreq = models.FloatField()
    pvalue = models.FloatField()
    pvalueMLog = models.FloatField()
    pvalueText = models.CharField(max_length=255)
    orOrBeta = models.CharField(max_length=255)
    ci = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    cnv = models.CharField(max_length=255)


    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.disease+' '+self.mappedGene);

#model for drug
class drugModel(models.Model):
    acc = models.CharField(max_length=255)
    geneSymbol = models.CharField(max_length=255)
    hgncId = models.CharField(max_length=255)
    uniprotId = models.CharField(max_length=255)
    proteinName = models.CharField(max_length=255)

    drugbankId = models.CharField(max_length=255)
    drugName = models.CharField(max_length=255)
    drugType = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.geneSymbol+' '+self.drugbankId);

#model for drug does not contain pathogen species info, we generate this model with mysql view
#select `mainview`.`species` AS `species`,`mainview`.`speciesTaxonomy` AS `speciesTaxonomy`,`mainview`.`strain` AS `strain`,`analysis_drugmodel`.`geneSymbol` AS `geneSymbol`,`analysis_drugmodel`.`hgncId` AS `hgncId`,`analysis_drugmodel`.`uniprotId` AS `uniprotId`,`analysis_drugmodel`.`proteinName` AS `proteinName`,`analysis_drugmodel`.`drugbankId` AS `drugbankId`,`analysis_drugmodel`.`drugName` AS `drugName`,`analysis_drugmodel`.`drugType` AS `drugType` from (`mainview` join `analysis_drugmodel`) where (`mainview`.`humanHomolog` = `analysis_drugmodel`.`geneSymbol`) order by `mainview`.`species`
class drugModelWithInt(models.Model):
    acc = models.IntegerField(primary_key=True)
    species = models.CharField(max_length=255)
    speciesTaxonomy = models.CharField(max_length=255)
    strain = models.CharField(max_length=255)
    geneSymbol = models.CharField(max_length=255)
    hgncId = models.CharField(max_length=255)
    uniprotId = models.CharField(max_length=255)
    proteinName = models.CharField(max_length=255)

    drugbankId = models.CharField(max_length=255)
    drugName = models.CharField(max_length=255)
    drugType = models.CharField(max_length=255)
    drugGroup = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.species+' '+self.geneSymbol+' '+self.drugbankId+' '+self.drugGroup);

#ppi from HPRD database
class ppi(models.Model):
    geneSymbol1 = models.CharField(max_length=50)
    hprdId1 = models.CharField(max_length=10)
    refseqId1 = models.CharField(max_length=50)
    geneSymbol2 = models.CharField(max_length=50)
    hprdId2 = models.CharField(max_length=10)
    refseqId2 = models.CharField(max_length=50)
    expType = models.CharField(max_length=50)
    pubmedId = models.CharField(max_length=255)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.geneSymbol1+' '+self.geneSymbol2+' '+self.expType+' '+self.pubmedId);

#statistics page, the table is filled in the view, see detailed there
class overlapStatistics(models.Model):
    geneSymbol = models.CharField(max_length=50)
    speciesNumber = models.IntegerField()
    speciesList = models.TextField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.geneSymbol+' '+str(self.speciesNumber)+' '+self.speciesList);

#for distribution page, the table is filled in view
class overlapDistribution(models.Model):
    pathogenNumber = models.IntegerField()
    geneNumber = models.IntegerField()
    geneList = models.TextField()
    type = models.CharField(max_length=20)  #primary or confirmed(no primary)





