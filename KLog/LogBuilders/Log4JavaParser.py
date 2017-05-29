import re
from collections import deque
from _datetime import datetime

from rest_framework.parsers import BaseParser

import settings


class Log4JavaParser(BaseParser):
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        print('dsds')
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        print('algo')
        print(stream.readline())
        return stream.read().decode(encoding)


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