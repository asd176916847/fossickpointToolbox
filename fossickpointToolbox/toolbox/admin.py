from django.contrib import admin
from django.contrib import admin
from .models import User
from .models import PersonalInfo, Content, UserContent
# Register your models here.
admin.site.register(User)
admin.site.register(PersonalInfo)
admin.site.register(Content)
admin.site.register(UserContent)

