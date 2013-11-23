# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
import re
import pdb
import datetime
from django.utils.timezone import utc
from django.utils import simplejson

from models import Profile, Question, Rating, QuestionCount, Location, Scale, Color, Note


def validate(code):
    if len(code) != 4:
        return -1
    try:
        a = int(float(code[:2]))
        b = int(float(code[2:]))
        if (a+66)%100 == b:
            return a
        else:
            return -1
    except:
        return -1
#This is the main entrypoint of the application
def login(request):
    error = ""
    #if a code is submitted, use it to login
    if request.POST.__contains__('code'):
        #Force uppercase
        code = request.POST["code"].upper()
        #force alphanumeric
        code = re.sub('\W', '', code)
        
        if validate(code)>=0:
            #code is ok
            user = None
            try:
                user = auth.models.User.objects.get(username__iexact=code)
                print "user found: " + user.username
            except auth.models.User.DoesNotExist:
                user = auth.models.User.objects.create_user(code, "we@nouseema.il", code)
                user.is_active=True    
                user.save()
            user = auth.authenticate(username=code, password=code)
            auth.login(request, user)
        else:
            error = "Koden er ikke korrekt! Prøv igen."
            
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/overview/')
 
        #find profile for user
        profile = None
        try:
            profile = Profile.objects.get(user=request.user, active=True)
        except:
            return HttpResponseRedirect('/baseinfo/')
        
        #User has profile decide what to do

        #As long as actor is evaluating the profile we force him to take quizzes
        if profile.location and profile.location.state == Location.EVALUATING:
            return HttpResponseRedirect('/quiz/')
        #user is assigned a location
        if profile.location:
            return HttpResponseRedirect('/directions/')
        
        #question is waiting
        if profile.question or profile.force_questions > 0:
            return HttpResponseRedirect('/quiz/')
        
        #what locations are possible?
        locations = Location.getAvailableLocations(profile)
        if len(locations) == 0:
            return HttpResponseRedirect('/quiz/')
        else:
            #if len(locations) == 1:
            #    #there is no choice, just send the guy
            #    profile.location = locations[0]
            #else:
            #    #you have a choice
            return HttpResponseRedirect('/choose/')
        
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Login",
        'error': error,
        'test': request.user,
           
    }
    return render_to_response('login.html', c, context_instance=RequestContext(request))



