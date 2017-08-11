import json
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import User,PersonalInfo
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
    if (request.POST):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        try:
            user = User.objects.get(userName = userName)
            return JsonResponse({"status":-1})
        except:
            user = User(userName=userName, userPassword=password, userType=1)

            user.save()
            if (gender == "male"):
                personalInfo = PersonalInfo(user=user,gender=0)
            else:
                personalInfo = PersonalInfo(user=user,gender=1)
            personalInfo.save()
            return JsonResponse({"status": 1})
    return render(request,"toolbox/register.html")


def user_home(request):
    try:
        user = User.objects.get(id = request.session['uuid'])
        if (user.userType == 0):
            response = ""
            studentList = User.objects.filter(userType = 1)
            for student in studentList:
                response += student.userName + "<br>"
            return HttpResponse("Welcome admin. Your student List:<br>" + response )
        else:
            return HttpResponse("Welcome " + user.userName)
    except:
        return HttpResponse("error")
    #return JsonResponse({"id":request.session['uuid']})
    # if (request.session['uuid']):
    #     return HttpResponse("login successful")
    # else:
    #     return HttpResponse("You have not login")