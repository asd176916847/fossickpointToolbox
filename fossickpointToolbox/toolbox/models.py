from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=30)
    userType = models.IntegerField(default=1)  #0: admin 1:user

    def __str__(self):
        return self.userName

class PersonalInfo(models.Model):
    user = models.ForeignKey(User)
    gender = models.IntegerField(default=0)  #0:male 1:female
    age = models.IntegerField(default=20)
    hobby = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.user.userName

class Content(models.Model):
    name = models.CharField(max_length=30)

    type_choice = (('doc','doc'),('pdf','pdf'),('image', 'image'),('vedio', 'vedio'),('audio', 'audio'),('other','other'))
    type = models.CharField(max_length=30,choices=type_choice)
    tag = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    address = models.FileField(upload_to='contents/')
    preContent = models.ForeignKey('self',related_name='precontent',null=True)
    nextContent = models.ForeignKey('self',related_name='nextcontent',null=True)
    def __str__(selfs):
        return selfs.name

class Group(models.Model):
    name = models.CharField(max_length=30)
    contents = models.TextField(max_length=None)
    def __str__(selfs):
        return selfs.name

class UserContent(models.Model):
    user = models.ForeignKey(User)
    contents = models.TextField(max_length=None)
    def __str__(selfs):
        return selfs.user.name