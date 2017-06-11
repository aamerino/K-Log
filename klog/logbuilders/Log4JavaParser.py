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
        start = datetime.now()
        self.regexException = re.compile(self.RE_EXCEPTION)
        self.regexExceptionName = re.compile(self.RE_EXCEPTION_NAME)
        print("Time generating regex: %s" % (datetime.now() - start))

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
