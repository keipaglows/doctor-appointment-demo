from collections import defaultdict
from typing import Dict, List

from requests import Session

from doctor_appointment_demo.core import DR_CHRONO_HOST
from doctor_appointment_demo.libs.errors import AppointmentException


class AppointmentService:

    appointments_url: str = f'{DR_CHRONO_HOST}/api/appointments'
    patients_url: str = f'{DR_CHRONO_HOST}/api/patients'

    def make_and_get_an_appoinment(self, params: dict, session: Session):
        date = params['date'].isoformat()
        time = params['time'].isoformat()

        appointments = self._get_office_appointments(params, session)
        exam_room_id = self._get_exam_room_id(time, appointments)
        patient_id = self._get_patient_id(params, session)

        appointment_response = session.post(self.appointments_url, data={
            'doctor': params['doctor_id'],
            'office': params['office_id'],
            'exam_room': exam_room_id,
            'patient': patient_id,
            'scheduled_time': f'{date}T{time}',
            'duration': 30  # in minutes
        })

        if appointment_response:
            return appointment_response.json()

        raise AppointmentException('No open appointments found for these parameters')


    def _get_office_appointments(self, params: dict, session: Session) -> List[dict]:
        office_appointments_response = session.get(self.appointments_url, params={
            'doctor': params['doctor_id'],
            'office': params['office_id'],
            'date': params['date'].isoformat()
        })

        if office_appointments_response:
            return office_appointments_response.json()['results']

        raise AppointmentException('Could not receive appointments')

    def _get_exam_room_id(self, schedule_time: str, appointments: List[dict]) -> int:
        exam_room_time_map = self._make_exam_room_time_map(appointments)

        # trying to get an exam room which doesn't have a requested time
        for exam_room, scheduled_times in exam_room_time_map.items():
            if schedule_time not in scheduled_times:
                return exam_room

        raise AppointmentException('No open appointments found for these parameters')

    def _get_patient_id(self, params: dict, session: Session) -> int:
        patients_response = session.get(
            self.patients_url,
            params={'email': params['patient']['email']}
        )

        if patients_response:
            # trying to return existing patient_id
            if patients := patients_response.json()['results']:
                return patients[0]['id']

            # if we can't, then we're trying to create a new one and return it
            patient_response = session.post(
                self.patients_url,
                data={'doctor': params['doctor_id'], **params['patient']}
            )

            if patient_response:
                return patient_response.json()['id']

        raise AppointmentException('Could not receive patient info')

    @staticmethod
    def _make_exam_room_time_map(appointments: List[dict]) -> Dict[int, List[str]]:
        exam_room_time_map = defaultdict(dict)

        for appointment in appointments:
            exam_room = appointment['exam_room']
            scheduled_time = appointment['scheduled_time'].split('T')[1]

            if not exam_room_time_map[exam_room]:
                exam_room_time_map[exam_room] = []

            exam_room_time_map[exam_room].append(scheduled_time)

        return exam_room_time_map


appointment_service = AppointmentService()
