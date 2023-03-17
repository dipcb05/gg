from django.http import JsonResponse
from django.shortcuts import redirect
from .utils import get_google_credentials, generate_google_url, handle_google_callback
from google.auth.transport.requests import Request
import requests
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def health(request):
    credentials = get_google_credentials(request)    
    if credentials is None or credentials.expired:
        if credentials and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            auth_url = generate_google_url(request)
            return redirect(auth_url)
    access_token = credentials.token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    data_sources_url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources'
    data_sources_res = requests.get(data_sources_url, headers=headers)
    data_sources = json.loads(data_sources_res.text)
    print(data_sources)

    data_types_url = 'https://www.googleapis.com/fitness/v1/users/me/dataTypes'
    data_types_res = requests.get(data_types_url, headers=headers)
    data_types = json.loads(data_types_res.text)
    print(data_types)

    aggregate_url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
    aggregate_data = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta",
            "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        }],
        "bucketByTime": { "durationMillis": 86400000 },
        "startTimeMillis": 1646918400000,
        "endTimeMillis": 1647004800000
    }
    aggregate_res = requests.post(aggregate_url, headers=headers, json=aggregate_data)
    aggregated_data = json.loads(aggregate_res.text)
    print(aggregated_data)

    profile_url = 'https://www.googleapis.com/fitness/v1/users/me'
    profile_res = requests.get(profile_url, headers=headers)
    profile_info = json.loads(profile_res.text)
    print(profile_info)

    response_data = {
        'data_sources': data_sources,
        'data_types': data_types,
        'aggregated_data': aggregated_data,
        'profile_info': profile_info,
    }
    
    return JsonResponse({'status': 'authorization successful', 'data': response_data})
    
def oauth2callback(request):
    return handle_google_callback(request)