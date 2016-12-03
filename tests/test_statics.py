import os

from django.test import TestCase

from django.contrib.staticfiles import finders


class StaticTestCase(TestCase):

    def test_font_awesome(self):
        path = 'plugins/font-awesome/css/font-awesome.min.css'
        absolute_path = finders.find(path)
        assert absolute_path is not None
        assert os.path.exists(absolute_path)

        path = 'plugins/font-awesome/fonts/FontAwesome.otf'
        absolute_path = finders.find(path)
        assert absolute_path is not None
        assert os.path.exists(absolute_path)
