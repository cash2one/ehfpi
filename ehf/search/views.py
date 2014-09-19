from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from browse.models import *
from django.db.models import Q
from browse.browse_view_models import allEHFPI
from news.models import news
from search.models import das
from django.shortcuts import HttpResponseRedirect
from analysis.models import vtpModel
from django.utils.encoding import smart_str,smart_unicode
import csv
from ehf.settings import PAGINATION_DEFAULT_PAGINATION
from ehf.settings import URL_PREFIX
from ehf.commonVar import fieldDic,field,fieldDes
from analysis.models import idNameMap,heatmapModel

def index(request):
    return HttpResponseRedirect(URL_PREFIX)


#given query and searchType, return a result
# we define this function from quick search, because gea analysis use this function too
def getResult(query, searchType):
    result = ""
    if searchType == 'gene':  #exact match
        result = allEHFPI.objects.filter(
            Q(drosophilaGene__iexact=query) |Q(humanHomolog__iexact=query)| Q(entrezId__iexact=query) | Q(uniprotId__iexact=query) | Q(
                previousName__icontains=query) | Q(synonyms__icontains=query) | Q(ensemblGeneId__iexact=query))
    elif searchType == 'pathogen':
        result = allEHFPI.objects.filter(
            Q(fullName__iexact=query) | Q(abbreviation__iexact=query) | Q(aliases__iexact=query) | Q(
                strain__iexact=query) | Q(genus__iexact=query)| Q(species__iexact=query) | Q(family__iexact=query) | Q(
                group__iexact=query) | Q(kingdom__iexact=query))
    elif searchType == 'publication':
        result = allEHFPI.objects.filter(
            Q(pubmedId__iexact=query) | Q(title__iexact=query) | Q(author__iexact=query) | Q(
                journal__iexact=query) | Q(year__iexact=query))
    elif searchType == 'ehfpiacc':
        result = allEHFPI.objects.filter(Q(ehfpiAcc__iexact=query))
    else:
        result = allEHFPI.objects.filter(
            Q(drosophilaGene__iexact=query) |Q(humanHomolog__iexact=query) | Q(entrezId__iexact=query) | Q(uniprotId__iexact=query) | Q(
                previousName__icontains=query) | Q(synonyms__icontains=query) |Q(ensemblGeneId__iexact=query)|
                Q(fullName__iexact=query) | Q(
                abbreviation__iexact=query) | Q(aliases__iexact=query) | Q(strain__iexact=query) | Q(
                species__iexact=query) | Q(genus__iexact=query)| Q(family__iexact=query) | Q(group__iexact=query) | Q(
                kingdom__iexact=query) | Q(pubmedId__iexact=query) | Q(title__iexact=query) | Q(
                author__iexact=query) | Q(journal__iexact=query) | Q(year__iexact=query) | Q(
                ehfpiAcc__iexact=query))
    return result


# Create your views here.
# code for quick search
def quickSearch(request):

    if request.method == 'GET':  # If the form has been submitted...
        searchType = request.GET['searchType']
        query = request.GET['query']

        #change columns?
        if 'columns' in request.GET:
            selectedColumns_tmp = request.GET['columns']
            selectedColumns = selectedColumns_tmp.split(',')
            request.session['has_changed'] = True  # set the session, not change
            request.session['selectedColumns'] = selectedColumns  #store the columns

        if 'has_changed' not in request.session:
            defaultColumns = ['ehfpiAcc', 'geneSymbol', 'entrezId', 'strain', 'title']
            request.session['selectedColumns'] = defaultColumns  #store the columns

        if request.GET['query']:  #not empty search
            result = getResult(query.strip(), searchType)

            if (len(result)):
                #sort the column
                order = request.GET.get('order_by', 'ehfpiAcc')
                result = result.order_by(order)


            #custom display columns start!
            columns = []
            for i in range(0, len(field), 1):
                columns.append([field[i], fieldDes[i]])
            #custom display columns end

            #columns to display start!

            displayColumns = request.session['selectedColumns']
            if displayColumns == '':
                displayColumns = ['ehfpiAcc', 'geneSymbol', 'entrezId', 'strain', 'title']
            displayColumnsDic = []
            for item in displayColumns:
                displayColumnsDic.append([item, fieldDic[item]])
            #columns to display end

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
            return render_to_response('search/searchResult.html',
                                      {'searchType': searchType, 'query': query, 'publicationNum': publicationNum,
                                       'ehfNum': ehfNum, 'result': result, 'columns': columns,
                                       'displayColumnsDic': displayColumnsDic},
                                      context_instance=RequestContext(request))
        else:
            all_news = news.objects.all()[0:4]
            mark = 0
            if len(news.objects.all()) > 4:
                mark = 1
            return render_to_response('index.html', {'news': all_news, 'mark': mark})
    else:
        return render_to_response('index.html')


