import requests


def check_api_key(api_key):
    url = 'https://api.stripe.com/v1/customers'  # You can choose any endpoint here
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return True
    except requests.exceptions.HTTPError:
        return False
