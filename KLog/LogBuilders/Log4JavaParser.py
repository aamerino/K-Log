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
        print(stream)
        return stream.read().decode(encoding)