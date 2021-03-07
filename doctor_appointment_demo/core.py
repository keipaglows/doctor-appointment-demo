# pylint: disable=line-too-long
import os


ENV_NAME = os.environ.get('ENV_NAME', 'dev')

OAUTH2_REDIRECT_URI = os.environ.get('OAUTH2_REDIRECT_URI', 'http://127.0.0.1:8010/api/oauth2-authorize')

DR_CHRONO_HOST = os.environ.get('DR_CHRONO_HOST', 'https://app.drchrono.com')
DR_CHRONO_CLIENT_ID = os.environ.get('DR_CHRONO_CLIENT_ID', 'h14jXtM9jGrK1r4rJCG398sNGpQY9kYo5MB9Bc6T')
DR_CHRONO_CLIENT_SECRET = os.environ.get('DR_CHRONO_CLIENT_SECRET', 'UEtJ9sLPcEiAlZUwqPKDKO14dRB4lpW1qa3PKunaOEYzlArpSBJIZXvsnQFDPMAADpYD7iwLfXJ6Uaagplk0jBBpopulMWEZSFVKoPWa2AjvaVAOhmi8AOeX55Hi7geH')

DR_CHRONO_OAUTH2_AUTH_URL = f'{DR_CHRONO_HOST}/o/authorize/?redirect_uri={OAUTH2_REDIRECT_URI}&response_type=code&client_id={DR_CHRONO_CLIENT_ID}'
