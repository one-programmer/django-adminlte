import copy
import json

from django.contrib.auth.models import User
from django.db import models


class AdminlteLogType(models.Model):
    name = models.CharField('name', max_length=100)
    code = models.CharField('code', max_length=100, unique=True)
    description = models.TextField('description', null=True, blank=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class AdminlteLog(models.Model):
    LEVEL_DEBUG = 0
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3

    LEVEL_CHOICES = ((LEVEL_DEBUG, 'debug'), (LEVEL_INFO, 'info'), (LEVEL_WARNING, 'warning'), (LEVEL_ERROR, 'error'),)

    type = models.ForeignKey(AdminlteLogType)
    user = models.ForeignKey(User)
    level = models.IntegerField('level', choices=LEVEL_CHOICES)
    sort_desc = models.CharField('sort desc', max_length=255)
    _ext_data = models.TextField(db_column='ext_data')
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    @classmethod
    def log(cls, level, log_type, user, sort_desc, **kwargs):
        if isinstance(log_type, str):
            log_type = AdminlteLogType.objects.get(code=log_type)
        return AdminlteLog.objects.create(type=log_type, user=user, level=level, sort_desc=sort_desc, ext_data=kwargs)

    @classmethod
    def debug(cls, log_type, user, sort_desc, **kwargs):
        return cls.log(cls.LEVEL_DEBUG, log_type, user, sort_desc, **kwargs)

    @classmethod
    def info(cls, log_type, user, sort_desc, **kwargs):
        return cls.log(cls.LEVEL_INFO, log_type, user, sort_desc, **kwargs)

    @classmethod
    def warning(cls, log_type, user, sort_desc, **kwargs):
        return cls.log(cls.LEVEL_WARNING, log_type, user, sort_desc, **kwargs)

    @classmethod
    def error(cls, log_type, user, sort_desc, **kwargs):
        return cls.log(cls.LEVEL_ERROR, log_type, user, sort_desc, **kwargs)

    @property
    def ext_data(self):
        return json.loads(self._ext_data)

    @ext_data.setter
    def ext_data(self, data):
        self._ext_data = json.dumps(copy.deepcopy(data))
