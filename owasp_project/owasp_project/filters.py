import hashlib
import logging
import re

logger = logging.getLogger('dotrade')

class SensitiveDataFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        self.regex = re.compile(email_regex)

    def filter(self, record):
        formatter = logging.Formatter()
        log_message = formatter.format(record)
        if self.regex.search(log_message):
            logger.info("Filtering out sensitive log")
            return False
        return True

class RedactingFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        # Redact sensitive information in the message
        return re.sub(email_regex, self.hashString, message)

    def hashString(self, match):
        email = match.group()
        hashed_email = self.calculate_hash(email)
        return "[REDACTED]" + hashed_email[-4:]

    @staticmethod
    def calculate_hash(string, algorithm='sha256'):
        hash_object = hashlib.new(algorithm)
        hash_object.update(string.encode('utf-8'))
        return hash_object.hexdigest()