
from datetime import date, time

import falcon
from marshmallow import fields, validate, Schema

from doctor_appointment_demo.core import DR_CHRONO_HOST
from doctor_appointment_demo.libs.errors import AppointmentException
from doctor_appointment_demo.libs.utils import get_and_validate_schema
from doctor_appointment_demo.services import appointment_service


GENDERS = ['Male', 'Female', 'Other']


class PatientSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(GENDERS))


class AppointmentPostSchema(Schema):

    doctor_id = fields.Integer(required=True, validate=validate.Range(min=0))
    office_id = fields.Integer(required=True, validate=validate.Range(min=0))
    date = fields.Date(missing=date.today())
    time = fields.Time(missing=time(9))
    patient = fields.Nested(PatientSchema, required=True)


class AppointmentCollection:

    appointments_url: str = f'{DR_CHRONO_HOST}/api/appointments'

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        params = get_and_validate_schema(AppointmentPostSchema, req)

        try:
            resp.media = appointment_service.make_and_get_an_appoinment(
                params, req.context.session
            )
        except AppointmentException as exc:
            raise falcon.HTTPUnprocessableEntity(exc.args[0]) from exc
