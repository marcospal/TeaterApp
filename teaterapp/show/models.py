from django.db import models
from django.contrib.auth.models import User


class Scale(models.Model):
    name = models.CharField(primary_key=True, max_length=256)
    def __unicode__(self):
        return "%s" % (self.name)

#Quiz
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    #some questions are part of a branch, we mark those we can start with
    can_start = models.BooleanField(default=True)
    def __unicode__(self):
        a = ''
        for ans in self.possible_answers.all():
            a += ans.text + " "
        return "%s : ( %s)" % (self.text, a)

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    
    question = models.ForeignKey(Question, related_name='possible_answers')
    
    next_question = models.ForeignKey(Question, related_name='pre_answer', blank=True, null=True)
    #if the answer affect a scale
    scale = models.ForeignKey(Scale, related_name='answers', blank=True, null=True)
    #how much
    modifier = models.IntegerField(default=0)



    def __unicode__(self):
        m = ''
        if self.scale != None:
            m = "(%s : %d)" % (self.scale.name, self.modifier)
        return "%s : %s %s" % (self.question.text, self.text, m)

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=256)
    
    #what is the max capacity of this location
    capacity = models.IntegerField(default=1)

    #Is this location only for unlocked profiles
    safe = models.BooleanField(default=True)
    
    #state of location
    CLOSED, OPEN_FOR_VISITORS, IN_SESSION, NUM_PHASES = range(4)
    PHASES = (
        (CLOSED, 'Closed'),
        (OPEN_FOR_VISITORS, 'Open for visitors'),
        (IN_SESSION, 'Closed'),
    )
    def stateStr(self):
        for a,b in self.PHASES:
            if a == self.phase:
                return b
    state = models.IntegerField(choices=PHASES, default=CLOSED)

    #What scale does this location relate to (optional)
    scale = models.ForeignKey(Scale, related_name='locations', blank=True, null=True)

    def __unicode__(self):
        return "%s - Kapacitet: %d - Skala: %s - Safe: %s" % (self.name, self.capacity, self.scale, self.safe)
 
 
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    
    #user has code as username
    user = models.ForeignKey(User, related_name='Profiles')

    date = models.DateTimeField(auto_now_add=True)
    
    #When this number is larger than zero questions must be answered 
    force_questions = models.IntegerField(default=5)
    
    #We store the players answers
    given_answers = models.ManyToManyField(Answer)
    
    #Unique code for Profile
    name = models.CharField(max_length=30)
    year_of_birth = models.IntegerField(default=0)
    MALE, FEMALE, UNKNOWN, NUM_GENDERS = range(4)
    GENDERS = (
        (MALE, 'M'),
        (FEMALE, 'F'),
        (UNKNOWN, '?'),
    )
    def genderStr(self):
        for a,b in self.GENDERS:
            if a == self.gender:
                return b
    gender = models.IntegerField(choices=GENDERS, default=UNKNOWN)
    
    ratings = models.ManyToManyField(Scale, through='Rating')    
    
    #A Profile can be locked, so he is only sent to safe locations
    locked = models.BooleanField(default=False)
    
    #When show end all Profiles are made inactive
    active = models.BooleanField(default=True)

    #possible next question
    question = models.ForeignKey(Question, related_name='answers', blank=True, null=True)
    
    #A possible location we are assigned to
    location = models.ForeignKey(Location, related_name='profiles', blank=True, null=True)
    
    #What locations has this profile visited
    locations = models.ManyToManyField(Location, related_name='visitors', blank=True, null=True)


    def __unicode__(self):
        a = ""
        if(self.active):
            a = "active"
        return "%s - %s - %s%d - code: '%s' - %s" % (self.date.strftime("%d/%m/%Y %H:%M"), self.name, self.genderStr(), self.year_of_birth, self.user.username, a)

    def addNote(self, text, lock):
        pass
        #Note.
        #self


#Rating binds Profiles to scales 
class Rating(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile)
    scale = models.ForeignKey(Scale)
    value = models.IntegerField(default=5)

    def __unicode__(self):
        return "%s %s %d - %s: %d" % (self.profile.user.username, self.profile.name, self.profile.year_of_birth , self.scale.name, self.value)



#Notes are attached to Profiles
class Note(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    text = models.CharField(primary_key=True, max_length=256)
    Profile = models.ForeignKey(Profile, related_name='notes')
    




