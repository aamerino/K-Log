from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework.response import Response

from klog.models import Log


def countExceptions():
    classes_count = Log.objects.values('exception_name') \
        .annotate(total=Count('exception_name')) \
        .order_by('total')
    print(classes_count)
    return classes_count


def getExceptionsWithDateTime():
    print(Log.objects \
          .annotate(day=TruncDay('date_time')))
    return Log.objects\
        .annotate(day=TruncDay('date_time'))\
        .values('day')\
        .annotate(c=Count('id'))\
        .values('day', 'c')


actionsDict={
    "countExceptions": countExceptions,
    "getExceptionsWithDateTime": getExceptionsWithDateTime
}
