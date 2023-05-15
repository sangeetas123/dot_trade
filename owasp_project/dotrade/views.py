from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import get_list_or_404
from django.http import Http404

from .models import PurchasedStock

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control
from .forms import UserCreationForm
from .decorators import group_required

from django.contrib.auth.models import Group

def index(request):
    return render(request, 'dotrade/index.html')

@login_required(login_url='/dotrade/accounts/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        userPurchasedStocks = get_list_or_404(PurchasedStock, userId=request.user.id)
        context = {'stocks': userPurchasedStocks}
        return render(request, 'dotrade/dashboard.html', context)
    except Http404:
        return render(request, 'dotrade/nothing.html')

@login_required(login_url='/dotrade/accounts/login')
@group_required('Early Adopters')
def analytics(request):
    return render(request, 'dotrade/analytics.html')

def logout_view(request):
    logout(request)
    return redirect('/dotrade')

def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # add the user to the group
            group = Group.objects.get(name='Customers')
            user.groups.add(group)

            return redirect('/dotrade/dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})