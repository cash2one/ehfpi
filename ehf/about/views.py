from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
from browse.models import *
from browse.browse_view_models import allEHFPI
from about.models import *
from about.forms import submitForm,contactForm,submitFileForm
from chartit import DataPool, Chart
from ehf.settings import URL_PREFIX
import sys

# Create your views here.
def index(request):
    return render_to_response('about/index.html')

def statistics(request):
    geneNumber = len(gene.objects.values_list("humanHomolog").distinct())
    if len(gene.objects.filter(humanHomolog='')):  #test space in humanHomolog
        geneNumber = geneNumber -1

    speciesNumber = len(pathogen.objects.distinct().values_list("species"))
    kingdomList = pathogen.objects.distinct().values_list("kingdom")
    kingdom = []
    for i in kingdomList:
        kingdom.append(i[0])

    # for kingdom pie chart
    ds = DataPool(
       series=
        [{'options': {
            'source': kingdomStatistics.objects.all()},
          'terms': [
            'kingdom',
            'speciesCount']}
         ])

    cht = Chart(
        datasource = ds,
        series_options =
          [{'options':{
              'type': 'pie',
              'stacking': False},
            'terms':{
              'kingdom': [
                'speciesCount']
              }}],
        chart_options =
          {'title': {
               'text': 'Number of Species for each Kingdom'}})

    return render_to_response('about/statistics.html',{'geneNumber':geneNumber,'speciesNumber':speciesNumber,'kingdom':kingdom,'kingdomPie': cht})

def siteIndex(request):
    return render_to_response('about/siteIndex.html')


def submitHistory(request):
    order = request.GET.get('order_by', '-time')
    submitList = submitModel.objects.all().order_by(order)

    return render_to_response('about/submitHistory.html',{'result':submitList},context_instance=RequestContext(request))

def submit(request):
    if request.method == 'POST':
        if 'type' in request.POST:
            postType = request.POST['type']
            if postType == 'file':
                myFileForm = submitFileForm(request.POST, request.FILES)

                if myFileForm.is_valid():
                    myFileForm.save()
                    return HttpResponseRedirect(URL_PREFIX+'/about/submitHistory')
            else:
                myForm = submitForm(request.POST)
                if myForm.is_valid():
                    myForm.save()
                    return HttpResponseRedirect(URL_PREFIX+'/about/submitHistory')

    myForm = submitForm()
    myFileForm = submitFileForm()

    return render_to_response('about/submit.html',locals(),context_instance=RequestContext(request))

def contact(request):
    myForm = contactForm()
    if request.method == 'POST':
        myForm = contactForm(request.POST)
        if myForm.is_valid():
            myForm.save()
            # send a mail to administrator
            # get administrator email from settings.py
            # title = myForm.cleaned_data['title']
            # email = myForm.cleaned_data['email']
            # content = myForm.cleaned_data['content']
            # send_mail(title, content, email, [ADMIN_EMAIL], fail_silently=True)
            return HttpResponseRedirect(URL_PREFIX+'/about/thanks/')

    return render_to_response('about/contact.html',locals(),context_instance=RequestContext(request))

def copyright(request):
    return render_to_response('about/copyright.html')

def external(request):
    return render_to_response('about/external.html')

def thanks(request):
    return render_to_response('about/thanks.html')
