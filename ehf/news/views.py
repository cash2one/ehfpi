from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from browse.models import *
from django.template import RequestContext
from news.models import news

# Create your views here.
def index(request):
    all_news = news.objects.all()
    return render_to_response('news/index.html',{'news':all_news},context_instance=RequestContext(request))

# def detail(request,id):
#     current_news = news.objects.filter(newsId=id)
#     return render_to_response('news/detail.html',{'news':current_news})
