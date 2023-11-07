import requests
import json
import logging

def login(key, key_id, url, duration=43200):
    # global s
    s = requests.Session()

    payload = {
        "key": key,
        "key_id": key_id,
        "duration": duration,
    }

    try:
        response = s.post("{}/v2/auth/login".format(url), json=payload)
        response.raise_for_status()
        if response.status_code == 200:
            logging.info('logged in successfully')
            s.headers['X-Auth-Token'] = response.json().get('token')
        return s
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.TooManyRedirects as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
