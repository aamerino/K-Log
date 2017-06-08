from django.db.models import Count
from django.db.models.functions import TruncDay

from klog.models import Log


def countExceptions():
    classes_count = Log.objects.values('exception_name') \
        .annotate(total=Count('exception_name')) \
        .order_by('total')
    print(classes_count)
    return classes_count


def getExceptionsWithDateTime():
    return Log.objects\
        .annotate(date=TruncDay('date_time')) \
        .values('date')\
        .annotate(count=Count('id'))\
        .values('date', 'count')\
        .order_by('date')


actionsDict={
    "countExceptions": countExceptions,
    "getExceptionsWithDateTime": getExceptionsWithDateTime
}
