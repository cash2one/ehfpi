import csv
from collections import defaultdict
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.utils.encoding import smart_str, smart_unicode

from browse.browse_view_models import allEHFPI
from browse.models import publication, gene
from analysis.forms import networkForm
from ehf.settings import URL_PREFIX, PKL_DIR
from ehf.commonVar import fieldDic, field, fieldDes
from analysis.models import *





#serilization
import os
import cPickle as pickle
import hashlib

#chartit
from chartit import DataPool, Chart

# Create your views here.
def index(request):
    return render_to_response('analysis/index.html')


#create with article and taxonomy info, used in gea and network analysis
def generateTree():
    # construct tree
    resultB = taxonomy.objects.filter(kingdom="bacteria").values()
    resultV = taxonomy.objects.filter(kingdom="virus").values()
    resultF = taxonomy.objects.filter(kingdom="fungi").values()

    # generate tree view list
    treeB = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    treeV = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    treeF = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    tree_taxonomy = {}
    # bacteria
    for item in resultB:
        kingdom = item['kingdom']
        # virus has family, bacteria has genus
        genus = item['genus']
        species = item['species']
        pubmedId = item['pubmedId']

        #display author,journal and pubmed_id info
        pub = publication.objects.filter(pubmedId=pubmedId)[0]
        firstAuthor = pub.firstAuthor
        year = pub.year
        title = pub.title

        tree_taxonomy[kingdom] = item['kingdomTaxonomy']
        tree_taxonomy[genus] = item['genusTaxonomy']
        tree_taxonomy[species] = item['speciesTaxonomy']

        tree_taxonomy[firstAuthor + '-' + str(year) + '-' + title] = pubmedId

        if firstAuthor + '-' + str(year) + '-' + title not in treeB[kingdom][genus][species]:
            treeB[kingdom][genus][species].append(firstAuthor + '-' + str(year) + '-' + title)

    # virus
    for item in resultV:
        kingdom = item['kingdom']
        # virus has family, bacteria has genus
        family = item['family']
        species = item['species']
        pubmedId = item['pubmedId']

        #display author,journal and pubmed_id info
        pub = publication.objects.filter(pubmedId=pubmedId)[0]
        firstAuthor = pub.firstAuthor
        year = pub.year
        title = pub.title

        tree_taxonomy[kingdom] = item['kingdomTaxonomy']
        tree_taxonomy[family] = item['familyTaxonomy']
        tree_taxonomy[species] = item['speciesTaxonomy']

        tree_taxonomy[firstAuthor + '-' + str(year) + '-' + title] = pubmedId

        if firstAuthor + '-' + str(year) + '-' + title not in treeV[kingdom][family][species]:
            treeV[kingdom][family][species].append(firstAuthor + '-' + str(year) + '-' + title)


    # fungi
    for item in resultF:
        kingdom = item['kingdom']
        # virus has family, bacteria has genus, fungi we only use genus
        genus = item['genus']
        species = item['species']
        pubmedId = item['pubmedId']

        #display author,journal and pubmed_id info
        pub = publication.objects.filter(pubmedId=pubmedId)[0]
        firstAuthor = pub.firstAuthor
        year = pub.year
        title = pub.title

        tree_taxonomy[kingdom] = item['kingdomTaxonomy']
        tree_taxonomy[genus] = item['genusTaxonomy']
        tree_taxonomy[species] = item['speciesTaxonomy']

        tree_taxonomy[firstAuthor + '-' + str(year) + '-' + title] = pubmedId

        if firstAuthor + '-' + str(year) + '-' + title not in treeF[kingdom][genus][species]:
            treeF[kingdom][genus][species].append(firstAuthor + '-' + str(year) + '-' + title)

    # a three level tree
    for obj in treeB:
        treeB[obj].default_factory = None
        for item in treeB[obj]:
            treeB[obj][item].default_factory = None

    for obj in treeV:
        treeV[obj].default_factory = None
        for item in treeV[obj]:
            treeV[obj][item].default_factory = None

    for obj in treeF:
        treeF[obj].default_factory = None
        for item in treeF[obj]:
            treeF[obj][item].default_factory = None

    treeB = dict(treeB)
    treeV = dict(treeV)
    treeF = dict(treeF)
    tree = []
    tree.append(treeB)
    tree.append(treeV)
    tree.append(treeF)

    # calculate the badge number start
    # notice the number is based on human gene numbers
    #the number displayed in badge, we use four dict to avoid duplicate items in four field

    result = allEHFPI.objects.all()
    badge_taxonomy = defaultdict(int)
    kingdomGeneList = defaultdict(list)
    familyList = defaultdict(list)
    genusList = defaultdict(list)
    speciesList = defaultdict(list)
    speciesArticleList = defaultdict(list)
    allList = []

    for item in result:
        if item.humanHomolog != '':
            if item.humanHomolog not in allList:
                badge_taxonomy['all'] += 1
                allList.append(item.humanHomolog)

            if item.humanHomolog not in kingdomGeneList[item.kingdom]:
                badge_taxonomy[item.kingdom] += 1
                kingdomGeneList[item.kingdom].append(item.humanHomolog)

            if item.family != '':
                if item.humanHomolog not in familyList[item.family]:
                    badge_taxonomy[item.family] += 1
                    familyList[item.family].append(item.humanHomolog)

            if item.genus != '':
                if item.humanHomolog not in genusList[item.genus]:
                    badge_taxonomy[item.genus] += 1
                    genusList[item.genus].append(item.humanHomolog)

            if item.humanHomolog not in speciesList[item.species]:
                badge_taxonomy[item.species] += 1
                speciesList[item.species].append(item.humanHomolog)

            if item.humanHomolog not in speciesArticleList[item.species + '_' + item.firstAuthor + '-' + str(
                    item.year) + '-' + title]:
                badge_taxonomy[item.species + '_' + item.firstAuthor + '-' + str(item.year) + '-' + item.title] += 1
                speciesArticleList[
                    item.species + '_' + item.firstAuthor + '-' + str(item.year) + '-' + item.title].append(
                    item.humanHomolog)

    badge_taxonomy = dict(badge_taxonomy)

    #calculate the badge number end

    return tree, tree_taxonomy, badge_taxonomy


def gea(request):
    if os.path.isfile(PKL_DIR + '/gea.pkl'):  #have pickle
        file_out = file(PKL_DIR + '/gea.pkl', 'rb')
        tree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        badge_taxonomy = pickle.load(file_out)
        file_out.close()
    else:
        tree, tree_taxonomy, badge_taxonomy = generateTree()
        #generate pickle
        file_gea = file(PKL_DIR + '/gea.pkl', 'wb')
        pickle.dump(tree, file_gea, True)
        pickle.dump(tree_taxonomy, file_gea, True)
        pickle.dump(badge_taxonomy, file_gea, True)
        file_gea.close()

    return render_to_response('analysis/gea.html',
                              {'tree': tree, 'tree_taxonomy': tree_taxonomy, 'badge_taxonomy': badge_taxonomy},
                              context_instance=RequestContext(request))


# given a species list, return the related gene list
def getGeneList(request):
    if request.method == 'GET':
        pathogen = request.GET.getlist('pathogen[]')

        speciesList = []
        articleList = []
        for item in pathogen:
            if item.startswith('species'):
                speciesList.append(item[item.find('_') + 1:])
            if item.startswith('article'):
                articleList.append(item[item.find('_') + 1:])

        #a article may contain several species, a species may contain several article. So if species is selected, all article
        # under it must be selected too, if a article is selected, we must use and between it and its species!!!
        qTotal = Q()
        for item in articleList:
            speciesItem = item[0:item.find('_')]
            pubmedIdItem = item[item.find('_') + 1:]
            qTotal = qTotal | (Q(speciesTaxonomy=speciesItem) & Q(pubmedId=pubmedIdItem))

        qTotal = qTotal | Q(speciesTaxonomy__in=speciesList)

        result = allEHFPI.objects.filter(qTotal)
        geneList = []
        for item in result:
            geneList.append(item.humanHomolog)
        geneList = list(set(geneList))

        if '' in geneList:
            geneList.remove('')

        return render_to_response('analysis/getGeneList.html', {'geneList': ','.join(geneList)})


#added: 20140925 return david result
def davidResult(request):
    if request.method == 'GET':
        pathogen = request.GET['pathogen'].split(',')

        speciesList = []
        articleList = []
        for item in pathogen:
            if item.startswith('species'):
                speciesList.append(item[item.find('_') + 1:])
            if item.startswith('article'):
                articleList.append(item[item.find('_') + 1:])

        #a article may contain several species, a species may contain several article. So if species is selected, all article
        # under it must be selected too, if a article is selected, we must use and between it and its species!!!
        qTotal = Q()
        for item in articleList:
            speciesItem = item[0:item.find('_')]
            pubmedIdItem = item[item.find('_') + 1:]
            qTotal = qTotal | (Q(speciesTaxonomy=speciesItem) & Q(pubmedId=pubmedIdItem))

        qTotal = qTotal | Q(speciesTaxonomy__in=speciesList)

        result = allEHFPI.objects.filter(qTotal)
        geneList = []
        for item in result:
            geneList.append(item.humanHomolog)
        geneList = list(set(geneList))

        if '' in geneList:
            geneList.remove('')

        #detail page for each item, we use the same function but different param to simplify the implementation
        if 'type' in request.GET:
            type = request.GET['type']
            geneResultList = []
            if type == 'bp':
                AnnoResult = geneSymbolToGOBP.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.gobp: item.gobpAnnotation})

                result = dict(result)

            elif type == 'cc':
                AnnoResult = geneSymbolToGOCC.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.gocc: item.goccAnnotation})

                result = dict(result)

            elif type == 'mf':
                AnnoResult = geneSymbolToGOMF.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.gomf: item.gomfAnnotation})

                result = dict(result)

            elif type == 'BBID':
                AnnoResult = geneSymbolToPathwayBBID.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append(item.BBID)

                result = dict(result)

            elif type == 'KEGG':
                AnnoResult = geneSymbolToPathwayKEGG.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.KEGG: item.KEGGAnnotation})

                result = dict(result)

            elif type == 'PANTHER':
                AnnoResult = geneSymbolToPathwayPANTHER.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.PANTHER: item.PANTHERAnnotation})

                result = dict(result)

            elif type == 'REACTOME':
                AnnoResult = geneSymbolToPathwayREACTOME.objects.filter(geneSymbol__in=geneList)
                recordNum = len(AnnoResult)

                #same geneSymbol aggregate
                result = defaultdict(list)
                for item in AnnoResult:
                    result[item.geneSymbol.upper()].append({item.REACTOME: item.REACTOMEAnnotation})

                result = dict(result)


            else:
                return HttpResponseRedirect(
                    URL_PREFIX + '/analysis/gea/')  #we do not direct to the result page otherwise the query page

            #here return the detail page
            # maybe we need to query the gene model to get gene name first since the gene name provided by DAVID is not accurate
            for item in AnnoResult.values_list('geneSymbol').distinct():
                geneResultList.append(item[0])

            print len(geneResultList)
            geneNameDict = {}
            tmpRes = gene.objects.filter(humanHomolog__in=geneResultList).values('humanHomolog',
                                                                                 'geneDescription').distinct()
            for item in tmpRes:
                geneNameDict[item['humanHomolog']] = item['geneDescription']

            return render_to_response('analysis/davidDetail.html',
                                      {'geneNameDict': geneNameDict, 'result': result, 'type': type,
                                       'recordNum': recordNum})

        #statistics default
        bpNum = len(geneSymbolToGOBP.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        ccNum = len(geneSymbolToGOCC.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        mfNum = len(geneSymbolToGOMF.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        BBID = len(geneSymbolToPathwayBBID.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        KEGG = len(geneSymbolToPathwayKEGG.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        PANTHER = len(
            geneSymbolToPathwayPANTHER.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())
        REACTOME = len(
            geneSymbolToPathwayREACTOME.objects.filter(geneSymbol__in=geneList).values_list('geneSymbol').distinct())

        print len(geneList)
        print bpNum, ccNum, mfNum, BBID, KEGG, PANTHER, REACTOME

        #used to visualize the bar width
        maxGO = max(bpNum, ccNum, mfNum)
        maxPathway = max(BBID, KEGG, PANTHER, REACTOME)

    return render_to_response('analysis/davidResult.html',
                              {'geneList': ','.join(geneList), 'bpNum': bpNum, 'ccNum': ccNum, 'mfNum': mfNum,
                               'BBID': BBID,
                               "KEGG": KEGG, "PANTHER": PANTHER, 'REACTOME': REACTOME, 'maxGO': maxGO,
                               'maxPathway': maxPathway})


def downAnnotationReport(request):
    if 'type' in request.GET and 'pathogen' in request.GET:  #

        #get gene list
        pathogen = request.GET['pathogen'].split(',')
        speciesList = []
        articleList = []
        for item in pathogen:
            if item.startswith('species'):
                speciesList.append(item[item.find('_') + 1:])
            if item.startswith('article'):
                articleList.append(item[item.find('_') + 1:])

        #a article may contain several species, a species may contain several article. So if species is selected, all article
        # under it must be selected too, if a article is selected, we must use and between it and its species!!!
        qTotal = Q()
        for item in articleList:
            speciesItem = item[0:item.find('_')]
            pubmedIdItem = item[item.find('_') + 1:]
            qTotal = qTotal | (Q(speciesTaxonomy=speciesItem) & Q(pubmedId=pubmedIdItem))

        qTotal = qTotal | Q(speciesTaxonomy__in=speciesList)

        result = allEHFPI.objects.filter(qTotal)
        geneList = []
        for item in result:
            geneList.append(item.humanHomolog)
        geneList = list(set(geneList))

        if '' in geneList:
            geneList.remove('')

        #get annotations
        type = request.GET['type']
        if type == 'bp':
            AnnoResult = geneSymbolToGOBP.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'gobp', 'gobpAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'gobp': 'GO id',
                                  'gobpAnnotation': 'Annotation'
            }


        elif type == 'cc':
            AnnoResult = geneSymbolToGOCC.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'gocc', 'goccAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'gocc': 'GO id',
                                  'goccAnnotation': 'Annotation'
            }

        elif type == 'mf':
            AnnoResult = geneSymbolToGOMF.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'gomf', 'gomfAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'gomf': 'GO id',
                                  'gomfAnnotation': 'Annotation'
            }

        elif type == 'BBID':
            AnnoResult = geneSymbolToPathwayBBID.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'BBID']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'BBID': 'BBID',
            }


        elif type == 'KEGG':
            AnnoResult = geneSymbolToPathwayKEGG.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'KEGG','KEGGAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'KEGG': 'KEGG ID',
                                  'KEGGAnnotation':'KEGG Annotation'
            }

        elif type == 'PANTHER':
            AnnoResult = geneSymbolToPathwayPANTHER.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'PANTHER','PANTHERAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'PANTHER': 'PANTHER ID',
                                  'PANTHERAnnotation':'PANTHER Annotation'
            }

        elif type == 'REACTOME':
            AnnoResult = geneSymbolToPathwayREACTOME.objects.filter(geneSymbol__in=geneList).values()
            selectcolumn = ['geneSymbol', 'REACTOME','REACTOMEAnnotation']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'REACTOME': 'REACTOME ID',
                                  'REACTOMEAnnotation':'REACTOME Annotation'
            }
        else:
            pass

        response = HttpResponse(content_type="text/csv")
        response.write('\xEF\xBB\xBF')
        response['Content-Disposition'] = 'attachment; filename=david.csv'
        writer = csv.writer(response)

        # store row title description
        rowTitle = []
        for item in selectcolumn:
            rowTitle.append(fieldDesStatistics[item])
        writer.writerow(rowTitle)

        #get data from database
        for item in AnnoResult:
            res = []
            for i in selectcolumn:
                res.append(smart_str(item[i]))
            writer.writerow(res)
        return response

    return HttpResponseRedirect(
        URL_PREFIX + '/analysis/gea/')  #we do not direct to the result page otherwise the query page


