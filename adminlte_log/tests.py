from django.contrib.auth.models import User
from django.test import TestCase

from adminlte_log.models import AdminlteLogType, AdminlteLog


class AdminlteLogTest(TestCase):

    def setUp(self):
        AdminlteLogType.objects.create(name='test', code='test')
        self.user = User.objects.create_user(username='bohan')

    def test_log(self):
        log = AdminlteLog.info('test', user=self.user, sort_desc='This is a log', foo='bar')
        self.assertEqual(log.id, 1)
