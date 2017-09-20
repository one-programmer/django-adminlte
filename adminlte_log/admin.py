from django.contrib import admin

from .models import AdminlteLog, AdminlteLogType


admin.site.register(AdminlteLog)
admin.site.register(AdminlteLogType)
