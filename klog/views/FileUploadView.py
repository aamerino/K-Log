from rest_framework.response import Response
from rest_framework.views import APIView

from klog.logbuilders.Log4JavaParser import Log4JavaParser
from klog.models import Log


class FileUploadView(APIView):
    parser_classes = (Log4JavaParser,)

    def put(self, request, filename=None, format=None):
        for log4JavaDTO in request.data:
            Log.objects.create(exception_name=log4JavaDTO.exceptionName,
                               error_class=log4JavaDTO.className,
                               date_time=log4JavaDTO.dateTime)
        content = "file load ok: loaded exceptions= %s" % len(request.data)
        return Response(content, status=200)
