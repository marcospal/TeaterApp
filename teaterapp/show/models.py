# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
import datetime
from django.conf import settings
from django.db.models import Q

class Scale(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, help_text='General name of the scale.')
    def __unicode__(self):
        return "%s" % (self.name)

class Color(models.Model):
    title = models.CharField(u'Title', max_length=250)
    color = models.CharField(max_length=6,default='ffffff')
    def __unicode__(self):
        return "%s" % (self.title)

#Quiz
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(help_text='The question to ask. fx "Have you been to Africa?')
    
    #use the priority to sort order of questions
    priority = models.IntegerField(default=1,help_text='The lower priority, the earlier the question will be asked. 0 first, 1000 last.')
    
    #if a leading answer exist this question cant start
    leading_answer = models.OneToOneField('Answer', related_name='next_question', help_text='Select ---- to make independent question', unique=True, blank=True, null=True)
    
    
    def __unicode__(self):
        
        a = ''
        for ans in self.possible_answers.all():
            a += ans.text + " "
        return "%d (%d) %s ( %s)" % (self.getPriority() ,self.id, self.text, a)


    def getPriority(self):
        if self.leading_answer: #recursive get score of parent question
            return self.leading_answer.question.getPriority()
        else:
            return self.priority

    def getscore(self, profile):
        score = self.priority
        #lower score if question has been answered
        try:
            qc = QuestionCount.objects.get(profile=profile, question=self)
            score += qc.times * 10000   

        except:
            pass    
        

        return score




