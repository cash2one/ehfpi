from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Q
from browse.models import *
from collections import defaultdict
from django.template import RequestContext
from browse.browse_view_models import allEHFPI
from analysis.models import taxonomy, idNameMap, vtpModel
import json
import csv
import types
from django.utils.encoding import smart_str
import codecs
from ehf.settings import URL_PREFIX
from ehf.commonVar import field,fieldDes,fieldDic

#serilization
import os
import cPickle as pickle
from ehf.settings import PKL_DIR

#the welcome page
def guide(request):
    return render_to_response('browse/guide.html', context_instance=RequestContext(request))


# Create your views here.
def index(request):
    #change columns?
    if 'columns[]' in request.GET:
        selectedColumnsBrowse = request.GET.getlist('columns[]')
        request.session['has_changed_browse'] = True  # set the session, not change
        request.session['selectedColumnsBrowse'] = selectedColumnsBrowse  #store the columns

    if 'has_changed_browse' not in request.session:
        defaultColumns = ['ehfpiAcc', 'geneSymbol', 'species', 'title', 'phenotype']
        request.session['selectedColumnsBrowse'] = defaultColumns  #store the columns

    selected = []
    if 'selected[]' in request.GET:  #it is pagination request. e.g., /browse/?page=2&selected[]=year_2000&selected[]=year_2001
        selected = request.GET.getlist('selected[]')  #store the species list
        speciesList = []
        yearList = []
        journalList = []
        phenotypeList = []

        for item in selected:
            if item.startswith('species_'):
                speciesList.append(item[item.find('_') + 1:])
            elif item.startswith('year_'):
                yearList.append(item[item.find('_') + 1:])
            elif item.startswith('journal_'):
                journalList.append(item[item.find('_') + 1:])
            elif item.startswith('phenotype_'):
                phenotypeList.append(item[item.find('_') + 1:])
            else:
                print ""

        #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
        speciesNameList = []
        if speciesList:
            idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
            for item in idMap:
                speciesNameList.append(item.name)

        phenotypeNameList = []
        if phenotypeList:
            idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
            for item in idMap:
                phenotypeNameList.append(item.name)

        qTotal = Q()
        if speciesNameList:
            qTotal = qTotal & Q(species__in=speciesNameList)
        if yearList:
            qTotal = qTotal & Q(year__in=yearList)
        if journalList:
            qTotal = qTotal & Q(journal__in=journalList)
        if phenotypeNameList:
            qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

        result = allEHFPI.objects.filter(qTotal)
    else:
        result = allEHFPI.objects.all()  #first request or user doesn't select a filter

    # calculate the badge number start
    # notice the number is based on  ehfpiacc, not gene numbers, so we calculate it from allEHFPI
    #the number displayed in badge, we use four dict to avoid duplicate items in four field

    badge_taxonomy = defaultdict(int)
    badge_year = defaultdict(int)
    badge_journal = defaultdict(int)
    badge_phenotype = defaultdict(int)
    for item in result:
        badge_taxonomy[item.kingdom] += 1
        badge_taxonomy[item.species] += 1
        badge_year[item.year] += 1
        badge_journal[item.journal] += 1
        badge_phenotype[item.phenotype] += 1
    badge_taxonomy['all'] = len(result)
    badge_year['all'] = len(result)
    badge_journal['all'] = len(result)
    badge_phenotype['all'] = len(result)

    badge_taxonomy = dict(badge_taxonomy)
    badge_year = dict(badge_year)
    badge_journal = dict(badge_journal)
    badge_phenotype = dict(badge_phenotype)

    #calculate the badge number end
    if os.path.isfile(PKL_DIR+'/browse.pkl'): #have pickle
        file_out = file(PKL_DIR+'/browse.pkl', 'rb')
        taxonomyTree = pickle.load(file_out)
        tree_taxonomy = pickle.load(file_out)
        yearDict = pickle.load(file_out)
        journalDict = pickle.load(file_out)
        phenotypeDict = pickle.load(file_out)
        file_out.close()
    else:

        #construct the left tree start
        # one: taxonomy, only kingdom and species
        taxonomyTree = defaultdict(list)
        tree_taxonomy = {}  # we need this because for tree larger than two layer, we can not store taxonomy info for upper layer
        res = taxonomy.objects.all().values()

        for item in res:
            kingdom = item['kingdom']
            species = item['species']
            taxonomyTree[kingdom].append(species)
            tree_taxonomy[kingdom] = item['kingdomTaxonomy']
            tree_taxonomy[species] = item['speciesTaxonomy']

        taxonomyTree = dict(taxonomyTree)

        #remove duplicate item in list
        for key, value in taxonomyTree.items():
            tmp = list(set(list(value)))
            taxonomyTree[key] = tmp

        # two: publication year
        yearDict = {}
        res = publication.objects.all().values()
        for item in res:
            yearDict[item['year']] = item['year']

        # three: phenotype and publication journal, we need to register the name in the idNameMap?
        phenotypeDict = {}
        res = idNameMap.objects.filter(type='phenotype')
        for item in res:
            phenotypeDict[item.acc] = item.name

        journalDict = {}
        res = idNameMap.objects.filter(type='journal')
        for item in res:
            journalDict[item.acc] = item.name

        #construct the left tree end

        #generate pickle
        file_browse = file(PKL_DIR+'/browse.pkl', 'wb')
        pickle.dump(taxonomyTree, file_browse, True)
        pickle.dump(tree_taxonomy, file_browse, True)
        pickle.dump(yearDict, file_browse, True)
        pickle.dump(journalDict, file_browse, True)
        pickle.dump(phenotypeDict, file_browse, True)
        file_browse.close()

    #custom display columns start!

    columns = []
    for i in range(0, len(field), 1):
        columns.append([field[i], fieldDes[i]])
    #custom display columns end

    #columns to display start!

    displayColumns = request.session['selectedColumnsBrowse']
    displayColumnsDic = []
    for item in displayColumns:
        displayColumnsDic.append([item, fieldDic[item]])
    #columns to display end

    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'ehfpiAcc')
        result = result.order_by(order)

    #get publication number and EHF gene number
    publicationNum = len(set(result.values_list('title')))

    geneList = []
    for item in result.values_list('humanHomolog'):
        geneList.append(item[0].strip().upper())
    geneList = list(set(geneList))
    if '' in geneList:
        geneList.remove('')
    ehfNum = len(geneList)
    #end

    guideSelected = []  #not used for index
    return render_to_response('browse/index.html',
                              {'result': result, 'publicationNum': publicationNum, 'ehfNum': ehfNum,
                               'taxonomyTree': taxonomyTree, 'tree_taxonomy': tree_taxonomy,
                               'yearDict': yearDict, 'journalDict': journalDict, 'phenotypeDict': phenotypeDict,
                               'columns': columns, 'badge_taxonomy': badge_taxonomy, 'badge_year': badge_year,
                               'badge_journal': badge_journal, 'badge_phenotype': badge_phenotype,
                               'displayColumnsDic': displayColumnsDic, 'selected': ';'.join(selected),'guideSelected':";".join(guideSelected)},
                              context_instance=RequestContext(request))


