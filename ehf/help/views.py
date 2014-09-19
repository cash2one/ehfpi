from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render_to_response('help/indexHelp.html')

def ehfHelp(request):
    return render_to_response('help/ehfHelp.html')

def searchHelp(request):
    return render_to_response('help/searchHelp.html')

def browseHelp(request):
    return render_to_response('help/browseHelp.html')

def analysisHelp(request):
    return render_to_response('help/analysisHelp.html')

def restHelp(request):
    return render_to_response('help/restHelp.html')

def citeHelp(request):
    return render_to_response('help/citeHelp.html')

