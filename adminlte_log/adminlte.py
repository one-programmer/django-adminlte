from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response

from adminlte.utils import AdminLTEBaseView, AdminMenu, Pager
from .models import AdminlteLog, AdminlteLogType


log_manager = AdminMenu("日志管理", icon_classes='fa-safari')


class LogView(AdminLTEBaseView):
    template_name = 'log/index.html'

    menu = AdminMenu(name="日志列表", parent_menu=log_manager)

    def get(self, request, *args, **kwargs):
        query = AdminlteLog.objects.all()

        pager = Pager.from_request(query, request)
        return render(request, self.template_name, context={
            "pager": pager
        })
