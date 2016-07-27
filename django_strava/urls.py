from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^account/$', views.account, name='account'),
    url(r'^authorization/(?P<session_key>.*)/$', views.authorize, name='authorization'),
]