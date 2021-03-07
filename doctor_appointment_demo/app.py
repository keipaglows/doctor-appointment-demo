import webbrowser

import falcon

from doctor_appointment_demo import core, resources
from doctor_appointment_demo.middlewares.session import SessionMiddleware
from doctor_appointment_demo.middlewares.cors import CORSMiddleware


def get_app():
    api = falcon.API(middleware=[CORSMiddleware(), SessionMiddleware()])

    api.add_route('/api/appointments', resources.AppointmentCollection())
    api.add_route('/api/doctors', resources.DoctorCollection())
    api.add_route('/api/oauth2-authorize', resources.OAuth2AuthCallbackDocument())
    api.add_route('/api/offices', resources.OfficeCollection())
    api.add_error_handler(falcon.HTTPUnprocessableEntity, http_422_handler)

    # authorizing this app at drchrone ouath endpoint
    open_drchrono_auth_page()

    return api


def open_drchrono_auth_page():
    webbrowser.open(core.DR_CHRONO_OAUTH2_AUTH_URL)


def http_422_handler(_req: falcon.Request, resp: falcon.Response, ex: Exception, _params: dict):
    resp.status = ex.status
    errors = [ex.title] if isinstance(ex.title, list) else ex.title

    resp.media = {'errors': errors}
