import json
import os
from itertools import chain
from django.core import serializers
from .forms import UploadFileForm, ContentForm
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import User,PersonalInfo,Content,Profile,Program,ProgramDetail
from django.http import JsonResponse
from django.db.models import Q


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
    try:
        user = User.objects.get(id = request.session['uuid'])
        if (user.userType == 0):
            response = ""
            info = {'userName' : user.userName,'contentCount' : Content.objects.count(), 'userCount' : User.objects.filter(userType=1).count()}
            "contentCount":Content.objects.count()}
            for student in studentList:
               response += student.userName + "<br>"
            return HttpResponse("Welcome admin. Your student List:<br>" + response )
            return render(request, "toolbox/homepage.html",info)
        else:
            return HttpResponse("Welcome " + user.userName)
    except:
       return HttpResponse("error")
    return JsonResponse({"id":request.session['uuid']})
    if (request.session['uuid']):
        return HttpResponse("login successful")
    else:
        return HttpResponse("You have not login")
def content(request,contentID):
    content = Content.objects.get(id=contentID)
    context = {"content" : content}
    return render(request, "toolbox/content.html", context)
def contents(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        #add content
        if (operation == 'add'):
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = request.POST.get('profile')
                title = request.POST.get('title')
                type = request.POST.get('type')
                if 'thumbnail' in request.FILES:
                    content = Content(name=title,type=request.POST.get('type'),tag=request.POST.get('tag'), keyword=request.POST.get('keyword'),address=request.FILES['file'],focus=request.POST.get('focus'),profileText=profile,thumbnail=request.FILES['thumbnail'])
                else:
                    thumbnail = 'contents/' + type + '.png'
                    content = Content(name=title,type=request.POST.get('type'),tag=request.POST.get('tag'), keyword=request.POST.get('keyword'),address=request.FILES['file'],focus=request.POST.get('focus'),profileText=profile,thumbnail=thumbnail)

                profiles = profile.split(';')
                content.save()
                for aProfile in profiles:
                    content.profile.add(Profile.objects.get(profileName=aProfile))
                return JsonResponse({"status":1})
            else:
                return JsonResponse({"status":0})
        elif (operation == 'require'):
            content = Content.objects.get(id=request.POST.get('id'))
            content_json = serializers.serialize('json', [content, ])
            content_json += "status:1"
            return JsonResponse(content_json)
        else:
            if (operation == 'delete'):
                content = Content.objects.get(id=request.POST.get('id'))
                address = content.address
                os.remove(address.name)
                content.delete()
                return JsonResponse({"status":1})
            else:
                focus = request.POST.get('focusSearch')
                tag = request.POST.get('tagSearch')
                keyword = request.POST.get('keywordSearch')
                profilesText = request.POST.getlist('profileSearch')
                if focus == "All Focuses":
                    q = Content.objects.all()

                else:
                    q = Content.objects.filter(focus=focus)
                if tag != "All tags":
                    q = q.filter(tag=tag)
                if profilesText[0] != "All profiles":
                    q2 = Content.objects.filter(tag="null")
                    for profileText in profilesText:
                        aProfile = Profile.objects.get(profileName=profileText)
                        q3 = q.filter(profile=aProfile)
                        q2 = chain(q3,q2)
                    q = set(q2)
                contentList = q
                list = [];
                for content in contentList.values():
                    content["thumbnail"] = content["thumbnail"].split("/")[1]
                    list.append(content)
                context = {'contentList':list}
                return render(request, "toolbox/contents.html", context)

    contentList = Content.objects.all().values()
    for content in contentList:
        content["thumbnail"] = content["thumbnail"].split("/")[1]
    context = {'contentList':contentList}
    return render(request,"toolbox/contents.html",context)


def handle_uploaded_file(f):
    with open(os.path.join('static', f.name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def programs(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        if operation == 'create':
            programName = request.POST.get('programName')
            programDescription = request.POST.get('programDescription')
            aProgram = Program(name=programName, describe=programDescription)
            aProgram.save()
            return JsonResponse({"status" : 1})

    programList = Program.objects.all().values()
    context = {'programList':programList}
    return render(request,"toolbox/programs.html", context)

def program(request, programID):
    if (request.method) == 'POST':
        operation = request.POST.get('operation')
        if operation == 'update':
            aProgram = Program.objects.filter(id=programID)
            contentsNumber = 0
            for key, val in request.POST.iteritems():
                contentsNumber = contentsNumber + 1
                aContent = Content.objects.get(id=val)
                programDetail = ProgramDetail.objects.filter(program=aProgram, content=aContent)
                if (programDetail):
                    programDetail.update(order=key)
                else:
                    programDetail = ProgramDetail(content=aContent, program=aProgram, order=key)
                    programDetail.save()
            aProgram.update(contentsNumber=contentsNumber)
            return JsonResponse({"status" : 1})

        if operation == 'delete':
            aProgram = Program.objects.filter(id=programID)
            contentId = request.POST.get('contentId')
            aContent = Content.objects.filter(id=contentId)
            order = ProgramDetail.objects.filter(program = aProgram, content=aContent).order
            ProgramDetail.objects.filter()
        if operation == 'add':
            aProgram = Program.objects.filter(id=programID)
            contentId = request.POST.get('contentId')
            aContent = Content.objects.filter(id=contentId)
            order = aProgram.contentsNumber + 1
            programDetail = ProgramDetail(content=aContent, program=aProgram, order=order)
            programDetail.save()
            aProgram.update(order=order)
    aProgram = Program.objects.get(id=programID)
    contentList = Content.objects.all().values()
    programDetails = ProgramDetail.objects.filter(program=aProgram).order_by("order")
    programContents = []
    for programDetail in programDetails:
        aContent = programDetail.content
        programContents.append(aContent)
    context = {'programID': programID,'contentList':contentList, 'program': programContents,'programName': aProgram.name}

    return render(request, "toolbox/program.html", context)

def user(request):
    studentList = User.objects.filter(userType=1)

    return render(request,"toolbox/user.html",{'studentList':studentList})




