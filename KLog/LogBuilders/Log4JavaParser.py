import re
from collections import deque
from _datetime import datetime

from rest_framework.parsers import BaseParser


class Log4JavaParser(BaseParser):

    parser_context = 'Log4Java'

    def parse(self, stream, media_type=None, parser_context=''):
        return stream.read

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
#
#
# if __name__ == "__main__":
#     fileParser = FileParser()
#     fileParser.parse('log4j-application.log')
