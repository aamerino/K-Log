import re
from datetime import datetime, time

from rest_framework.parsers import BaseParser

from klog import settings


class Log4JavaParser(BaseParser):
    RE_EXCEPTION = b"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).+?([[])([\w]+)"
    RE_EXCEPTION_NAME = b"([^.]*)(\\n+\')"

    media_type = 'multipart/form-data'

    regexException = ""
    regexExceptionName = ""

    def __init__(self):
        self.regexException = re.compile(self.RE_EXCEPTION)
        self.regexExceptionName = re.compile(self.RE_EXCEPTION_NAME)

    def parse(self, stream, media_type=None, parser_context=None):
        logs4JavaDTO = []
        start = datetime.now()
        for line in stream:
            if (re.match(self.regexException, line)):
                startParse = datetime.now()
                exception = re.match(self.regexException, line)
                fecha = exception.group(1)
                classe = exception.group(3)
                line = stream.readline()
                logs4JavaDTO.append(Log4JavaDTO(fecha, classe, line.decode(settings.DEFAULT_CHARSET).rsplit('.', 1)[1]))
                print("Time generating: %s" % (datetime.now() - startParse))
        print("%s parsing: %s" % (len(logs4JavaDTO), (datetime.now() - start)))
        return logs4JavaDTO

class Log4JavaDTO():
    def __init__(self, time, className, exceptionName):
        self.dateTime = datetime.strptime(time.decode(settings.DEFAULT_CHARSET), '%Y-%m-%d %H:%M:%S,%f')
        self.className = className.decode(settings.DEFAULT_CHARSET)
        self.exceptionName = exceptionName


# class FileParser:
#     RE_EXCEPTION = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).+?([[])([\w]+)"
#     RE_PACKAGE = r"([^.]+)(.)([\w]+[(])"
#
#     regexException = ""
#     currentException = deque([])
#
#     def __init__(self):
#         self.regexException = re.compile(self.RE_EXCEPTION)
#         self.packageException = re.compile(self.RE_PACKAGE)
#
#     def parse(self, file):
#         with open(file) as f:
#             line = f.readline()
#             if (re.match(self.regexException, line)):
#                 exception = re.match(self.regexException, line)
#                 fecha = exception.group(1)
#                 classe = exception.group(3)
#                 line = f.readline()
#                 exceptionName = line.rsplit('.', 1)[1]
#
#
#                 # l = re.search(self.regexException, line)
#                 # print(l)
#                 # test = datetime.strptime(l.group(1), '%Y-%m-%d %H:%M:%S,%f')
#                 # print(l.group(0))
#                 # print(l.group(4))
#                 # print(l.group(2))
#                 # print(l.group(1))
#                 # print(f.readline())
#                 # test = f.readline()
#                 # print(test)
#                 # classNameRegex = re.search(self.packageException, test)
#                 # print(classNameRegex.group(1))