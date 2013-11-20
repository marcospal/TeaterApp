from django.conf.urls import patterns, include, url
from django.conf import settings
#from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    #login page and where the game is updated
    url(r'^$', 'teaterapp.show.views.login', name='login'),

    #Administrator overview
    url(r'^overview/$', 'teaterapp.show.views.overview', name='overview'),
    url(r'^overview/version/$', 'teaterapp.show.views.overviewversion', name='overviewversion'),
    
    #Administrator location
    url(r'^location/(?P<id>\d+)/$', 'teaterapp.show.views.location', name='location'),
    url(r'^location/(?P<id>\d+)/version/$', 'teaterapp.show.views.locationversion', name='locationversion'),

    #Administrator inspect profile
    url(r'^profile/(?P<id>\d+)/$', 'teaterapp.show.views.profile', name='profile'),
    url(r'^profile/(?P<id>\d+)/version/$', 'teaterapp.show.views.profileversion', name='profileversion'),
    
    #users without profile is sent here to create one    
    url(r'^baseinfo/$', 'teaterapp.show.views.baseinfo', name='baseinfo'),
    
    #users without profile is sent here to create one    
    url(r'^quiz/$', 'teaterapp.show.views.quiz', name='quiz'),

    #Users are sent here to choose a location    
    url(r'^choose/$', 'teaterapp.show.views.choose', name='choose'),

    #Directions
    url(r'^directions/$', 'teaterapp.show.views.directions', name='dircetions'),
        
    #We logout here
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    

    #Go to gate
    url(r'^gotogate/$', 'teaterapp.show.views.gotogate', name='gotogate'),
    

    #Reset
    url(r'^reset/$', 'teaterapp.show.views.reset', name='reset'),

    #State
    url(r'^state/$', 'teaterapp.show.views.state', name='state'),
    
    #color thingie
    url(r'^color/$', 'teaterapp.show.views.color', name='color'),
    url(r'^setcolor/(?P<color>\w+)/$', 'teaterapp.show.views.setcolor', name='setcolor'),

    url(r'^admin/', include(admin.site.urls)),
)
