from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework.response import Response
from rest_framework.views import APIView

from klog.models import Log


class ExceptionView(APIView):
    def get(self, request, action, format=None):
        try:
            return Response(actionsDict[action]())
        except KeyError:
            content = "Invalid method"
            return Response(content, status=405)


def countExceptions():
    classes_count = Log.objects.values('exception_name') \
        .annotate(total=Count('exception_name')) \
        .order_by('total')
    print(classes_count)
    return classes_count

def getExceptionsWithDateTime():
    return Log.objects \
        .annotate(date=TruncDay('date_time')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .values('date', 'count') \
        .order_by('date')


actionsDict = {
    "countExceptions": countExceptions,
    "getExceptionsWithDateTime": getExceptionsWithDateTime,
}
