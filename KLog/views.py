from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from KLog.LogBuilders.Log4JavaParser import Log4JavaParser


class FileUpload(viewsets.ModelViewSet):
    parser_classes = (Log4JavaParser,)

    def put(self, request, file, format=None):
        file = self.request.FILES['file']
        return Response(status=status.HTTP_400_BAD_REQUEST)
        return file.readline()