#ajax response for filter tree change, the ajax request is from browse.js
def updateTable(request):
    if request.method == 'GET':
        #change columns?

        if 'columns[]' in request.GET:
            selectedColumnsBrowse = request.GET.getlist('columns[]')
            request.session['has_changed_browse'] = True  # set the session, not change
            request.session['selectedColumnsBrowse'] = selectedColumnsBrowse  #store the columns

        if 'has_changed_browse' not in request.session:
            defaultColumns = ['ehfpiAcc', 'geneSymbol', 'species', 'title', 'phenotype']
            request.session['selectedColumnsBrowse'] = defaultColumns  #store the columns

        if 'selected[]' in request.GET:  #interesting, when the tree is not filtered, selected doesn't pass here
            selected = request.GET.getlist('selected[]')
            #store the species list
            speciesList = []
            yearList = []
            journalList = []
            phenotypeList = []

            for item in selected:
                if item.startswith('species_'):
                    speciesList.append(item[item.find('_') + 1:])
                elif item.startswith('year_'):
                    yearList.append(item[item.find('_') + 1:])
                elif item.startswith('journal_'):
                    journalList.append(item[item.find('_') + 1:])
                elif item.startswith('phenotype_'):
                    phenotypeList.append(item[item.find('_') + 1:])
                else:
                    print ""

            #since speciesList store taxonomy id, phenotypeList store phenotype id, journalList store journal id, we get corresponding name
            speciesNameList = []
            if speciesList:
                idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                for item in idMap:
                    speciesNameList.append(item.name)

            phenotypeNameList = []
            if phenotypeList:
                idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                for item in idMap:
                    phenotypeNameList.append(item.name)

            journalNameList = []
            if journalList:
                idMap = idNameMap.objects.filter(acc__in=journalList, type='journal')
                for item in idMap:
                    journalNameList.append(item.name)

            qTotal = Q()
            if speciesNameList:
                qTotal = qTotal & Q(species__in=speciesNameList)
            if yearList:
                qTotal = qTotal & Q(year__in=yearList)
            if journalList:
                qTotal = qTotal & Q(journal__in=journalNameList)
            if phenotypeNameList:
                qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

            result = allEHFPI.objects.filter(qTotal)
        else:
            result = allEHFPI.objects.all()

        #columns to display start!

        displayColumns = request.session['selectedColumnsBrowse']
        displayColumnsDic = []
        for item in displayColumns:
            displayColumnsDic.append([item, fieldDic[item]])
        #columns to display end

        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'ehfpiAcc')
            result = result.order_by(order)

        return render_to_response('browse/updateTable.html', {'result': result, 'displayColumnsDic': displayColumnsDic},
                                  context_instance=RequestContext(request))


