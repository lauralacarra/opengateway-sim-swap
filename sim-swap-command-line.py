import os
import sys
from opengateway_sandbox_sdk import Simswap

def main() -> None:
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    phone_number = sys.argv[1]
    if CLIENT_ID is None:
        raise ValueError("CLIENT_ID environment variable is not set")
    if CLIENT_SECRET is None:
        raise ValueError("CLIENT_SECRET environment variable is not set")

    simswap_client = Simswap(CLIENT_ID, CLIENT_SECRET, phone_number)
    print(f'CIBA auth success')

    if simswap_client.check(max_age=2400):
        print('Simswap in the last 100 days')
    else:
        print('Not Simswap in the last 100 days')

    last_swap = simswap_client.retrieve_date()
    print(f'Last SIM Swap was in {last_swap}')

if __name__ == "__main__":
    main()
