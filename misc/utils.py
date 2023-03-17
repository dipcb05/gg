# utils.py

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
import requests
import json
from django.core.cache import cache

def authenticate_with_google(request):
    adapter = GoogleOAuth2Adapter(client_id=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
                                  client_secret=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
                                  redirect_uri=request.build_absolute_uri(reverse('google_auth_callback')))
    provider = providers.registry.by_id('google')
    login_url = provider.get_login_url(request, adapter)
    return redirect(login_url)

@login_required
def google_auth_callback(request):
    adapter = GoogleOAuth2Adapter(client_id=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
                                  client_secret=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
                                  redirect_uri=request.build_absolute_uri(reverse('google_auth_callback')))
    provider = providers.registry.by_id('google')
    sociallogin = provider.complete_login(request, adapter, response=None)
    token = sociallogin.token.token
    access_token = token['access_token']
    return JsonResponse({'access_token': access_token})

def cache_access_token(request):
    access_token = request.GET.get('access_token')
    if access_token:
        cache.set('google_access_token', access_token, timeout=None)
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponseBadRequest()