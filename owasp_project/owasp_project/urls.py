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

from django_otp.decorators import otp_required
from django_otp.forms import OTPTokenForm
from django.shortcuts import render, redirect

from . import views
from .views import login_wrapper

class OTPAdmin(OTPAdminSite):
    pass

class StockAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    actions = ["delete_selected", "delete_model"]

    @admin.action(description="Mark selected stories as my deleted")
    @otp_required
    def delete_selected(self, request, client):
        if request.user.is_verified():
            print("delete_selected")
            pass
            #super().delete_model(request, client)

    @admin.action(description="Mark selected model as my deleted")
    def delete_model(self, request, client):
        print("here once, next:", request.POST)
        if request.POST.get('post'):
            print("deleting model")
            super().delete_model(request, client)
        else:
            request.POST.next = request.path
            print("here after, next:", request.POST.next)
            return redirect("/verifyOtp", request)
        '''
        print(request.user)
        if request.user.is_verified():
            print("delete_model")
            redirect(OTPView)
            super().delete_model(request, client) '''

    @admin.action(description="Mark selected queryset as dsfd")
    # @otp_required
    def delete_queryset(self, request, queryset):
        if request.user.is_verified():
            print("delete_queryset")
            pass
            #queryset.delete()

'''
    @admin.action(description="Mark selected stories as dsfd")
    #@otp_required
    def delete_queryset(self, request, queryset):
        #if request.user.is_verified():
            queryset.delete()

    @admin.action(description="Mark selected stories as deleted")
    #@otp_required
    def delete_model(self, request, client):
        #if request.user.is_verified():
            super().delete_model(request, client)
'''



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
    #path('admin/auth/user/{user_id}/delete', views.deleteUserView),
    path('', RedirectView.as_view(url='dotrade/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
