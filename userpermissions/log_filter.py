import logging


class AwesomeFilter(logging.Filter):
    def filter(self, rec):
        if 'DEBUG' == rec.levelname or rec.name.startswith('django'):
            return 0
        # you may need to filter based on `getMessage()` if
        # you can't find the information in the pre-formatted msg field
        return 1
