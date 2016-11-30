# Django AdminLTE

## Install

```
pip install django-adminlte-admin
```

## Quick start

1. Add "adminlte" to your INSTALLED_APPS setting like this::

```python
INSTALLED_APPS = [
    ...
    'adminlte.apps.AdminlteConfig',
]
```

2. Include the adminlte URLconf in your project urls.py like this::

```python
url(r'^adminlte/', include('adminlte.urls')),
```

3. Run `python manage.py migrate` to create the adminlte models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/adminlte/ to participate in the adminlte.


## Develop

```shell
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```
