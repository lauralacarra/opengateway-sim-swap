import logging
import os
import re
import base64
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Instantiate Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Get client credentials as provided on your app’s registration from environment variables
app_client_id = os.getenv("APP_CLIENT_ID")
app_client_secret = os.getenv("APP_CLIENT_SECRET")
api_gateway_url = os.getenv("API_GATEWAY_URL")
# SimSwap URLs
simswap_base_url = f'{api_gateway_url}/sim-swap/v0/'
RETRIEVE_DATE_URL = f'{simswap_base_url}retrieve-date'
CHECK_URL = f'{simswap_base_url}check'

@app.route('/retrieve_date/<string:phone_number>')
def retrieve_date(phone_number = None):
    try:
        auth_token = getAccessToken(phone_number)
        headers =  {
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        }
        payload = { 'phoneNumber': phone_number }

        # Retrieve last SIM Swap date
        response = requests.post(RETRIEVE_DATE_URL, json=payload, headers=headers, timeout=5)
    except ValueError as e:
        return jsonify(message=str(e)), 401
    data = response.json()
    return jsonify(message = f'Last SIM Swap was in {data.get('latestSimChange', 'Unknow')}')

@app.route('/check/<string:phone_number>/<int:max_age>')
def check(phone_number, max_age = 240):
    auth_token = getAccessToken(phone_number)
    headers =  {
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'phoneNumber': phone_number,
        'max_age': max_age
        }

    # Retrieve last SIM Swap date
    response = requests.post(CHECK_URL, json=payload, headers=headers, timeout=5)
    data = response.json()
    return jsonify(message=f'It is {data.get('swapped', 'Unknow')} that there has been a sim swap in the last {max_age} hours.')

# CIBA settings
PURPOSE = os.getenv("PURPOSE")
GRANT_TYPE = os.getenv("GRANT_TYPE")

def getAccessToken(phone_number):
    authorization = app_client_id + ':' + app_client_secret
    encoded_authorization = base64.b64encode(authorization.encode()).decode()
    headers = {
        'Authorization': "Basic %s" % encoded_authorization,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request_body = {
        'purpose': PURPOSE,
        'login_hint':  f'phone_number:{phone_number}'
    }
    response = requests.post(
            f'{api_gateway_url}/bc-authorize',
            data=request_body,
            headers=headers,
            timeout=5
        )
    if response.status_code != 200:
        raise ValueError(f'Something was wrong: {response.status_code} ==> {response.json().get('message', None)}')

    data = response.json()
    if response.status_code == 200:
        consent_url = data.get('consent_url', None)
        if consent_url:
            raise ValueError(f'try again, consent was being processed.')

    request_body = {'grant_type': GRANT_TYPE, 'auth_req_id': data['auth_req_id']}
    r = requests.post(
        f'{api_gateway_url}/token',
        data=request_body,
        headers=headers,
        timeout=5
    )
    token_resp = r.json()
    if r.status_code == 200:
        return f'{token_resp['token_type']} {token_resp['access_token']}'
    else:
        raise ValueError(f'Could not get token: {response.status_code}')

if __name__ == "__main__":
    class NoPhone(logging.Filter):
        def filter(self, record):
            PHONE_REGEX = re.compile('\\+[0-9]{9,11}')
            for arg in record.args:
                if isinstance(arg, str):
                    record.args = tuple(PHONE_REGEX.sub('+***********', arg)  for arg in record.args)
            return True

    logging.getLogger('werkzeug').addFilter(NoPhone())
    app.run(host="0.0.0.0", port=3000)
