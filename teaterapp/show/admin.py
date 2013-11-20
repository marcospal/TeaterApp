# -*- coding: utf-8 -*-

from models import *

from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)


class ColorAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title',)
admin.site.register(Color, ColorAdmin)


class ScaleAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
admin.site.register(Scale, ScaleAdmin)


class LocationScaleInLine(admin.TabularInline):
    model = Location.parameters.through



class LocationAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    inlines = [ LocationScaleInLine, ]
    exclude = ('version',)
admin.site.register(Location, LocationAdmin)

class ProfileScaleInLine(admin.TabularInline):
    model = Profile.ratings.through

class ProfileNoteInLine(admin.TabularInline):
    model = Note
    #fk_name = 'question' #or 'world', as applicable.
    extra=1


class ProfileAdmin(admin.ModelAdmin):
    ordering = ('active', )
    search_fields = ('code',)
    inlines = [ ProfileScaleInLine, ProfileNoteInLine ]
admin.site.register(Profile, ProfileAdmin)


#class RatingAdmin(admin.ModelAdmin):
#    ordering = ('value', )
#admin.site.register(Rating, RatingAdmin)



class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'question' #or 'world', as applicable.
    extra=1

class QuestionAdmin(admin.ModelAdmin):
    ordering = ('id', )
    search_fields = ('text',)
    inlines = [
        AnswerInline,
    ]
admin.site.register(Question, QuestionAdmin)


#class NoteAdmin(admin.ModelAdmin):
#    ordering = ('id', )
#    search_fields = ('text',)
#admin.site.register(Note, NoteAdmin)


#class AnswerAdmin(admin.ModelAdmin):
#    ordering = ('id', )
#    search_fields = ('text',)
#admin.site.register(Answer, AnswerAdmin)