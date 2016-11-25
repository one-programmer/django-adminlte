from django.conf.urls import url

from . import views
from . import utils


urlpatterns = utils.AdminLTEBaseView.urlpatterns()

urlpatterns += [
            url(r'^login$', views.login, name='adminlte.login'),
            url(r'^logout$', views.logout, name='adminlte.logout'),
]
