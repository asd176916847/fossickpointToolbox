from django.db import models
# Create your models here.

# user model
class User(models.Model):
    userName = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=30)
    # todo
    # change userType to 4 levels. 0: admin 1: user who can visit trail content;  2: user who can visit all content; 3: user who can have tailor program
    userType = models.IntegerField(default=1)  #0: admin 1:user

    def __str__(self):
        return self.userName

 # profile model
class Profile(models.Model):
    profileName = models.TextField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.profileName

    class Meta:
        ordering = ('profileName',)

    # program model
class Program(models.Model):
    name = models.CharField(max_length=100)
    describe = models.CharField(max_length=200)
    contentsNumber = models.IntegerField(default=0)

    def __str__(self):
        return self.name
# user personal info model
class PersonalInfo(models.Model):
    user = models.ForeignKey(User)
    gender = models.IntegerField(default=0)  #0:male 1:female
    age = models.IntegerField(default=20)
    hobby = models.CharField(max_length=100)
    email = models.EmailField()
    name = models.CharField(max_length=100,default='')
    note = models.CharField(max_length=300,null=True, blank=True)
    # todo
    # add more detail information such as country, city, job
    nation = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    occupation = models.CharField(max_length=100,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    programs = models.ManyToManyField(Program)
    profile = models.ManyToManyField(Profile)
    def __str__(self):
        return self.user.userName



# content model
class Content(models.Model):
    name = models.CharField(max_length=100)
    type_choice = (('doc','doc'),('pdf','pdf'),('image', 'image'),('video', 'video'),('audio', 'audio'),('other','other'))
    type = models.CharField(max_length=30,choices=type_choice)
    focus_choice = (('Emotional Intelligence','Emotional Intelligence'),('Social Intelligence','Social Intelligence'),('Self Actualization','Self Actualization'))
    focus = models.CharField(max_length=30,choices=focus_choice,default='Emotional Intelligence')
    tag_choice = (('Images','Images'),('Formulas','Formulas'),('Activities','Activities'),('Skills','Skills'),('Social frameworks','Social frameworks'),('Concepts','Concepts'),('Myths & notions','Myths & notions'),('Principles','Principles'))
    tag = models.CharField(max_length=30,choices=tag_choice)
    thumbnail = models.ImageField(upload_to='contents/', null=True)
    profile = models.ManyToManyField(Profile)
    profileText = models.TextField(max_length=100,default='')
    keyword = models.CharField(max_length=100)
    address = models.FileField(upload_to='contents/')
    def __str__(selfs):
        return selfs.name
    # convert the model to dict
    def __iter__(self):
        yield 'name', self.name
        yield 'focus', self.focus
        yield 'tag', self.tag
        yield 'thumbnail', self.thumbnail.url
        yield 'id', self.id
        yield 'profileText', self.profileText
        yield 'keyword', self.keyword


# doesn't need now
class Group(models.Model):
    name = models.CharField(max_length=30)
    contents = models.TextField(max_length=None)
    def __str__(selfs):
        return selfs.name

# doesn't need now
class UserContent(models.Model):
    user = models.ForeignKey(User)
    contents = models.TextField(max_length=None)
    def __str__(selfs):
        return selfs.user.name


# program detail model
class ProgramDetail(models.Model):
    content = models.ForeignKey(Content)
    program = models.ForeignKey(Program)
    order = models.IntegerField()
