import logging

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        if 'sensitive' in record.msg:
            return False  # Do not log sensitive messages
        return True