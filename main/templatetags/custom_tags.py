from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='content_shorten')
@stringfilter
def content_shorten(value, max_len=100):
    if len(value) > max_len:
        return value[:max_len] + ' ...'
    return value