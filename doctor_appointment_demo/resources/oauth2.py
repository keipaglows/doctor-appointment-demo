import requests

from doctor_appointment_demo import core


class OAuth2AuthCallbackDocument:

    def on_get(self, req, resp):
        response = requests.post(f'{core.DR_CHRONO_HOST}/o/token/', data={
            'code': req.params['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': core.OAUTH2_REDIRECT_URI,
            'client_id': core.DR_CHRONO_CLIENT_ID,
            'client_secret': core.DR_CHRONO_CLIENT_SECRET
        })
        response.raise_for_status()
        response_json = response.json()

        req.context.session.set_headers(
            response_json['access_token'],
            response_json['refresh_token']
        )
