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
    
    #Administrator location
    url(r'^location/(?P<id>\d+)/$', 'teaterapp.show.views.location', name='location'),

    #Administrator inspect profile
    url(r'^profile/(?P<id>\d+)/$', 'teaterapp.show.views.profile', name='profile'),
    
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
    
    url(r'^admin/', include(admin.site.urls)),
)
