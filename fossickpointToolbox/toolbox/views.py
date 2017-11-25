import json
import os
from itertools import chain
from django.core import serializers
from .forms import UploadFileForm, ContentForm
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import User,PersonalInfo,Content,Profile,Program,ProgramDetail
from django.http import JsonResponse
from django.db.models import Q

# /index
def index(request):
    if 'uuid' in request.session:
            return HttpResponseRedirect('home')
    else:
        return render(request,"toolbox/index.html")

# /login
def user_login(request):
    if (request.POST):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        try:
            user = User.objects.get(userName = userName)
        except:
            return HttpResponse("login failed")

        if (user is not None and user.userPassword == password):
            request.session['uuid'] = user.id
            return JsonResponse({"status": 0})
        else:
            return JsonResponse({"status": 1})

# /logout
def logout(request):
    del request.session['uuid']
    return JsonResponse({"status": 1})

# /register
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
                personalInfo = PersonalInfo(user=user,gender=0,name=userName)
            else:
                personalInfo = PersonalInfo(user=user,gender=1,name=userName)
            personalInfo.save()
            return JsonResponse({"status": 1})
    return render(request,"toolbox/register.html")

# /home
def user_home(request):
     # try:
    user = User.objects.get(id = request.session['uuid'])
    if (user.userType == 0):
        response = ""
        info = {'userName' : user.userName,'contentCount' : Content.objects.count(), 'userCount' : User.objects.filter(userType=1).count(), 'programCount': Program.objects.count()}

        return render(request, "toolbox/homepage.html",info)
    else:
            # to do
            # user side
        return HttpResponse("Welcome " + user.userName)
     # except:
            # return HttpResponse("You have not login")

# /content
def content(request,contentID):
    if 'uuid' in request.session:
        # todo
        # update content
        content = Content.objects.get(id=contentID)
        programdetails = ProgramDetail.objects.filter(content=content)
        programList = []
        for programdetail in programdetails:
            program = programdetail.program
            programList.append(program)

        # return content detail
        context = {"content" : content, "programList": programList}
        if (request.method) == 'POST':
            operation = request.POST.get("operation")
            # update user profile and note
            if operation == "update":
                # Function update of files has not been finished yet
                # file = request.POST.get("file")
                # thumbnail = request.POST.get("thumbnail")
                name = request.POST.get("title")
                type = request.POST.get("type")
                tag = request.POST.get("tag")
                profile = request.POST.get("profile")
                focus = request.POST.get("focus")
                keyword = request.POST.get("keyword")

                content.name = name
                content.type = type
                content.tag = tag
                content.focus = focus
                content.keyword = keyword
                content.profile.clear()
                profiles = profile.split(';')
                for aProfile in profiles:
                    if aProfile != '':
                        content.profile.add(Profile.objects.get(profileName=aProfile))
                content.save()
                return JsonResponse({"status": 1})
            # remove assigned program
        #todo
        #content preview
        return render(request, "toolbox/content.html", context)
    else:
        return HttpResponse("You have not login")
    # todo
    # userside

