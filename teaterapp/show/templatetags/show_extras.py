from django import template

register = template.Library()

import datetime

@register.filter(name='gender')
def gender(value):
    return value.genderStr()



@register.filter(name='relative')
def relative(value):
    from_date = datetime.datetime.now().date() - value
    return value
    
@register.filter(name='scaleval')
def scaleval(value, arg):
    return value.rating_set.get(scale=arg.scale).value



@register.filter(name='statestr')
def sstatestr(value):
    return value.stateStr()