class Location(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=256, help_text='Name of location.')
    isEnding = models.BooleanField(default=False, help_text='Bliver kun tilbudt ved afslutningen')
    isStartRoom = models.BooleanField(default=False, help_text='Bliver kun tilbudt første gang')
    directions = models.TextField(max_length=256, help_text='How to get there',blank=True)

    #what is the max capacity of this location
    capacity = models.IntegerField(default=1, help_text='Maximum number of people that it can hold')
    capacity_min = models.IntegerField(default=1, help_text='Minimum number of people that it can hold (not directly used)')

    #use the priority to sort order of questions
    priority = models.IntegerField(default=1)
    

    #Is this location only for unlocked profiles
    safe = models.BooleanField(default=True, help_text='Skal vaere checked medmindre det er et kosteskab/venterum for folk der er laast.')
    
    show_opened = models.DateTimeField(default=datetime.datetime.now)


    first_arrived_time = models.DateTimeField(default=datetime.datetime.now)
    def isOverTimeLimit(self):
        if self.isEnding:
            return False
        if self.state == Location.FIRST_ARRIVED:
            return (datetime.datetime.now()-self.first_arrived_time).seconds>4*60 #4 minutes time limit
        else:
            return False
    #state of location
    CLOSED, OPEN_FOR_VISITORS, FIRST_ARRIVED,IN_SESSION, EVALUATING, NUM_PHASES = range(6)
    PHASES = (
        (CLOSED, u'Lukket'),
        (OPEN_FOR_VISITORS, u'Åben'),
        (FIRST_ARRIVED, u'Første ankommet'),
        (IN_SESSION, u'Igang'),
        (EVALUATING, u'Evaluerer'),
    )
    def stateStr(self):
        for a,b in self.PHASES:
            if a == self.state:
                return b
    state = models.IntegerField(choices=PHASES, default=CLOSED, help_text='State of location')

    #What scale does this location relate to (optional)
    scale = models.ForeignKey(Scale, related_name='locations', blank=True, null=True, help_text='Scale that this location relates to.')


    parameters = models.ManyToManyField(Scale, through='Parameter')    
    
    version = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - Kapacitet: %d - Skala: %s - Safe: %s" % (self.name, self.capacity, self.scale, self.safe)

    def aciveProfiles(self):
        return Profile.objects.filter(location=self, active=True)

    def getscore(self, profile):
        score = 0
        if self in profile.available_locations.all():
            score += 0
        else:
            score -= 1000
        #print 
        #go through each parameter of room
        n = 0
        for p in self.parameter_set.all():
            r = 5
            try:
                r = profile.rating_set.get(scale=p.scale).value
                #print "profile has rating on this scale", r
            except:
                pass
                #print "profile has no rating on this scale"

            #print "room has ", p.value, " profile has ", r, " difference = ", p.value - r
            
            score += r
            n += 1
        if n > 0:
            score /= n

        if profile.location != None:
            if profile.location.isEnding:
                score -= 1000 #if it already got a room, then don't count it as part of the top of the list any more.
        #print self.name, "___ profile vs room score is: ", score, "___ for ", profile

        #Add rooms own priority (handicap if you like)
        #print "we are adding a priority bonus of", self.priority
        score += self.priority
        actives = Profile.objects.filter(location=self, active=True).count()
        #if over minimum down prioritize room
        #TODO: probably syntax list len error
        if actives>=self.capacity_min:
            score += settings.LOCATION_OVER_MINUMUM_SCORE
        elif actives>0:
            score += settings.LOCATION_OVER_ONE_SCORE

        #If there are very few free participants, try not to offer rooms they cannot fill
        freeProfiles = len(list(Profile.objects.filter(active=True, location__isnull=True)))
        if freeProfiles<settings.MIN_FREE_PROFILES_TO_OFFER_NEW_ROOMS:
            if actives == 0 and self.capacity_min > 1: #if we can't fill it, then don't offer it
                score += settings.MIN_FREE_PROFILES_TO_OFFER_NEW_ROOMS_SCORE
        #lower score if location has been visited before
        #try:
        #    qc = VisitCount.objects.get(profile=profile, location=self)
            #print "and subtracting ", qc.times, " * 10000"
        #    score -= qc.times * 10000   
        #except:
        #    pass    
        #

        return score

    @staticmethod
    def getAvailableLocations(profile):
        if profile.endLocation != None:
            tmp = []
            tmp.append(profile.endLocation)

            return tmp
        #find all possible locations (OPEN_FOR_VISITORS, and available seats)
        #Q(income__gte=5000) | Q(income__isnull=True)
        locations = profile.available_locations.annotate(visitor_count=Count('profiles')).filter(Q(state=Location.OPEN_FOR_VISITORS) | Q(state=Location.FIRST_ARRIVED))
        #old:locations = Location.objects.annotate(visitor_count=Count('profiles')).filter(state=Location.OPEN_FOR_VISITORS)
        otherProfiles = list(Profile.objects.filter(active=True))
       

        #order them in relation to this profile
        def score(a):

            #score = a.getscore(profile)
            def otherSort(p):
                p.tmp_score = a.getscore(p)
                return p.tmp_score
            #get rank between all other profiles
            otherProfiles.sort(key=otherSort)
            otherProfiles.reverse()
            order = 0
            #print "______room>  "+str(a)
            result = 0
            lastScore = 10000
            for other in otherProfiles:
                #print "____sort___: "+str(order) +" > " + str(other)
                if other.id == profile.id:
                    break
                if other.endLocation != None:
                    continue

                if other.tmp_score<lastScore:
                    lastScore = other.tmp_score
                    order = order+1
            #print "RESULT____sort___: "+str(order) +" > " + str(other)
            if a.isEnding and order == 0 and len(list(a.endProfiles.all())) == 0:
                profile.endLocation = a
                profile.save()
                return 0

            elif a.isEnding:
                return 600+order # if it's ending but not first, then don't offer

            return order
        

       
        #print "_________Locations: "
        tmp = []
        for l in list(locations):
            #print "Location score: "+ str(l.getscore(profile))
            if l.capacity <= len(list(l.endProfiles.all())):
                continue
            if l.capacity > l.visitor_count and l.isOverTimeLimit() == False:
                if profile.state == Profile.INTRO:
                    if l.isStartRoom:
                        tmp.append(l)
                elif profile.state == Profile.ENDING:
                    if l.isEnding:
                        tmp.append(l)
                elif profile.state == Profile.RUNNING:
                    if l.safe and not l.isStartRoom and not l.isEnding:
                        tmp.append(l)
                    if  profile.locked and not l.safe:
                        tmp.append(l)

        tmp.sort(key=score)
        #tmp.reverse()

        #print them
        #for l in tmp:
            #print l
            #print 'Score', l.getscore(profile)
            #print 'Visitors: ',l.visitors.all()
            #print 'Visitors count: ',l.visitor_count
        maxOffered = settings.MAX_ROOM_OFFERED
        

        return tmp[0:maxOffered]

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    
    question = models.ForeignKey(Question, related_name='possible_answers')
    
    #if the answer affect a scale
    scale = models.ForeignKey(Scale, related_name='answers', blank=True, null=True)
    #how much
    modifier = models.IntegerField(default=0)
    ignoreLocations = models.ManyToManyField(Location,blank=True, null=True)  


    def __unicode__(self):
        m = ''
        if self.scale != None:
            m = "(%s : %d)" % (self.scale.name, self.modifier)
        return "%s : %s %s" % (self.question.text, self.text, m)

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    
    endLocation = models.ForeignKey(Location, related_name='endProfiles', blank=True, null=True)
    #A Profile can be locked, so he is only sent to safe locations
    locked = models.BooleanField(default=False)
    
    #When show end all Profiles are made inactive
    active = models.BooleanField(default=True)

    #user has code as username
    user = models.ForeignKey(User, related_name='Profiles')

    date = models.DateTimeField(auto_now_add=True)
    
    #When this number is larger than zero questions must be answered 
    force_questions = models.IntegerField(default=5)

    #We store the questions the player answers and the answers
    answered_questions = models.ManyToManyField(Question, related_name='profiles_that_have_answered', through='QuestionCount')
    given_answers = models.ManyToManyField(Answer, related_name='profiles_that_have_answered', blank=True)
    
    #Set if player has a question pending
    question = models.ForeignKey(Question, related_name='pending_profiles', blank=True, null=True)
    
    #available locations. all should be added when profile is created
    available_locations = models.ManyToManyField(Location, related_name='posible_profiles',blank=True, null=True)

    #Unique code for Profile
    name = models.CharField(max_length=30)
    #year_of_birth = models.IntegerField(default=0)
    age = models.IntegerField()
    MALE, FEMALE, UNKNOWN, NUM_GENDERS = range(4)
    GENDERS = (
        (MALE, 'M'),
        (FEMALE, 'K'),
        (UNKNOWN, '?'),
    )
    def genderStr(self):
        for a,b in self.GENDERS:
            if a == self.gender:
                return b

    gender = models.IntegerField(choices=GENDERS, default=UNKNOWN)
    
    ratings = models.ManyToManyField(Scale, through='Rating')    
    
    version = models.IntegerField(default=1)
    
    INTRO, RUNNING, ENDING, NUM_STATES = range(4)
    STATES = (
        (INTRO, 'INTRO'),
        (RUNNING, 'RUNNING'),
        (ENDING, 'ENDING'),
    )
    state = models.IntegerField(choices=STATES, default=INTRO)
    #todo: Set til intro i baseinfo

    #location related
    #A possible location we are assigned to
    location = models.ForeignKey(Location, related_name='profiles', blank=True, null=True)
    location_set_time = models.DateTimeField(default=datetime.datetime.now)


    #What locations has this profile visited
    #locations = models.ManyToManyField(Location, related_name='visitors', through='VisitCount', blank=True, null=True)

    def __unicode__(self):
        a = ""
        if(self.active):
            a = "active"
        return "%s - %s %s - code: '%s' - %s" % (self.name, self.genderStr(), self.age, self.user.username, a)


#Binds Profiles to questions answered. Need counter to rate next question 
class QuestionCount(models.Model):
    profile = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    times = models.IntegerField(default=0)



#Rating binds Profiles to scales 
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile)
    scale = models.ForeignKey(Scale)
    value = models.IntegerField(default=5)

    class Meta:
        unique_together = ('profile', 'scale')

    def __unicode__(self):
        return "%s %s - %s: %d" % (self.profile.user.username, self.profile.name, self.scale.name, self.value)

#Rating binds Locations to scales 
class Parameter(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location)
    scale = models.ForeignKey(Scale)
    value = models.IntegerField(default=5)

    class Meta:
        unique_together = ('location', 'scale')

    def __unicode__(self):
        return "%s" % (self.location.name)

#Notes are attached to Profiles
class Note(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=256)
    isRead = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    profile = models.ForeignKey(Profile, related_name='notes', blank=True, null=True)
    location = models.ForeignKey(Location, related_name='notes', blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.profile.name, self.text)

