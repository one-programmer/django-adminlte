from django.conf import settings
from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponseForbidden


class IndexView(View):
    template_name = 'dashboard.html'

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