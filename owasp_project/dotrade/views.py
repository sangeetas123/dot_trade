from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import get_list_or_404

from .models import PurchasedStock

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'dotrade/index.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
    userPurchasedStocks = get_list_or_404(PurchasedStock, userId=request.user.id)
    context = {'stocks': userPurchasedStocks}
    return render(request, 'dotrade/dashboard.html', context)

def loginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/dotrade/dashboard')
        # Redirect to a success page.




