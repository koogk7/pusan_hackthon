import datetime
import json
import pprint

from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from meongg.common_const import INSIDE, OUTSIDE, DATA_VALUE, DATA_TIME
from meongg.fuctions import getDataList
from meongg.models import Hackathon
"""
    1. 데이터 페이징 처리해서 가져오기?
    2. 가져온 데이터 뿌려주기!
"""

def index(request):
    print("Entry Index")
    print(request)
    default_type = "CAI"

    insideDataList = getDataList(INSIDE, default_type, DATA_VALUE)
    outsideDataList = getDataList( OUTSIDE, default_type, DATA_VALUE)
    timeDataList = getDataList(INSIDE, default_type, DATA_TIME)
    timeDataList = [i.strftime("%H:%M:%S") for i in timeDataList]

    print(timeDataList)
    json_timeList = json.dumps(timeDataList)

    return render(request, "graph.html", {
        "insideData": insideDataList, "insideTime": json_timeList,
        "outsideData": outsideDataList
    })


def update(request):
    print("Entry update")
    dataType = request.POST["dataType"]
    testAddData = request.POST["testData"]

    response = dict()
    response['data'] = testAddData
    response['insideData'] = getDataList(INSIDE, dataType, DATA_VALUE)
    response['outsideData'] = getDataList( OUTSIDE, dataType, DATA_VALUE)
    response['dataTime'] = getDataList(INSIDE, dataType, DATA_TIME)
    response['dataTime'] = [i.strftime("%H:%M:%S") for i in response['dataTime']]


    response = json.dumps(response)
    return HttpResponse(response)

def addValue(request):
    print("Entry addValue")
    dataType = request.POST["dataType"]
    airQuerySet = Hackathon.objects.order_by('-idx').all().filter(data_type=dataType)

    response = dict()
    response['inside'] = list(airQuerySet.filter(data_from=INSIDE).values())[0][DATA_VALUE]
    response['outside'] = list(airQuerySet.filter(data_from=OUTSIDE).values())[0][DATA_VALUE]
    response['dataTime'] = list(airQuerySet.filter(data_from=OUTSIDE).values())[0][DATA_TIME]
    response['dataTime'] = response['dataTime'].strftime("%H:%M:%S")

    response = json.dumps(response)
    return HttpResponse(response)

