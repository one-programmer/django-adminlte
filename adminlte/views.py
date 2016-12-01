from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect

from .utils import AdminLTEBaseView, AdminMenu


class IndexView(AdminLTEBaseView):
    template_name = 'adminlte/index.html'

    menu = AdminMenu(name="Dashboard", description='Empty Dashboard page', icon_classes='fa-dashboard', sort=99999)


def login(request):
    if request.method == 'GET':
        return render(request, 'adminlte/login.html')
    else:
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


def logout(request):
    django_logout(request)
    return redirect('adminlte.login')
