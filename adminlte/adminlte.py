from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.db.models import Q

from adminlte.forms import PermissionForm
from .utils import AdminLTEBaseView, AdminMenu, Pager


class IndexView(AdminLTEBaseView):
    template_name = 'adminlte/index.html'

    menu = AdminMenu(name="Dashboard", description='Empty Dashboard page', icon_classes='fa-dashboard', sort=99999)


class LogoutView(AdminLTEBaseView):

    def get(self, request, *args, **kwargs):
        django_logout(request)
        return redirect(getattr(settings, 'ADMINLTE_LOGIN_VIEW', 'adminlte.login'))


class LoginView(AdminLTEBaseView):

    login_required = False

    def get(self, request, *args, **kwargs):
        return render(request, 'adminlte/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password, type=1)
        if not user or not user.is_staff:
            message = 'user name or password error'
            return render(request, 'adminlte/login.html', context={
                "message": message
            })
        django_login(request, user)
        return redirect('adminlte.index')


permission_group_menu = AdminMenu(name="Permissions", icon_classes='fa-lock')


class PermissionsView(AdminLTEBaseView):

    menu = AdminMenu('Permissions', parent_menu=permission_group_menu)

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')

        query = Permission.objects.all()

        if search:
            query = query.filter(
                Q(name__contains=search) | Q(codename__contains=search))

        pager = Pager.from_request(query, request)
        return render(request, 'adminlte/permissions/index.html', context={
            "pager": pager,
            "search": search
        })


class PermissionsCreateView(AdminLTEBaseView):

    menu = AdminMenu('Add Permissions', parent_menu=permission_group_menu)

    template_name = 'adminlte/permissions/edit.html'

    def post(self, request, *args, **kwargs):
        form = PermissionForm(request.POST)

        if form.is_valid():
            Permission.objects.create(codename=form.cleaned_data['codename'],
                                      name=form.cleaned_data['name'],
                                      content_type=ContentType.objects.get(model='permission'))
            messages.add_message(request, messages.SUCCESS, '增加成功')
            return redirect('adminlte.permissions')

        messages.add_message(request, messages.ERROR, '参数错误')
        return render(request, self.template_name)


class PermissionDeleteView(AdminLTEBaseView):

    _regex_name = 'permissions/(?P<pk>[0-9]+)/delete'

    def get(self, request, pk, *args, **kwargs):
        permission = Permission.objects.get(pk=pk)
        permission.delete()
        messages.add_message(request, messages.SUCCESS, 'delete success')
        return redirect('adminlte.permissions')


class PermissionEditView(AdminLTEBaseView):
    _regex_name = 'permissions/(?P<pk>[0-9]+)/edit'

    template_name = 'adminlte/permissions/edit.html'

    def get(self, request, pk, *args, **kwargs):
        permission = Permission.objects.get(pk=pk)
        return render(request, self.template_name, context={
            "permission": permission
        })

    def post(self, request, pk, *args, **kwargs):
        form = PermissionForm(request.POST)

        if form.is_valid():
            permission = Permission.objects.get(pk=pk)
            permission.codename = form.cleaned_data['codename']
            permission.name = form.cleaned_data['name']
            permission.save()
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect('adminlte.permissions')

        messages.add_message(request, messages.ERROR, '参数错误')
        return render(request, self.template_name)