def updateBadge(request):
    if request.method == 'GET':
        if request.GET.getlist('selected[]'):
            selected = request.GET.getlist('selected[]')
            #store the species list
            speciesList = []
            yearList = []
            journalList = []
            phenotypeList = []
            for item in selected:
                if item.startswith('species_'):
                    speciesList.append(item[item.find('_') + 1:])
                elif item.startswith('year_'):
                    yearList.append(item[item.find('_') + 1:])
                elif item.startswith('journal_'):
                    journalList.append(item[item.find('_') + 1:])
                elif item.startswith('phenotype_'):
                    phenotypeList.append(item[item.find('_') + 1:])
                else:
                    print ""

            #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
            speciesNameList = []
            if speciesList:
                idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                for item in idMap:
                    speciesNameList.append(item.name)

            phenotypeNameList = []
            if phenotypeList:
                idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                for item in idMap:
                    phenotypeNameList.append(item.name)

            journalNameList = []
            if journalList:
                idMap = idNameMap.objects.filter(acc__in=journalList, type='journal')
                for item in idMap:
                    journalNameList.append(item.name)

            qTotal = Q()
            if speciesNameList:
                qTotal = qTotal & Q(species__in=speciesNameList)
            if yearList:
                qTotal = qTotal & Q(year__in=yearList)
            if journalList:
                qTotal = qTotal & Q(journal__in=journalNameList)
            if phenotypeNameList:
                qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

            result = allEHFPI.objects.filter(qTotal)

            # calculate the badge number start
            # notice the number is based on  ehfpiacc, not gene numbers, so we calculate it from allEHFPI
            #the number displayed in badge, we use four dict to avoid duplicate items in four field

            badge_update = defaultdict(int)

            #used to map name to id
            kingdomDict = {}
            speciesDict = {}
            phenotypeDict = {}
            journalDict = {}
            idMap = idNameMap.objects.filter(type='kingdom')
            for item in idMap:
                kingdomDict[item.name] = item.acc

            idMap = idNameMap.objects.filter(type='species')
            for item in idMap:
                speciesDict[item.name] = item.acc

            idMap = idNameMap.objects.filter(type='phenotype')
            for item in idMap:
                phenotypeDict[item.name] = item.acc

            idMap = idNameMap.objects.filter(type='journal')
            for item in idMap:
                journalDict[item.name] = item.acc

            for item in result:  # note the original data must be the same with models in analysis
                badge_update['kingdom_' + str(kingdomDict.get(item.kingdom, '')) + '_Badge'] += 1
                badge_update['species_' + str(speciesDict.get(item.species, '')) + '_Badge'] += 1
                badge_update['year_' + str(item.year) + '_Badge'] += 1
                badge_update['journal_' + str(journalDict.get(item.journal, '')) + '_Badge'] += 1
                badge_update['phenotype_' + str(phenotypeDict.get(item.phenotype, '')) + '_Badge'] += 1

            badge_update['all'] = len(result)

            badge_update = dict(badge_update)

            #calculate the badge number end

            #get publication number and EHF gene number
            publicationNum = len(set(result.values_list('title')))
            geneList = []
            for item in result.values_list('humanHomolog'):
                geneList.append(item[0].strip().upper())
            geneList = list(set(geneList))
            if '' in geneList:
                geneList.remove('')
            ehfNum = len(geneList)
            #end

            return render_to_response('browse/updateBadge.js',
                                      {'badge_update': json.dumps(badge_update), 'publicationNum': publicationNum,
                                       'ehfNum': ehfNum, 'resultNumber': len(result)},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX+'/browse/')