# code for advanced search
def advancedSearch(request):
    if request.method == 'GET':  # If the form has been submitted...
        if len(request.GET):
            #change columns?
            if 'columns' in request.GET:
                selectedColumns_tmp = request.GET['columns']
                selectedColumns = selectedColumns_tmp.split(',')
                request.session['has_changed'] = True  # set the session, not change
                request.session['selectedColumns'] = selectedColumns  #store the columns

            if 'has_changed' not in request.session:
                defaultColumns = ['ehfpiAcc', 'geneSymbol', 'entrezId', 'strain', 'title']
                request.session['selectedColumns'] = defaultColumns  #store the columns

            conditionNum = 0  # search condition number, based on smartSearchSubtype number in POST
            condition = {}  #map to store the condition
            type = {}  #store the search type of each condition
            for key, value in request.GET.iteritems():
                if key.startswith("smartSearchSubtype"):
                    conditionNum = conditionNum + 1
                    conKey = key[key.rfind("_") + 1:]
                    condition[conKey] = ""  #initialize the map
                    type[conKey] = value

            #parse condition
            for conditionKey, conditionValue in type.items():
                if conditionValue == "publication":  #AND phrase
                    pubList = {}
                if conditionValue == "pathogen":  #AND phrase
                    pathogenList = {}

                for key, value in request.GET.iteritems():
                    if key.find("_") != -1:
                        if key[key.rfind("_") + 1:] == conditionKey:  #parse it
                            if conditionValue == "gene":
                                if key.startswith("geneList"):  #get gene list
                                    condition[conditionKey] = value
                            elif conditionValue == "pathogen":
                                if key.startswith("pathogen_species"):
                                    pathogenList["species"] = request.GET.getlist(key)
                                if key.startswith("pathogen_kingdom"):
                                    pathogenList["kingdom"] = request.GET.getlist(key)

                            elif conditionValue == "publication":
                                if key.startswith("publication_title"):
                                    pubList["title"] = request.GET.getlist(key)
                                elif key.startswith("publication_journal"):
                                    pubList["journal"] = request.GET.getlist(key)
                                elif key.startswith("publication_year"):
                                    pubList["year"] = request.GET.getlist(key)
                                else:
                                    print ""

                            elif conditionValue == "scope":
                                if key.startswith("scope"):
                                    condition[conditionKey] = request.GET.getlist(key)
                            elif conditionValue == "function":
                                if key.startswith("function"):
                                    condition[conditionKey] = request.GET.getlist(key)
                            else:
                                print "It is impossible"

                if conditionValue == "publication":  #AND phrase
                    condition[conditionKey] = pubList

                if conditionValue == "pathogen":  #AND phrase
                    condition[conditionKey] = pathogenList

            # combine the search condition
            # we can combine the query condition with Q object
            qDict = {}
            for key, value in condition.items():
                if type[key] == "gene":
                    if value.find(",") > 0:
                        geneList_temp = value.split(",")  #use comma ,
                    else:
                        geneList_temp = value.split("\r\n")  #use return
                    geneList = []
                    for i in geneList_temp:
                        geneList.append(i.strip())
                    geneList = list(set(geneList))
                    qDict[key] = Q(drosophilaGene__in=geneList) | Q(humanHomolog__in=geneList) |Q(entrezId__in=geneList) | Q(uniprotId__in=geneList) \

                    #since previous name and synonyms may have multiple, so we use icontains
                    for aa in geneList:
                        qDict[key] = qDict[key] | Q(synonyms__icontains=aa) | Q(previousName__icontains=aa)

                elif type[key] == 'pathogen':
                    speciesList = value["species"]
                    kingdomList = value["kingdom"]

                    if "all" in speciesList:  #all species
                        if "all" in kingdomList:  #check the kingdom
                            qDict[key] = ""
                        else:
                            qDict[key] = Q(kingdom__in=kingdomList)
                    else:  # not all species
                        qDict[key] = Q(species__in=speciesList)

                elif type[key] == 'publication':
                    titleList = value["title"]
                    journalList = value["journal"]
                    yearList = value["year"]
                    q_title = Q(title__in=titleList)
                    q_journal = Q(journal__in=journalList)
                    q_year = Q(year__in=yearList)

                    if "all" in titleList:
                        if "all" in journalList:
                            if "all" in yearList:
                                qDict[key] = ""
                            else:
                                qDict[key] = q_year
                        else:
                            if "all" in yearList:
                                qDict[key] = q_journal
                            else:
                                qDict[key] = q_journal & q_year
                    else:
                        if "all" in journalList:
                            if "all" in yearList:
                                qDict[key] = q_title
                            else:
                                qDict[key] = q_title & q_year
                        else:
                            if "all" in yearList:
                                qDict[key] = q_title & q_journal
                            else:
                                qDict[key] = q_title & q_journal & q_year

                elif type[key] == 'scope':
                    scopeList = value
                    if "all" in scopeList:
                        qDict[key] = ""
                    else:
                        qDict[key] = Q(scope__in=scopeList)

                elif type[key] == 'function':
                    functionList = value
                    if "all" in functionList:
                        qDict[key] = ""
                    else:
                        qDict[key] = Q(phenotype__in=functionList)
                else:
                    print "It is impossible!"

            result = ""
            if conditionNum > 1:
                qTotal = Q()
                comp = request.GET.get("smartComparator")
                #print comp
                containAll = False
                for key, value in qDict.items():
                    if value == "":
                        containAll = True

                if containAll and comp == "or":  # if contains all and smartComparator = OR, we return all list
                    result = allEHFPI.objects.all()
                else:  # condition doesn't contains all or smartComparator = "AND"
                    for key, value in qDict.items():
                        if value:
                            if comp == "and":
                                qTotal = qTotal & value
                            else:
                                qTotal = qTotal | value
                result = allEHFPI.objects.filter(qTotal)
            else:
                for key, value in qDict.items():
                    if value:
                        result = allEHFPI.objects.filter(value)
                    else:
                        result = allEHFPI.objects.all()

            if (len(result)):
                #sort the column
                order = request.GET.get('order_by', 'ehfpiAcc')
                result = result.order_by(order)

                # else:   #only one condition, complicated!!!
            #     for key,value in condition.items():
            #         if type[key]=="gene":
            #             geneList_temp = value.split("\r\n")
            #             geneList = []
            #             for i in geneList_temp:
            #                 geneList.append(i.strip())
            #             geneList = list(set(geneList))
            #             q = Q(geneSymbol__in = geneList) | Q(entrezId__in = geneList) | Q(uniprotId__in = geneList) | Q(previousName__in = geneList) | Q(synonyms__in = geneList)
            #             result = allEHFPI.objects.filter(q)
            #
            #         elif type[key] == 'pathogen':
            #             speciesList = value["species"]
            #             kingdomList = value["kingdom"]
            #
            #             if "all" in speciesList:  #all species
            #                 if "all" in kingdomList:  #check the kingdom
            #                     result = allEHFPI.objects.all()
            #                 else:
            #                     result = allEHFPI.objects.filter(Q(kingdom__in = kingdomList))
            #             else:   # not all species
            #                 result = allEHFPI.objects.filter(Q(species__in = speciesList))
            #
            #         elif type[key] == 'publication':
            #             authorList = value["author"]
            #             journalList = value["journal"]
            #             yearList = value["year"]
            #             q_author = Q(author__in=authorList)
            #             q_journal = Q(journal__in=journalList)
            #             q_year = Q(year__in=yearList)
            #
            #             if "all" in authorList:
            #                 if "all" in journalList:
            #                     if "all" in yearList:
            #                         q = ""
            #                     else:
            #                         q = q_year
            #                 else:
            #                     if "all" in yearList:
            #                         q = q_journal
            #                     else:
            #                         q = q_journal & q_year
            #             else:
            #                 if "all" in journalList:
            #                     if "all" in yearList:
            #                         q = q_author
            #                     else:
            #                         q = q_author & q_year
            #                 else:
            #                     if "all" in yearList:
            #                         q = q_author & q_journal
            #                     else:
            #                         q = q_author & q_journal & q_year
            #
            #             if q:
            #                 result = allEHFPI.objects.filter(q)
            #             else:
            #                 result = allEHFPI.objects.all()
            #
            #         elif type[key] == 'scope':
            #             scopeList = value
            #             if "all" in scopeList:
            #                 result = allEHFPI.objects.all()
            #             else:
            #                 result = allEHFPI.objects.filter(Q(scope__in = scopeList))
            #
            #         elif type[key] == 'function':
            #             functionList = value
            #             if "all" in functionList:
            #                 result = allEHFPI.objects.all()
            #             else:
            #                 result = allEHFPI.objects.filter(Q(phenotype__in=functionList))
            #
            #         else:
            #             print "It is impossible!"
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

            # 20140418, when add analysis function to advanced search result, to avoid the above complex calculation, we send all
            # ehfpiacc of result as a hidden div in the result page
            idsList = []
            for item in result:
                idsList.append(str(item.ehfpiAcc))
            ids = ','.join(idsList)

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

            return render_to_response('search/advancedSearchResult.html',
                                      {'result': result, 'publicationNum': publicationNum, 'ehfNum': ehfNum,
                                       'columns': columns, 'displayColumnsDic': displayColumnsDic, 'ids': ids},
                                      context_instance=RequestContext(request))

    return render_to_response('search/advancedSearch.html', context_instance=RequestContext(request))


