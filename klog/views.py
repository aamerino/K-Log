import pprint

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from klog.logbuilders.Log4JavaParser import Log4JavaParser
from klog.models import Log


class FileUploadView(APIView):
    parser_classes = (Log4JavaParser, )

    def put(self, request, filename, format=None):
        print(filename)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.data)
        for log4JavaDTO in request.data:
            print(log4JavaDTO.dateTime)
            Log.objects.create(exception_name=log4JavaDTO.exceptionName,
                               error_class=log4JavaDTO.exceptionName,
                               date_time=log4JavaDTO.dateTime)
        return Response(status=204)


class ClientView(APIView):

    def get(self, request, format=None):
        classes_count = Log.objects.values('exception_name')\
            .annotate(total=Count('exception_name'))\
            .order_by('total')
        return Response(classes_count)