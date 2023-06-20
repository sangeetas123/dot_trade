from django.http import HttpResponseNotAllowed

class HeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Server'] = "dotrade"
        return response

import logging

logger = logging.getLogger('dotrade')

class AllowGetPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ['GET', 'PUT']:
            logger.info('Request with invalid method %s', request.method)
            return HttpResponseNotAllowed(['GET', 'PUT'])

        return self.get_response(request)