def baseinfo(request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    if request.user.is_staff:
        return HttpResponseRedirect('/overview/');  

    profile = None 
    #lookup profile
    try:
        profile = Profile.objects.get(user=request.user, active=true)
        #profile exist
        return HttpResponseRedirect('/')
    except:
        pass

    

    _code = request.POST.get('code')
    _sex = request.POST.get('sex')
    _age = request.POST.get('age') 
    _name = "Anders Andersen"
    print _code, _sex, _age
    if _code != None and _sex != None and _age != None:
        print _code, _sex, _age

        for a,b in Profile.GENDERS:
            if b == _sex:
                _sex = a
        
        #print _sex

        _locations = Location.objects.all()
        #print d
        profile = Profile(user=request.user, name=_name, age=_age, gender=_sex, force_questions=settings.USER_FORCED_QUESTIONS)
        
        profile.save()
        profile.available_locations = _locations
        profile.save()
        #print "creating default ratings"
        for s in Scale.objects.all():
            #print s
            r = Rating(profile=profile, scale=s)
            r.save()
        profile.save()
        return HttpResponseRedirect('/')


    c = {

        #'user':request.user,
        'STATIC_URL': settings.STATIC_URL,
        'title': "baseinfo",
        'code': request.user.username,
        'name': _name,
        'USER_TIMEOUT_SECONDS' : settings.USER_TIMEOUT_SECONDS
    }
    return render_to_response('baseinfo.html', c, context_instance=RequestContext(request))


def quiz(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    profile = Profile.objects.filter(user=request.user, active=True)
    if profile.exists():
        profile = profile.get()
        print "profile found"
    else:
        return HttpResponseRedirect('/')
    
    question = request.POST.get("question")
    answer = request.POST.get("answer")
    
    
    if question != None and answer != None:
        question = Question.objects.filter(id=int(float(question)))
        if question.exists():
            question = question.get()
            
            #print "1>", question
            #print "2>", answer
            #print "3>", profile


            if question == profile.question:
                a = question.possible_answers.filter(text=answer)
                if a.exists():
                    a = a.get()
                    #print "found answer"
                    #print "--->",a
                    
                    try:
                        profile.question = a.next_question
                    except Question.DoesNotExist:
                        profile.question = None
                    
                    #print "next question found: %s" % (profile.question)
                    
                    profile.given_answers.add(a)

                    qc = None
                    try:
                        qc = QuestionCount.objects.get(profile=profile, question=question)
                    except:
                        qc = QuestionCount(profile=profile, question=question)
                    qc.times += 1
                    qc.save()

                    if a.ignoreLocations != None:
                        for loc in a.ignoreLocations.all():
                            profile.available_locations.remove(loc)
                    if a.scale != None:
                        r = None
                        try:
                            r = Rating.objects.get(profile=profile, scale=a.scale)
                        except:
                            r = Rating(profile=profile, scale=a.scale)
                        r.value += a.modifier
                        
                        r.save()

                    profile.force_questions -= 1
                    if profile.force_questions < 0:
                        profile.force_questions = 0
                    profile.save()

                else:
                    print "answer not found in current question"
            else:
                print "answering non pending question"
    
    
    #Find what question to ask
    if not profile.question:
        if (profile.force_questions <= 0 and len(Location.getAvailableLocations(profile)) > 0) or profile.location != None:
            profile.question = None
            profile.save()
            return HttpResponseRedirect('/')


        #find all possible questions
        questions = Question.objects.filter(leading_answer__isnull=True)
        
        #order them in relation to this profile
        def score(a):
            return a.getscore(profile)
        questions = list(questions)
        questions.sort(key=score) #lowest score first
        

        #print them
        for s in questions:
            print s, s.getscore(profile), s.profiles_that_have_answered.all()

        profile.question = questions[0]
        profile.save()
        print "giving new question"
    else:
        print "user already has question"


    c = {
        'profile': profile,
        'STATIC_URL': settings.STATIC_URL,
        'title': "quiz",
        'question': profile.question,
        'USER_TIMEOUT_SECONDS' : settings.USER_TIMEOUT_SECONDS

    }
    return render_to_response('quiz.html', c, context_instance=RequestContext(request))


def choose(request):
    print "choose"

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    profile = Profile.objects.filter(user=request.user, active=True)
    if profile.exists():
        profile = profile.get()
        print "profile found"
    else:
        return HttpResponseRedirect('/')

    location = request.POST.get("location")

    if location != None:
        location = Location.objects.filter(name=location)
        if location.exists():
            location = location.get()
            
            #check its open and that it has the capacity
            if location in Location.getAvailableLocations(profile):
                profile.location = location
                profile.version += 1
                profile.location_set_time = datetime.datetime.now()
                profile.save()
                location.version += 1
                location.save()
                return HttpResponseRedirect('/')
        else:
            print "unknown location"

    locations = Location.getAvailableLocations(profile)

    if not len(locations) > 0:
        return HttpResponseRedirect('/')
    #if request.POST["choice"]:
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'choice': locations,
        'USER_TIMEOUT_SECONDS' : settings.USER_TIMEOUT_SECONDS,
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,

    }
    return render_to_response('choose.html', c, context_instance=RequestContext(request))

def directions(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    profile = Profile.objects.filter(user=request.user, active=True)
    if profile.exists():
        profile = profile.get()
        print "profile found"
    else:
        return HttpResponseRedirect('/')

    if profile.location == None:
        return HttpResponseRedirect('/')

    print request.POST

    done = request.POST.get("done")

    if done != None:
        
        #qc = None
        #try:
        #    qc = VisitCount.objects.get(profile=profile, location=profile.location)
        #except:
        #    qc = VisitCount(profile=profile, location=profile.location)
        #qc.times += 1
        profile.available_locations.remove(profile.location)

        qc.save()

        profile.version += 1
        profile.force_questions = 5
        profile.save()
        profile.location.version+=1
        profile.location.save()

        profile.location = None

        profile.save()
        return HttpResponseRedirect('/')

    age = (datetime.datetime.now() - profile.location_set_time).seconds
    

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Directions",
        'location': profile.location,
        'profile' : profile,
        'age': age,
        'score': profile.location.getscore(profile),
        'USER_TIMEOUT_SECONDS' : settings.USER_TIMEOUT_SECONDS,
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,
        'USER_SELF_CONTINUE' : settings.USER_SELF_CONTINUE,
           
    }
    return render_to_response('directions.html', c, context_instance=RequestContext(request))



def gotogate(request):
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'profiles' : Profile.objects.filter(active=True),
        'USER_TIMEOUT_SECONDS' : settings.USER_TIMEOUT_SECONDS,
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,
        'USER_SELF_CONTINUE' : settings.USER_SELF_CONTINUE,
           
    }
    return render_to_response('gotogate.html', c, context_instance=RequestContext(request))


