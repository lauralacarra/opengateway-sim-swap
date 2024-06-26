<h1 align="center">
  Simswap sample app (Backend)
</h1>

<h4 align="center">This project attempts to present a sample application that demonstrates the operation of the sim-swap api. The BE development framework used is Python. </h4>

## Prerequisites

To run the sample:
  - Windows
  - [Python](https://nodejs.org/)
  - [Git](https://git-scm.com)


Requirements needed to develop/run the backend through the sdk sandbox
                  
    Client credentials (App APIKey provided by Sandbox)
    opengateway-sandbox-sdk-python library available from https://test.pypi.org/project/opengateway-sandbox-sdk/

## Configuration
Some variables must be set in the environment. For that, create or update update variables of  `.env` file on the project root folder and set the values with the correct. (Sample in .env.sample)

If you're going to run sim-swap.py file, the program that use opengateway-sandbox-sdk library, you'll only need to set APP_API_KEY variable.
  - APP_API_KEY: APIKey generated by developer from Opengateway Sandbox
```.env
APP_API_KEY=your_sandbox_api_key
```
If you run sim-swap-no-sdk.py, you need three additional variables:
 - API_GATEWAY_URL: Url of the sandbox aggregator
 - PURPOSE: purpose of the sim-swap API
 - GRANT_TYPE: We use Client-Initiated Backchannel Authentication (CIBA)

```.env
APP_API_KEY=your_sandbox_api_key
API_GATEWAY_URL=https://sandbox.opengateway.telefonica.com/apigateway
PURPOSE=dpv:FraudPreventionAndDetection#sim-swap
GRANT_TYPE=urn:openid:params:grant-type:ciba
```


## How to use

To clone and run this application, make sure you meet all the above prerequisites. Then, from your command line:

```bash
# Clone this repository
$ git clone https://github.com/Telefonica/opengateway-sim-swap-be.git
cd opengateway-sim-swap-be

pip install -r requirements.txt
# Install simswap sdk from test.pypi.org
pip install -i https://test.pypi.org/simple/ opengateway-sandbox-sdk
# Option A: Run app using SDK
python sim-swap.py
# Option B: Run app without SDK
python sim-swap-no-sdk.py

```

It is also possible to run the application from the command line without a front end using the curl command (replace the phone number 000000000 with the one you want to test): 

curl --location 'http://127.0.0.1:3000/retrieve_date/+34000000000'
curl --location 'http://127.0.0.1:3000/check/+34000000000/240'

If you don't want to set up a server on your computer, you can run the sim-swap-command-line.py file from the command line and you will be able to see how the library works by simply running the command (remember change the phonenumber for the testing number):
```bash
python .\sim-swap-command-line.py +3400000000
```

## Project compoments
- Front repository: https://github.com/Telefonica/opengateway-sim-swap-app



## How to use the SDK in your code

BE Sample code for retrive last sim_swap:
```code
    from sandbox.opengatewaysdk import Simswap
    simswap_client = SIMSwap('your-SDK-APIKey', phone_number)
    simswap_client.retrieve_date()
```

BE Sample code for check :
```code
    from sandbox.opengatewaysdk import Simswap
    simswap_client = SIMSwap('your-SDK-APIKey', phone_number)
    simswap_client.chek()
```
    