def overlapIndex(request):
    return render_to_response('analysis/overlap.html')


#this function process the file and return the gene symbol list
def handle_uploaded_file(uploadFile):
    geneList = []
    if 'file' in uploadFile:
        oriText = ''
        for chunk in uploadFile['file'].chunks():
            oriText += chunk
        oriText = oriText.strip()
        geneListTemp = []
        if oriText.find(',') > 0:
            geneListTemp = oriText.split(',')
        elif oriText.find('\r') > 0:
            geneListTemp = oriText.split('\r')
        elif oriText.find('\n') > 0:
            geneListTemp = oriText.split('\n')
        else:
            geneListTemp = oriText.split('\r\n')

        geneList = []
        for item in geneListTemp:
            geneList.append(item.strip())

        geneList = list(set(geneList))
        if 'None' in geneList:
            geneList.remove('None')

        if '' in geneList:
            geneList.remove('')

    return geneList


def overlapNetwork(request):
    #jsTreeList store pathogen tree
    #geneList store input gene List
    #request.FILES['file'] store uploaded file
    if request.method == 'POST':
        form = networkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            #process jsTreeList and get gene list
            geneList1 = []

            #we want to put species submitted above all others, so we must store it in a separate list
            aboveSpeciesList = []

            pathogen = request.POST['jsTreeList'].strip()
            name = '-'.join(pathogen)
            name = 'network-' + hashlib.md5(name).hexdigest()

            if len(pathogen):
                if os.path.isfile(PKL_DIR + '/' + name + '.pkl'):  #have pickle
                    file_out = file(PKL_DIR + '/' + name + '.pkl', 'rb')
                    geneList1 = pickle.load(file_out)
                    file_out.close()
                else:

                    pathogen = pathogen.split(',')
                    speciesList = []
                    articleList = []
                    for item in pathogen:
                        if item.startswith('species'):
                            speciesList.append(item[item.find('_') + 1:])
                        if item.startswith('article'):
                            articleList.append(item[item.find('_') + 1:])

                    idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                    speciesNameList = []
                    for item in idMap:
                        speciesNameList.append(item.name)

                        if item.name not in aboveSpeciesList:
                            aboveSpeciesList.append(item.name)

                    idMap = idNameMap.objects.filter(type='species')
                    speciesDict = {}
                    for item in idMap:
                        speciesDict[item.acc] = item.name

                    #a article may contain several species, a species may contain several article. So if species is selected, all article
                    # under it must be selected too, if a article is selected, we must use and between it and its species!!!
                    taxo = taxonomy.objects.all()
                    articleDict = defaultdict(list)
                    for item in taxo:  #store pubmed id for each species
                        articleDict[item.species].append(item.pubmedId)
                    for key, value in articleDict.items():
                        articleDict[key] = list(set(value))

                    qTotal = Q()
                    for item in articleList:
                        speciesItem = item[0:item.find('_')]
                        if speciesDict[speciesItem] not in aboveSpeciesList:
                            aboveSpeciesList.append(speciesDict[speciesItem])

                        pubmedIdItem = item[item.find('_') + 1:]
                        qTotal = qTotal | (Q(species=speciesDict[speciesItem]) & Q(pubmedId=pubmedIdItem))

                    qTotal = qTotal | Q(species__in=speciesNameList)

                    result = allEHFPI.objects.filter(qTotal)

                    for item in result:
                        geneList1.append(item.humanHomolog)  #not gene symbol, since it contains dro.
                    geneList1 = list(set(geneList1))

                    #generate pickle
                    file_network = file(PKL_DIR + '/' + name + '.pkl', 'wb')
                    pickle.dump(geneList1, file_network, True)
                    file_network.close()

            geneList1 = list(set(geneList1))
            if '' in geneList1:
                geneList1.remove('')

            #process geneList
            geneList2Temp = request.POST['geneList'].strip()
            geneList2 = []
            if len(geneList2Temp):
                if geneList2Temp.find(',') > 0:
                    geneList2Temp = geneList2Temp.split(',')
                elif geneList2Temp.find('\r') > 0:
                    geneList2Temp = geneList2Temp.split('\r')
                elif geneList2Temp.find('\n') > 0:
                    geneList2Temp = geneList2Temp.split('\n')
                else:
                    geneList2Temp = geneList2Temp.split('\r\n')

            for item in geneList2Temp:
                geneList2.append(item.strip())

            geneList2 = list(set(geneList2))
            if '' in geneList2:
                geneList2.remove('')

            #parse uploaded file
            geneList3 = handle_uploaded_file(request.FILES)

            geneList = geneList1 + geneList2 + geneList3
            geneList = list(set(geneList))

            return render_to_response('analysis/overlapNetworkOthers.html',
                                      {'geneList': ','.join(geneList), 'aboveSpeciesList': ';'.join(aboveSpeciesList)},
                                      context_instance=RequestContext(request))
    else:
        form = networkForm()

    if os.path.isfile(PKL_DIR + '/network.pkl'):  #have pickle
        file_out = file(PKL_DIR + '/network.pkl', 'rb')
        tree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        badge_taxonomy = pickle.load(file_out)
        file_out.close()
    else:
        tree, tree_taxonomy, badge_taxonomy = generateTree()
        #generate pickle
        file_network = file(PKL_DIR + '/network.pkl', 'wb')
        pickle.dump(tree, file_network, True)
        pickle.dump(tree_taxonomy, file_network, True)
        pickle.dump(badge_taxonomy, file_network, True)
        file_network.close()

    return render_to_response('analysis/overlapNetwork.html',
                              {'tree': tree, 'tree_taxonomy': tree_taxonomy, 'form': form,
                               'badge_taxonomy': badge_taxonomy}, context_instance=RequestContext(request))


def displayNetwork(request):
    if request.method == 'POST' and 'text' in request.POST:
        aboveSpeciesList = []
        if 'aboveSpeciesList' in request.POST:
            tmp = request.POST['aboveSpeciesList'].strip()
            if len(tmp):
                if ';' in tmp:
                    aboveSpeciesList = tmp.split(';')
                else:
                    aboveSpeciesList.append(tmp)

        genes = request.POST['text'].split(',')
        geneList = []
        for i in genes:
            if len(i.strip()):
                geneList.append(i.strip())
        geneList = list(set(geneList))  # query gene list
        if '' in geneList:
            geneList.remove('')

        if len(geneList):
            result = allEHFPI.objects.filter(humanHomolog__in=geneList).values()  #relation list we get
            gene_result_tuble = allEHFPI.objects.filter(humanHomolog__in=geneList).values_list(
                'humanHomolog').distinct()
            pathogen_result_tuble = allEHFPI.objects.filter(humanHomolog__in=geneList).values_list('species').distinct()
            gene_result = []  # gene list we get
            pathogen_result = []  # pathogen list we get
            for i in gene_result_tuble:
                gene_result.append(i[0])
            for i in pathogen_result_tuble:
                pathogen_result.append(i[0])

            # generate interaction map start
            jsonRes = []  # a list
            lineIndex = 0
            # generate json file
            for item in geneList:  # generate gene node
                boolIn = 0  # upper case how????
                itemStandard = ""
                for k in gene_result:
                    if k.upper() == item.upper():
                        boolIn = 1
                        itemStandard = k

                if boolIn:  # gene in database
                    node = {}
                    node['name'] = itemStandard  # name attr
                    #node['name'] = ''
                    node['id'] = itemStandard  #id attr

                    data = {}  #data attr
                    data['$type'] = 'circle'
                    data['nodeType'] = 'gene'
                    for j in result:
                        if j['humanHomolog'].upper() == item.upper():
                            data['des'] = j['geneDescription']
                            break

                    # set adjacencies attr
                    adjacencies = []
                    adjacenciesNumber = 0
                    for j in result:
                        if j['humanHomolog'].upper() == item.upper():
                            relation = {}
                            relation['nodeTo'] = j['species']
                            relation['nodeFrom'] = itemStandard
                            nodeData = {}  # can overwrite
                            lineIndex += 1
                            #nodeData["$labelid"] = "lineIndex"+str(lineIndex)
                            #nodeData["$labeltext"] = j['phenotype']
                            #phenote has three types, inhibit, enhance, other
                            if j['phenotype'] == 'Inhibited infection':
                                nodeData["$color"] = "#8b0000"
                            elif j['phenotype'] == 'Increased infection':
                                nodeData["$color"] = "#339900"
                            else:  #other type,neither inhibit nor enhance
                                nodeData["$color"] = "#23A4FF"

                            relation['data'] = nodeData
                            adjacencies.append(relation)
                            adjacenciesNumber = adjacenciesNumber + 1  #calculate common and specific gene

                    node['adjacencies'] = adjacencies
                    if adjacenciesNumber > 1:
                        data['$color'] = '#416D9C'
                    else:
                        data['$color'] = '#800080'

                    node['data'] = data

                    jsonRes.append(node)

                else:  # solidate node
                    node = {}
                    node['name'] = item  # name attr
                    node['id'] = item  #id attr

                    data = {}  #data attr
                    data['$color'] = 'red'
                    data['$type'] = 'triangle'
                    data['des'] = 'this gene is not in EHFPI'
                    data['nodeType'] = 'gene'
                    node['data'] = data

                    adjacencies = []
                    node['adjacencies'] = adjacencies
                    jsonRes.append(node)

            for item in pathogen_result:  # generate pathogen node
                node = {}
                node['name'] = item  # name attr
                #node['name'] = ''
                node['id'] = item  #id attr

                data = {}  #data attr
                data['$color'] = '#EBB056'
                data['$type'] = 'star'
                data['$dim'] = 8
                data['nodeType'] = 'species'
                strain_list = []
                for j in result:
                    if j['species'].upper() == item.upper():
                        strain_list.append(j['strain'])
                strain_list = list(set(strain_list))
                data['des'] = '_'.join(strain_list)
                node['data'] = data

                # set adjacencies attr
                adjacencies = []
                for j in result:
                    if j['species'].upper() == item.upper():
                        relation = {}
                        relation['nodeTo'] = j['humanHomolog']
                        relation['nodeFrom'] = item
                        nodeData = {}  # can overwrite
                        relation['data'] = nodeData
                        adjacencies.append(relation)
                node['adjacencies'] = adjacencies
                jsonRes.append(node)
            toJson = json.dumps(jsonRes)
            # generate interaction map end

            # calculate gene number of each species
            speciesNumber = defaultdict(list)
            for item in result:
                speciesNumber[item['species']].append(item['humanHomolog'])

            speciesNumber = dict(speciesNumber)
            for key, value in speciesNumber.items():
                speciesNumber[key] = len(list(set(value)))

            #store the species submitted above
            speciesNumberAbove = {}
            for item in aboveSpeciesList:
                if item in speciesNumber.keys():
                    speciesNumberAbove[item] = speciesNumber[item]
                    speciesNumber.pop(item)

            # calculate gene number of each species end

            return render_to_response('analysis/displayNetwork.js',
                                      {'toJson': toJson, 'speciesNumber': sorted(speciesNumber.iteritems()),
                                       'speciesNumberAbove': sorted(speciesNumberAbove.iteritems())},
                                      context_instance=RequestContext(request))
        else:  # empty
            return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork',
                                        context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork',
                                    context_instance=RequestContext(request))


