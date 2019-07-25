from meongg.models import Hackathon


def getDataList(data_from, data_type, column_name, offset=0, size=100):
    startOffset = offset * size
    airQuerySet = Hackathon.objects.order_by('-idx').all().filter(data_type=data_type)
    fromQuerySet = airQuerySet.filter(data_from=data_from)[startOffset:size].values()
    fromQuerySet = list(fromQuerySet)

    return [ i[column_name] for i in reversed(fromQuerySet)]
