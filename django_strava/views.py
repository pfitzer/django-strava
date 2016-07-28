from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from models import StravaUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from stravalib.client import Client
from django.conf import settings

client_id = settings.DJANGO_STRAVA_CLIENT_ID
client_secret = settings.DJANGO_STRAVA_CLIENT_SECRET
redirect_url = settings.DJANGO_STRAVA_REDIRECT_URL


@login_required()
def profile(request, athleteid=None):
    """
    shows the strava user profile of the current user, or if athleteid is given the strava profile
    of the given user

    Args:
        request:
        athleteid: the strava athlete id

    Returns:

    """
    client = Client()
    try:
        strava_user = StravaUser.objects.get(uid=request.user)
        client.access_token = strava_user.access_token
        curr_athlete = client.get_athlete(athlete_id=athleteid)
        athlete_friends = client.get_athlete_friends(athlete_id=athleteid)
        return HttpResponse(render(request, 'profile.html', {'athlete': curr_athlete, 'athlete_friends': athlete_friends}))
    except ObjectDoesNotExist:
        session_key = request.session._session_key
        authorize_url = client.authorization_url(client_id=client_id,
                                                 redirect_uri='%s/strava/authorization/%s' % (
                                                 redirect_url, session_key))
        return HttpResponse(render(request, 'profile.html', {'auth_url': authorize_url}))
    except Exception as e:
        raise Http404


def authorize(request, session_key):
    """

    Args:
        request:
        session_key:

    Returns:

    """
    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    try:
        user = User.objects.get(id=uid)
    except ObjectDoesNotExist:
        raise Http404
    client = Client()
    code = request.GET.get('code')  # or whatever your framework does
    access_token = client.exchange_code_for_token(client_id=client_id,
                                                  client_secret=client_secret, code=code)
    strava_user = StravaUser(uid=user, access_token=access_token)
    strava_user.save()
    return redirect('strava_profile')
