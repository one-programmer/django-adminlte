from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect, render_to_response

from .utils import Pager, AdminLTEBaseView, AdminMenu
from .models import Page
from .forms import PageForm


page_manager = AdminMenu("富文本管理", icon_classes='fa-safari')


class IndexView(AdminLTEBaseView):
    template_name = 'adminlte/index.html'

    menu = AdminMenu(name="Dashboard", description='控制面板页面', icon_classes='fa-dashboard')


class ExampleView(AdminLTEBaseView):
    template_name = 'adminlte/example.html'

    menu = AdminMenu(name="样例", description='这是一个测试页面', icon_classes='fa-code')

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Hello world.')
        messages.add_message(request, messages.ERROR, 'Hello world.')
        messages.add_message(request, messages.SUCCESS, 'Hello world.')
        return render(request, self.template_name)


class ExamplePagesView(AdminLTEBaseView):
    template_name = 'adminlte/pages/index.html'

    menu = AdminMenu(name="富文本列表", parent_menu=page_manager)

    def get(self, request, *args, **kwargs):
        query = Page.objects.all()

        pager = Pager.from_request(query, request)
        return render(request, self.template_name, context={
            "pager": pager
        })


class ExamplePagesCreateView(AdminLTEBaseView):
    template_name = 'adminlte/pages/edit.html'

    menu = AdminMenu(name="新页面", parent_menu=page_manager)

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST)
        if form.is_valid():
            Page.objects.create(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            messages.add_message(request, messages.SUCCESS, '增加成功')
            return redirect('adminlte.example.pages')

        messages.add_message(request, messages.ERROR, '参数错误')
        return render(request, self.template_name)


class ExamplePageEditView(AdminLTEBaseView):
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
