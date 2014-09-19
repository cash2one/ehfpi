from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from download.models import fieldDescription,legacyModel
from download.forms import registerForm
from browse.browse_view_models import allEHFPI
from django.http import HttpResponse
import csv
import types
from django.utils.encoding import smart_str
from ehf.settings import URL_PREFIX
import sys
from ehf.commonVar import fieldDic,field,fieldDes

# Create your views here.
def custom(request):
    description = fieldDescription.objects.all()
    return render_to_response('download/custom.html',{'description':description})

def legacy(request):
    legacy = legacyModel.objects.all()
    return render_to_response('download/legacy.html',{'legacy':legacy})

# the register page
def register(request):
    if request.session.get('has_registered', False):
        return HttpResponseRedirect(URL_PREFIX+'/download/downloadAll/')
    else:
        myForm = registerForm()
        if request.method == 'POST':
            myForm = registerForm(request.POST)
            if myForm.is_valid():
                myForm.save()
                request.session['has_registered'] = True  # set the session
                return HttpResponseRedirect(URL_PREFIX+'/download/downloadAll/')
        return render_to_response('download/register.html',locals(),context_instance=RequestContext(request))

def downloadAll(request):
    # if request.session.get('has_registered', False):   #registered, may cheat? we allow direct download without register
    result = []
    for i in range(0,len(field),1):
        result.append([field[i],fieldDes[i]])

    version = legacyModel.objects.all()
    return render_to_response('download/download.html', {'result': result,'version':version},context_instance=RequestContext(request))
    # else:
    #     return HttpResponseRedirect(URL_PREFIX+'/download/register/')

def gencsv(request):
    if request.method == 'POST':
        checkbox = request.POST.getlist('checkboxDownload')
        version = request.POST['version']

        if len(checkbox):
            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=ehfpi.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in checkbox:
                rowTitle.append(fieldDic[item])
            writer.writerow(rowTitle)

            #get data from database, leave interface for legacy data
            if version == 'ver1':
                data = allEHFPI.objects.values()

            for item in data:
                res = []
                for i in checkbox:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response
        else:
            return HttpResponseRedirect(URL_PREFIX+'/download/downloadAll/')
    else:
        return HttpResponseRedirect(URL_PREFIX+'/download/downloadAll/')

