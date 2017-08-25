import json
import os
from .forms import UploadFileForm
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import User,PersonalInfo,Content
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
            return JsonResponse({"status": 1})

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
    #try:
        user = User.objects.get(id = request.session['uuid'])
        if (user.userType == 0):
            response = ""
            studentList = User.objects.filter(userType = 1)
            info = {'userName' : user.userName,'contentCount' : Content.objects.count(), 'userCount' : User.objects.count()}
            #"contentCount":Content.objects.count()}
            #for student in studentList:
            #    response += student.userName + "<br>"
            #return HttpResponse("Welcome admin. Your student List:<br>" + response )
            return render(request, "toolbox/homepage.html",info)
        else:
            return HttpResponse("Welcome " + user.userName)
    #except:
    #    return HttpResponse("error")
    #return JsonResponse({"id":request.session['uuid']})
    # if (request.session['uuid']):
    #     return HttpResponse("login successful")
    # else:
    #     return HttpResponse("You have not login")

def content(request):
    contentList = Content.objects.all().values()
    context = {'contentList':contentList,}
    operation = request.POST.get('operation')
    if request.method == 'POST':
        if (operation == 'add'):
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = Content(name=request.POST.get('title'),type=request.POST.get('type'),tag=request.POST.get('tag'),keyword=request.POST.get('keyword'),address=request.FILES['file'])
                file.save()
                return JsonResponse({"status":1})
            else:
                return JsonResponse({"status":0})
        if (operation == 'delete'):
            content = Content.objects.get(id=request.POST.get('id'))
            address = content.address
            os.remove(address.name)
            content.delete()
            return JsonResponse({"status":1})

    return render(request,"toolbox/content.html",context)

def handle_uploaded_file(f):
    with open(os.path.join('static', f.name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)