from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('logout', views.logout_view, name='customlogout'),
    path('accounts/signup', views.signupView, name='signup'),
]