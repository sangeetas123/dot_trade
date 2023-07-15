import json
from http.client import HTTPResponse

from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_list_or_404
from django.views.decorators.csrf import csrf_exempt

from .decorators import api_key_required
from .models import APIKey, PurchasedStock


@api_key_required
def get_stocks(request):
    userPurchasedStocks = get_list_or_404(PurchasedStock, userId=request.user.id)
    serialized_objects = serializers.serialize('json', userPurchasedStocks)

    # Create a JsonResponse object with the serialized data
    return JsonResponse(serialized_objects, safe=False)

import secrets

def generate_api_key():
    key = secrets.token_hex(16)  # Generate a random hexadecimal string of length 16
    return key

@csrf_exempt
def get_api_key(request):
    #username = request.POST.get('username')
    #password = request.POST.get('password')
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    print("Username ", data.get("username"), " Pass ", data.get("password") )
    user = authenticate(username=data.get("username"), password=data.get("password"))
    if not user:
        return HttpResponseNotFound()

    api_key = None
    try:
        api_key = APIKey.objects.get(user=user)
    except APIKey.DoesNotExist:
        if not api_key:
            api_key = generate_api_key()
            api_key_instance = APIKey(user=user, key=api_key)
            api_key_instance.save()
    return HttpResponse(api_key)


