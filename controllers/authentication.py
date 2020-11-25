from django.conf import settings
from controllers.playlist import init_user
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from authlib.integrations.django_client import OAuth
from django.contrib.auth import login, authenticate

gh = settings.AUTHLIB_OAUTH_CLIENTS['github']
oauth = OAuth()
oauth.register(
    name='github',
    client_id=gh['client_id'],
    client_secret=gh['client_secret'],
    access_token_url=gh['access_token_url'],
    access_token_params=gh['access_token_params'],
    authorize_url=gh['authorize_url'],
    api_base_url=gh['api_base_url'],
    client_kwargs=gh['client_kwargs'],
)


def oauth_github_authorize(request):
    github = oauth.create_client('github')
    redirect = request.build_absolute_uri('/oauth/github/callback')
    return github.authorize_redirect(request, redirect)


def oauth_github_callback(request):
    token = oauth.github.authorize_access_token(request)
    resp = oauth.github.get('user', token=token)
    profile = resp.json()

    u, created = get_user_model().objects.get_or_create(
        username=profile['login'],
        email=profile['email'],
        # first_name=profile['name'].split(' ')[0],
    )
    if created:
        init_user(u)

    login(request, user=u, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/app')
