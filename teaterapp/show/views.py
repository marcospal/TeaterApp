from django.conf import settings
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required
import re

from models import Profile, Question, Rating


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
            return HttpResponseRedirect('/quiz/');
        
        #Get list of open locations with room for me

        #Sort list of locations

        #Offer the best 3

        #No relevant location -> more questions
        return HttpResponseRedirect('/quiz/');

        print profile

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

    try:
        _code = request.POST['code'];
        _name = request.POST['name'];
        _sex = request.POST['sex'];
        _year = int(float(request.POST['year'])) ;

        for a,b in Profile.GENDERS:
            if b == _sex:
                _sex = a
        
        profile = Profile(user=request.user, name=_name, year_of_birth=_year, gender=_sex)
        profile.save()
        return HttpResponseRedirect('/')
    except:
        pass


    c = {


        'STATIC_URL': settings.STATIC_URL,
        'title': "baseinfo",
        'code': request.user.username
    }
    return render_to_response('baseinfo.html', c, context_instance=RequestContext(request))


def quiz(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    _profile = None
    try:
        _profile = Profile.objects.get(user=request.user, active=True)
        print "profile found"
    except:
        return HttpResponseRedirect('/')
    
    print request.POST

    #recieve answers
    try:
        question = int(float(request.POST["question"]))
        answer = request.POST["answer"]

        question = Question.objects.get(id=question)
        for a in question.possible_answers.all():
            if a.text == answer:
                _profile.question = a.next_question
                _profile.given_answers.add(a)
                
                print "a"
                if a.scale != None:
                    print "b"
                    r = None
                    try:
                        print "c"
                        r = Rating.objects.get(profile=_profile, scale=a.scale)
                        print "done.."

                    except:
                        print "def"
                    
                        r = Rating(profile=_profile, scale=a.scale)
                        print "aaa"
                    r.value += a.modifier
                    r.save()
                    print "done"

                _profile.force_questions -= 1
                _profile.save();
                print "Answered %s" % (a.text)
                break
        #Attempt to answer question
        pass
    except:
        pass



    q = None

    if _profile.question:
        q = _profile.question
    else:
        qlist = Question.objects.filter(can_start=True)
        
        #order list so questions answered before has lowest rank


        if len(qlist) == 0:
            print "no more questions"
        q = qlist[0]

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "quiz",
        'question': q,

    }
    return render_to_response('quiz.html', c, context_instance=RequestContext(request))


def choose(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    profile = None
    try:
        profile = Profile.objects.get(username__iexact=request.user.username, active=true)
        print "profile found"
    except:
        return HttpResponseRedirect('/')
    #if request.POST["choice"]:
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "choose",
    }
    return render_to_response('choose.html', c, context_instance=RequestContext(request))

def directions(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    profile = None
    try:
        profile = Profile.objects.get(username__iexact=request.user.username, active=true)
        print "profile found"
    except:
        return HttpResponseRedirect('/')

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Directions",
        'instructions': "Go to ",
           
    }
    return render_to_response('directions.html', c, context_instance=RequestContext(request))

#admin views below

@staff_member_required
def overview(request):
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "overview",
    }
    return render_to_response('overview.html', c, context_instance=RequestContext(request))

@staff_member_required
def location(request, id):
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "location",
    }
    return render_to_response('location.html', c, context_instance=RequestContext(request))

@staff_member_required
def profile(request, id):
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect('/')
    #if not request.user.is_superuser:
    #    return HttpResponseRedirect('/')

    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "profile",
    }
    return render_to_response('profile.html', c, context_instance=RequestContext(request))
    

