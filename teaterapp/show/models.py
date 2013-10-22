from django.db import models

class Scale(models.Model):
    name = models.CharField(primary_key=True, max_length=256)
    def __unicode__(self):
        return "%s" % (self.name)
 
class Participant(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    #Unique code for participant
    code = models.CharField(primary_key=True, max_length=4)
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
    #A participant can be locked, so he is only sent to safe locations
    locked = models.BooleanField(default=False)
    #When show end all participants are made inactive
    active = models.BooleanField(default=True)
    
    def __unicode__(self):

        a = ""
        if(self.active):
            a = "active"
        return "%s - %s - %s%d - code: '%s' - %s" % (self.date.strftime("%d/%m/%Y %H:%M"), self.name, self.genderStr(), self.age, self.code, a)

    def addNote(self, text, lock):
        pass
        #Note.
        #self


#Rating binds participants to scales 
class Rating(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    participant = models.ForeignKey(Participant)
    scale = models.ForeignKey(Scale)
    value = models.IntegerField(default=5)

#Notes are attached to participants
class Note(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    text = models.CharField(primary_key=True, max_length=256)
    participant = models.ForeignKey(Participant, related_name='notes')
    
class Location(models.Model):
    name = models.CharField(primary_key=True, max_length=256)
    capacity = models.IntegerField(default=1)

    safe = models.BooleanField(default=True)
    
    participants = models.ManyToManyField(Participant)

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
 


#Quizz
class Question(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(primary_key=True, max_length=256)


class Answer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(primary_key=True, max_length=256)
    question = models.ForeignKey(Question, related_name='answers')
    next_question = models.ForeignKey(Scale, related_name='pre_answer', blank=True, null=True)
    participants = models.ManyToManyField(Participant)
