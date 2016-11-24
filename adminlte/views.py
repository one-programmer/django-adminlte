from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect, render_to_response
from django.views import View

from .utils import admin_only, Pager
from .models import Page
from .forms import PageForm


class AdminMenu(object):

    def __init__(self, name, icon_classes='fa-circle-o', description=None, parent_menu=None):
        self.description = description
        self.icon_classes = icon_classes
        self.view_name = None
        self.name = name
        self.sub_menus = []
        self.extra_view_names = []
        self.parent_menu = parent_menu
        self.sub_menus = []

    def active(self, view_name):

        if view_name == self.view_name:
            return True

        return False


class MenuHub(object):
    page_manager = AdminMenu("富文本管理", icon_classes='fa-safari')


class OdminBaseView(View):
    template_name = 'adminlte/index.html'

    # menu = AdminMenu(name="Dashboard", description='控制面板页面', icon_classes='fa-dashboard')

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.

        if getattr(self, 'login_required', True):
            if not request.user.id or not request.user.is_staff:
                return redirect('adminlte.login')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @classmethod
    def menus(cls):
        menus = []
        for clzss in cls.__subclasses__():
            if hasattr(clzss, 'menu'):
                menu = clzss.menu
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
                if parent_menu not in last_menus:
                    last_menus.append(parent_menu)

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

        urlpatterns += [
            url(r'^login$', login, name='adminlte.login'),
            url(r'^logout$', logout, name='adminlte.logout'),
            url(r'^pages/(?P<page_id>[0-9]+)/$', pages, name='adminlte.example.pages'),
        ]
        print('urlpatterns:', urlpatterns)
        return urlpatterns


class IndexView(OdminBaseView):
    template_name = 'adminlte/index.html'

    menu = AdminMenu(name="Dashboard", description='控制面板页面', icon_classes='fa-dashboard')


class ExampleView(OdminBaseView):
    template_name = 'adminlte/example.html'

    menu = AdminMenu(name="样例", description='这是一个测试页面', icon_classes='fa-code')

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Hello world.')
        messages.add_message(request, messages.ERROR, 'Hello world.')
        messages.add_message(request, messages.SUCCESS, 'Hello world.')
        return render(request, self.template_name)


class ExamplePagesView(OdminBaseView):
    template_name = 'adminlte/pages/index.html'

    menu = AdminMenu(name="富文本列表", parent_menu=MenuHub.page_manager)

    def get(self, request, *args, **kwargs):
        query = Page.objects.all()

        pager = Pager.from_request(query, request)
        return render(request, self.template_name, context={
            "pager": pager
        })


class ExamplePagesCreateView(OdminBaseView):
    template_name = 'adminlte/pages/edit.html'

    menu = AdminMenu(name="新页面", parent_menu=MenuHub.page_manager)

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST)
        if form.is_valid():
            Page.objects.create(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            messages.add_message(request, messages.SUCCESS, '增加成功')
            return redirect('adminlte.example.pages')

        messages.add_message(request, messages.ERROR, '参数错误')
        return render(request, self.template_name)


class ExamplePageEditView(OdminBaseView):
    template_name = 'adminlte/pages/edit.html'

    _regex_name = 'pages/(?P<page_id>[0-9]+)/edit'

    def get(self, request, page_id, *args, **kwargs):
        page = Page.objects.get(pk=page_id)
        return render(request, self.template_name, context={
            "page": page
        })

    def post(self, request, page_id, *args, **kwargs):
        page = Page.objects.get(pk=page_id)
        form = PageForm(request.POST)
        if form.is_valid():
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.save()
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect('adminlte.example.pages')

        messages.add_message(request, messages.ERROR, '参数错误')
        return render(request, self.template_name)


def login(request):
    if request.method == 'GET':
        return render(request, 'adminlte/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password, type=1)
        if not user or not user.is_staff:
            message = '用户名或密码错误'
            return render(request, 'adminlte/login.html', context={
                "message": message
            })
        django_login(request, user)
        return redirect('adminlte.index')


def logout(request):
    django_logout(request)
    return redirect('adminlte.login')


def pages(request, page_id):
    page = Page.objects.get(pk=page_id)
    return render_to_response('adminlte/page.html', context={
        "page": page
    })