#added : 20140812
#function: download the EHF-pathogen graph as a csv file
def downloadCSV(request):
    if request.method == 'POST' and 'text' in request.POST:

        genes = request.POST['text'].split(',')
        geneList = []
        for i in genes:
            if len(i.strip()):
                geneList.append(i.strip())
        geneList = list(set(geneList))  # query gene list
        if '' in geneList:
            geneList.remove('')

        if len(geneList):
            result_specific = overlapStatistics.objects.filter(geneSymbol__in=geneList, speciesNumber=1).order_by(
                'geneSymbol').values()
            result_common = overlapStatistics.objects.filter(geneSymbol__in=geneList, speciesNumber__gt=1).order_by(
                'geneSymbol').values()

        #now generate csv file
        selectcolumnCSV = ['geneSymbol', 'speciesNumber', 'speciesList']
        # code from download app
        fieldDesCSV = {'geneSymbol': 'Gene Symbol',
                       'speciesNumber': 'Pathogen Number',
                       'speciesList': 'Pathogen List'
        }

        response = HttpResponse(content_type="text/csv")
        response.write('\xEF\xBB\xBF')
        response['Content-Disposition'] = 'attachment; filename=network.csv'
        writer = csv.writer(response)

        # store row title description
        #common gene summary
        if len(result_common):
            writer.writerow(['Common Gene Summary'])
            rowTitle = []
            for item in selectcolumnCSV:
                rowTitle.append(fieldDesCSV[item])
            writer.writerow(rowTitle)

            #get data from database
            for item in result_common:
                res = []
                for i in selectcolumnCSV:
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            writer.writerow([])

        # store row title description
        # specific gene summary
        if len(result_specific):
            writer.writerow(['Specific Gene Summary'])
            rowTitle = []
            for item in selectcolumnCSV:
                rowTitle.append(fieldDesCSV[item])
            writer.writerow(rowTitle)

            #get data from database
            for item in result_specific:
                res = []
                for i in selectcolumnCSV:
                    res.append(smart_str(item[i]))
                writer.writerow(res)
        return response

    return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork',
                                context_instance=RequestContext(request))


def overlapHeatMap(request):
    if os.path.isfile(PKL_DIR + '/overlap.pkl'):  #have pickle
        file_out = file(PKL_DIR + '/overlap.pkl', 'rb')
        tree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        file_out.close()
    else:

        # construct tree tree
        resultB = taxonomy.objects.filter(kingdom="bacteria").values()
        resultV = taxonomy.objects.filter(kingdom="virus").values()
        resultF = taxonomy.objects.filter(kingdom="fungi").values()

        # generate tree view list
        treeB = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        treeV = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        treeF = defaultdict(lambda: defaultdict(list))

        #used to map group id
        groupRes = idNameMap.objects.filter(type='group')
        groupDic = {}
        for item in groupRes:
            groupDic[item.name] = item.acc

        tree_taxonomy = {}
        # bacteria
        for item in resultB:
            kingdom = item['kingdom']
            group = item['group']
            # virus has family, bacteria has genus
            genus = item['genus']
            species = item['species']

            tree_taxonomy[kingdom] = item['kingdomTaxonomy']
            tree_taxonomy[group] = groupDic[item['group']]
            tree_taxonomy[genus] = item['genusTaxonomy']
            tree_taxonomy[species] = item['speciesTaxonomy']
            if species not in treeB[kingdom][group][genus]:
                treeB[kingdom][group][genus].append(species)

        # virus
        for item in resultV:
            kingdom = item['kingdom']
            group = item['group']
            # virus has family, bacteria has genus
            family = item['family']
            species = item['species']

            tree_taxonomy[kingdom] = item['kingdomTaxonomy']
            tree_taxonomy[group] = groupDic[item['group']]
            tree_taxonomy[family] = item['familyTaxonomy']
            tree_taxonomy[species] = item['speciesTaxonomy']

            if species not in treeV[kingdom][group][family]:
                treeV[kingdom][group][family].append(species)

        # fungi
        for item in resultF:
            kingdom = item['kingdom']
            # virus has family, bacteria has genus, fungi we only use genus, and it has no group info
            genus = item['genus']
            species = item['species']

            tree_taxonomy[kingdom] = item['kingdomTaxonomy']
            tree_taxonomy[genus] = item['genusTaxonomy']
            tree_taxonomy[species] = item['speciesTaxonomy']

            if species not in treeF[kingdom][genus]:
                treeF[kingdom][genus].append(species)

        # a three level tree for fungi, four level for bacteria and fungi
        for obj in treeB:
            treeB[obj].default_factory = None
            for subItem in treeB[obj]:
                treeB[obj][subItem].default_factory = None

        for obj in treeV:
            treeV[obj].default_factory = None
            for subItem in treeV[obj]:
                treeV[obj][subItem].default_factory = None

        for obj in treeF:
            treeF[obj].default_factory = None

        treeB = dict(treeB)
        treeV = dict(treeV)
        treeF = dict(treeF)
        tree = []
        tree.append(treeB)
        tree.append(treeV)
        tree.append(treeF)
        # print tree
        # print tree_taxonomy

        # for aa in tree:
        #     for kingdom,value in aa.items():
        #         print kingdom
        #         for species,strainList in value.items():
        #             print "++"+species
        #             for strain in strainList:
        #                 print "++++"+strain

        #generate pickle
        file_overlap = file(PKL_DIR + '/overlap.pkl', 'wb')
        pickle.dump(tree, file_overlap, True)
        pickle.dump(tree_taxonomy, file_overlap, True)
        file_overlap.close()

    return render_to_response('analysis/overlapHeatMap.html', {'tree': tree, 'tree_taxonomy': tree_taxonomy},
                              context_instance=RequestContext(request))


def overlapHeatMapArticle(request):
    result = taxonomy.objects.all()
    article = {}

    for item in result:
        species = item.species
        speciesTaxonomy = item.speciesTaxonomy  #species name may have blanks, we use taxonomyId
        pubmedId = item.pubmedId

        pub = publication.objects.filter(pubmedId=pubmedId)[0]
        firstAuthor = pub.firstAuthor
        year = pub.year
        title = pub.title
        article[str(speciesTaxonomy) + '_' + str(pubmedId)] = species + ' [' + firstAuthor + '-' + str(
            year) + '-' + title + ']'

    return render_to_response('analysis/overlapHeatMapArticle.html', {'article': article},
                              context_instance=RequestContext(request))


def displayHeatMap(request):
    if request.method == 'POST':
        level = request.POST['level']
        #print level
        pathogenList = request.POST.getlist('pathogen[]')
        #print pathogenList

        name = '-'.join(pathogenList)  #too long
        name = level + '-' + hashlib.md5(name).hexdigest()

        if len(pathogenList):
            if os.path.isfile(PKL_DIR + '/' + name + '.pkl'):  #have pickle
                file_out = file(PKL_DIR + '/' + name + '.pkl', 'rb')
                data = pickle.load(file_out)
                file_out.close()
            else:

                # get the dict
                result = idNameMap.objects.all()
                taxonomyDict = {}
                for item in result:
                    taxonomyDict[item.acc] = item.name

                data = {}
                if level == 'kingdom':  # kingdom level
                    kingdomList = []
                    for item in pathogenList:
                        if item.startswith('kingdom'):
                            kingdomList.append(item[item.find('_') + 1:])
                    # construct the json struct
                    nodes = []
                    for i, item in enumerate(kingdomList):
                        node = {}
                        node['name'] = taxonomyDict[item]
                        node['acc'] = item  # this is used to generate nice url in the heatmap
                        node['group'] = i + 1  # one kingdom, one group
                        nodes.append(node)
                    links = []
                    # print kingdomList
                    for i in range(0, len(kingdomList)):
                        for j in range(i, len(kingdomList)):
                            res = heatmapModel.objects.filter(
                                (Q(a=kingdomList[i]) & Q(b=kingdomList[j])) | (
                                    Q(a=kingdomList[j]) & Q(b=kingdomList[i])))
                            link = {}
                            for item in res:
                                link['source'] = i
                                link['target'] = j
                                link['value'] = item.commonGeneNumber
                                link['commonGene'] = item.commonGeneList
                                links.append(link)

                    data['nodes'] = nodes
                    data['links'] = links
                    data['type'] = 'kingdom'

                elif level == 'group':  # group level, only one group is allowed, so we detect it in js
                    groupList = []
                    for item in pathogenList:
                        if item.startswith('group'):
                            groupList.append(item[item.find('_') + 1:])
                    # construct the json struct
                    nodes = []
                    for i, item in enumerate(groupList):
                        node = {}
                        node['name'] = taxonomyDict[item]
                        node['acc'] = item  # this is used to generate nice url in the heatmap
                        node['group'] = i + 1  # one kingdom, one group
                        nodes.append(node)
                    links = []
                    # print kingdomList
                    for i in range(0, len(groupList)):
                        for j in range(i, len(groupList)):
                            res = heatmapModel.objects.filter(
                                (Q(a=groupList[i]) & Q(b=groupList[j])) | (Q(a=groupList[j]) & Q(b=groupList[i])))
                            link = {}
                            for item in res:
                                link['source'] = i
                                link['target'] = j
                                link['value'] = item.commonGeneNumber
                                link['commonGene'] = item.commonGeneList
                                links.append(link)

                    data['nodes'] = nodes
                    data['links'] = links
                    data['type'] = 'group'

                elif level == 'family':  # family level, only virus will be considered
                    familyList = []
                    for item in pathogenList:
                        if item.startswith('family'):
                            familyList.append(item[item.find('_') + 1:])
                    # construct the json struct
                    nodes = []
                    for i, item in enumerate(familyList):
                        node = {}
                        node['name'] = taxonomyDict[item]
                        node['acc'] = item  # this is used to generate nice url in the heatmap
                        node['group'] = i + 1  # one family, one group, because only virus
                        nodes.append(node)
                    links = []
                    # print familyList
                    for i in range(0, len(familyList)):
                        for j in range(i, len(familyList)):
                            res = heatmapModel.objects.filter(
                                (Q(a=familyList[i]) & Q(b=familyList[j])) | (Q(a=familyList[j]) & Q(b=familyList[i])))
                            link = {}
                            for item in res:
                                link['source'] = i
                                link['target'] = j
                                link['value'] = item.commonGeneNumber
                                link['commonGene'] = item.commonGeneList
                                links.append(link)

                    data['nodes'] = nodes
                    data['links'] = links
                    data['type'] = 'family'

                elif level == 'genus':  # genus level
                    genusList = []
                    for item in pathogenList:
                        if item.startswith('genus'):
                            genusList.append(item[item.find('_') + 1:])
                    # construct the json struct
                    nodes = []
                    for i, item in enumerate(genusList):
                        node = {}
                        node['name'] = taxonomyDict[item]
                        node['acc'] = item  # this is used to generate nice url in the heatmap
                        node['group'] = i + 1  # grouped based on family or genus
                        nodes.append(node)
                    links = []
                    # print genusList
                    for i in range(0, len(genusList)):
                        for j in range(i, len(genusList)):
                            res = heatmapModel.objects.filter(
                                (Q(a=genusList[i]) & Q(b=genusList[j])) | (Q(a=genusList[j]) & Q(b=genusList[i])))
                            link = {}
                            for item in res:
                                link['source'] = i
                                link['target'] = j
                                link['value'] = item.commonGeneNumber
                                link['commonGene'] = item.commonGeneList
                                links.append(link)

                    data['nodes'] = nodes
                    data['links'] = links
                    data['type'] = 'genus'

                elif level == 'species':  # species level
                    speciesList = []
                    for item in pathogenList:
                        if item.startswith('species'):
                            speciesList.append(item[item.find('_') + 1:])
                    # construct the json struct
                    nodes = []
                    group = {}  #group id dict, acc:groupid
                    i = 0
                    for item in speciesList:
                        node = {}
                        node['name'] = taxonomyDict[item]
                        node['acc'] = item  # this is used to generate nice url in the heatmap

                        parent = getParent(item)
                        # print parent
                        if group.has_key(parent):
                            node['group'] = group[parent]  # one genus one group, otherwise only fungi and bacteria
                        else:
                            node['group'] = i
                            group[parent] = i
                            i += 1
                        nodes.append(node)

                    links = []
                    # print speciesList
                    for i in range(0, len(speciesList)):
                        for j in range(i, len(speciesList)):
                            res = heatmapModel.objects.filter(
                                (Q(a=speciesList[i]) & Q(b=speciesList[j])) | (
                                    Q(a=speciesList[j]) & Q(b=speciesList[i])))
                            link = {}
                            for item in res:
                                link['source'] = i
                                link['target'] = j
                                link['value'] = item.commonGeneNumber
                                link['commonGene'] = item.commonGeneList
                                links.append(link)

                    data['nodes'] = nodes
                    data['links'] = links
                    data['type'] = 'species'
                else:
                    return render_to_response('analysis/overlapHeatMap.html', context_instance=RequestContext(request))

                #generate pickle
                file_heatmap = file(PKL_DIR + '/' + name + '.pkl', 'wb')
                pickle.dump(data, file_heatmap, True)
                file_heatmap.close()

            return render_to_response('analysis/displayHeatMap.js', {'data': json.dumps(data)},
                                      context_instance=RequestContext(request))

    return render_to_response('analysis/overlapHeatMap.html', context_instance=RequestContext(request))


