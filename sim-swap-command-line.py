import os
import sys
from opengateway_sandbox_sdk import Simswap

def main() -> None:
    API_KEY = os.getenv('APP_API_KEY')
    phone_number = sys.argv[1]
    if API_KEY is None:
        raise ValueError("API_KEY environment variable is not set")
    
    simswap_client = Simswap(API_KEY, phone_number)
    print(f'CIBA auth success')

    if simswap_client.check(max_age=2400):
        print('Simswap in the last 100 days')
    else:
        print('Not Simswap in the last 100 days')

    last_swap = simswap_client.retrieve_date()
    print(f'Last SIM Swap was in {last_swap}')

if __name__ == "__main__":
    main()
