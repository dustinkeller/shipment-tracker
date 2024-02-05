import sys
import requests
import time
from os import environ


api_key = environ.get('API_KEY')

if api_key:
    trackingUrl = 'https://parcelsapp.com/api/v3/shipments/tracking'
    try:
        tracking_num = sys.argv[1]
    except IndexError as err:
        print("Enter your tracking number in the command line...")
        raise err
    
    shipment = {'trackingId': tracking_num, 'language': 'en', 'country': 'United States'}
    response = requests.post(trackingUrl, json={'apiKey': api_key, 'shipments': shipment})


    if response.status_code == 200:
        # Get UUID from response
        uuid = response.json()['uuid']
        # Function to check tracking status with UUID
        def check_tracking_status():
            response = requests.get(trackingUrl, params={'apiKey': api_key, 'uuid': uuid})
            if response.status_code == 200:
                if response.json()['done']:
                    print('Tracking complete')
                else:
                    print('Tracking in progress...')
                    time.sleep(10) # sleep for N sec
                    check_tracking_status()
            else:
                print(response.text)
        check_tracking_status()
    else:
        print(response.text)
else:
    print("No API Key found...")