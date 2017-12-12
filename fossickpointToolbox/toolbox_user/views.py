from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from toolbox.models import Content
# Create your views here.
def index(request):
    tempContentList = Content.objects.all()
    contentList = []
    for content in tempContentList:
        content = dict(content)
        content["thumbnail"] = content["thumbnail"].split("/")[1]
        contentList.append(content)
    context = {'contentList':contentList}
    return render(request, 'toolbox_user/index.html', context)