# process the ajax get in addParms functions, it passes {'r': row,'st': searchType}
def ajaxParms(request):
    if request.method == 'GET':
        rowId = request.GET['r']
        searchType = request.GET['st']
        if searchType == "gene":  # gene tab
            return render_to_response('search/ajaxGene.do', {'row': rowId})

        elif searchType == "pathogen":
            kingdom_list = pathogen.objects.order_by('kingdom').distinct().values_list("kingdom")
            species_list = pathogen.objects.order_by('species').distinct().values_list("species")
            kingdom = []
            species = []
            for item in kingdom_list:
                kingdom.append(item[0].strip())
            for item in species_list:
                species.append(item[0].strip())
            return render_to_response('search/ajaxPathogen.do', {'kingdom': kingdom, 'species': species, 'row': rowId})

        elif searchType == "publication":
            title_list = publication.objects.order_by('title').distinct().values_list("title")
            journal_list = publication.objects.order_by('journal').distinct().values_list("journal")
            year_list = publication.objects.order_by('year').distinct().values_list("year")
            title = []
            journal = []
            year = []
            for item in title_list:
                title.append(item[0].strip())
            for item in journal_list:
                journal.append(item[0].strip())
            for item in year_list:
                year.append(item[0])
            return render_to_response('search/ajaxPublication.do',
                                      {'title': title, 'journal': journal, 'year': year, 'row': rowId})

        elif searchType == "scope":
            scope_list = screen.objects.order_by('scope').distinct().values_list("scope")
            scope = []
            for item in scope_list:
                scope.append(item[0].strip())
            return render_to_response('search/ajaxScope.do', {'scope': scope, 'row': rowId})

        elif searchType == "function":
            function_list = screen.objects.order_by('phenotype').distinct().values_list("phenotype")  # ehf function == phenotype ?
            function = []
            for item in function_list:
                function.append(item[0].strip())
            return render_to_response('search/ajaxFunction.do', {'function': function, 'row': rowId})

        else:
            return render_to_response('search/advancedSearch.html')
            #return render_to_response('search/advancedSearch.html')
    else:
        return render_to_response('search/advancedSearch.html')