# /contents
def contents(request):
    if 'uuid' in request.session:

        if request.method == 'POST':
            operation = request.POST.get('operation')
            #add content
            if (operation == 'add'):
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    profile = request.POST.get('profile')
                    title = request.POST.get('title')
                    type = request.POST.get('type')
                    # if user has uploaded a thumbnail, use it. Otherwise use a default thumbnail depending on type of uploading file
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
            # return needed content
            elif (operation == 'require'):
                content = Content.objects.get(id=request.POST.get('id'))
                content_json = serializers.serialize('json', [content, ])
                content_json += "status:1"
                return JsonResponse(content_json)
            elif (operation == 'delete'):
                content = Content.objects.get(id=request.POST.get('id'))
                address = content.address
                os.remove(address.name)
                content.delete()
                return JsonResponse({"status":1})
            # search content
            else:
                focus = request.POST.get('focusSearch')
                tag = request.POST.get('tagSearch')
                keyword = request.POST.get('keywordSearch')
                profilesText = request.POST.getlist('profileSearch')
                # if focus == "All Focuses":
                #     q = Content.objects.all()
                #
                # else:
                #     q = Content.objects.filter(focus=focus)
                # if tag != "All tags":
                #     q = q.filter(tag=tag)
                # if profilesText[0] != "All profiles":
                #     q2 = Content.objects.filter(tag="null")
                #     for profileText in profilesText:
                #         aProfile = Profile.objects.get(profileName=profileText)
                #         q3 = q.filter(profile=aProfile)
                #         q2 = chain(q3,q2)
                #     q = set(q2)
                # contentList = q
                # list = [];
                # for content in contentList.values():
                #     content["thumbnail"] = content["thumbnail"].split("/")[1]
                #     list.append(content)
                list = search(focus=focus, tag=tag, profilesText=profilesText)
                context = {'contentList':list}
                return render(request, "toolbox/contents.html", context)

        contentList = Content.objects.all().values()
        for content in contentList:
            content["thumbnail"] = content["thumbnail"].split("/")[1]
        context = {'contentList':contentList}
        return render(request,"toolbox/contents.html",context)
    else:
        return HttpResponse("You have not login")

def search(focus, tag, profilesText):
    if focus == "All Focuses":
        q = Content.objects.all()
    else:
        q = Content.objects.filter(focus=focus)
    if tag != "All tags":
        q = q.filter(tag=tag)
    if profilesText[0] != "All profiles":
    #     q2 = Content.objects.filter(tag="null")
        profileList = []
        for profileText in profilesText:
            aProfile = Profile.objects.get(profileName=profileText)
            profileList.append(aProfile)
    #         q3 = q.filter(profile=aProfile)
    #         q2 = chain(q3, q2)
    #     q = set(q2)
        queries = [Q(profile=profile) for profile in profileList]
        query = queries.pop()

        for item in queries:
            query |= item
        q = q.filter(query)
    contentList = q
    list = [];
    for content in contentList:
        content = dict (content)
        content["thumbnail"] = content["thumbnail"].split("/")[1]
        list.append(content)
    return list
