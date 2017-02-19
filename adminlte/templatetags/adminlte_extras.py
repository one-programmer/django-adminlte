from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

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
def confirm_btn(view_name, css_class='btn btn-danger', text="Delete", title="Are you sure?", **kwargs):
    """
    a button with confirm, you can just use this tag like {% url 'foo' %}
    e.g: {% confirm_btn view_name="foo" pk=permission.id %}
    :param view_name: view name
    :param css_class: css class, default: btn btn-danger
    :param text: button text
    :param title: title of the confirm box
    :param kwargs: kwargs for url reverse
    :return:
    """
    url = reverse(view_name, kwargs=kwargs)

    return mark_safe("""<button class="%s confirm-to-href-btn" data-title="%s" data-href="%s">%s</button>""" % (
        css_class, title, url, text))


@register.inclusion_tag('adminlte/lib/_pagination.html', takes_context=True)
def pagination(context):
    return context


@register.inclusion_tag('adminlte/lib/_list_search_form.html', takes_context=True)
def search_form(context, placeholder='Search'):
    return dict(value=context.get('search', ''), placeholder=placeholder)
