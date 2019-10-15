from django.shortcuts import render
import csv
from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models.functions import Length
from rest_framework.decorators import api_view
# Create your views here.

#redirect to home file
def home(request):
    return render(request, 'index.html')

#function for searching in the dataset
@api_view(['GET', 'POST', ])
def search(request):
    try:
        search_str = request.GET.get('search_str')
        start_list = []
        if search_str:
            start_list = list(DataSet.objects.annotate(text_len=Length('name')).filter(name__istartswith=search_str).
                              order_by('text_len').values('id', 'name', 'value'))[:25]
            len_start_list = len(start_list)
            if len_start_list < 25:
                start_id_list = [x.get('id') for x in start_list]
                extra_filter = ~Q(id__in=start_id_list)
                all_list = list(DataSet.objects.annotate(text_len=Length('name')).
                                filter(extra_filter, name__icontains=search_str).order_by('text_len').
                                values('id', 'name', 'value'))[:25-len_start_list]
                start_list.extend(all_list)
        return Response(data=start_list, status=status.HTTP_200_OK, template_name='index.html')
    except Exception as e:
        print(e.args)

#function to save data set from the file
def save_data_set(request):
    try:
        msg = 'Data set already present'
        data_count = DataSet.objects.filter().count()
        if data_count == 0:
            with open('search/extra_file/word_search.tsv') as f:
                reader = csv.reader(f, delimiter='\t')
                create_list = []
                for data in reader:
                    obj = DataSet()
                    obj.name = data[0]
                    obj.value = data[1]
                    create_list.append(obj)
                if create_list:
                    DataSet.objects.bulk_create(create_list)
                    msg = 'Data set saved successfully .'
        return HttpResponse(msg)
    except Exception as e:
        print(e.args)
