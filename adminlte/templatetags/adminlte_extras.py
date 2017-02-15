from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

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


@register.simple_tag
def confirm_btn(view_name, **kwargs):
    """
    a button with confirm, you can just use this tag like {% url 'foo' %}
    e.g: {% confirm_btn view_name="foo" pk=permission.id %}
    :param view_name: view name
    :param kwargs:
    :return:
    """
    css_class = kwargs.pop('css_class', 'btn btn-danger')
    text = kwargs.pop('text', 'Delete')
    url = reverse(view_name, kwargs=kwargs)

    return mark_safe("""<button class="%s confirm-to-href-btn" data-href="%s">%s</button>""" % (css_class, url, text))
