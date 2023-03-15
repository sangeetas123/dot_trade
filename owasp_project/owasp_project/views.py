from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited

from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import HttpResponse, HttpResponseForbidden

def login_wrapper(login_func):

    @ratelimit(key='ip', method='POST', rate='2/5m')
    def admin_login(request, **kwargs):
        if getattr(request, 'limited', False):  # was_limited
            messages.error(request, 'Too many login attempts, please wait 5 minutes')
            return redirect('/dotrade')
        else:
            return login_func(request, **kwargs)

    return admin_login


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        messages.error(request, 'Too many incorrect login attempts, please wait 5 minutes')
        return redirect('/admin')
    return HttpResponseForbidden('Forbidden')