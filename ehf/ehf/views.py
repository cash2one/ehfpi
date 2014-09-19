import json
from collections import defaultdict
import codecs
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from news.models import news
from browse.browse_view_models import allEHFPI
from browse.models import *
from analysis.models import idNameMap


#for google
def google(request):
    return render_to_response('google32523cba53827540.html')

#index page of the website
def index(request):
    all_news = news.objects.all()[0:4]
    mark = 0
    if len(news.objects.all()) > 4:
        mark = 1
    return render_to_response('index.html', {'news': all_news, 'mark': mark})


#verison too low for browser
def versionUpdate(request):
    return render_to_response('versionUpdate.html')


#error page
def error(request):
    return render_to_response('500.html')


# TOOLS #
# this function is for typeahead, return the required json file
def getJson(request):
    if request.method == 'GET':
        if request.GET['type']:  # with type param
            type = request.GET['type']
            resultList = []
            jsonList = []
            if type == 'gene':  # first we don't consider the QUERY
                result = gene.objects.all()
                for item in result:
                    if item.geneSymbol.find('{') > 0:  #Dro.
                        resultList.append(item.geneSymbol[0:item.geneSymbol.find('{')])
                    resultList.append(item.humanHomolog)
                    if ';' in item.previousName:
                        tmp = item.previousName.split(';')
                        for aa in tmp:
                            resultList.append(aa)
                    else:
                        resultList.append(item.previousName)

                    if ';' in item.synonyms:
                        tmp = item.synonyms.split(';')
                        for aa in tmp:
                            resultList.append(aa)
                    else:
                        resultList.append(item.synonyms)

                    resultList.append(item.entrezId)
                    resultList.append(item.uniprotId)
                    resultList.append(item.ensemblGeneId)
                resultList = list(set(resultList))
                if '' in resultList:
                    resultList.remove('')
                for item in resultList:
                    jsonDic = {}
                    jsonDic['gene'] = item
                    jsonList.append(jsonDic)

            elif type == 'pathogen':
                result = pathogen.objects.all()
                for item in result:
                    resultList.append(item.fullName)
                    resultList.append(item.abbreviation)
                    resultList.append(item.aliases)
                    resultList.append(item.strain)
                    resultList.append(item.species)
                    resultList.append(item.genus)
                    resultList.append(item.family)
                    resultList.append(item.group)
                    resultList.append(item.kingdom)
                resultList = list(set(resultList))
                if '' in resultList:
                    resultList.remove('')
                for item in resultList:
                    jsonDic = {}
                    jsonDic['pathogen'] = item
                    jsonList.append(jsonDic)

            elif type == 'publication':
                result = publication.objects.all()
                for item in result:
                    resultList.append(str(item.pubmedId))
                    resultList.append(item.title)
                    resultList.append(item.author)
                    resultList.append(item.journal)
                    resultList.append(str(item.year))
                resultList = list(set(resultList))
                if '' in resultList:
                    resultList.remove('')
                for item in resultList:
                    jsonDic = {}
                    jsonDic['publication'] = item
                    jsonList.append(jsonDic)

            else:
                result = allEHFPI.objects.all().values_list('ehfpiAcc')
                for item in result:
                    resultList.append(str(item[0]))
                resultList = list(set(resultList))
                if '' in resultList:
                    resultList.remove('')
                for item in resultList:
                    jsonDic = {}
                    jsonDic['acc'] = item
                    jsonList.append(jsonDic)
            return render_to_response('getJson.html', {'jsonList': json.dumps(jsonList)})


