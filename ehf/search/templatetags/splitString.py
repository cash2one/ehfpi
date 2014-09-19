from django import template
register = template.Library()
@register.filter
def splitStr(mapping,key):
  return mapping.split(key)