import math

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.views.generic import View
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden


class AdminMenu(object):

    def __init__(self, name, icon_classes='fa-circle-o', description=None, parent_menu=None, sort=0):
        self.description = description
        self.icon_classes = icon_classes
        self.view_name = None
        self.name = name
        self.sub_menus = []
        self.extra_view_names = []
        self.parent_menu = parent_menu
        self.sub_menus = []
        self.sort = sort

    def active(self, view_name):

        if view_name == self.view_name:
            return True

        return False


class AdminLTEBaseView(View):
    template_name = 'adminlte/index.html'

    login_required = True

    menu = None

    permission = None

    @staticmethod
    def _default_is_login_func(request):
        return not isinstance(request.user, AnonymousUser) and request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.

        if getattr(self, 'login_required', True):
            is_login = getattr(settings, 'ADMINLTE_IS_LOGIN_FUNC', self._default_is_login_func)
            login_view = getattr(settings, 'ADMINLTE_LOGIN_VIEW', 'adminlte.login')
            if not is_login(request):
                return redirect(login_view)

        if self.permission:
            if not request.user.has_perm(self.permission):
                return HttpResponseForbidden()

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @classmethod
    def menus(cls, user):
        menus = []
        for clzss in cls.__subclasses__():

            menu = clzss.menu
            if menu:
                permission = clzss.permission
                if permission:
                    if not user.is_superuser and not user.has_perm(clzss.permission):
                        continue

                menu.view_name = clzss._view_name()
                menus.append(menu)

        last_menus = []
        for menu in menus:
            if not menu.parent_menu:
                last_menus.append(menu)
            else:
                parent_menu = menu.parent_menu
                if menu not in parent_menu.sub_menus:
                    parent_menu.sub_menus.append(menu)
                    parent_menu.sub_menus.sort(key=lambda sub_menu: sub_menu.sort, reverse=True)
                if parent_menu not in last_menus:
                    last_menus.append(parent_menu)

        last_menus.sort(key=lambda menu: menu.sort, reverse=True)
        return last_menus

    @classmethod
    def _regex_name(cls):
        char_list = []

        name = cls.__name__.replace('View', '')
        for index, char in enumerate(name):
            if char.isupper():
                if index != 0:
                    char_list.append('/')
                char_list.append(char.lower())
            else:
                char_list.append(char)

        return r'^%s$' % ''.join(char_list)

    @classmethod
    def _view_name(cls):
        char_list = []

        name = cls.__name__.replace('View', '')
        for index, char in enumerate(name):
            if char.isupper():
                char_list.append('.')
                char_list.append(char.lower())
            else:
                char_list.append(char)

        return 'adminlte' + ''.join(char_list)

    @classmethod
    def urlpatterns(cls):
        from django.conf.urls import url

        urlpatterns = []
        for clzss in cls.__subclasses__():
            regex_name = clzss._regex_name() if callable(clzss._regex_name) else clzss._regex_name
            if regex_name == r'^index$':
                urlpatterns.append(url(r'^$', clzss.as_view()))
            urlpatterns.append(url(regex_name, clzss.as_view(), name=clzss._view_name()))

        return urlpatterns


class RootMenu(object):

    def __init__(self, current_view_name, init_menus):
        self.current_view_name = current_view_name
        self.current_menu = None
        self.parent_menu = None
        self.menus = []

        for menu in init_menus:
            self.add_menu(menu)

    def add_menu(self, menu):
        view_name = self.current_view_name
        if menu.active(view_name):
            self.current_menu = menu
        elif menu.sub_menus:
            for sub_menu in menu.sub_menus:
                if sub_menu.active(view_name):
                    self.current_menu = sub_menu
                    self.parent_menu = menu
                    break

        self.menus.append(menu)
        return self


class Pager(object):

    def __init__(self, query, page, size, params=None):
        self.count = query.count()

        start = (page - 1) * size
        end = start + size
        self.items = query[start: end]
        self.page = page
        self.size = size
        self.params = params

    @property
    def has_next(self):
        return self.count > self.page * self.size

    @property
    def has_next_two(self):
        return self.count > (self.page + 1) * self.size

    @property
    def last_page(self):
        return math.ceil(self.count / self.size)

    @classmethod
    def from_request(cls, query, request):
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 20))
        order_by = request.GET.get('order_by', '-id')

        params = {k: v[0] for k, v in dict(request.GET).items()}

        if 'page' in params:
            params.pop('page')

        if 'size' in params:
            params.pop('size')

        params.update(size=size)

        query = query.order_by(order_by)
        return Pager(query, page, size, params)

    @property
    def url_params(self):
        return urlencode(self.params)


def admin_config(request):

    if isinstance(request.user, AnonymousUser):
        name = 'Guest'
        date_joined = None
    else:
        name = "{first_name} {last_name}".format(first_name=request.user.first_name, last_name=request.user.last_name)
        date_joined = request.user.date_joined

    view_name = request.resolver_match.view_name if request.resolver_match else None
    return {
        "ROOT_MENU": RootMenu(current_view_name=view_name, init_menus=AdminLTEBaseView.menus(user=request.user)),
        "current_view_name": view_name,
        "current_user": {
            "nickname": name,
            "avatar_url": "/static/adminLTE/img/avatar5.png",
            "date_joined": date_joined,
        },
    }
