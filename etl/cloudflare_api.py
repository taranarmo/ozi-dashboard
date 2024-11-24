import requests

API_URL = 'https://api.cloudflare.com/client/v4/radar/netflows/timeseries'

def get_cloudflare_traffic_for_country(country_iso2, api_token, copy_to_file=False):
    params = {
        "name": "main",
        "location": country_iso2,
        "dateRange": "52w"
    }
    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print("An error occurred during cloudflare API call:", e)

    return data