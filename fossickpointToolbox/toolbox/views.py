import json
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import User
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,"toolbox/index.html")

def user_login(request):
    if (request.POST):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        try:
            user = User.objects.get(userName = userName)
        except:
            return HttpResponse("login failed")
        #User.
        if (user is not None and user.userPassword == password):
            request.session['uuid'] = user.id
            return JsonResponse({"status": 0})
        else:
            return JsonResponse({"status": -1})

def user_register(request):
    return render(request,"toolbox/register.html")


def user_home(request):
    return JsonResponse({"id":request.session['uuid']})
    # if (request.session['uuid']):
    #     return HttpResponse("login successful")
    # else:
    #     return HttpResponse("You have not login")