#download function for browse, this function can be implemented in download application,
# but we want to remove couple.
def download(request):
    if request.method == 'GET':
        if request.GET['selectcolumn'] and request.GET['type']:
            selectcolumn_temp = request.GET['selectcolumn']
            selectcolumn = selectcolumn_temp.split(',')
            type = request.GET['type']
            selected_temp = request.GET['selected']
            selected = selected_temp.split(',')

            if type == 'all':
                data = allEHFPI.objects.values()
            elif type == 'allPage':  # a bit complicated
                # code from updateTable
                #store the species list
                speciesList = []
                yearList = []
                journalList = []
                phenotypeList = []

                for item in selected:
                    if item.startswith('species_'):
                        speciesList.append(item[item.find('_') + 1:])
                    elif item.startswith('year_'):
                        yearList.append(item[item.find('_') + 1:])
                    elif item.startswith('journal_'):
                        journalList.append(item[item.find('_') + 1:])
                    elif item.startswith('phenotype_'):
                        phenotypeList.append(item[item.find('_') + 1:])
                    else:
                        print ""

                #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
                speciesNameList = []
                if speciesList:
                    idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                    for item in idMap:
                        speciesNameList.append(item.name)

                phenotypeNameList = []
                if phenotypeList:
                    idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                    for item in idMap:
                        phenotypeNameList.append(item.name)

                qTotal = Q()
                if speciesNameList:
                    qTotal = qTotal & Q(species__in=speciesNameList)
                if yearList:
                    qTotal = qTotal & Q(year__in=yearList)
                if journalList:
                    qTotal = qTotal & Q(journal__in=journalList)
                if phenotypeNameList:
                    qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

                data = allEHFPI.objects.filter(qTotal).values()

            else:  #type == 'currentPage'
                data = allEHFPI.objects.filter(ehfpiAcc__in=selected).values()

            # code from download app

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=ehfpi.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in selectcolumn:
                rowTitle.append(fieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in data:
                res = []
                for i in selectcolumn:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect(URL_PREFIX+'/browse/')


#gea analysis in browse
def gea(request):
    if request.method == 'GET':
        if request.GET['type']:
            type = request.GET['type']
            selected = request.GET.getlist('selected[]')

            if type == 'all':
                result = allEHFPI.objects.all()
            elif type == 'allPage':  # a bit complicated
                # code from updateTable
                #store the species list
                speciesList = []
                yearList = []
                journalList = []
                phenotypeList = []

                for item in selected:
                    if item.startswith('species_'):
                        speciesList.append(item[item.find('_') + 1:])
                    elif item.startswith('year_'):
                        yearList.append(item[item.find('_') + 1:])
                    elif item.startswith('journal_'):
                        journalList.append(item[item.find('_') + 1:])
                    elif item.startswith('phenotype_'):
                        phenotypeList.append(item[item.find('_') + 1:])
                    else:
                        print ""

                #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
                speciesNameList = []
                if speciesList:
                    idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                    for item in idMap:
                        speciesNameList.append(item.name)

                phenotypeNameList = []
                if phenotypeList:
                    idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                    for item in idMap:
                        phenotypeNameList.append(item.name)

                qTotal = Q()
                if speciesNameList:
                    qTotal = qTotal & Q(species__in=speciesNameList)
                if yearList:
                    qTotal = qTotal & Q(year__in=yearList)
                if journalList:
                    qTotal = qTotal & Q(journal__in=journalList)
                if phenotypeNameList:
                    qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

                result = allEHFPI.objects.filter(qTotal)

            else:  #type == 'currentPage'
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            return render_to_response('analysis/getGeneList.html', {'geneList': ','.join(geneList)})

    return HttpResponseRedirect(URL_PREFIX+'/browse/')


#vtp analysis in browse
def pip(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected'].split(',')

            if type == 'all':
                result = allEHFPI.objects.all()
            elif type == 'allPage':  # a bit complicated
                # code from updateTable
                #store the species list
                speciesList = []
                yearList = []
                journalList = []
                phenotypeList = []

                for item in selected:
                    if item.startswith('species_'):
                        speciesList.append(item[item.find('_') + 1:])
                    elif item.startswith('year_'):
                        yearList.append(item[item.find('_') + 1:])
                    elif item.startswith('journal_'):
                        journalList.append(item[item.find('_') + 1:])
                    elif item.startswith('phenotype_'):
                        phenotypeList.append(item[item.find('_') + 1:])
                    else:
                        print ""

                #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
                speciesNameList = []
                if speciesList:
                    idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                    for item in idMap:
                        speciesNameList.append(item.name)

                phenotypeNameList = []
                if phenotypeList:
                    idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                    for item in idMap:
                        phenotypeNameList.append(item.name)

                qTotal = Q()
                if speciesNameList:
                    qTotal = qTotal & Q(species__in=speciesNameList)
                if yearList:
                    qTotal = qTotal & Q(year__in=yearList)
                if journalList:
                    qTotal = qTotal & Q(journal__in=journalList)
                if phenotypeNameList:
                    qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

                result = allEHFPI.objects.filter(qTotal)

            else:  #type == 'currentPage'
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))

            if '' in geneList:
                geneList.remove('')

            #get the geneSymbol-VTP model
            result = vtpModel.objects.filter(geneSymbol__in=geneList)
            GeneNumberSubmit = len(geneList)  # number of gene submitted
            interactions = len(result)  #number of genes in EHFPI
            GeneNumberIn = GeneNumberSubmit  #number of genes in EHFPI
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
                                      {'GeneNumberSubmit': GeneNumberSubmit, 'GeneNumberIn': GeneNumberIn,'interactions':interactions,
                                       'GeneNumberVTP': GeneNumberVTP, 'result': result},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX+'/browse/')


