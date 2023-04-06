from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited

from django.shortcuts import redirect
from django.contrib import messages

from django.http import HttpResponseForbidden

from django_otp.forms import OTPTokenForm
from django_otp.decorators import otp_required

from django.shortcuts import render

def login_wrapper(login_func):

    @ratelimit(key='ip', method='POST', rate='2/5m')
    def admin_login(request, **kwargs):
        return login_func(request, **kwargs)

    return admin_login


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        messages.error(request, 'Too many incorrect login attempts, please wait 5 minutes')
        return redirect('/admin')
    return HttpResponseForbidden('Forbidden')

@otp_required
def otpView(request):
    print("in otp view ", request)
    if request.method == 'POST':
        print("anon " , request.POST)
        form = OTPTokenForm(request.user, request, request.POST)
        print("error form", form.errors.as_data())
        if form.is_valid():
            #go back to deletion
            next = request.POST.get('next', '/')
            print("valid form, redirecting ", next)
            return redirect(next)

        else:
            print("invalid form", form.errors.as_data(), " ", form.non_field_errors())
            field_errors = [ (field.label, field.errors) for field in form]
            print("errors ", field_errors)

    else:
        request.referrer = request.META.get('HTTP_REFERER', '/')
        print("request_session ", request.referrer)
        form = OTPTokenForm(request.user)
    return render(request, 'otp.html', {'form': form})

'''
def otpView(request):
    if request.method == 'POST':
        form = OTPTokenForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/dotrade/dashboard')
    else:
        form = OTPTokenForm()
    return render(request, 'registration/signup.html', {'form': form}) '''