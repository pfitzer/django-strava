from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import StravaUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from stravalib.client import Client
from django.conf import settings

client_id = settings.DJANGO_STRAVA_CLIENT_ID
client_secret = settings.DJANGO_STRAVA_CLIENT_SECRET


@login_required()
def account(request):
    client = Client()
    try:
        strava_user = StravaUser.objects.get(uid=request.user)
        client.access_token = strava_user.access_token
        curr_athlete = client.get_athlete()
        return HttpResponse(render(request, 'account.html', {'athlete': curr_athlete}))
    except ObjectDoesNotExist:
        session_key = request.session._session_key
        authorize_url = client.authorization_url(client_id=client_id,
                                                 redirect_uri='http://localhost:8000/strava/authorization/' + session_key)
        return HttpResponse(render(request, 'account.html', {'auth_url': authorize_url}))
    except Exception as e:
        return HttpResponse(status=404)



def authorize(request, session_key):
    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    user = User.objects.get(id=uid)
    client = Client()
    code = request.GET.get('code')  # or whatever your framework does
    access_token = client.exchange_code_for_token(client_id=client_id,
                                                  client_secret=client_secret, code=code)
    strava_user = StravaUser(uid=user, access_token=access_token)
    strava_user.save()
    return redirect('account')