# article tree
def displayHeatMapArticle(request):
    if request.method == 'POST':
        articleList = request.POST.getlist('article[]')
        name = '-'.join(articleList)  #too long
        name = "article-" + hashlib.md5(name).hexdigest()

        # print articleList
        if len(articleList):
            if os.path.isfile(PKL_DIR + '/' + name + '.pkl'):  #have pickle
                file_out = file(PKL_DIR + '/' + name + '.pkl', 'rb')
                data = pickle.load(file_out)
                file_out.close()
            else:

                data = {}
                article = []
                for item in articleList:
                    if item.startswith('article'):  #article: speciesTaxonomy_pubmedId
                        article.append(item[item.find('_') + 1:])

                #display pathogen name
                result = idNameMap.objects.all()
                taxonomyDict = {}
                for item in result:
                    taxonomyDict[item.acc] = item.name

                # construct the json struct
                nodes = []
                for i, item in enumerate(article):
                    node = {}
                    spe = item[0:item.find('_')]
                    art = item[item.find('_') + 1:]
                    res = publication.objects.filter(pubmedId=art)[0]
                    #print res.firstAuthor, res.year
                    node['name'] = taxonomyDict[spe] + '[' + res.firstAuthor + ',' + str(res.year) + ']'
                    node['acc'] = item  # this is used to generate nice url in the heatmap
                    node['group'] = i + 1  # one kingdom, one group
                    nodes.append(node)
                links = []
                # print article
                for i in range(0, len(article)):
                    for j in range(i, len(article)):
                        res = heatmapModel.objects.filter(
                            (Q(a=article[i]) & Q(b=article[j])) | (Q(a=article[j]) & Q(b=article[i])))
                        link = {}
                        for item in res:
                            link['source'] = i
                            link['target'] = j
                            link['value'] = item.commonGeneNumber
                            link['commonGene'] = item.commonGeneList
                            links.append(link)

                data['nodes'] = nodes
                data['links'] = links
                data['type'] = 'article'
                # print data

                #generate pickle
                file_heatmap = file(PKL_DIR + '/' + name + '.pkl', 'wb')
                pickle.dump(data, file_heatmap, True)
                file_heatmap.close()

            return render_to_response('analysis/displayHeatMap.js', {'data': json.dumps(data)},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('analysis/overlapHeatMapArticle.html', context_instance=RequestContext(request))


#given a species taxonomy id, get the genus or family parent taxonomy id
def getParent(child):
    result = taxonomy.objects.filter(speciesTaxonomy=child)
    for res in result:
        familyTaxonomy = res.familyTaxonomy
        genusTaxonomy = res.genusTaxonomy
    return familyTaxonomy + genusTaxonomy


# return a list of result in the heatmap click
def heatMapResult(request):
    if request.method == 'GET':

        #change columns?
        if 'columns' in request.GET:
            selectedColumns_tmp = request.GET['columns']
            selectedColumns = selectedColumns_tmp.split(',')
            request.session['has_changed'] = True  # set the session, not change
            request.session['selectedColumns'] = selectedColumns  #store the columns

        if 'has_changed' not in request.session:
            defaultColumns = ['ehfpiAcc', 'geneSymbol', 'entrezId', 'strain', 'title']
            request.session['selectedColumns'] = defaultColumns  #store the columns

        a = request.GET['a']
        b = request.GET['b']
        type = request.GET['type']
        searchList = []
        searchList.append(a)
        searchList.append(b)
        searchList = list(set(searchList))
        searchName = []

        if type == 'article':  #for article, species_taxonomy, pubmed id
            speciesList = []
            articleList = []
            for item in searchList:
                speciesTemp = item[0:item.find('_')]
                articleTemp = item[item.find('_') + 1:]
                if speciesTemp not in speciesList:
                    speciesList.append(speciesTemp)
                if articleTemp not in articleList:
                    articleList.append(articleTemp)

        elif type == 'group':
            idMap = idNameMap.objects.filter(acc__in=searchList)
            for item in idMap:
                if item.acc in searchList:
                    searchName.append(item.name)
        else:
            searchName = searchList

        res = heatmapModel.objects.filter((Q(a=a) & Q(b=b)) | (Q(a=b) & Q(b=a)))
        geneList_temp = ''
        for item in res:
            geneList_temp = smart_unicode(item.commonGeneList)
        geneList = geneList_temp.split(';')

        result = ''
        if type == 'kingdom':
            result = allEHFPI.objects.filter(kingdomTaxonomy__in=searchName, humanHomolog__in=geneList)
            # print result
        elif type == 'group':
            result = allEHFPI.objects.filter(group__in=searchName, humanHomolog__in=geneList)
        elif type == 'family':
            result = allEHFPI.objects.filter(familyTaxonomy__in=searchName, humanHomolog__in=geneList)
        elif type == 'genus':
            result = allEHFPI.objects.filter(genusTaxonomy__in=searchName, humanHomolog__in=geneList)
        elif type == 'species':
            result = allEHFPI.objects.filter(speciesTaxonomy__in=searchName, humanHomolog__in=geneList)
        elif type == 'article':
            result = allEHFPI.objects.filter(speciesTaxonomy__in=speciesList, pubmedId__in=articleList,
                                             humanHomolog__in=geneList)
            #print result
        else:
            result = ''

        #custom display columns start!
        columns = []
        for i in range(0, len(field), 1):
            columns.append([field[i], fieldDes[i]])
        #custom display columns end

        #columns to display start!
        displayColumns = request.session['selectedColumns']
        displayColumnsDic = []
        for item in displayColumns:
            displayColumnsDic.append([item, fieldDic[item]])
            #columns to display end

        # use the method of advanced search
        idsList = []
        for item in result:
            idsList.append(str(item.ehfpiAcc))
        ids = ','.join(idsList)

        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'ehfpiAcc')
            result = result.order_by(order)

        #get publication number and EHF gene number
        publicationNum = len(set(result.values_list('title')))

        geneList1 = []
        for item in result.values_list('humanHomolog'):
            geneList1.append(item[0].strip().upper())
        geneList1 = list(set(geneList1))
        if '' in geneList1:
            geneList1.remove('')
        ehfNum = len(geneList1)

        #end

        return render_to_response('search/heatMapSearchResult.html',
                                  {'result': result, 'publicationNum': publicationNum, 'ehfNum': ehfNum,
                                   'columns': columns, 'displayColumnsDic': displayColumnsDic, 'ids': ids},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('analysis/overlapHeatMap.html', context_instance=RequestContext(request))


#added: 20140710
#return the table which list the pathogen list of a specific gene, this function can facilitate broad - spectrum drug design
def statistics(request):
    '''# We can calculate every time, but store the data into database is a better choice, so we can fetch data from database directly
    result = allEHFPI.objects.all().values('humanHomolog','strain','species')
    numberDict = defaultdict(int)
    speciesDict = defaultdict(list)
    for item in result:
        if item['species'] not in speciesDict[item['humanHomolog']]:
            numberDict[item['humanHomolog']] += 1
            speciesDict[item['humanHomolog']].append(item['species'])

    if '' in numberDict.keys():
        numberDict.pop('')

    if '' in speciesDict.keys():
        speciesDict.pop('')

    numberDict = dict(numberDict)
    speciesDict = dict(speciesDict)

    for key,value in numberDict.items():
        p1 = overlapStatistics(geneSymbol=key,speciesNumber=value,speciesList=','.join(speciesDict[key]))
        p1.save()

    '''
    result = overlapStatistics.objects.all().order_by('-speciesNumber')
    if (len(result)):
        order = request.GET.get('order_by', '-speciesNumber')
        result = result.order_by(order)

    if 'geneSymbol' in request.GET:
        geneSymbol = request.GET['geneSymbol']
        geneSymbolListTmp = []
        if ',' in geneSymbol:
            geneSymbolListTmp = geneSymbol.split(',')
        elif ';' in geneSymbol:
            geneSymbolListTmp = geneSymbol.split(';')
        else:
            geneSymbolListTmp.append(geneSymbol)

        geneSymbolList = []
        for item in geneSymbolListTmp:
            if item.strip() != '':
                geneSymbolList.append(item.strip())

        if len(geneSymbolList):
            result = result.filter(geneSymbol__in=geneSymbolList)

    idsList = []
    for item in result:
        idsList.append(item.geneSymbol)
    ids = ','.join(idsList)

    interactions = len(result)

    return render_to_response('analysis/overlapStatistics.html',
                              {'result': result, 'ids': ids, 'interactions': interactions},
                              context_instance=RequestContext(request))


#download the gene and related pathogen list
def downloadStatistics(request):
    if request.method == 'POST':
        print 'hello'
        if 'selected[]' in request.POST:
            selected = request.POST.getlist('selected[]')
            print selected

            data = overlapStatistics.objects.filter(geneSymbol__in=selected).values()

            selectcolumn = ['geneSymbol', 'speciesNumber', 'speciesList']
            # code from download app
            fieldDesStatistics = {'geneSymbol': 'Gene Symbol',
                                  'speciesNumber': 'pathogen Number',
                                  'speciesList': 'pathogen List'
            }

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=statistics.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in selectcolumn:
                rowTitle.append(fieldDesStatistics[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in data:
                res = []
                for i in selectcolumn:
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect(URL_PREFIX)


#this function gives the graph representation of primary as well as confirmed hits distribution
def distribution(request):
    '''
    result = allEHFPI.objects.exclude(humanHomolog='').values('humanHomolog','species','geneNote')

    # store intermediate variable
    allNumberDict = defaultdict(int)
    allSpeciesDict = defaultdict(list)
    confirmedNumberDict = defaultdict(int)
    confirmedSpeciesDict = defaultdict(list)
    primaryNumberDict = defaultdict(int)
    primarySpeciesDict = defaultdict(list)

    for item in result:
        if item['species'] not in allSpeciesDict[item['humanHomolog']]:
                allNumberDict[item['humanHomolog']] += 1
                allSpeciesDict[item['humanHomolog']].append(item['species'])

        if item['geneNote'] == 'confirmed hits': #confirmed hits
            if item['species'] not in confirmedSpeciesDict[item['humanHomolog']]:
                confirmedNumberDict[item['humanHomolog']] += 1
                confirmedSpeciesDict[item['humanHomolog']].append(item['species'])
        else:
            if item['species'] not in primarySpeciesDict[item['humanHomolog']]:
                primaryNumberDict[item['humanHomolog']] += 1
                primarySpeciesDict[item['humanHomolog']].append(item['species'])

    print confirmedNumberDict
    print primaryNumberDict

    #next we convert the intermediate into final result
    allNumberDict = dict(allNumberDict)
    confirmedNumberDict = dict(confirmedNumberDict)
    primaryNumberDict = dict(primaryNumberDict)

    #for all
    allFinalNumber = defaultdict(int)
    allFinalList = defaultdict(list)
    for key,value in allNumberDict.items():
        allFinalNumber[value] += 1
        allFinalList[value].append(key)

    allFinalNumber = dict(allFinalNumber)
    allFinalList = dict(allFinalList)
    for key,value in allFinalNumber.items():
        p1 = overlapDistribution(pathogenNumber=key,geneNumber=value,geneList=','.join(allFinalList[key]),type='all')
        p1.save()

    #for confirmed
    confirmedFinalNumber = defaultdict(int)
    confirmedFinalList = defaultdict(list)
    for key,value in confirmedNumberDict.items():
        confirmedFinalNumber[value] += 1
        confirmedFinalList[value].append(key)

    confirmedFinalNumber = dict(confirmedFinalNumber)
    confirmedFinalList = dict(confirmedFinalList)
    for key,value in confirmedFinalNumber.items():
        p1 = overlapDistribution(pathogenNumber=key,geneNumber=value,geneList=','.join(confirmedFinalList[key]),type='confirmed hits')
        p1.save()

    #for primary
    primaryFinalNumber = defaultdict(int)
    primaryFinalList = defaultdict(list)

    for key,value in primaryNumberDict.items():
        primaryFinalNumber[value] += 1
        primaryFinalList[value].append(key)

    primaryFinalNumber = dict(primaryFinalNumber)
    primaryFinalList = dict(primaryFinalList)
    for key,value in primaryFinalNumber.items():
        p1 = overlapDistribution(pathogenNumber=key,geneNumber=value,geneList=','.join(primaryFinalList[key]),type='primary hits')
        p1.save()
    '''

    dsAll = DataPool(
        series=
        [{'options': {
            'source': overlapDistribution.objects.filter(type='all')},
          'terms': [
              'pathogenNumber',
              'geneNumber'
          ]}
        ])

    allColumn = Chart(
        datasource=dsAll,
        series_options=
        [{'options': {
            'type': 'column'},
          'terms': {
              'pathogenNumber': [
                  'geneNumber']
          }}],
        chart_options=
        {
            'chart': {
                'backgroundColor': '#F3F3FF',
                'borderWidth': 1,
                'borderRadius': 5,
                'plotBackgroundColor': '#ffffff',
                'plotShadow': 'false',
                'plotBorderWidth': 0,
                'plotBorderColor': 'black',
                'spacingRight': 30
            },
            'title': {
                'text': 'Distribution of EHFs',
                'style': {
                    'fontWeight': 'bold'
                }
            },
            'subtitle': {
                'text': 'all EHF genes (confirmed and primary hits)'
            },
            'xAxis': {
                'title': {
                    'text': 'Pathogen Number'},
                'gridLineWidth': 1,
                'labels': {
                    'style': {
                        'color': 'black'
                    }
                },
                'lineColor': 'black',
                'lineWidth': 1

            },
            'yAxis': {
                'title': {
                    'text': 'EHF Gene Number'},
                'gridLineWidth': 1,
                'minorTickInterval': 'auto',
                'type': 'logarithmic',  #'linear', 'logarithmic' and 'datetime'
                'labels': {
                    'style': {
                        'color': 'black'
                    }
                },
                'lineColor': 'black',
                'lineWidth': 1

            },
            'tooltip': {
                'backgroundColor': '#ffffff',
                'borderColor': '#4572A7',
                'borderRadius': 2,
                'borderWidth': 1
            },
            'legend': {
                'align': 'left',
                'verticalAlign': 'top',
                'floating': 'true'
            },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 1,
                    'color': '#4572A7',
                },
                'series': {
                    'shadow': 'true',
                    'dataLabels': {
                        'enabled': 'true',
                        'color': '#4572A7'
                    }
                }
            },
        })

    dsPrimary = DataPool(
        series=
        [{'options': {
            'source': overlapDistribution.objects.filter(type='primary hits')},
          'terms': [
              'pathogenNumber',
              'geneNumber'

          ]}
        ])

    primaryColumn = Chart(
        datasource=dsPrimary,
        series_options=
        [{'options': {
            'type': 'column'
        },
          'terms': {
              'pathogenNumber': ['geneNumber']
          }
         }],

        chart_options=
        {
            'chart': {
                'backgroundColor': '#F3F3FF',
                'borderWidth': 1,
                'borderRadius': 5,
                'plotBackgroundColor': '#ffffff',
                'plotShadow': 'false',
                'plotBorderWidth': 0,
                'plotBorderColor': 'black',
                'spacingRight': 30
            },
            'title': {
                'text': 'Distribution of EHFs',
                'style': {
                    'fontWeight': 'bold'
                }
            },
            'subtitle': {
                'text': 'primary hits'
            },
            'xAxis': {
                'title': {
                    'text': 'Pathogen Number'},
                'gridLineWidth': 1,
                'labels': {
                    'style': {
                        'color': 'black'
                    }
                },
                'lineColor': 'black',
                'lineWidth': 1

            },
            'yAxis': {
                'title': {
                    'text': 'EHF Gene Number'},
                'gridLineWidth': 1,
                'minorTickInterval': 'auto',
                'type': 'linear',  #'linear', 'logarithmic' and 'datetime'
                'labels': {
                    'style': {
                        'color': 'black'
                    }
                },
                'lineColor': 'black',
                'lineWidth': 1

            },
            'tooltip': {
                'backgroundColor': '#ffffff',
                'borderColor': '#4572A7',
                'borderRadius': 2,
                'borderWidth': 1
            },
            'legend': {
                'align': 'left',
                'verticalAlign': 'top',
                'floating': 'true'
            },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 1,
                    'color': '#4572A7',
                },
                'series': {
                    'shadow': 'true',
                    'dataLabels': {
                        'enabled': 'true',
                        'color': '#4572A7'
                    }
                }
            },
        })

    resultAll = overlapDistribution.objects.filter(type='all').filter(pathogenNumber__gte=4).order_by('-pathogenNumber')
    resultPrimary = overlapDistribution.objects.filter(type='primary hits').filter(pathogenNumber__gte=3).order_by(
        '-pathogenNumber')

    return render_to_response('analysis/distribution.html',
                              {'charts': [allColumn, primaryColumn], 'resultAll': resultAll,
                               'resultPrimary': resultPrimary},
                              context_instance=RequestContext(request))


