from django.conf.urls import url, include

urlpatterns = [
    url(r'^adminlte/', include('adminlte.urls')),
]
