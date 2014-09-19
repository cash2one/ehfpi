from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from django.shortcuts import render_to_response

from browse.browse_view_models import allEHFPI
from rest.serializers import EhfpiSerializer
from rest_framework.renderers import JSONRenderer, XMLRenderer, YAMLRenderer,BrowsableAPIRenderer
from django.db.models import Q
from ehf.commonVar import fieldDic,field,fieldDes

# csv
from rest_framework_csv.renderers import CSVRenderer

class EHFPICSVRenderer(CSVRenderer):
    def __init__(self):
        super(EHFPICSVRenderer,self).__init__(field)

# Paginated, omitted
class PaginatedCSVRenderer(EHFPICSVRenderer):
    results_field = 'title'

    def render(self, data, media_type=None, renderer_context=None):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return super(PaginatedCSVRenderer, self).render(data, media_type, renderer_context)

class EhfpiList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    renderer_classes = (BrowsableAPIRenderer,EHFPICSVRenderer,XMLRenderer,JSONRenderer)
    def get(self, request, format=None):
        item = allEHFPI.objects.all()
        serializer = EhfpiSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EhfpiSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EhfpiDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    #renderer_classes = (r.CSVRenderer, ) + api_settings.DEFAULT_RENDERER_CLASSES
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,EHFPICSVRenderer,XMLRenderer)
    def get_object(self, pk):
        try:
            return allEHFPI.objects.get(ehfpiAcc=pk)
        except allEHFPI.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = EhfpiSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = EhfpiSerializer(item, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def index(request):
    return render_to_response('rest/rest.html')


#added:2014 04 21 not using ehfpi/a url, implement with multiple query type
class select_entry(APIView):
    """
    List all snippets satisfied the query, or create a new snippet.
    """
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,EHFPICSVRenderer,XMLRenderer)
    def get(self, request, format=None):
        parms = {}
        #query type must be in field,

        for item,value in request.GET.items():
            for item1 in field:
                if item1.upper() == item.upper():  #ignore case
                    valuePrimary = value.split(',')
                    arr = []
                    for val in valuePrimary:  #remove space etc
                        arr.append(val.strip())
                    if '' in arr:  #remove only ''
                        arr.remove('')
                    if len(arr):  #has a parms, otherwise, we remove this
                        parms[item1] = arr

        #construct Q query object
        qTotal = Q()
        for key,value in parms.items():
            qTotal = qTotal & Q(**{key+'__in': value})

        item = allEHFPI.objects.filter(qTotal)
        serializer = EhfpiSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EhfpiSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
@api_view(['GET', 'POST'])
def ehfpi_list(request,pk=None,format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = allEHFPI.objects.all()
        serializer = EhfpiSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EhfpiSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ehfpi_detail(request, pk,format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        ehfpiItem = allEHFPI.objects.get(ehfpiAcc=pk)
    except ehfpiItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EhfpiSerializer(ehfpiItem)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EhfpiSerializer(ehfpiItem, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ehfpiItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''