# this function get the corresponding species select form based on kingdom select form
def getSpecies(request):
    if request.method == 'GET':
        rowId = request.GET['r']
        val = request.GET['stv']
        selectVal = val.split(",")
        species_list = []

        if "all" in selectVal:  #all in the list
            species_list = pathogen.objects.distinct().values_list("species")
        else:
            species_list = pathogen.objects.filter(kingdom__in=selectVal).distinct().values_list("species")

        species = []
        for item in species_list:
            species.append(item[0])

        return render_to_response('search/getSpecies.do', {'row': rowId, 'species': species})


#this is test case
def searchDetail(request, id):
    result = allEHFPI.objects.filter(ehfpiAcc__iexact=id)
    geneSymbol = ''
    for item in result:
        geneSymbol = item.humanHomolog
    dasRes = das.objects.filter(geneSymbol__iexact=geneSymbol)

    return render_to_response('search/searchDetail.html', {'id': id, 'result': result, 'das': dasRes})


#download function for browse, this function can be implemented in download application,
# but we want to remove couple.
def download(request):
    if request.method == 'GET':
        if 'selectcolumn' in request.GET and 'type' in request.GET:
            selectcolumn_temp = request.GET['selectcolumn']
            selectcolumn = selectcolumn_temp.split(',')
            type = request.GET['type']
            selected_temp = request.GET['selected']
            selected = selected_temp.split(',')

            if type == 'allPage':  # a bit complicated

                query = selected[0]
                searchType = selected[1]
                data = getResult(query,searchType).values()

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

    return HttpResponseRedirect(URL_PREFIX)


