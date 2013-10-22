from models import *

from django.contrib import admin


class ScaleAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
admin.site.register(Scale, ScaleAdmin)

class LocationAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
admin.site.register(Location, LocationAdmin)


class ParticipantAdmin(admin.ModelAdmin):
    ordering = ('active', 'code',)
    search_fields = ('code',)
admin.site.register(Participant, ParticipantAdmin)