def pip(request):
    if 'geneList' in request.GET:  #stupid method, otherwise we have to implement our own pagination method, actually we can directed to another link

        geneList1 = []
        #parse geneList
        if request.GET['geneList'].find(',') > 0:
            genes = request.GET['geneList'].split(',')
        elif request.GET['geneList'].find('\n') > 0:
            genes = request.GET['geneList'].split('\n')
        elif request.GET['geneList'].find('\r') > 0:
            genes = request.GET['geneList'].split('\r')
        else:
            genes = request.GET['geneList'].split('\r\n')

        for i in genes:
            if len(i.strip()):
                geneList1.append(i.strip())
        geneList1 = list(set(geneList1))  # query gene list

        #parse pathogen
        geneList2 = []
        pathogen = request.GET.getlist('pathogen[]')
        speciesList = []
        for item in pathogen:
            if item.startswith('species'):
                speciesList.append(item[item.find('_') + 1:])

        result = allEHFPI.objects.filter(speciesTaxonomy__in=speciesList)
        for item in result:
            geneList2.append(item.humanHomolog)
        geneList2 = list(set(geneList2))

        #print geneList
        geneList = geneList1 + geneList2
        geneList = list(set(geneList))

        if '' in geneList:
            geneList.remove('')

        inEHFPI = allEHFPI.objects.filter(humanHomolog__in=geneList)
        ehfpiList = []
        GeneNumberIn = 0  #number of genes in EHFPI
        for item in inEHFPI:
            if item.humanHomolog != '' and item.humanHomolog not in ehfpiList:
                ehfpiList.append(item.humanHomolog)
                GeneNumberIn += 1

        #get the geneSymbol-VTP model
        result = vtpModel.objects.filter(geneSymbol__in=geneList)
        GeneNumberSubmit = len(geneList)  # number of gene submitted
        interactions = len(result)  #number of genes in EHFPI
        GeneNumberVTP = 0  # number of genes that are also VTP
        vtpList = []
        for item in result:
            if item.geneSymbol not in vtpList:
                vtpList.append(item.geneSymbol)
                GeneNumberVTP += 1

        if (len(result)):
            order = request.GET.get('order_by', 'geneSymbol')
            result = result.order_by(order)

        return render_to_response('analysis/getVTPList.html',
                                  {'GeneNumberSubmit': GeneNumberSubmit, 'GeneNumberIn': GeneNumberIn,
                                   'interactions': interactions,
                                   'GeneNumberVTP': GeneNumberVTP, 'result': result, 'ids': ','.join(vtpList)},
                                  context_instance=RequestContext(request))

    else:  # for pagination consideration
        if os.path.isfile(PKL_DIR + '/pip.pkl'):  #have pickle
            file_out = file(PKL_DIR + '/pip.pkl', 'rb')
            tree = pickle.load(file_out)
            tree_taxonomy = pickle.load(file_out)
            file_out.close()
        else:

            # construct tree tree
            resultB = taxonomy.objects.filter(kingdom="bacteria").values()
            resultV = taxonomy.objects.filter(kingdom="virus").values()
            resultF = taxonomy.objects.filter(kingdom="fungi").values()

            # generate tree view list
            treeB = defaultdict(lambda: defaultdict(list))
            treeV = defaultdict(lambda: defaultdict(list))
            treeF = defaultdict(lambda: defaultdict(list))

            tree_taxonomy = {}
            # bacteria
            for item in resultB:
                kingdom = item['kingdom']
                # virus has family, bacteria has genus
                genus = item['genus']
                species = item['species']

                tree_taxonomy[kingdom] = item['kingdomTaxonomy']
                tree_taxonomy[genus] = item['genusTaxonomy']
                tree_taxonomy[species] = item['speciesTaxonomy']
                if species not in treeB[kingdom][genus]:
                    treeB[kingdom][genus].append(species)

            # virus
            for item in resultV:
                kingdom = item['kingdom']
                # virus has family, bacteria has genus
                family = item['family']
                species = item['species']

                tree_taxonomy[kingdom] = item['kingdomTaxonomy']
                tree_taxonomy[family] = item['familyTaxonomy']
                tree_taxonomy[species] = item['speciesTaxonomy']
                if species not in treeV[kingdom][family]:
                    treeV[kingdom][family].append(species)

            # fungi
            for item in resultF:
                kingdom = item['kingdom']
                # virus has family, bacteria has genus, fungi we only use genus
                genus = item['genus']
                species = item['species']

                tree_taxonomy[kingdom] = item['kingdomTaxonomy']
                tree_taxonomy[genus] = item['genusTaxonomy']
                tree_taxonomy[species] = item['speciesTaxonomy']

                if species not in treeF[kingdom][genus]:
                    treeF[kingdom][genus].append(species)

            # a three level tree
            for obj in treeB:
                treeB[obj].default_factory = None
            for obj in treeV:
                treeV[obj].default_factory = None
            for obj in treeF:
                treeF[obj].default_factory = None

            treeB = dict(treeB)
            treeV = dict(treeV)
            treeF = dict(treeF)
            tree = []
            tree.append(treeB)
            tree.append(treeV)
            tree.append(treeF)

            #generate pickle
            file_pip = file(PKL_DIR + '/pip.pkl', 'wb')
            pickle.dump(tree, file_pip, True)
            pickle.dump(tree_taxonomy, file_pip, True)
            file_pip.close()

        return render_to_response('analysis/pip.html', {'tree': tree, 'tree_taxonomy': tree_taxonomy})


