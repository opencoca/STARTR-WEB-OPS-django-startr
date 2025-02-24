from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """ 
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value
    what, to = arg.split('|')
    return value.replace(what, to)

@register.filter
def capitalize(value):
    """
    Capitalize filter
    Use `{{ "aaa"|capitalize }}`
    """
    if not isinstance(value, str):
        return value
    return str(value).strip().capitalize()
