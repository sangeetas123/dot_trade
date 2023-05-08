import os

from django.db.models.expressions import RawSQL
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.shortcuts import get_list_or_404
from django.http import Http404

from .models import PurchasedStock, Comment

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.cache import cache_control
from .forms import UserCreationForm, CommentForm, EmailForm
from .decorators import group_required

from django.contrib.auth.models import Group

import subprocess

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

def commentView(request):
    comments = Comment.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            comment = Comment(user=request.user, comment=comment_text)
            comment.save()
            return redirect('/dotrade/comment_history')
    else:
        form = CommentForm()

    return render(request, 'dotrade/feedback.html', {
        'comments': comments,
        'form': form,
    })

def comment_history(request):
    try:
        comments = get_list_or_404(Comment, user=request.user)
        context = {'comments': comments}
        return render(request, 'dotrade/comment_history.html', context)
    except Http404:
        return render(request, 'dotrade/nothing.html')

def comment_detail(request, comment_id):
    #query = f"SELECT * FROM dotrade_comment WHERE id = '{comment_id}'"
    #query = f"SELECT * FROM dotrade_comment WHERE id = %s"
    #comments = Comment.objects.raw(query, [comment_id])
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            return generate_report(request)
    else:
        form = EmailForm()

    return render(request, 'dotrade/comment_detail.html', {'comment': comment, 'form':form})

def generate_report(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        #sanitized_email = ''.join(c for c in email if c.isalnum() or c == '@' or c == '.')

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the script
        script_path = os.path.join(current_dir, 'generate_report.sh')
        command = "bash " + script_path  + " " + email
        output = subprocess.check_output(command, shell=True)
        #command = ["bash", script_path, sanitized_email]
        #result = subprocess.run(command, capture_output=True)
        return HttpResponse(output)
    else:
        return HttpResponse("Errors in sending email")