import json

from django.db import models
from django.auth.models import User


class AdminlteLogType(models.Model):
    name = models.CharFiled('name', max_length=100)
    description = models.TextField('description')
    is_deleted = models.BooleanField(default=False, db_index=True)

class AdminlteLog(models.Model):
    type = models.ForignKey(AdminlteLogType)
    user = models.ForignKey(User)
    sort_desc = models.CharFiled('sort desc', max_length=255)
    _ext_data = models.TextField(column='ext_data')
    is_deleted = models.BooleanField(default=False, db_index=True)

    @property
    def ext_data(self):
        return json.loads(_ext_data)

    @ext_data.setter
    def ext_data(self, data):
        self._ext_data = json.dumps(data)