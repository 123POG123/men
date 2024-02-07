import hashlib
from urllib.parse import urlencode

from django import template
from datetime import date


register = template.Library()


@register.simple_tag
def total_year_users(post):
    print(post)
    today = date.today()
    age = today.year - post.year - ((today.month, today.day) < (post.month, post.day))
    # if date_user is not None:
    #     return age
    suffix = 'лет'
    if (age // 10) % 10 != 1:
        if age % 10 == 1:
            suffix = 'год'
        elif age % 10 in (2, 3, 4):
            suffix = 'года'
    if age <= 0:
        return None
    else:
        return f'{age} {suffix}'


@register.simple_tag
def add_space(world):
    return mark_safe(f'{world}'.ljust(20))


register = template.Library()


# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
    default = "https://example.com/static/images/defaultavatar.jpg"
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email.lower()).hexdigest(), urlencode({'d': default, 's': str(size)}))


# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" width="%d" height="%d">' % (url, size, size))


@register.filter
def www(val):
    return f'{val.upper()}===='