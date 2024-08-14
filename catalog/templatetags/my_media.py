from django import template

register = template.Library()


@register.filter(name='mymedia')
def mymedia(data):
    if data:
        return f'/media/{data}'
    return '#'
