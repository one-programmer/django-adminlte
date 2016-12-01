import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'dsaflkjxzvc'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    "tests",
    "adminlte",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
