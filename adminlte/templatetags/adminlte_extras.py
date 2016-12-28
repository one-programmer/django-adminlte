
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def order_th(context, name, field):
    order_by = context['pager'].params.get('order_by')
    desc = False
    if order_by == field:
        css_class = 'sorting_asc'
    elif order_by == '-%s' % field:
        css_class = 'sorting_desc'
        desc = True
    else:
        css_class = 'sorting'

    return mark_safe('<th class="click_sorting {css_class}" data-field="{field}" data-desc="{desc}">{name}</th>'.format(
        css_class=css_class, field=field, name=name, desc=int(desc)
    ))