#network analysis in browse
def network(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected'].split(',')

            if type == 'all':
                result = allEHFPI.objects.all()
            elif type == 'allPage':  # a bit complicated
                # code from updateTable
                #store the species list
                speciesList = []
                yearList = []
                journalList = []
                phenotypeList = []

                for item in selected:
                    if item.startswith('species_'):
                        speciesList.append(item[item.find('_') + 1:])
                    elif item.startswith('year_'):
                        yearList.append(item[item.find('_') + 1:])
                    elif item.startswith('journal_'):
                        journalList.append(item[item.find('_') + 1:])
                    elif item.startswith('phenotype_'):
                        phenotypeList.append(item[item.find('_') + 1:])
                    else:
                        print ""

                #since speciesList store taxonomy id, phenotypeList store phenotype id, we get corresponding name
                speciesNameList = []
                if speciesList:
                    idMap = idNameMap.objects.filter(acc__in=speciesList, type='species')
                    for item in idMap:
                        speciesNameList.append(item.name)

                phenotypeNameList = []
                if phenotypeList:
                    idMap = idNameMap.objects.filter(acc__in=phenotypeList, type='phenotype')
                    for item in idMap:
                        phenotypeNameList.append(item.name)

                qTotal = Q()
                if speciesNameList:
                    qTotal = qTotal & Q(species__in=speciesNameList)
                if yearList:
                    qTotal = qTotal & Q(year__in=yearList)
                if journalList:
                    qTotal = qTotal & Q(journal__in=journalList)
                if phenotypeNameList:
                    qTotal = qTotal & Q(phenotype__in=phenotypeNameList)

                result = allEHFPI.objects.filter(qTotal)

            else:  #type == 'currentPage'
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))

            return render_to_response('analysis/overlapNetworkOthers.html', {'geneList': ','.join(geneList)},context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX+'/browse/')


