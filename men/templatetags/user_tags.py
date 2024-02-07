from django import template
from datetime import date
from django.utils.safestring import mark_safe

from ..models import Men

register = template.Library()


@register.simple_tag
def total_year_users(post=None):
    today = date.today()
    if post is None:
        return 'Не установленно'
    else:
        age = today.year - post.year - ((today.month, today.day) < (post.month, post.day))
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
def xxx():
    return Men.published.count()


@register.simple_tag
def add_space(world):
    return mark_safe(f'{world}'.ljust(20))
