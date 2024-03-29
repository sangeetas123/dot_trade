"""owasp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.apps import apps

from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from django.shortcuts import redirect

from . import views
from .views import login_wrapper

from django.urls import include, path

class OTPAdmin(OTPAdminSite):
    pass

class StockAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    actions = ["delete_selected"]

    @admin.action(description="Mark selected stocks to delete")
    def delete_selected(self, request, client):
        if request.POST.get('post'):
            super().delete_model(request, client)
            request.session.pop('tmp_data')
        else:
            request.POST.next = request.path
            request.session['tmp_data'] = request.POST.get('_selected_action')
            return redirect("/verifyOtp", request)

    @admin.action(description="Mark selected models to delete")
    def delete_model(self, request, client):
        if request.POST.get('post'):
            super().delete_model(request, client)
            request.session.pop('tmp_data')
        else:
            request.POST.next = request.path
            request.session['tmp_data'] = request.POST.get('_selected_action')
            return redirect("/verifyOtp", request)


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
#admin_site.register(apps.get_model('dotrade', 'Stock'))
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.register(apps.get_model('dotrade', 'Stock'), StockAdmin)

admin_site.login = login_wrapper(admin_site.login)  # rate limit

handler403 = views.handler403

urlpatterns = [
    path('admin/', admin_site.urls),
    path('dotrade/', include('dotrade.urls')),
    path('verifyOtp/', views.otpView),
    path('', RedirectView.as_view(url='dotrade/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
