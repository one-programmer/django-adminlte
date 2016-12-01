import logging

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.test import TestCase

from adminlte.utils import AdminMenu
from adminlte.views import IndexView


class MenuTest(TestCase):

    def setUp(self):
        menus = []
        menu = AdminMenu('1', sort=10)
        menus.append(menu)
        menu = AdminMenu('2', sort=8)
        menus.append(menu)
        menu = AdminMenu('3', sort=9)
        menus.append(menu)
        menus.sort(key=lambda menu: menu.sort, reverse=True)
        self.menus = menus

    def test_menu_count(self):
        self.assertTrue(self.menus.pop().sort == 8)
        self.assertTrue(self.menus.pop().sort == 9)
        self.assertTrue(self.menus.pop().sort == 10)


class ViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='bohan', email='bohan.zhang@speedx.com', password='123456')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

    def test_index_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/adminlte/index')

        request.user = AnonymousUser()

        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 302, msg='anonymous user will redirect to login page')

        request.user = self.user

        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
