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
    if request.method == 'POST':
        form = OTPTokenForm(request.user, request, request.POST)
        stockId = request.session.get('tmp_data')
        if form.is_valid():
            #go back to deletion
            url = "/admin/dotrade/stock/%s/delete/" % stockId
            return redirect(url)
    else:
        form = OTPTokenForm(request.user)
    return render(request, 'otp.html', {'form': form})
