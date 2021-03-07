from datetime import date

import falcon

from doctor_appointment_demo.core import DR_CHRONO_HOST


class DoctorCollection:

    doctors_url: str = f'{DR_CHRONO_HOST}/api/doctors'

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        response = req.context.session.get(self.doctors_url, params={
            'since': date.today().isoformat()
        })

        resp.media = response.json()
