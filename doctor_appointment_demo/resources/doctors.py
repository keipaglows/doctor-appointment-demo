from datetime import date

from doctor_appointment_demo.core import DR_CHRONO_HOST


class DoctorCollection:

    doctors_url: str = f'{DR_CHRONO_HOST}/api/doctors'

    def on_get(self, req, resp):
        response = req.context.session.get(self.doctors_url, params={
            'since': date.today().isoformat()
        })

        resp.media = response.json()
