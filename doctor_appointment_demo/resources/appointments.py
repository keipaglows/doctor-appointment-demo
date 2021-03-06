
from collections import defaultdict
from datetime import date, time
from typing import List

import falcon
from marshmallow import fields, validate, Schema

from doctor_appointment_demo.core import DR_CHRONO_HOST
from doctor_appointment_demo.libs.utils import get_and_validate_schema


patient_id = 92829633


class AppointmentPostSchema(Schema):

    doctor_id = fields.Integer(required=True, validate=validate.Range(min=0))
    office_id = fields.Integer(required=True, validate=validate.Range(min=0))
    date = fields.Date(missing=date.today())
    time = fields.Time(missing=time(9))


class AppointmentCollection:

    appointments_url: str = f'{DR_CHRONO_HOST}/api/appointments'

    def on_post(self, req, resp):
        params = get_and_validate_schema(AppointmentPostSchema, req)
        office_appointments_response = req.context.session.get(self.appointments_url, params={
            'doctor': params['doctor_id'],
            'office': params['office_id'],
            'date': params['date'].isoformat()
        })

        if office_appointments_response:
            appointments = office_appointments_response.json()['results']
            exam_room_time_map = self._make_exam_room_time_map(appointments)
            date = params['date'].isoformat()
            time = params['time'].isoformat()

            for _exam_room, scheduled_times in exam_room_time_map.items():
                if time not in scheduled_times:
                    exam_room = _exam_room
                    break

            if exam_room:
                response = req.context.session.post(self.appointments_url, data={
                    'doctor': params['doctor_id'],
                    'office': params['office_id'],
                    'exam_room': exam_room,
                    'patient': patient_id,
                    'scheduled_time': f'{date}T{time}',
                    'duration': 30  # in minutes
                })
                resp.media = response.json()

                return

        raise falcon.HTTPUnprocessableEntity('No open appointments found for these parameters')

    @staticmethod
    def _make_exam_room_time_map(appointments: List[dict]):
        exam_room_time_map = defaultdict(dict)

        for appointment in appointments:
            exam_room = appointment['exam_room']
            scheduled_time = appointment['scheduled_time'].split('T')[1]

            if not exam_room_time_map[exam_room]:
                exam_room_time_map[exam_room] = []

            exam_room_time_map[exam_room].append(scheduled_time)

        return exam_room_time_map