#admin views below

def getOverviewVersion():
    v = 0
    for l in Location.objects.all():
        v += l.version
    for p in Profile.objects.filter(active=True):
        v += p.version
    return v


@staff_member_required
def overview(request):
    
    locations = Location.objects.all()

    print request.POST

    profile = request.POST.get("profile")
    location = request.POST.get("location")

    
    if profile != None and location != None:
        try:
            profile = Profile.objects.get(id=profile)
            location = Location.objects.get(id=location)
            profile.location = location
            profile.version += 1
            profile.save()
            location.version += 1
            location.save()

        except:
            pass

    profiles = Profile.objects.filter(active=True, location__isnull=True)
    

    allProfiles = Profile.objects.filter(active=True)

    state = "Intro"
    if(len(allProfiles)>0):
        state = allProfiles[0].state
    if state == Profile.INTRO:
        state = "Intro"
    if state == Profile.ENDING:
        state = "Slutfase"
    if state == Profile.RUNNING:
        state = "I gang"



    closedLocations = Location.objects.filter(state=Location.CLOSED)
    for freeP in profiles:
        freeP.sendToOptions = Location.getAvailableLocations(freeP)
    c = {
        'profile' : profile,
        'STATIC_URL': settings.STATIC_URL,
        'title': "overview",
        'locations': locations,
        'free_profiles' : profiles,
        'version': getOverviewVersion(),
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,
        'openLocations' : len(list(locations))-len(list(closedLocations)),
        'totalLocations' : len(list(locations)) ,
        'freeParticipants': len(profiles),
        'allParticipants': len(allProfiles),
        'state': state,
    }
    return render_to_response('overview.html', c, context_instance=RequestContext(request))


@staff_member_required
def overviewversion(request):
    return HttpResponse(simplejson.dumps(
        {
            'version': getOverviewVersion()
        }), mimetype='application/json')
    


@staff_member_required
def location(request, id):
    profile = None
    try:
        location = Location.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')


    print request.POST

    #Allow location owner to adjust profile    
    p = request.POST.get('profile')
    a = request.POST.get('action')
    n = request.POST.get('note')
   
    if n != None:
        n = Note(text=n, location=location)
        n.save()
        location.version += 1
        location.save()

    if(a != None):
        
        if a == 'evaluate':
            location.state = Location.CLOSED
            location.version += 1
            location.save()


            for p in location.profiles.all():
                p.location = None
                p.force_questions = 2 #NULLO: Hvor mange spørgsmål efter at blive sendt ud
                p.version += 1
                p.available_locations.remove(location)
                p.save()

            for rat in request.POST:
                ratingId = rat[6:]
                if ratingId.isdigit():
                    ratingId = int(ratingId)
                    val = int(request.POST.get(rat))

                    try:
                        r = Rating.objects.get(id=ratingId)
                    except Rating.DoesNotExist:
                        continue 
                    r.value = r.value + val
                    r.save()
                    location.version += 1
                    location.save()

       
        if a == 'close':
            for p in location.profiles.all():
                p.location = None
                p.force_questions = 2 #NULLO: Hvor mange spørgsmål efter at blive sendt ud
                p.version += 1

                #record where people have been
                #try:
                #    v = VisitCount.objects.get(profile=p, location=location)
                #    v.times += 1
                #    v.save()
                #except:
                #    v = VisitCount(profile=p, location=location)
                #    v.save()
                p.available_locations.remove(location)

                p.save()
            location.state = Location.CLOSED
            location.version += 1
            location.save()
        if a == 'open':
            location.state = Location.OPEN_FOR_VISITORS
            location.version += 1
            location.save()
        if a == 'start':
            location.first_arrived_time = datetime.datetime.now()
            location.state = Location.IN_SESSION
            location.version += 1
            location.save()
        if a == 'firstParticipant':
            if len(list(location.profiles.all())) >0:
                location.first_arrived_time = datetime.datetime.now()
                location.state = Location.FIRST_ARRIVED
                location.version += 1
                location.save()
        if a == 'evaluate':
            location.state = Location.EVALUATING
            location.version += 1
            location.save()



    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "location",
        'location': location,
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,
    }
    return render_to_response('location.html', c, context_instance=RequestContext(request))

@staff_member_required
def locationversion(request, id):
    location = None
    try:
        location = Location.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')

    return render_to_response('locationJson.html', {'location':location}, context_instance=RequestContext(request))
    #return HttpResponse(simplejson.dumps(
    #    {
    #        'version': location.version
    #    }), mimetype='application/json')
    

