from django.conf import settings
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
#from django.template.loader import get_template
#from django.template import Context
#from datetime import datetime
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponseRedirect, HttpResponse, Http404
#from django.core import serializers
#from django.contrib.admin.views.decorators import staff_member_required
#from django.utils.html import strip_tags
#import re
#import random
#from django.contrib.auth.models import User
#from models import GA, Membership, Topic, Comment, Vote, QuickLogin, QuickLoginAccess
#from models import SimpleLog, logFunc
#from paypal.standard.ipn.models import PayPalIPN
#import pdb
#from django.contrib.auth.backends import ModelBackend
#from login.models import Message
#import time
#from django.contrib import auth
#from django.core.mail import send_mail



#Enter keycode 
def login(request):
    c = {
        'STATIC_URL': settings.STATIC_URL,
        'title': "Login",
        #color of background
        #'sitename': settings.SITENAME,
    }
    
    if request.POST.__contains__('code'):
        code = request.POST["code"]
        if len(code) == 4:
            #Lookup code in active participants

            #if remaining data is ready create participant and pass on 
            #kode
            #navn
            #year of birth
            #sex


            #if not found pass to baseinfo
            c["code"] = code 
            return render_to_response('baseinfo.html', c, context_instance=RequestContext(request))
    return render_to_response('login.html', c, context_instance=RequestContext(request))

def baseinfo(request):
    pass


def quiz(request):
    pass