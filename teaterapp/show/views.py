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



from models import Profile, Question, Rating, QuestionCount, Location, VisitCount, Scale


#This is the main entrypoint of the application
def login(request):
    
    #if a code is submitted, use it to login
    if request.POST.__contains__('code'):
        #Force uppercase
        code = request.POST["code"].upper()
        #force alphanumeric
        code = re.sub('\W', '', code)
        if len(code) == 6:
            print "code ok"
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
            
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/overview/');
 
        #find profile for user
        profile = None
        try:
            profile = Profile.objects.get(user=request.user, active=True)
        except:
            return HttpResponseRedirect('/baseinfo/');
        
        #User has profile decide what to do

        #user is assigned a location
        if profile.location:
            return HttpResponseRedirect('/directions/');
        
        #question is waiting
        if profile.question or profile.force_questions > 0:
            return HttpResponseRedirect('/quiz/')
        
        #what locations are possible?
        locations = Location.getAvailableLocations(profile)
        if len(locations) == 0:
            return HttpResponseRedirect('/quiz/');
        else:
            #if len(locations) == 1:
            #    #there is no choice, just send the guy
            #    profile.location = locations[0]
            #else:
            #    #you have a choice
            return HttpResponseRedirect('/choose/');
        
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Login",
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

        print request.POST

    _code = request.POST.get('code');
    _name = request.POST.get('name');
    _sex = request.POST.get('sex');
    _day = request.POST.get('day') ;
    _month = request.POST.get('month') ;
    _year = request.POST.get('year') ;

    if _code != None and _name != None and _sex != None and _day != None and _month != None and _year != None:
        print _code, _name, _sex, _day, _month, _year

        for a,b in Profile.GENDERS:
            if b == _sex:
                _sex = a
        
        print _sex

        _year = int(float(_year))
        _month = int(float(_month))
        _day = int(float(_day))

        print _year, _month, _day

        d = datetime.date(_year,_month, _day)
        print d
        profile = Profile(user=request.user, name=_name, birth=d, gender=_sex)
        profile.save()

        print "creating default ratings"
        for s in Scale.objects.all():
            print s
            r = Rating(profile=profile, scale=s)
            r.save()

        return HttpResponseRedirect('/')


    c = {


        'STATIC_URL': settings.STATIC_URL,
        'title': "baseinfo",
        'code': request.user.username
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
            
            print "1>", question
            print "2>", answer
            print "3>", profile


            if question == profile.question:
                a = question.possible_answers.filter(text=answer)
                if a.exists():
                    a = a.get()
                    print "found answer"
                    print "--->",a
                    
                    try:
                        profile.question = a.next_question
                    except Question.DoesNotExist:
                        profile.question = None
                    print "next question found: %s" % (profile.question)
                    

                    profile.given_answers.add(a)

                    qc = None
                    try:
                        qc = QuestionCount.objects.get(profile=profile, question=question)
                    except:
                        qc = QuestionCount(profile=profile, question=question)
                    qc.times += 1
                    qc.save()

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
    
    if profile.force_questions <= 0 and len(Location.getAvailableLocations(profile)) > 0:
        profile.question = None
        profile.save()
        return HttpResponseRedirect('/');

    #Find what question to ask
    if not profile.question:
        #find all possible questions
        questions = Question.objects.filter(leading_answer__isnull=True)
        
        #order them in relation to this profile
        def score(a):
            return a.getscore(profile)
        questions = list(questions)
        questions.sort(key=score)
        questions.reverse()

        #print them
        for s in questions:
            print s, s.getscore(profile), s.profiles_that_have_answered.all()

        profile.question = questions[0]
        profile.save()
        print "giving new question"
    else:
        print "user already has question"


    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "quiz",
        'question': profile.question,

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
                profile.location_set_time = datetime.datetime.now()
                profile.save()
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
        
        qc = None
        try:
            qc = VisitCount.objects.get(profile=profile, location=profile.location)
        except:
            qc = VisitCount(profile=profile, location=profile.location)
        qc.times += 1
        qc.save()

        profile.location = None

        profile.save()
        return HttpResponseRedirect('/')

    age = (datetime.datetime.now() - profile.location_set_time).seconds
    

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Directions",
        'location': profile.location,
        'age': age,
        'score': profile.location.getscore(profile)
           
    }
    return render_to_response('directions.html', c, context_instance=RequestContext(request))

#admin views below

@staff_member_required
def overview(request):
    
    locations = Location.objects.all()

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "overview",
        'locations': locations,
        'free_profiles' : Profile.objects.filter(active=True, location__isnull=True)
    }
    return render_to_response('overview.html', c, context_instance=RequestContext(request))

@staff_member_required
def location(request, id):
    profile = None
    try:
        location = Location.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')

    #Allow location owner to adjust profile    
    l = request.POST.get('location');
    p = request.POST.get('profile');
    a = request.POST.get('action');
    if(l != None and p != None and a != None):
        p = Profile.objects.get(id=int(p))
        l = Location.objects.get(id=int(l))
        r = None
        try:
            r = Rating.objects.get(profile=p, scale=l.scale)
        except Rating.DoesNotExist:
            r = Rating(profile=p, location=l.scale)

        if a == '+':
            r.value = min(9, r.value + 1)
            r.save()
            print "add"
        if a == '-':
            r.value = max(1, r.value - 1)
            r.save()
            print "sub"

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "location",
        'location': location
    }
    return render_to_response('location.html', c, context_instance=RequestContext(request))

@staff_member_required
def profile(request, id):
    profile = None
    try:
        profile = Profile.objects.get(active=True, id=id)
    except:
        return HttpResponseRedirect('/')

    print request.POST
    #Allow location owner to adjust profile    
    s = request.POST.get('scale');
    p = request.POST.get('profile');
    a = request.POST.get('action');
    if(s != None and p != None and a != None):
        p = Profile.objects.get(id=int(float(p)))
        s = Scale.objects.get(id=int(float(s)))
        r = None
        try:
            r = Rating.objects.get(profile=p, scale=s)
        except Rating.DoesNotExist:
            r = Rating(profile=p, location=s)

        if a == '+':
            r.value = min(9, r.value + 1)
            r.save()
            print "add"
        if a == '-':
            r.value = max(1, r.value - 1)
            r.save()
            print "sub"


    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title' : "profile",
        'profile' : profile,
        'next' : Location.getAvailableLocations(profile)   
    }
    return render_to_response('profile.html', c, context_instance=RequestContext(request))
    