def handle_uploaded_file(f):
    with open(os.path.join('static', f.name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def programs(request):
    if 'uuid' in request.session:
        if request.method == 'POST':
            operation = request.POST.get('operation')
            if operation == 'create':
                programName = request.POST.get('programName')
                programDescription = request.POST.get('programDescription')
                aProgram = Program(name=programName, describe=programDescription)
                aProgram.save()
                return JsonResponse({"status" : 1})
            if operation == 'delete':
                programId = request.POST.get('programId')
                aProgram = Program.objects.filter(id=programId)
                ProgramDetail.objects.filter(program=aProgram).delete()
                aProgram.delete()
                return JsonResponse({"status" : 1})
        if request.GET.get('keywordSearch'):
            keyword = request.GET.get('keywordSearch')
            programList = Program.objects.filter(Q(name__contains = keyword) | Q(describe__contains = keyword))
            list = []
            for program in programList.values():
                list.append(program)
            context = {'programList':list}
            return render(request,"toolbox/programs.html", context)

        programList = Program.objects.all().values()
        context = {'programList':programList}
        return render(request,"toolbox/programs.html", context)
    else:
        return HttpResponse("You have not login")


def program(request, programID):
    if 'uuid' in request.session:
        aProgram = Program.objects.get(id=programID)
        if (request.method) == 'POST':
            operation = request.POST.get('operation')
            if operation == 'update':
                aProgram = Program.objects.filter(id=programID)
                contentsNumber = 0
                for key, val in request.POST.iteritems():
                    if key != 'operation':
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
                aProgramObj = Program.objects.get(id=programID)
                contentsNumber = aProgramObj.contentsNumber
                contentId = request.POST.get('contentId')
                aContent = Content.objects.filter(id=contentId)
                programDetail = ProgramDetail.objects.filter(program=aProgram, content=aContent)
                programDetail.delete()
                aProgram.update(contentsNumber=contentsNumber - 1)
                return JsonResponse({"status" : 1})
            if operation == 'add':
                aProgram = Program.objects.filter(id=programID)
                aProgramObj = Program.objects.get(id=programID)
                contentId = request.POST.get('contentId')
                aContent = Content.objects.get(id=contentId)
                order = aProgramObj.contentsNumber
                programDetail = ProgramDetail(content=aContent, program=aProgramObj, order=order)
                programDetail.save()
                aProgram.update(contentsNumber=order + 1)
                return JsonResponse({"status" : 1})

        if request.GET.get('focusSearch'):
            focus = request.GET.get('focusSearch')
            profile = request.GET.getlist('profileSearch')
            tag = request.GET.get('tagSearch')
            contentList = search(focus, tag, profile)
            programDetails = ProgramDetail.objects.filter(program=aProgram).order_by("order")
            programContents = []
            for programDetail in programDetails:
                aContent = programDetail.content
                aContentDict = dict(aContent)
                aContentDict["thumbnail"] = aContentDict["thumbnail"].split("/")[1]
                programContents.append(aContentDict)
                if aContentDict in contentList:
                    contentList.remove(aContentDict)
            contentDictList = contentList
        else:
            contentList = list(Content.objects.all())
            programDetails = ProgramDetail.objects.filter(program=aProgram).order_by("order")
            programContents = []
            for programDetail in programDetails:
                aContent = programDetail.content
                aContentDict = dict(aContent)
                aContentDict["thumbnail"] = aContentDict["thumbnail"].split("/")[1]
                programContents.append(aContentDict)
                if aContent in contentList:
                    contentList.remove(aContent)
            contentDictList = []
            for content in contentList:
                contentDict=dict(content)
                contentDict["thumbnail"] = contentDict["thumbnail"].split("/")[1]
                contentDictList.append(contentDict)
        context = {'programID': programID,'contentList':contentDictList, 'program': programContents,'programName': aProgram.name}
        return render(request, "toolbox/program.html", context)
    else:
        return HttpResponse("You have not login")

def users(request):
    # if 'uuid' in request.session:
    #
    #     studentList = User.objects.filter(userType=1)
    #     return render(request, "toolbox/users.html",{'studentList':studentList})
    return HttpResponseRedirect("/toolbox/user/1")

def user(request,userID=1):
    if 'uuid' in request.session:
        personalInfo = PersonalInfo.objects.get(id=userID)
        if (request.method) == 'POST':
            operation = request.POST.get("operation")
            # update user profile and note
            if operation == "update":
                profile = request.POST.get("profile")
                note = request.POST.get("note")
                personalInfo.note = note
                personalInfo.profile.clear()
                profiles = profile.split(';')
                for aProfile in profiles:
                    if aProfile != '':
                        personalInfo.profile.add(Profile.objects.get(profileName=aProfile))
                personalInfo.save()
                return JsonResponse({"status": 1})
            # remove assigned program
            if operation == "remove":
                programID = request.POST.get("program")
                program = Program.objects.get(id=programID)
                personalInfo.programs.remove(program)
                return JsonResponse({"status": 1})
            if operation == "assign":
                programID = request.POST.get("program")
                program = Program.objects.get(id=programID)
                personalInfo.programs.add(program)
                return JsonResponse({"status": 1})

        studentList = PersonalInfo.objects.filter(user__userType=1)
        programs = personalInfo.programs.all()
        programNameList = []
        for program in programs:
            programNameList.append(program.name)
        programList = Program.objects.exclude(name__in=programNameList)

        return render(request,"toolbox/user.html",{'studentList':studentList, 'programList':programList, 'user':personalInfo})

    else:
        return HttpResponse("You have not login")


