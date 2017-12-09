from django.contrib import admin
from django.contrib import admin
from django.utils.html import format_html

from .models import User
from .models import PersonalInfo, Content, UserContent,Profile,Program,ProgramDetail,Category
# Register your models here.
admin.site.register(User)
admin.site.register(PersonalInfo)
admin.site.register(Content)
admin.site.register(UserContent)
admin.site.register(Profile)
admin.site.register(Program)
admin.site.register(ProgramDetail)
admin.site.register(Category)


class Model1Admin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.thumbnail))

    image_tag.short_description = 'Image'

    list_display = ['image_tag',]