# given a gene list or species list, return the related vtp gene list
def getVTPList(request):
    if request.method == 'GET' and 'source' in request.GET:
        source = request.GET['source']
        geneList = []
        if source == 'geneList':
            genes = request.GET['geneList'].split(',')
            for i in genes:
                if len(i.strip()):
                    geneList.append(i.strip())
            geneList = list(set(geneList))  # query gene list

        elif source == 'pathogen':
            pathogen = request.GET.getlist('pathogen[]')
            speciesList = []
            for item in pathogen:
                if item.startswith('species'):
                    speciesList.append(item[item.find('_') + 1:])

            idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
            speciesNameList = []
            for item in idMap:
                speciesNameList.append(item.name)

            result = allEHFPI.objects.filter(species__in=speciesNameList)
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
        else:
            print 'impossible'
        #print geneList

        if '' in geneList:
            geneList.remove('')

        inEHFPI = allEHFPI.objects.filter(humanHomolog__in=geneList)
        ehfpiList = []
        GeneNumberIn = 0  #number of genes in EHFPI
        for item in inEHFPI:
            if item.humanHomolog != '' and item.humanHomolog not in ehfpiList:
                ehfpiList.append(item.humanHomolog)
                GeneNumberIn += 1

        #get the geneSymbol-VTP model
        result = vtpModel.objects.filter(geneSymbol__in=geneList)
        GeneNumberSubmit = len(geneList)  # number of gene submitted
        interactions = len(result)  #interactions number
        GeneNumberVTP = 0  # number of genes that are also VTP
        vtpList = []
        for item in result:
            if item.geneSymbol not in vtpList:
                vtpList.append(item.geneSymbol)
                GeneNumberVTP += 1

        return render_to_response('analysis/getVTPList.html',
                                  {'GeneNumberSubmit': GeneNumberSubmit, 'GeneNumberIn': GeneNumberIn,
                                   'interactions': interactions,
                                   'GeneNumberVTP': GeneNumberVTP, 'ids': ','.join(vtpList), 'result': result},
                                  context_instance=RequestContext(request))


