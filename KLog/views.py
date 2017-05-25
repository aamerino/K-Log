from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


# class FileUpload(viewsets.ModelViewSet):
#     parser_classes = (Log4JavaParser,)
#     queryset = Log.objects.all()
#
#     def put(self, request, file=None, format=None):
#         file = self.request.FILES['file']
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#         return file.readline()

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)
