from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_list_or_404

from .models import PurchasedStock



def index(request):
    return HttpResponse("Welcome to DoMyTrade!")

def getAllStocksForUser(request, user):
    userPurchasedStocks = get_list_or_404(PurchasedStock, userId=user)
    context = {'stocks': userPurchasedStocks}
    return render(request, 'dotrade/dashboard.html', context)