def download(request):
    if request.method == 'GET':
        if 'selected' in request.GET:
            selected = request.GET['selected'].split(',')

            data = vtpModel.objects.filter(geneSymbol__in=selected).values()

            selectcolumn = ['geneSymbol', 'proteinName', 'uniprotId', 'virusTaxid', 'virusName', 'resources', 'note']
            # code from download app
            fieldDesVTP = {'geneSymbol': 'Gene Symbol',
                           'proteinName': 'Protein Name',
                           'uniprotId': 'UniProt ID',
                           'virusTaxid': 'Virus Taxid',
                           'virusName': 'Virus Name',
                           'resources': 'Resources',
                           'note': 'note'
            }

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=pip.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in selectcolumn:
                rowTitle.append(fieldDesVTP[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in data:
                res = []
                for i in selectcolumn:
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect(URL_PREFIX)


def network(request):
    if request.method == 'POST':
        if 'selected' in request.POST:
            selected = request.POST['selected']
            selected = selected.split(',')

            return render_to_response('analysis/overlapNetworkOthers.html', {'geneList': ','.join(selected)},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)


#ppi network for pip analysis
def ppiOthers(request):
    if request.method == 'POST':
        if 'selected' in request.POST:
            selected = request.POST['selected']
            return render_to_response('analysis/ppiOthers.html', {'geneList': selected})

    return HttpResponseRedirect(URL_PREFIX)


#genrate the ppi network json data
def displayPPI(request):
    if request.method == 'POST' and 'geneList' in request.POST:
        genes = request.POST['geneList'].split(',')
        geneList = []
        for i in genes:
            if len(i.strip()):
                geneList.append(i.strip())
        geneList = list(set(geneList))  # query gene list
        if '' in geneList:
            geneList.remove('')

        qTotal = Q(geneSymbol1__in=geneList) | Q(geneSymbol2__in=geneList)

        result = ppi.objects.filter(qTotal)

        #calculate the degree of each node first
        degree = defaultdict(int)
        for item in result:
            degree[item.geneSymbol1] += 1
            degree[item.geneSymbol2] += 1

        degree = dict(degree)
        #print sorted(degree.items(), key=lambda d: d[1])

        toJson = {}

        #nodes
        nodes = []
        #edges
        edges = []
        for item in result:
            #first node
            node1 = {}
            dataAttr = {}
            dataAttr['id'] = item.geneSymbol1
            dataAttr['name'] = item.geneSymbol1
            dataAttr['refseqId'] = item.refseqId1
            dataAttr['weight'] = degree[item.geneSymbol1]
            dataAttr['height'] = degree[item.geneSymbol1]
            #dataAttr['des'] = 'gene name'
            dataAttr['hprd'] = item.hprdId1
            node1['data'] = dataAttr
            if item.geneSymbol1 in geneList:  #submitted
                node1['classes'] = 'submitted'
            else:
                node1['classes'] = 'other'
            nodes.append(node1)  #add node1

            #second node
            node2 = {}
            dataAttr = {}
            dataAttr['id'] = item.geneSymbol2
            dataAttr['name'] = item.geneSymbol2
            dataAttr['refseqId'] = item.refseqId2
            dataAttr['weight'] = degree[item.geneSymbol2]
            dataAttr['height'] = degree[item.geneSymbol2]
            #dataAttr['des'] = 'gene name'
            dataAttr['hprd'] = item.hprdId2
            node2['data'] = dataAttr
            if item.geneSymbol2 in geneList:  #submitted
                node2['classes'] = 'submitted'
            else:
                node2['classes'] = 'other'
            nodes.append(node2)  #add node2

            #edge
            edge = {}
            dataAttr = {}
            dataAttr['source'] = item.geneSymbol1
            dataAttr['target'] = item.geneSymbol2
            dataAttr['expType'] = item.expType
            dataAttr['pubmedId'] = item.pubmedId
            edge['data'] = dataAttr
            edges.append(edge)

        toJson['nodes'] = nodes
        toJson['edges'] = edges

        toJson = json.dumps(toJson)

        #using ppi interaction data from HPRD
        return render_to_response('analysis/displayPPI.js', {'toJson': toJson},
                                  context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX + '/analysis/pip/')


#gwas analysis, same as gea analysis
def gwasIndex(request):
    if os.path.isfile(PKL_DIR + '/gwas.pkl'):  #have pickle
        file_out = file(PKL_DIR + '/gwas.pkl', 'rb')
        tree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        badge_taxonomy = pickle.load(file_out)
        file_out.close()
    else:
        tree, tree_taxonomy, badge_taxonomy = generateTree()
        #generate pickle
        file_gwas = file(PKL_DIR + '/gwas.pkl', 'wb')
        pickle.dump(tree, file_gwas, True)
        pickle.dump(tree_taxonomy, file_gwas, True)
        pickle.dump(badge_taxonomy, file_gwas, True)
        file_gwas.close()

    return render_to_response('analysis/gwas.html',
                              {'tree': tree, 'tree_taxonomy': tree_taxonomy, 'badge_taxonomy': badge_taxonomy},
                              context_instance=RequestContext(request))


#process submitted data
def gwasResults(request):
    if request.method == 'GET':
        if 'jsTreeList' in request.GET:
            jsTreeList = request.GET['jsTreeList']
            result, aboveSpeciesList = geneListForGwasAndDrug(jsTreeList)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = set(geneList)
            if '' in geneList:
                geneList.remove('')

            #result = []
            GeneNumberGWAS = []
            #resultTmp = gwas.objects.all()
            # for item in resultTmp:
            #     if item.mappedGene.strip() != '-':
            #         genes = []
            #         if ' - ' in item.mappedGene:
            #             genes = item.mappedGene.strip().split(' - ')
            #         elif ';' in item.mappedGene:
            #             genes = item.mappedGene.strip().split(';')
            #         else:
            #             genes.append(item.mappedGene.strip())
            #         if len(geneList & set(genes)) > 0:
            #             GeneNumberGWAS = GeneNumberGWAS + list(geneList & set(genes))
            #             result.append(item)

            # for item in resultTmp:
            #     genes = []
            #     if ', ' in item.reportedGene:
            #         genes = item.reportedGene.strip().split(', ')
            #     else:
            #         genes.append(item.reportedGene.strip())
            #     if len(geneList & set(genes)) > 0:
            #         GeneNumberGWAS = GeneNumberGWAS + list(geneList & set(genes))
            #         result.append(item)

            #
            result = gwas.objects.filter(reportedGene__in=geneList)
            speciesAll = []  #all species
            for item in result:
                GeneNumberGWAS.append(item.reportedGene)
                speciesAll.append(item.species)

            #other species, not submitted
            speciesAll = list(set(speciesAll))
            otherSpecies = list(set(speciesAll))

            #dict
            speciesDict = {}
            speciesDictReverse = {}  #used in template to store taxonomy info
            aboveSpecies = []
            idMap = idNameMap.objects.filter(name__in=speciesAll, type='species')
            for item in idMap:
                speciesDict[item.acc] = item.name
                speciesDictReverse[item.name] = item.acc

            for item in aboveSpeciesList:
                if item in speciesDict.keys():
                    otherSpecies.remove(speciesDict[item])
                    aboveSpecies.append(speciesDict[item])
            #note some species may not have any drug information

            aboveSpecies.sort()
            otherSpecies.sort()

            GeneNumberSubmit = len(geneList)
            GeneNumberGWAS = len(set(GeneNumberGWAS))

            #if column in the url, we filter the result
            if 'columns' in request.GET:
                columns = request.GET['columns']
                if len(columns.strip()) > 0:
                    columns = columns.split(',')
                    speciesSelected = []
                    for item in columns:
                        speciesSelected.append(speciesDict[item])
                    result = result.filter(species__in=speciesSelected)

            interactions = len(result)

            #sort the table
            if (len(result)):
                order = request.GET.get('order_by', 'reportedGene')
                result = result.order_by(order)
                #sort the column
                #
                # #stupid method, too slow, but do we have any answer to this problem
                # if order.startswith('-'):
                #     result.sort(lambda x, y: -cmp(getattr(x, order[1:]), getattr(y, order[1:])))
                # else:
                #     result.sort(lambda x, y: cmp(getattr(x, order), getattr(y, order)))


            # gwasDict = defaultdict(set)
            # for aa in result:
            #     gwasDict[aa.reportedGene].add(aa['species'])
            #
            # gwasDict = dict(gwasDict)
            # myDic = {}
            # for key,value in gwasDict.items():
            #     myDic[key] = len(value)
            # print sorted(myDic.items(), key=lambda d: d[1])

            return render_to_response('analysis/gwasResults.html',
                                      {'result': result, 'GeneNumberSubmit': GeneNumberSubmit,
                                       'interactions': interactions, 'GeneNumberGWAS': GeneNumberGWAS,
                                       'aboveSpecies': aboveSpecies, 'otherSpecies': otherSpecies,
                                       'speciesDictReverse': speciesDictReverse},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX + '/analysis/gwas/')


#gwas download
def gwasDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET:
            type = request.GET['type']
            if 'selected' in request.GET:
                selected = request.GET['selected']
                if type == 'all':
                    result, aboveSpeciesList = geneListForGwasAndDrug(selected[11:])

                    geneList = []
                    for item in result:
                        geneList.append(item.humanHomolog)
                    geneList = set(geneList)
                    if '' in geneList:
                        geneList.remove('')

                    #data = []
                    #resultTmp = gwas.objects.all().values()
                    # for item in resultTmp:
                    #     if item['mappedGene'].strip() != '-':
                    #         genes = []
                    #         if ' - ' in item['mappedGene']:
                    #             genes = item['mappedGene'].strip().split(' - ')
                    #         elif ';' in item['mappedGene']:
                    #             genes = item['mappedGene'].strip().split(';')
                    #         else:
                    #             genes.append(item['mappedGene'].strip())
                    #         if len(geneList & set(genes)) > 0:
                    #             data.append(item)
                    # for item in resultTmp:
                    #     genes = []
                    #     if ', ' in item['reportedGene']:
                    #         genes = item['reportedGene'].strip().split(', ')
                    #     else:
                    #         genes.append(item['reportedGene'].strip())
                    #     if len(geneList & set(genes)) > 0:
                    #         data.append(item)
                    data = gwas.objects.filter(reportedGene__in=geneList)
                    #if column in the url, we filter the result
                    if 'columns' in request.GET:
                        columns = request.GET['columns']
                        if len(columns.strip()) > 0:
                            columns = columns.split(',')
                            speciesSelected = []

                            speciesDict = {}
                            idMap = idNameMap.objects.filter(type='species')
                            for item in idMap:
                                speciesDict[item.acc] = item.name

                            for item in columns:
                                speciesSelected.append(speciesDict[item])

                            data = data.filter(species__in=speciesSelected)
                    data = data.values()

                else:
                    selected = request.GET['selected'].split(',')

                    data = gwas.objects.filter(acc__in=selected).values()

                selectcolumn = ['pubmedId', 'firstAuthor', 'journal', 'link', 'study', 'disease',
                                'initialSampleSize', 'replicationSampleSize', 'cytogeneticLoc', 'chrId', 'charPos',
                                'reportedGene', 'mappedGene', 'upstreamGeneId', 'downstreamGeneId', 'snpGeneId',
                                'upstreamGeneDistance', 'downstreamGeneDistance', 'strongSnpAllele', 'snps', 'merged',
                                'snpIdCurrent', 'context', 'interGenetic', 'riskAlleleFreq', 'pvalue', 'pvalueMLog',
                                'pvalueText',
                                'orOrBeta', 'ci', 'platform', 'cnv']

                # code from download app
                fieldDesDrug = {'pubmedId': 'PUBMEDID',
                                'firstAuthor': 'First Author',
                                'journal': 'Journal',
                                'link': 'Link',
                                'study': 'Study',
                                'disease': 'Disease/Trait',
                                'initialSampleSize': 'Initial Sample Size',
                                'replicationSampleSize': 'Replication Sample Size',
                                'cytogeneticLoc': 'Region',
                                'chrId': 'Chr_id',
                                'charPos': 'Chr_pos',
                                'reportedGene': 'Reported Gene(s)',
                                'mappedGene': 'Mapped_gene',
                                'upstreamGeneId': 'Upstream_gene_id',
                                'downstreamGeneId': 'Downstream_gene_id',
                                'snpGeneId': 'Snp_gene_ids',
                                'upstreamGeneDistance': 'Upstream_gene_distance',
                                'downstreamGeneDistance': 'Downstream_gene_distance',
                                'strongSnpAllele': 'Strongest SNP-Risk Allele',
                                'snps': 'SNPs',
                                'merged': 'Merged',
                                'snpIdCurrent': 'Snp_id_current',
                                'context': 'Context',
                                'interGenetic': 'Intergenic',
                                'riskAlleleFreq': 'Risk Allele Frequency',
                                'pvalue': 'p-Value',
                                'pvalueMLog': 'Pvalue_mlog',
                                'pvalueText': 'p-Value (text)',
                                'orOrBeta': 'OR or beta',
                                'ci': '95% CI (text)',
                                'platform': 'Platform [SNPs passing QC]',
                                'cnv': 'CNV'
                }

                response = HttpResponse(content_type="text/csv")
                response.write('\xEF\xBB\xBF')
                response['Content-Disposition'] = 'attachment; filename=gwas.csv'
                writer = csv.writer(response)

                # store row title description
                rowTitle = []
                for item in selectcolumn:
                    rowTitle.append(fieldDesDrug[item])
                writer.writerow(rowTitle)

                #get data from database
                for item in data:
                    res = []
                    for i in selectcolumn:
                        res.append(smart_str(item[i]))
                    writer.writerow(res)
                return response

    return HttpResponseRedirect(URL_PREFIX + '/analysis/gwas/')


#drug target analysis
def drug(request):
    if os.path.isfile(PKL_DIR + '/drug.pkl'):  #have pickle
        file_out = file(PKL_DIR + '/drug.pkl', 'rb')
        tree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        badge_taxonomy = pickle.load(file_out)
        file_out.close()
    else:
        tree, tree_taxonomy, badge_taxonomy = generateTree()
        #generate pickle
        file_drug = file(PKL_DIR + '/drug.pkl', 'wb')
        pickle.dump(tree, file_drug, True)
        pickle.dump(tree_taxonomy, file_drug, True)
        pickle.dump(badge_taxonomy, file_drug, True)
        file_drug.close()

    return render_to_response('analysis/drug.html',
                              {'tree': tree, 'tree_taxonomy': tree_taxonomy, 'badge_taxonomy': badge_taxonomy},
                              context_instance=RequestContext(request))


#process submitted data
def drugResults(request):
    #get to support pagination
    if request.method == 'GET':
        if 'jsTreeList' in request.GET and 'geneList' in request.GET:

            #get gene list start
            jsTreeList = request.GET['jsTreeList']
            geneList1 = []
            aboveSpeciesList = []
            if len(jsTreeList.strip()):  #select jsTree
                result, aboveSpeciesList = geneListForGwasAndDrug(jsTreeList)
                for item in result:
                    geneList1.append(item.humanHomolog)

            geneList2Tmp = request.GET['geneList']
            geneList22 = []
            geneList2 = []
            if ',' in geneList2Tmp:
                geneList22 = geneList2Tmp.split(',')
            elif ';' in geneList2Tmp:
                geneList22 = geneList2Tmp.split(';')
            elif '\r' in geneList2Tmp:
                geneList22 = geneList2Tmp.split('\r')
            elif '\r\n' in geneList2Tmp:
                geneList22 = geneList2Tmp.split('\r\n')
            else:
                geneList22.append(geneList2Tmp.strip())
            for item in geneList22:
                geneList2.append(item.strip())

            geneList = list(set(geneList1) | set(geneList2))
            if '' in geneList:
                geneList.remove('')

            #get gene list end

            GeneDrug = []  #record gene number
            DrugList = []  #recored drug number
            speciesAll = []  #all species

            result = drugModelWithInt.objects.filter(geneSymbol__in=geneList)
            for item in result:
                GeneDrug.append(item.geneSymbol)
                DrugList.append(item.drugbankId)
                speciesAll.append(item.species)

            #other species, not submitted
            speciesAll = list(set(speciesAll))
            otherSpecies = list(set(speciesAll))

            #dict
            speciesDict = {}
            speciesDictReverse = {}  #used in template to store taxonomy info
            aboveSpecies = []
            idMap = idNameMap.objects.filter(name__in=speciesAll, type='species')
            for item in idMap:
                speciesDict[item.acc] = item.name
                speciesDictReverse[item.name] = item.acc

            for item in aboveSpeciesList:
                if item in speciesDict.keys():
                    otherSpecies.remove(speciesDict[item])
                    aboveSpecies.append(speciesDict[item])
            #note some species may not have any drug information

            aboveSpecies.sort()
            otherSpecies.sort()

            GeneNumberSubmit = len(geneList)
            GeneNumberDrug = len(set(GeneDrug))
            DrugNumber = len(set(DrugList))

            #if column in the url, we filter the result
            if 'columns' in request.GET:
                columns = request.GET['columns']
                if len(columns.strip()) > 0:
                    columns = columns.split(',')
                    speciesSelected = []
                    for item in columns:
                        speciesSelected.append(speciesDict[item])
                    result = result.filter(species__in=speciesSelected)

            interactions = len(result)

            #sort the table
            if len(result):
                #sort the column
                order = request.GET.get('order_by', 'species')
                result = result.order_by(order)

            return render_to_response('analysis/drugResults.html',
                                      {'result': result, 'GeneNumberSubmit': GeneNumberSubmit,
                                       'interactions': interactions, 'GeneNumberDrug': GeneNumberDrug,
                                       'DrugNumber': DrugNumber,
                                       'aboveSpecies': aboveSpecies, 'otherSpecies': otherSpecies,
                                       'speciesDictReverse': speciesDictReverse},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX + '/analysis/drug/')


#download drug data
def drugDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET:
            type = request.GET['type']
            if 'selected' in request.GET and 'geneList' in request.GET:
                selected = request.GET['selected']
                if type == 'all':
                    result, aboveSpeciesList = geneListForGwasAndDrug(selected)

                    geneList1 = []
                    for item in result:
                        geneList1.append(item.humanHomolog)

                    geneList2Tmp = request.GET['geneList']
                    geneList22 = []
                    geneList2 = []
                    if ',' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split(',')
                    elif ';' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split(';')
                    elif '\r' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split('\r')
                    elif '\r\n' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split('\r\n')
                    else:
                        geneList22.append(geneList2Tmp.strip())
                    for item in geneList22:
                        geneList2.append(item.strip())

                    geneList = list(set(geneList1) | set(geneList2))
                    if '' in geneList:
                        geneList.remove('')

                    data = drugModelWithInt.objects.filter(geneSymbol__in=geneList)
                    #if column in the url, we filter the result
                    if 'columns' in request.GET:
                        columns = request.GET['columns']
                        if len(columns.strip()) > 0:
                            columns = columns.split(',')
                            speciesSelected = []

                            speciesDict = {}
                            idMap = idNameMap.objects.filter(type='species')
                            for item in idMap:
                                speciesDict[item.acc] = item.name

                            for item in columns:
                                speciesSelected.append(speciesDict[item])

                            data = data.filter(species__in=speciesSelected)

                    data = data.values()

                else:
                    selected = request.GET['selected'].split(',')

                    data = drugModelWithInt.objects.filter(acc__in=selected).values()

                selectcolumn = ['species', 'speciesTaxonomy', 'geneSymbol', 'hgncId', 'uniprotId', 'proteinName',
                                'drugbankId', 'drugName',
                                'drugType', 'drugGroup']
                # code from download app
                fieldDesDrug = {'species': 'Pathogen(species)',
                                'speciesTaxonomy': 'Species Taxonomy',
                                'geneSymbol': 'Gene Symbol',
                                'hgncId': 'HGNC ID',
                                'uniprotId': 'UniProt ID',
                                'proteinName': 'Protein Name',
                                'drugbankId': 'DrugBank ID',
                                'drugName': 'Drug Name',
                                'drugType': 'Drug Type',
                                'drugGroup': 'Drug Group'
                }

                response = HttpResponse(content_type="text/csv")
                response.write('\xEF\xBB\xBF')
                response['Content-Disposition'] = 'attachment; filename=drug.csv'
                writer = csv.writer(response)

                # store row title description
                rowTitle = []
                for item in selectcolumn:
                    rowTitle.append(fieldDesDrug[item])
                writer.writerow(rowTitle)

                #get data from database
                for item in data:
                    res = []
                    for i in selectcolumn:
                        res.append(smart_str(item[i]))
                    writer.writerow(res)
                return response

    return HttpResponseRedirect(URL_PREFIX + '/analysis/drug/')


def drugNetwork(request):
    if request.method == 'POST':
        if 'type' in request.POST:
            type = request.POST['type']
            if 'selected' in request.POST and 'geneList' in request.POST:
                selected = request.POST['selected']
                #print selected
                if type == 'all':
                    #replace %2C with ,
                    if '%2C' in selected:
                        selected = selected.replace('%2C', ',')

                    #we get aboveSpeciesList here to display in the network. note we show all related relations, not the selected
                    #store taxonomy id is enough, not name
                    result, aboveSpeciesList = geneListForGwasAndDrug(selected)

                    geneList1 = []
                    for item in result:
                        geneList1.append(item.humanHomolog)

                    geneList2Tmp = request.POST['geneList']
                    #replace %2C with ,
                    if '%2C' in geneList2Tmp:
                        geneList2Tmp = geneList2Tmp.replace('%2C', ',')

                    geneList22 = []
                    geneList2 = []
                    if ',' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split(',')
                    elif ';' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split(';')
                    elif '\r' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split('\r')
                    elif '\r\n' in geneList2Tmp:
                        geneList22 = geneList2Tmp.split('\r\n')
                    else:
                        geneList22.append(geneList2Tmp.strip())
                    for item in geneList22:
                        geneList2.append(item.strip())

                    geneList = list(set(geneList1) | set(geneList2))
                    if '' in geneList:
                        geneList.remove('')

                    data = drugModelWithInt.objects.filter(geneSymbol__in=geneList)

                    #if column in the url, we filter the result
                    if 'columns' in request.POST:
                        columns = request.POST['columns']
                        if len(columns.strip()) > 0:
                            columns = columns.split(',')
                            speciesSelected = []

                            speciesDict = {}
                            idMap = idNameMap.objects.filter(type='species')
                            for item in idMap:
                                speciesDict[item.acc] = item.name

                            for item in columns:
                                speciesSelected.append(speciesDict[item])

                            data = data.filter(species__in=speciesSelected)

                    data = data.values_list('acc')

                else:
                    aboveSpeciesList = []
                    selected = request.POST['selected'].split(',')
                    data = drugModelWithInt.objects.filter(acc__in=selected).values_list('acc')

                #we should pass
                accList = []
                for item in data:
                    if item[0] not in accList:
                        accList.append(str(item[0]))

                return render_to_response('analysis/drugNetworkOthers.html',
                                          {'accList': ','.join(accList),
                                           'aboveSpeciesList': ';'.join(aboveSpeciesList)})

    return HttpResponseRedirect(URL_PREFIX + '/analysis/drug/')


#for gwas and drug, given a tree, generate result
def geneListForGwasAndDrug(jsTreeList):
    pathogen = []
    aboveSpeciesList = []
    if ',' in jsTreeList:
        pathogen = jsTreeList.split(',')
    else:
        pathogen.append(jsTreeList.strip())

    speciesList = []
    articleList = []
    for item in pathogen:
        if item.startswith('species'):
            speciesList.append(item[item.find('_') + 1:])
        if item.startswith('article'):
            articleList.append(item[item.find('_') + 1:])

    aboveSpeciesList = speciesList

    #a article may contain several species, a species may contain several article. So if species is selected, all article
    # under it must be selected too, if a article is selected, we must use and between it and its species!!!
    qTotal = Q()
    for item in articleList:
        speciesItem = item[0:item.find('_')]
        aboveSpeciesList.append(speciesItem)
        pubmedIdItem = item[item.find('_') + 1:]
        qTotal = qTotal | (Q(speciesTaxonomy=speciesItem) & Q(pubmedId=pubmedIdItem))

    qTotal = qTotal | Q(speciesTaxonomy__in=speciesList)

    result = allEHFPI.objects.filter(qTotal)

    aboveSpeciesList = list(set(aboveSpeciesList))

    return result, aboveSpeciesList


#render the drug network, this is for drugModel,since in this model, there is no pathogen info.
# def drugDisplayNetworkOld(request):
#     if request.method == 'POST' and 'text' in request.POST:
#         aboveSpeciesList = []
#         if 'aboveSpeciesList' in request.POST:
#             tmp = request.POST['aboveSpeciesList'].strip()
#             if len(tmp):
#                 if ';' in tmp:
#                     aboveSpeciesList = tmp.split(';')
#                 else:
#                     aboveSpeciesList.append(tmp)
#
#         accList = request.POST['text'].split(',')
#
#         #using accList in drug Model to get gene list
#         geneList = []
#         drugResult = drugModel.objects.filter(acc__in=accList).values('geneSymbol', 'drugbankId', 'drugName')
#         for item in drugResult:
#             geneList.append(item['geneSymbol'])
#
#         geneList = list(set(geneList))  # query gene list
#         if '' in geneList:
#             geneList.remove('')
#
#         if len(geneList):
#             allResult = allEHFPI.objects.filter(humanHomolog__in=geneList).values('humanHomolog', 'species',
#                                                                                   'strain')  #relation list we get
#
#             #get drug list and pathogen list
#             drugList = []
#             pathogenList = []
#             for item in drugResult:
#                 drugList.append(item['drugbankId'])
#             for item in allResult:
#                 pathogenList.append(item['species'])
#             drugList = list(set(drugList))
#             pathogenList = list(set(pathogenList))
#
#             # calculate drug number of each species
#             speciesNumber = defaultdict(list)
#
#             # generate interaction network start
#             jsonRes = []  # a list
#
#             # generate json file
#             for item in drugList:
#                 node = {}
#                 node['name'] = item  # name attr
#                 node['id'] = item  #id attr
#
#                 data = {}  #data attr
#                 data['$type'] = 'circle'
#                 data['nodeType'] = 'drug'
#
#                 # set adjacencies attr
#                 adjacencies = []
#                 adjacenciesNumber = 0
#
#                 for drugItem in drugResult:  # generate drug node
#                     if item == drugItem['drugbankId']:  #
#                         data['des'] = drugItem['drugName']  #drug name
#
#                         for allItem in allResult:
#                             if allItem['humanHomolog'].upper() == drugItem['geneSymbol'].upper():  #gene is the same
#                                 relation = {}
#                                 relation['nodeTo'] = allItem['species']
#                                 relation['nodeFrom'] = drugItem['drugbankId']
#                                 nodeData = {}  # can overwrite, edge attribute(display linked gene)
#                                 #nodeData["$color"] = "#8b0000"
#                                 #nodeData["$color"] = "#339900"
#                                 nodeData["$color"] = "#23A4FF"
#                                 nodeData['gene'] = drugItem['geneSymbol']
#                                 relation['data'] = nodeData
#                                 adjacencies.append(relation)
#                                 adjacenciesNumber = adjacenciesNumber + 1  #calculate common and specific gene
#
#                 node['adjacencies'] = adjacencies
#                 if adjacenciesNumber > 1:
#                     data['$color'] = '#416D9C'
#                 else:
#                     data['$color'] = '#800080'
#
#                 node['data'] = data
#
#                 jsonRes.append(node)
#
#             # generate json file
#             for item in pathogenList:
#                 node = {}
#                 node['name'] = item  # name attr
#                 node['id'] = item  #id attr
#
#                 data = {}  #data attr
#                 data['$color'] = '#EBB056'
#                 data['$type'] = 'triangle'
#                 data['nodeType'] = 'species'
#
#                 # set adjacencies attr
#                 adjacencies = []
#
#                 strain_list = []
#                 for allItem in allResult:  # generate pathogen node
#                     if allItem['species'] == item:
#                         strain_list.append(allItem['strain'])
#
#                         for drugItem in drugResult:
#                             if drugItem['geneSymbol'] == allItem['humanHomolog']:
#                                 speciesNumber[item].append(drugItem['drugbankId'])
#                                 relation = {}
#                                 relation['nodeTo'] = drugItem['drugbankId']
#                                 relation['nodeFrom'] = allItem['species']
#                                 nodeData = {}  # can overwrite
#                                 nodeData["$color"] = "#23A4FF"
#                                 nodeData['gene'] = drugItem['geneSymbol']
#                                 relation['data'] = nodeData
#                                 adjacencies.append(relation)
#
#                 strain_list = list(set(strain_list))
#                 data['des'] = '_'.join(strain_list)
#                 node['data'] = data
#                 node['adjacencies'] = adjacencies
#                 jsonRes.append(node)
#
#             toJson = json.dumps(jsonRes)
#             # generate interaction map end
#
#             speciesNumber = dict(speciesNumber)
#             for key, value in speciesNumber.items():
#                 speciesNumber[key] = len(list(set(value)))
#
#             #store the species submitted above
#             idMap = idNameMap.objects.filter(type='species', acc__in=aboveSpeciesList).values('acc', 'name')
#             idToName = {}
#             for item in idMap:
#                 idToName[item['acc']] = item['name']
#
#             speciesNumberAbove = {}
#             for item in aboveSpeciesList:
#                 if idToName[item] in speciesNumber.keys():
#                     speciesNumberAbove[idToName[item]] = speciesNumber[idToName[item]]
#                     speciesNumber.pop(idToName[item])
#
#             # calculate gene number of each species end
#
#             return render_to_response('analysis/displayDrugNetwork.js',
#                                       {'toJson': toJson, 'speciesNumber': sorted(speciesNumber.iteritems()),
#                                        'speciesNumberAbove': sorted(speciesNumberAbove.iteritems())})
#         else:  # empty
#             return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork')
#     else:
#         return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork')


#render the drug network, this is for drugModelWithInt, since pathogen info is in the model
def drugDisplayNetwork(request):
    if request.method == 'POST' and 'text' in request.POST:
        aboveSpeciesList = []
        if 'aboveSpeciesList' in request.POST:
            tmp = request.POST['aboveSpeciesList'].strip()
            if len(tmp):
                if ';' in tmp:
                    aboveSpeciesList = tmp.split(';')
                else:
                    aboveSpeciesList.append(tmp)

        accList = request.POST['text'].split(',')
        drugResult = drugModelWithInt.objects.filter(acc__in=accList).values('species', 'speciesTaxonomy', 'strain',
                                                                             'geneSymbol', 'drugbankId', 'drugName',
                                                                             'drugGroup')

        # drugDict = defaultdict(set)
        # for aa in drugResult:
        #     drugDict[aa['drugName']].add(aa['species'])
        #
        # drugDict = dict(drugDict)
        # myDic = {}
        # for key,value in drugDict.items():
        #     myDic[key] = len(value)
        # print sorted(myDic.items(), key=lambda d: d[1])


        #get drug list and pathogen list
        drugList = []
        pathogenList = []
        for item in drugResult:
            drugList.append(item['drugName'])
        for item in drugResult:
            pathogenList.append(item['species'])
        drugList = list(set(drugList))
        pathogenList = list(set(pathogenList))

        # calculate drug number of each species
        speciesNumber = defaultdict(list)

        # generate interaction network start
        jsonRes = []  # a list

        # generate json file
        for item in drugList:
            node = {}
            node['name'] = item  # name attr
            node['id'] = item  #id attr

            data = {}  #data attr
            data['$type'] = 'circle'
            data['nodeType'] = 'drug'

            # set adjacencies attr
            adjacencies = []
            #adjacenciesNumber = 0

            for drugItem in drugResult:  # generate drug node
                if item == drugItem['drugName']:  #
                    data['des'] = drugItem['drugbankId']  #drug name
                    relation = {}
                    relation['nodeTo'] = drugItem['species']
                    relation['nodeFrom'] = drugItem['drugName']
                    nodeData = {}  # can overwrite, edge attribute(display linked gene)
                    nodeData["$color"] = "#23A4FF"
                    nodeData['gene'] = drugItem['geneSymbol']
                    relation['data'] = nodeData
                    adjacencies.append(relation)
                    #adjacenciesNumber = adjacenciesNumber + 1  #calculate common and specific gene

            node['adjacencies'] = adjacencies
            #if adjacenciesNumber > 1:
            if drugItem['drugGroup'] == 'approved':  #approved drug
                data['$color'] = '#416D9C'
                data['drugGroup'] = 'approved'
            else:
                data['$color'] = '#800080'
                data['drugGroup'] = 'other'

            node['data'] = data

            jsonRes.append(node)

        # generate json file
        for item in pathogenList:
            node = {}
            node['name'] = item  # name attr
            node['id'] = item  #id attr

            data = {}  #data attr
            data['$color'] = '#EBB056'
            data['$type'] = 'triangle'
            data['nodeType'] = 'species'

            # set adjacencies attr
            adjacencies = []

            strain_list = []
            for drugItem in drugResult:  # generate pathogen node
                if drugItem['species'] == item:
                    strain_list.append(drugItem['strain'])
                    speciesNumber[item].append(drugItem['drugbankId'])
                    relation = {}
                    relation['nodeTo'] = drugItem['drugName']
                    relation['nodeFrom'] = drugItem['species']
                    nodeData = {}  # can overwrite
                    nodeData["$color"] = "#23A4FF"
                    nodeData['gene'] = drugItem['geneSymbol']
                    relation['data'] = nodeData
                    adjacencies.append(relation)

            strain_list = list(set(strain_list))
            data['des'] = '_'.join(strain_list)
            node['data'] = data
            node['adjacencies'] = adjacencies
            jsonRes.append(node)

        toJson = json.dumps(jsonRes)
        # generate interaction map end

        speciesNumber = dict(speciesNumber)
        for key, value in speciesNumber.items():
            speciesNumber[key] = len(list(set(value)))

        #store the species submitted above
        idMap = idNameMap.objects.filter(type='species', acc__in=aboveSpeciesList).values('acc', 'name')
        idToName = {}
        for item in idMap:
            idToName[item['acc']] = item['name']

        speciesNumberAbove = {}
        for item in aboveSpeciesList:
            if idToName[item] in speciesNumber.keys():
                speciesNumberAbove[idToName[item]] = speciesNumber[idToName[item]]
                speciesNumber.pop(idToName[item])

        # calculate gene number of each species end

        return render_to_response('analysis/displayDrugNetwork.js',
                                  {'toJson': toJson, 'speciesNumber': sorted(speciesNumber.iteritems()),
                                   'speciesNumberAbove': sorted(speciesNumberAbove.iteritems())})

    return HttpResponseRedirect(URL_PREFIX + '/analysis/overlap/overlapNetwork')
