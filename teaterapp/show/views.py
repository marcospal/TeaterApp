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
import datetime
import pdb


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
        print request.POST

        _code = request.POST['code'];
        _name = request.POST['name'];
        _sex = request.POST['sex'];
        _day = int(float(request.POST['day'])) ;
        _month = int(float(request.POST['month'])) ;
        _year = int(float(request.POST['year'])) ;

        print datetime.date(_year,_month,_day) 


        for a,b in Profile.GENDERS:
            if b == _sex:
                _sex = a
        
        profile = Profile(user=request.user, name=_name, birth=datetime.date(_year,_month,_day) , gender=_sex)
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
    
    #print request.POST

    #pdb.set_trace()
        

    #recieve answers
    print "post"

    question = request.POST.get("question")
    answer = request.POST.get("answer")
    
    if question != None and answer != None:
        question = Question.objects.get(id=int(float(question)))

        print "1>", question
        print "2>", answer
        print "3>", _profile


        if question == _profile.question:


            a = question.possible_answers.filter(text=answer)[:1]
            if a != None:
                
                print "found answer"
                print a.next_question
                    
                _profile.question = a.next_question
                _profile.given_answers.add(a)
                _profile.answered_questions.add(question)
                
                if a.scale != None:
                    r = None
                    try:
                        r = Rating.objects.get(profile=_profile, scale=a.scale)
                    except:
                        r = Rating(profile=_profile, scale=a.scale)
                    r.value += a.modifier
                    r.save()
                    print "done"

                _profile.force_questions -= 1
                _profile.save();
            else:
                print "answer not found in current question"
                
        else:
            print "answering non pending question"


    #Find what question to ask
    q = None

    #is a question assigned 
    if True: #not _profile.question:
        #possibly send back to root 
        prfl = [_profile]
        qlist = Question.objects.filter(leading_answer__isnull=True)
        

        def score(a):
            return a.getscore(_profile)

        print "aaa", qlist

        qlist = list(qlist)
        qlist.sort(key=score)

        print ">>>bbb", qlist
        for s in qlist:
            print s.getscore(_profile), s.profiles_that_have_answered.all()


        _profile.question = qlist[0]
        _profile.save()
        print "giving new question"
    else:
        print "user already has question"


    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "quiz",
        'question': _profile.question,

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
    

