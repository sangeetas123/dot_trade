import hashlib
import logging
import re

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        if 'sensitive' in record.msg:
            return False  # Do not log sensitive messages
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