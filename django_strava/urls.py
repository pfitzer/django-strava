from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='strava_profile'),
    url(r'^profile/(?P<athleteid>[0-9]+)/$', views.profile, name='strava_profile'),
    url(r'^authorization/(?P<session_key>.*)/$', views.authorize, name='strava_authorization'),
]