#the common function of kingdom, group, genus, family and species
def generatePreview(request,id,res,type):
    if type =='species':
        strainList = []
        for item in res:
            strainList.append(item.strain)
        strainList = list(set(strainList))

        result = previewSpeciesModel.objects.filter(strain__in=strainList)
        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'strain')
            result = result.order_by(order)
        publicationNum = len(set(result.values_list('title')))
        pathogenNum = len(set(result.values_list('strain')))

    else:
        speciesList = []
        for item in res:
            speciesList.append(item.speciesTaxonomy)
        speciesList = list(set(speciesList))

        result = previewModel.objects.filter(speciesTaxonomy__in=speciesList)
        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'species')
            result = result.order_by(order)
        publicationNum = len(set(result.values_list('title')))
        pathogenNum = len(set(result.values_list('species')))

    #group info
    groupDic = {
        'ssRNA-':'Single-Stranded Negative-Sense RNA',
        'ssRNA+':'Single-Stranded Positive-Sense RNA',
        'dsDNA':'Double-Stranded DNA',
        'dsRNA':'Double-Stranded RNA',
        'Retro-transcribed':'Retro-transcribed',
        'Gram-':'Gram-negative',
        'Gram+':'Gram-positive'
    }
    if id in groupDic.keys():
        id = groupDic[id]

    return render_to_response('browse/preview.html',{'result': result,'id':id,'type': type,'publicationNum':publicationNum,'pathogenNum':pathogenNum},
                                      context_instance=RequestContext(request))


def kingdom(request, id):
    result = taxonomy.objects.filter(kingdom=id)
    return generatePreview(request,id,result,'kingdom')

def group(request, id):
    #get species list
    result = taxonomy.objects.filter(group=id)
    return generatePreview(request,id,result,'group')

def family(request, id):
    #get species list
    result = taxonomy.objects.filter(family=id)
    return generatePreview(request,id,result,'family')

def genus(request, id):
    #get species list
    result = taxonomy.objects.filter(genus=id)
    return generatePreview(request,id,result,'genus')

def species(request, id):
    #get species list
    result = taxonomy.objects.filter(species=id)
    return generatePreview(request,id,result,'species')

#same work like search result page
def previewResult(request):
    if request.method == 'GET':  # If the form has been submitted...
        pubmedId = request.GET['pubmedId']

        #change columns?
        if 'columns' in request.GET:
            selectedColumns_tmp = request.GET['columns']
            selectedColumns = selectedColumns_tmp.split(',')
            request.session['has_changed_preview'] = True  # set the session, not change
            request.session['selectedColumnsPreview'] = selectedColumns  #store the columns

        if 'has_changed_preview' not in request.session:
            defaultColumns = ['ehfpiAcc', 'geneSymbol', 'entrezId', 'strain']
            request.session['selectedColumnsPreview'] = defaultColumns  #store the columns

        if 'species' in request.GET:
            speciesTaxonomy = request.GET['species']
            result = allEHFPI.objects.filter(pubmedId=pubmedId,speciesTaxonomy=speciesTaxonomy)


        if 'strain' in request.GET:
            strain= request.GET['strain']
            result = allEHFPI.objects.filter(pubmedId=pubmedId,strain=strain)

        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'ehfpiAcc')
            result = result.order_by(order)

        #custom display columns start!
        #[field] in commonVar.py

        #[fieldDes] in commonVar.py

        columns = []
        for i in range(0, len(field), 1):
             columns.append([field[i], fieldDes[i]])
        #custom display columns end

        #columns to display start! [fieldDic] in commonVar.py

        displayColumns = request.session['selectedColumnsPreview']
        displayColumnsDic = []
        for item in displayColumns:
            displayColumnsDic.append([item, fieldDic[item]])
        #columns to display end

        #get publication number and EHF gene number
        geneList = []
        for item in result.values_list('humanHomolog'):
            geneList.append(item[0].strip().upper())
        geneList = list(set(geneList))
        if '' in geneList:
            geneList.remove('')
        ehfNum = len(geneList)
        #end

        #publication info
        article = publication.objects.filter(pubmedId=pubmedId)

        #id info
        idsList = []
        for item in result:
            idsList.append(str(item.ehfpiAcc))
        ids = ','.join(idsList)

        #screen info
        screenId = interaction.objects.filter(ehfpiAcc__in=idsList)
        screenList = []
        for item in screenId:
            if item.screenAcc.screenAcc not in screenList:
                screenList.append(item.screenAcc.screenAcc)

        screenInfo = screen.objects.filter(screenAcc__in=screenList)
        print screenInfo

        return render_to_response('search/previewSearchResult.html',
                                      {'article':article,'ehfNum': ehfNum, 'result': result, 'columns': columns,
                                       'displayColumnsDic': displayColumnsDic,'ids': ids,'screenInfo':screenInfo},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(URL_PREFIX+'/browse/guide')