@staff_member_required
def profile(request, id):
    profile = None
    try:
        profile = Profile.objects.get(active=True, id=id)
    except:
        return HttpResponseRedirect('/')

    print request.POST
    




    #Allow location owner to adjust profile    
    s = request.POST.get('scale')
    p = request.POST.get('profile')
    a = request.POST.get('action')
    n = request.POST.get('note')

    ignoreLocation = request.POST.get('ignoreLocation')

    if ignoreLocation != None:
            l = Location.objects.get(id=int(ignoreLocation)) 
            if l != None:
                profile.available_locations.remove(l)
                profile.save()

    if a != None:
        if a == "toggle_lock":
            profile.locked = not profile.locked
            profile.version += 1
            profile.save()

    
    if p != None and p.isdigit():
       
        p = Profile.objects.get(id=int(p)) 
        
        if n != None:
            n = Note(text=n, profile=p)
            n.save()
            profile.locked = True
            profile.version +=1
            profile.save()
        
            
        
        if(s != None  and a != None):
            s = Scale.objects.get(id=int(float(s)))
            r = None
            try:
                r = Rating.objects.get(profile=p, scale=s)
            except Rating.DoesNotExist:
                r = Rating(profile=p, location=s)

            if a == '+':
                r.value = r.value +1
                r.save()
                print "add"
                profile.version+=1
                profile.save()
            if a == '-':
                r.value = r.value - 1
                r.save()
                print "sub"
                profile.version+=1
                profile.save()

    #prev = profile.locations.all()

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title' : "profile",
        'profile' : profile,
        'locations': profile.available_locations.all(),
        'next' : Location.getAvailableLocations(profile),
        'AJAX_REFRESH_INTERVAL' : settings.AJAX_REFRESH_INTERVAL,  
    }
    return render_to_response('profile.html', c, context_instance=RequestContext(request))
    

@staff_member_required
def profileversion(request, id):
    profile = None
    try:
        profile = Profile.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')
    return HttpResponse(simplejson.dumps(
        {
            'version': profile.version
        }), mimetype='application/json')


@staff_member_required
def reset(request):
    reset = request.POST.get('reset')

    print request.POST
    a = request.POST.get('action')
    if a == 'reset':
        for p in Profile.objects.all():
            p.active = False
            p.location = None
            p.version += 1
            p.save()
        for l in Location.objects.all():
            l.state = Location.CLOSED
            l.save()
        return HttpResponseRedirect('/')
    return render_to_response('reset.html', {}, context_instance=RequestContext(request))

@staff_member_required
def state(request):
    state = request.POST.get('state')
    message = ""
    a = request.POST.get('action')
    if a == 'introOver':
        message = "Intro er started"
        profs = list(Profile.objects.filter(active=True,location__isnull=False).all())
        
        def score(p):
            return len(p.available_locations.all())
        profs.sort(key=score) #lowest score first

        for p in profs:
            p.state = Profile.RUNNING
            #Todo: Randomize, then fill one location at a time, 
            #Will fail if no locataions. sort by rating with lowest first. english should give -100
            locs = Location.getAvailableLocations(p)
            if len(locs)>0:
                p.location = Location.getAvailableLocations(p)[0]
            p.version += 1
            p.save()
        
        for l in Location.objects.all():
            if l.isEnding:
                l.state = Location.CLOSED
                l.save()
            if l.isStartRoom:
                l.state = Location.CLOSED
                l.save()

        return HttpResponseRedirect('/overview')

    if a == 'startEnding':
        message = "Ending is started"
        for p in Profile.objects.all():
            p.state = Profile.ENDING
            p.save()
        
        for l in Location.objects.all():
            if l.isEnding:
                l.state = Location.OPEN_FOR_VISITORS
                l.save()


        return HttpResponseRedirect('/overview')

    if a == 'undoEnding':
        message = "Back to normal"
        for p in Profile.objects.all():
            p.state = Profile.RUNNING
            p.save()
        
        for l in Location.objects.all():
            if l.isEnding:
                l.state = Location.CLOSED
                l.save()
        return HttpResponseRedirect('/overview')

    return render_to_response('state.html', {}, context_instance=RequestContext(request))



def color(request):
    color = "ffffff"
    
    try:
        colorObj = Color.objects.all()[:1].get()
        color = colorObj.color
    except:
        color = "ffffff"
        pass
    return render_to_response('color.html', {'color':color}, context_instance=RequestContext(request))

def setcolor(request,color):
    
    try:
        colorObj = Color.objects.all()[:1].get()
        colorObj.color = color
        colorObj.save()
    except:
        pass
    return render_to_response('color.html', {'color':color}, context_instance=RequestContext(request))

