from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
import pprint

# class FileUpload(viewsets.ModelViewSet):
#     parser_classes = (Log4JavaParser,)
#     queryset = Log.objects.all()
#
#     def put(self, request, file=None, format=None):
#         file = self.request.FILES['file']
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#         return file.readline()
from logbuilders.Log4JavaParser import Log4JavaParser


class FileUploadView(APIView):
    parser_classes = (Log4JavaParser, )

    def put(self, request, filename, format=None):
        print(filename)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.data)
        # file_obj = request.data['lul']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)
