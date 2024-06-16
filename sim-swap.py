import os
import re
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from opengateway_sandbox_sdk import Simswap
from dotenv import load_dotenv

load_dotenv()

# Instantiate Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Get client credentials as provided on your app’s registration from environment variables
app_client_id = os.getenv("APP_CLIENT_ID")
app_client_secret = os.getenv("APP_CLIENT_SECRET")

@app.route('/retrieve_date/<string:phone_number>')
def sdk_retrieve_date(phone_number = None):
    try:
        simswap_client = Simswap(app_client_id, app_client_secret, phone_number)

        # Retrieve last SIM Swap date
        last_swap = simswap_client.retrieve_date()

        return jsonify(message=f'Last SIM Swap was in {last_swap}')
    except Exception as e:
        return jsonify(message=str(e)), 401

@app.route('/check/<string:phone_number>/<int:max_age>')
def sdk_check(phone_number = None, max_age = 240):
    try:
        simswap_client = Simswap(app_client_id, app_client_secret, phone_number)

        # Check if the SIM Swap is recent
        simswap_check = simswap_client.check(max_age=max_age)

        return jsonify(message=f'Its {simswap_check} that there has been a sim swap in the last {max_age/24} days.')
    except Exception as e:
        return jsonify(message=str(e)), 401

if __name__ == "__main__":
    class NoPhone(logging.Filter):
        def filter(self, record):
            PHONE_REGEX = re.compile('\\+[0-9]{9,11}')
            for arg in record.args:
                if isinstance(arg, str):
                    record.args = tuple(PHONE_REGEX.sub('***********', arg)  for arg in record.args)
            return True


    logging.getLogger('werkzeug').addFilter(NoPhone())
    app.run(host="0.0.0.0", port=3000)