def downloadAdvanced(request):
    print request
    if request.method == 'POST':
        if 'selectcolumn[]' in request.POST and 'selected[]' in request.POST:
            selectcolumn = request.POST.getlist('selectcolumn[]')
            selected = request.POST.getlist('selected[]')

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

    return HttpResponseRedirect(URL_PREFIX)


#gea analysis in search
def gea(request):
    if request.method == 'GET':
        if request.GET['type']:
            type = request.GET['type']
            selected = request.GET.getlist('selected[]')

            if type == 'allPage':  # a bit complicated
                query = selected[0]
                searchType = selected[1]
                result = getResult(query.strip(), searchType)

            else:  #type == 'currentPage'
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            return render_to_response('analysis/getGeneList.html', {'geneList': ','.join(geneList)})

    return HttpResponseRedirect(URL_PREFIX)


#network analysis in search
#first same as vtp, and in the specified template call ajax
def network(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected'].split(',')
            print type,selected

            if type == 'allPage':  # a bit complicated
                query = selected[0]
                searchType = selected[1]
                result = getResult(query.strip(), searchType)

            else:  #type == 'currentPage'
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            return render_to_response('analysis/overlapNetworkOthers.html', {'geneList': ','.join(geneList)},context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)


def networkAdvanced(request):
    if request.method == 'POST':
        if 'selected' in request.POST:
            selected = request.POST['selected']
            selected = selected.split(',')

            result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))

            return render_to_response('analysis/overlapNetworkOthers.html', {'geneList': ','.join(geneList)},context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)


#gea analysis in advanced search
def geaAdvanced(request):
    if request.method == 'POST':
        if 'selected[]' in request.POST:
            selected = request.POST.getlist('selected[]')
            result = allEHFPI.objects.filter(ehfpiAcc__in=selected)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            return render_to_response('analysis/getGeneList.html', {'geneList': ','.join(geneList)})

    return HttpResponseRedirect(URL_PREFIX)


#pip analysis in browse
def pip(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected'].split(',')

            if type == 'allPage':  # a bit complicated
                query = selected[0]
                searchType = selected[1]
                result = getResult(query.strip(), searchType)

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
            GeneNumberIn = GeneNumberSubmit  #number of genes in EHFPI
            interactions = len(result)  #interactions number
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
                                       'GeneNumberVTP': GeneNumberVTP, 'ids':','.join(vtpList),'result': result},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)


