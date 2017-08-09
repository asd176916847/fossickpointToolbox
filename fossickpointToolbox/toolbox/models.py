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

    def __str__(self):
        return self.user.userName