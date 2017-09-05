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
class Profile(models.Model):
    profileName = models.TextField(max_length=100)
    def __str__(self):              # __unicode__ on Python 2
        return self.profileName

    class Meta:
        ordering = ('profileName',)
class Content(models.Model):
    name = models.CharField(max_length=100)
    type_choice = (('doc','doc'),('pdf','pdf'),('image', 'image'),('video', 'video'),('audio', 'audio'),('other','other'))
    type = models.CharField(max_length=30,choices=type_choice)
    focus_choice = (('Being','Emotional Intelligence'),('Belonging','Social Intelligence'),('Becoming','Self Actualization'))
    focus = models.CharField(max_length=30,choices=focus_choice,default='Emotional Intelligence')
    tag_choice = (('Images','Images'),('Formulas','Formulas'),('Activities','Activities'),('Skills','Skills'),('Social frameworks','Social frameworks'),('Concepts','Concepts'),('Myths & notions','Myths & notions'),('Principles','Principles'))
    tag = models.CharField(max_length=30,choices=tag_choice)
    profile = models.ManyToManyField(Profile)
    profileText = models.TextField(max_length=100,default='')
    keyword = models.CharField(max_length=100)
    address = models.FileField(upload_to='contents/')

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

class profileRelation(models.Model):
    contentName = models.CharField(max_length=100)
    profileName = models.CharField(max_length=30)

