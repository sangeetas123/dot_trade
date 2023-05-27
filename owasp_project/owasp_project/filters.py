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
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex_patterns = {
            r'\d{4}-\d{2}-\d{2}': '****-**-**',  # Date of birth in yyyy-mm-dd format
            r'\b(\d{3}-\d{2}-\d{4})\b': '***-**-****',  # Social Security Number (SSN) format
            r'\b(\d{4}\s?\d{4}\s?\d{4}\s?\d{4})\b': '**** **** **** ****',  # Credit card number format
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b': '***@***.com', # Email id
        }

    def format(self, record):
        formatter = logging.Formatter()
        log_message = formatter.format(record)
        if record.msg:
            for pattern, replacement in self.regex_patterns.items():
                log_message = re.sub(pattern, replacement, log_message)
        return log_message
    '''
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
    '''