# TOOLS #
def generateHeatmap(request):
    ### parse rnai data
    '''
    file_in = codecs.open('C:/Users/jacky/Desktop/xdf/dro.txt','r','utf8')
    humanDict = {}
    title = ''
    id = ''
    for line in file_in:
        if line.startswith('#Publication Title'):
            title = line[line.find('=')+1:-1]
        if(line.startswith('#Pubmed ID')):
            id = line[line.find('=')+1:-1]
            humanDict[id] = title

    result = publication.objects.all().values_list('pubmedId')
    weList = []
    for item in result:
        weList.append(item[0])
    for key,value in humanDict.items():
        if key not in weList:
            print key+"\t"+value

    file_in.close()
    '''
    ###

    #file to write
    file_out = codecs.open('d:/taxonomy.txt', 'w', 'utf8')

    #1 generate kingdom level
    result = allEHFPI.objects.all()
    kingdomDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        kingdomTaxonomy = str(item.kingdomTaxonomy)
        if len(geneSymbol) and len(kingdomTaxonomy):  #not space
            if geneSymbol not in kingdomDict[kingdomTaxonomy]:
                kingdomDict[kingdomTaxonomy].append(geneSymbol)
    kingdomDict = dict(kingdomDict)
    keyList = []
    valueList = []
    for key, value in kingdomDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "kingdom" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)

    # 2 generate group level
    idName = idNameMap.objects.filter(type="group")
    idNameDict = {}
    for item in idName:
        idNameDict[item.name] = item.acc

    result = allEHFPI.objects.all()
    groupDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        groupName = item.group
        if len(groupName):
            groupAcc = idNameDict[groupName]
            if len(geneSymbol):  #not space
                if geneSymbol not in groupDict[groupAcc]:
                    groupDict[groupAcc].append(geneSymbol)

    groupDict = dict(groupDict)
    keyList = []
    valueList = []
    for key, value in groupDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "group" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)

    # 3 generate family level
    result = allEHFPI.objects.all()
    familyDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        familyTaxonomy = str(item.familyTaxonomy)
        if len(geneSymbol) and len(familyTaxonomy):  #not space
            if geneSymbol not in familyDict[familyTaxonomy]:
                familyDict[familyTaxonomy].append(geneSymbol)
    familyDict = dict(familyDict)

    keyList = []
    valueList = []
    for key, value in familyDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "family" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)

    # 4 generate genus level
    result = allEHFPI.objects.all()
    genusDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        genusTaxonomy = str(item.genusTaxonomy)
        if len(geneSymbol) and len(genusTaxonomy):  #not space
            if geneSymbol not in genusDict[genusTaxonomy]:
                genusDict[genusTaxonomy].append(geneSymbol)
    genusDict = dict(genusDict)

    keyList = []
    valueList = []
    for key, value in genusDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "genus" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)


    # 5 generate species level
    result = allEHFPI.objects.all()
    speciesDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        speciesTaxonomy = str(item.speciesTaxonomy)
        if len(geneSymbol) and len(speciesTaxonomy):  #not space
            if geneSymbol not in speciesDict[speciesTaxonomy]:
                speciesDict[speciesTaxonomy].append(geneSymbol)
    speciesDict = dict(speciesDict)

    keyList = []
    valueList = []
    for key, value in speciesDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "species" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)

    # 6 generate article level, a combination of species and pubmedid
    result = allEHFPI.objects.all()
    articleDict = defaultdict(list)  #key is kingdom name, value is genelist
    for item in result:
        geneSymbol = item.humanHomolog.strip().upper()
        speciesTaxonomy = str(item.speciesTaxonomy)
        pubmedId = str(item.pubmedId)
        if len(geneSymbol) and len(speciesTaxonomy) and len(pubmedId):  #not space
            if geneSymbol not in articleDict[speciesTaxonomy + "_" + pubmedId]:
                articleDict[speciesTaxonomy + "_" + pubmedId].append(geneSymbol)
    articleDict = dict(articleDict)

    keyList = []
    valueList = []
    for key, value in articleDict.items():
        keyList.append(key)
        valueList.append(value)

    for i in range(1, len(keyList) + 1):
        for j in range(i, len(keyList) + 1):
            res = list(set(valueList[i - 1]) & set(valueList[j - 1]))
            res_len = len(res)
            str_out = keyList[i - 1] + "\t" + keyList[j - 1] + "\t" + "article" + "\t" + str(res_len) + "\t" + ";".join(
                res) + "\r"
            file_out.write(str_out)

    file_out.close()

# this function calculate the overlap data for statistics map
def calOverlap(request):

    ''' First Graph
    #calculate species number
    pathogenNumberDict = defaultdict(int)
    result = pathogen.objects.all().values('kingdom','species').distinct()
    for item in result:
        pathogenNumberDict[item['kingdom']] += 1
    print 'Species number:'
    for key,value in pathogenNumberDict.items():
        print key+':'+str(value)

    # calculate overlap
    geneListDict = defaultdict(set)
    result = allEHFPI.objects.all().values('kingdom','humanHomolog').distinct()
    for item in result:
        if item['humanHomolog'] != '':
            geneListDict[item['kingdom']].add(item['humanHomolog'])
    print 'Gene number:'
    for key,value in geneListDict.items():
        print key+':'+str(len(value))

    print 'Overlap:'
    print 'Virus&Bacteria:'+str(len(geneListDict['Virus']&geneListDict['Bacteria']))
    print 'Virus&Fungi:'+str(len(geneListDict['Virus']&geneListDict['Fungi']))
    print 'Bacteria&Fungi:'+str(len(geneListDict['Bacteria']&geneListDict['Fungi']))
    print 'Bacteria&Fungi&Virus:'+str(len(geneListDict['Bacteria']&geneListDict['Fungi']&geneListDict['Virus']))
    '''

    #Second Graph, overview of EHFPI data
    groupDict = defaultdict()
    kingdomDict = defaultdict()
    result = pathogen.objects.all().values('kingdom','group','species').distinct()
    for item in result:
        groupDict[item['species']] = item['group']
        kingdomDict[item['species']] = item['kingdom']
    # print groupDict
    # print kingdomDict

    result = allEHFPI.objects.all().exclude(humanHomolog='').values('species','geneNote','humanHomolog').distinct()
    geneListDictConfirmed = defaultdict(list)
    geneNumberDictConfirmed = defaultdict(int)
    geneListDictPrimary = defaultdict(list)
    geneNumberDictPrimary = defaultdict(int)

    for item in result:
        if item['geneNote'] == 'confirmed hits':
            if item['humanHomolog'] not in geneListDictConfirmed[item['species']]:
                geneListDictConfirmed[item['species']].append(item['humanHomolog'])
                geneNumberDictConfirmed[item['species']] += 1
        else:
            if item['humanHomolog'] not in geneListDictPrimary[item['species']]:
                geneListDictPrimary[item['species']].append(item['humanHomolog'])
                geneNumberDictPrimary[item['species']] += 1

    # print geneNumberDictConfirmed
    # print geneListDictConfirmed
    # print geneNumberDictPrimary
    # print geneListDictPrimary
    print 'confirmed hits:'
    for key,value in geneNumberDictConfirmed.items():
        print key+'\t'+groupDict[key]+'\t'+kingdomDict[key]+'\t'+str(value)

    print 'primary hits'
    for key,value in geneNumberDictPrimary.items():
        print key+'\t'+groupDict[key]+'\t'+kingdomDict[key]+'\t'+str(value)