#pip analysis in advanced search
def pipAdvanced(request):
    if request.method == 'GET':
        if 'queryType' in request.GET:
            queryType = request.GET['queryType']
            if queryType == 'currentPage':
                selected = request.GET['selected'].split(',')
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)
            else:
                conditionNum = 0  # search condition number, based on smartSearchSubtype number in POST
                condition = {}  #map to store the condition
                type = {}  #store the search type of each condition
                for key, value in request.GET.iteritems():
                    if key.startswith("smartSearchSubtype"):
                        conditionNum = conditionNum + 1
                        conKey = key[key.rfind("_") + 1:]
                        condition[conKey] = ""  #initialize the map
                        type[conKey] = value

                #parse condition
                for conditionKey, conditionValue in type.items():
                    if conditionValue == "publication":  #AND phrase
                        pubList = {}
                    if conditionValue == "pathogen":  #AND phrase
                        pathogenList = {}

                    for key, value in request.GET.iteritems():
                        if key.find("_") != -1:
                            if key[key.rfind("_") + 1:] == conditionKey:  #parse it
                                if conditionValue == "gene":
                                    if key.startswith("geneList"):  #get gene list
                                        condition[conditionKey] = value
                                elif conditionValue == "pathogen":
                                    if key.startswith("pathogen_species"):
                                        pathogenList["species"] = request.GET.getlist(key)
                                    if key.startswith("pathogen_kingdom"):
                                        pathogenList["kingdom"] = request.GET.getlist(key)

                                elif conditionValue == "publication":
                                    if key.startswith("publication_title"):
                                        pubList["title"] = request.GET.getlist(key)
                                    elif key.startswith("publication_journal"):
                                        pubList["journal"] = request.GET.getlist(key)
                                    elif key.startswith("publication_year"):
                                        pubList["year"] = request.GET.getlist(key)
                                    else:
                                        print ""

                                elif conditionValue == "scope":
                                    if key.startswith("scope"):
                                        condition[conditionKey] = request.GET.getlist(key)
                                elif conditionValue == "function":
                                    if key.startswith("function"):
                                        condition[conditionKey] = request.GET.getlist(key)
                                else:
                                    print "It is impossible"

                    if conditionValue == "publication":  #AND phrase
                        condition[conditionKey] = pubList

                    if conditionValue == "pathogen":  #AND phrase
                        condition[conditionKey] = pathogenList

                # combine the search condition
                # we can combine the query condition with Q object
                qDict = {}
                for key, value in condition.items():
                    if type[key] == "gene":
                        if value.find(",") > 0:
                            geneList_temp = value.split(",")  #use comma ,
                        else:
                            geneList_temp = value.split("\r\n")  #use return
                        geneList = []
                        for i in geneList_temp:
                            geneList.append(i.strip())
                        geneList = list(set(geneList))
                        qDict[key] = Q(drosophilaGene__in=geneList) | Q(humanHomolog__in=geneList) |Q(entrezId__in=geneList) | Q(uniprotId__in=geneList) \

                        #since previous name and synonyms may have multiple, so we use icontains
                        for aa in geneList:
                            qDict[key] = qDict[key] | Q(synonyms__icontains=aa) | Q(previousName__icontains=aa)

                    elif type[key] == 'pathogen':
                        speciesList = value["species"]
                        kingdomList = value["kingdom"]

                        if "all" in speciesList:  #all species
                            if "all" in kingdomList:  #check the kingdom
                                qDict[key] = ""
                            else:
                                qDict[key] = Q(kingdom__in=kingdomList)
                        else:  # not all species
                            qDict[key] = Q(species__in=speciesList)

                    elif type[key] == 'publication':
                        titleList = value["title"]
                        journalList = value["journal"]
                        yearList = value["year"]
                        q_title = Q(title__in=titleList)
                        q_journal = Q(journal__in=journalList)
                        q_year = Q(year__in=yearList)

                        if "all" in titleList:
                            if "all" in journalList:
                                if "all" in yearList:
                                    qDict[key] = ""
                                else:
                                    qDict[key] = q_year
                            else:
                                if "all" in yearList:
                                    qDict[key] = q_journal
                                else:
                                    qDict[key] = q_journal & q_year
                        else:
                            if "all" in journalList:
                                if "all" in yearList:
                                    qDict[key] = q_title
                                else:
                                    qDict[key] = q_title & q_year
                            else:
                                if "all" in yearList:
                                    qDict[key] = q_title & q_journal
                                else:
                                    qDict[key] = q_title & q_journal & q_year

                    elif type[key] == 'scope':
                        scopeList = value
                        if "all" in scopeList:
                            qDict[key] = ""
                        else:
                            qDict[key] = Q(scope__in=scopeList)

                    elif type[key] == 'function':
                        functionList = value
                        if "all" in functionList:
                            qDict[key] = ""
                        else:
                            qDict[key] = Q(phenotype__in=functionList)
                    else:
                        print "It is impossible!"

                result = ""
                if conditionNum > 1:
                    qTotal = Q()
                    comp = request.GET.get("smartComparator")
                    #print comp
                    containAll = False
                    for key, value in qDict.items():
                        if value == "":
                            containAll = True

                    if containAll and comp == "or":  # if contains all and smartComparator = OR, we return all list
                        result = allEHFPI.objects.all()
                    else:  # condition doesn't contains all or smartComparator = "AND"
                        for key, value in qDict.items():
                            if value:
                                if comp == "and":
                                    qTotal = qTotal & value
                                else:
                                    qTotal = qTotal | value
                    result = allEHFPI.objects.filter(qTotal)
                else:
                    for key, value in qDict.items():
                        if value:
                            result = allEHFPI.objects.filter(value)
                        else:
                            result = allEHFPI.objects.all()

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            if '' in geneList:
                geneList.remove('')


            #get the geneSymbol-VTP model
            result = vtpModel.objects.filter(geneSymbol__in=geneList)
            GeneNumberSubmit = len(geneList)  # number of gene submitted
            GeneNumberIn = GeneNumberSubmit  #number of genes in EHFPI
            interactions = len(result)  #interactions number
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
                                       'GeneNumberVTP': GeneNumberVTP, 'ids':','.join(vtpList),'result': result},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)

