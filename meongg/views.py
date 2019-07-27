import datetime
import json
import pprint

from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from meongg.common_const import INSIDE, OUTSIDE, DATA_VALUE, DATA_TIME, API
from meongg.fuctions import getDataList
from meongg.models import Hackathon


def index(request):
    print("Entry Index")
    print(request)
    default_type = "CAI"

    insideDataList = getDataList(INSIDE, default_type, DATA_VALUE)
    outsideDataList = getDataList(OUTSIDE, default_type, DATA_VALUE)

    timeDataList = getDataList(INSIDE, default_type, DATA_TIME)
    timeDataList = [i.strftime("%H:%M:%S") for i in timeDataList]

    apiDataList = getDataList(API, default_type, DATA_VALUE)

    apiNullSize = len(insideDataList) - len(apiDataList)
    for i in range(0, apiNullSize):
        apiDataList.append(apiDataList[-1])

    print(timeDataList)
    json_timeList = json.dumps(timeDataList)

    return render(request, "graph.html", {
        "insideData": insideDataList, "insideTime": json_timeList,
        "outsideData": outsideDataList, "apiData" : apiDataList
    })


def update(request):
    print("Entry update")
    dataType = request.POST["dataType"]

    response = dict()
    response['insideData'] = getDataList(INSIDE, dataType, DATA_VALUE)
    response['outsideData'] = getDataList( OUTSIDE, dataType, DATA_VALUE)
    response['dataTime'] = getDataList(INSIDE, dataType, DATA_TIME)
    response['dataTime'] = [i.strftime("%H:%M:%S") for i in response['dataTime']]


    response = json.dumps(response)
    return HttpResponse(response)

def addValue(request):
    print("Entry addValue")
    dataType = request.POST["dataType"]
    offset = 0
    airQuerySet = Hackathon.objects.order_by('-idx').all().filter(data_type=dataType)


    response = dict()
    response['inside'] = list(airQuerySet.filter(data_from=INSIDE).values())[offset][DATA_VALUE]
    response['outside'] = list(airQuerySet.filter(data_from=OUTSIDE).values())[offset][DATA_VALUE]
    response['api'] = list(airQuerySet.filter(data_from=API).values())[offset][DATA_VALUE]
    response['dataTime'] = list(airQuerySet.filter(data_from=OUTSIDE).values())[offset][DATA_TIME]
    response['dataTime'] = response['dataTime'].strftime("%H:%M:%S")

    print(len(list(airQuerySet.filter(data_from=OUTSIDE).values())))

    response = json.dumps(response)
    return HttpResponse(response)

# def saveData(request):