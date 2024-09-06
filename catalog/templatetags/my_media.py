from django import template

register = template.Library()


@register.filter(name='mymedia')
def my_media(data):
    if data:
        return f'/media/{data}'
    return '#'
