from flask import Flask, request, redirect
import requests
from withings_api_example import config

app = Flask(__name__)

CLIENT_ID = config.get('withings_api_example', 'client_id')
CUSTOMER_SECRET = config.get('withings_api_example', 'customer_secret')
STATE = config.get('withings_api_example', 'state')
ACCOUNT_URL = config.get('withings_api_example', 'account_withings_url')
WBSAPI_URL = config.get('withings_api_example', 'wbsapi_withings_url')
CALLBACK_URI = config.get('withings_api_example', 'callback_uri')
#https://asia-southeast2-eric-han.cloudfunctions.net

@app.route("/")
def get_code():
    """
    Route to get the permission from an user to take his data.
    This endpoint redirects to a Withings' login page on which
    the user has to identify and accept to share his data
    """
    payload = {'response_type': 'code',  # imposed string by the api
               'client_id': CLIENT_ID,
               'state': STATE,
               'scope': 'user.metrics',  # see docs for enhanced scope
               'redirect_uri': CALLBACK_URI  # URL of this app
               }

    r_auth = requests.get(f'{ACCOUNT_URL}/oauth2_user/authorize2',
                          params=payload)

    return redirect(r_auth.url)


@app.route("/get_token")
def get_token():
    """
    Callback route when the user has accepted to share his data.
    Once the auth has arrived Withings servers come back with
    an authentication code and the state code provided in the
    initial call
    """
    code = request.args.get('code')
    state = request.args.get('state')

    payload = {'grant_type': 'authorization_code',
               'client_id': CLIENT_ID,
               'client_secret': CUSTOMER_SECRET,
               'code': code,
               'redirect_uri': CALLBACK_URI
               }

    r_token = requests.post(f'{ACCOUNT_URL}/oauth2/token',
                            data=payload).json()

    access_token = r_token.get('access_token', '')
    refresh_token = r_token.get('refresh_token', '')

    payload = {'action': 'requesttoken',
	'grant_type': 'refresh_token',
	'client_id' : CLIENT_ID,
	'client_secret': CUSTOMER_SECRET,
	'refresh_token': refresh_token}
    r_refresh_token = requests.get(f'{WBSAPI_URL}/v2/oauth2',
                            params=payload).json()
    access_token = r_refresh_token.get('access_token', '')
    print(r_refresh_token)
    print(r_refresh_token['body']['access_token'])
    
    access_token = r_refresh_token['body']['access_token']

    # GET Some info with this token
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'action': 'getdevice'}

    # List devices of returned user
    r_getdevice = requests.get(f'{WBSAPI_URL}/v2/user',
                               headers=headers,
                               params=payload).json()

    payload = {
        'action': 'getmeas', 
        'meastype': 71,
        }
    user_temp = requests.get(f'{WBSAPI_URL}/measure',
                               headers=headers,
                               params=payload).json()

    return user_temp
