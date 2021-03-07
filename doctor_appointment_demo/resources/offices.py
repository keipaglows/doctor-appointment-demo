import falcon
from marshmallow import fields, validate, Schema

from doctor_appointment_demo.core import DR_CHRONO_HOST
from doctor_appointment_demo.libs.utils import get_and_validate_schema


class OfficesGetSchema(Schema):

    doctor_id = fields.Integer(required=True, validate=validate.Range(min=0))


class OfficeCollection:

    offices_url: str = f'{DR_CHRONO_HOST}/api/offices'

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        params = get_and_validate_schema(OfficesGetSchema, req)

        response = req.context.session.get(self.offices_url, params={
            'doctor': params['doctor_id']
        })

        resp.media = response.json()
