from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user>/dashboard', views.getAllStocksForUser, name='dashboard'),
]