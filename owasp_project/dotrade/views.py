import os

from django.db.models.expressions import RawSQL
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.shortcuts import get_list_or_404
from django.http import Http404

from .models import PurchasedStock, Comment, Profile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.cache import cache_control

from .forms import UserCreationForm, CommentForm, EmailForm, ProfileForm

from .decorators import group_required

from django.contrib.auth.models import Group

import subprocess
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from django.core.signing import Signer

import logging

logger = logging.getLogger('dotrade')

def index(request):
    return render(request, 'dotrade/index.html')

@login_required(login_url='/dotrade/accounts/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        userPurchasedStocks = get_list_or_404(PurchasedStock, userId=request.user.id)
        context = {'stocks': userPurchasedStocks}
        response = render(request, 'dotrade/dashboard.html', context)
        logger.info('Loading the dashboard')
        return store_cookie(request, response)
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
    try:
        comment = get_object_or_404(Comment, pk=comment_id)
    except Exception:
        return HttpResponse("No comment found with that id")
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
        sanitized_email = ''.join(c for c in email if c.isalnum() or c == '@' or c == '.')

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the script
        script_path = os.path.join(current_dir, 'generate_report.sh')
        #command = "bash " + script_path  + " " + email
        #output = subprocess.check_output(command, shell=True)
        command = ["bash", script_path, sanitized_email]
        result = subprocess.run(command, capture_output=True)
        return HttpResponse(result.stdout)
    else:
        return HttpResponse("Errors in sending email")

def store_cookie(request, response):
    f = Fernet(b'T3hzrNTA9mMrkL1-vu6IUEz3skymjBU1yxE_z-2oJZo=')
    signer = Signer(key='SECRET_KEY')
    signed_cookie_value = request.get_signed_cookie('my_cookie',
                                                    salt='my_salt', default=None)
    if signed_cookie_value is not None:
        # Create a Signer instance

        encrypted_cookie_value = signer.unsign(signed_cookie_value)
        logger.debug("[sensitive] Cookie value %s", f.decrypt(encrypted_cookie_value.encode()))
    else:
        logger.debug("[sensitive] No cookie by that name, it might have expired")
        encrypted_data = f.encrypt(bytes(request.user.email, 'utf-8'))
        signed_data = signer.sign(encrypted_data.decode())
        expiry_time = datetime.now() + timedelta(seconds=30)
        response.set_signed_cookie('my_cookie', signed_data,
                                   salt='my_salt', expires=expiry_time)

    return response

@login_required(login_url='/dotrade/accounts/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request):
    try:
        print("userid ", request.user.id)
        user_profile = get_object_or_404(Profile, userId=request.user.id)
        context = {'profile': user_profile}
        response = render(request, 'dotrade/profile.html', context)
        return response
    except Http404:
        return render(request, 'dotrade/profile.html')


def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            cleaned_first_name = form.cleaned_data['first_name']
            cleaned_last_name = form.cleaned_data['last_name']
            cleaned_date_of_birth = form.cleaned_data['date_of_birth']
            cleaned_credit_card = form.cleaned_data['credit_card']
            cleaned_save_payment_information = form.cleaned_data['save_payment_information']

            if not cleaned_save_payment_information:
                cleaned_credit_card = None

            #print("PROFILES ", cleaned_first_name, " ", cleaned_last_name, " ",
            #                cleaned_credit_card, " ", cleaned_date_of_birth, " ",
            #      cleaned_save_payment_information)
            logger.info("PROFILES Name %s %s, Credit card %s, DOB %s, Save infor %s",
                        cleaned_first_name, cleaned_last_name, cleaned_credit_card,
                        cleaned_date_of_birth, cleaned_save_payment_information)

            Profile.objects.update_or_create(userId=request.user,
                                             defaults={'first_name': cleaned_first_name,
                                                       'last_name' : cleaned_last_name,
                                                       'date_of_birth': cleaned_date_of_birth,
                                                       'credit_card':cleaned_credit_card,
                                                       'save_payment_information':cleaned_save_payment_information
            },)
            return redirect('profile')
        else:
            print("Errors: ", form.errors)
    else:
        form = ProfileForm()

    return render(request, 'dotrade/getprofile.html', {'form': form})
