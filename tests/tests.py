import logging

from django.test import TestCase

from adminlte.utils import AdminMenu


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
