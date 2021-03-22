import json
import requests
from . import settings

def make_app(instance):
    data = {
        "client_name" : "mstd-statistics",
        "redirect_uris" : settings.host + "/r",
        "scopes" : "read"
    }
    r = requests.post(instance + '/api/v1/apps', data = data)
    client_id = r.json()['client_id']
    client_secret = r.json()['client_secret']
    return client_id, client_secret

def get_token(instance, client_id, client_secret, code):
    data = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "scope" : "read",
        "code" : code,
        "grant_type" : "authorization_code",
        "redirect_uri" : settings.host + "/r"
    }
    r = requests.post(instance + '/oauth/token', data = data)
    return r

def revoke_token(instance, client_id, client_secret, token):
    data = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "token" : token
    }
    requests.post(instance + '/oauth/revoke', data = data)