#pip analysis in heatmap search
def pipHeatmap(request):
    if request.method == 'GET':
        if 'queryType' in request.GET:
            queryType = request.GET['queryType']
            if queryType == 'currentPage':
                selected = request.GET['selected'].split(',')
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)
            else:
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
                        articleTemp = item[item.find('_')+1:]
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
                    result = allEHFPI.objects.filter(speciesTaxonomy__in=speciesList, pubmedId__in=articleList, humanHomolog__in=geneList)
                    #print result
                else:
                    result = ''

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            if '' in geneList:
                geneList.remove('')


            #get the geneSymbol-VTP model
            result = vtpModel.objects.filter(geneSymbol__in=geneList)
            GeneNumberSubmit = len(geneList)  # number of gene submitted
            GeneNumberIn = GeneNumberSubmit  #number of genes in EHFPI
            interactions = len(result)  #interactions number
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
                                       'GeneNumberVTP': GeneNumberVTP, 'ids':','.join(vtpList),'result': result},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)

#pip analysis in preview search
def pipPreview(request):
    if request.method == 'GET':
        if 'queryType' in request.GET:
            queryType = request.GET['queryType']
            if queryType == 'currentPage':
                selected = request.GET['selected'].split(',')
                result = allEHFPI.objects.filter(ehfpiAcc__in=selected)
            else:
                pubmedId = request.GET['pubmedId']
                if 'species' in request.GET:
                    speciesTaxonomy = request.GET['species']
                    result = allEHFPI.objects.filter(pubmedId=pubmedId,speciesTaxonomy=speciesTaxonomy)

                if 'strain' in request.GET:
                    strain= request.GET['strain']
                    result = allEHFPI.objects.filter(pubmedId=pubmedId,strain=strain)

            geneList = []
            for item in result:
                geneList.append(item.humanHomolog)
            geneList = list(set(geneList))
            if '' in geneList:
                geneList.remove('')


            #get the geneSymbol-VTP model
            result = vtpModel.objects.filter(geneSymbol__in=geneList)
            GeneNumberSubmit = len(geneList)  # number of gene submitted
            GeneNumberIn = GeneNumberSubmit  #number of genes in EHFPI
            interactions = len(result)  #interactions number
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
                                       'GeneNumberVTP': GeneNumberVTP, 'ids':','.join(vtpList),'result': result},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect(URL_PREFIX)