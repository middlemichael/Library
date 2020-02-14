import httplib2
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
import json
import requests
import oauth2client


def accesstoken():

    CLIENT_ID = 'CLIENT ID HERE'
    CLIENT_SECRET = 'CLIENT SECRET HERE'
    REFRESH_TOKEN = 'REFRESH TOKEN HERE'

    credentials = client.OAuth2Credentials(
        access_token=None,  # set access_token to None since we use a refresh token
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
        token_expiry=None,
        token_uri=GOOGLE_TOKEN_URI,
        user_agent=None,
        revoke_uri=GOOGLE_REVOKE_URI)

    credentials.refresh(httplib2.Http())  # refresh the access token (optional)
    http = credentials.authorize(httplib2.Http())  # apply the credentials
    s = credentials.to_json()[18:]
    return s.partition('"')[0] #return new access token




