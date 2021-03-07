from collections import defaultdict
from typing import Dict, List

from requests import Session

from doctor_appointment_demo.core import DR_CHRONO_HOST
from doctor_appointment_demo.libs.errors import AppointmentException


class AppointmentService:

    appointments_url: str = f'{DR_CHRONO_HOST}/api/appointments'
    patients_url: str = f'{DR_CHRONO_HOST}/api/patients'
    offices_url: str = f'{DR_CHRONO_HOST}/api/offices'

    def make_and_get_an_appoinment(self, params: dict, session: Session):
        date = params['scheduled_datetime'].date().isoformat()
        time = params['scheduled_datetime'].time().isoformat()

        appointments = self._get_office_appointments(params, session)
        office = self._get_office(params['office_id'], session)
        free_exam_room_id = self._get_free_exam_room_id(time, office['exam_rooms'], appointments)
        patient_id = self._get_patient_id(params, session)

        appointment_response = session.post(self.appointments_url, data={
            'doctor': params['doctor_id'],
            'office': params['office_id'],
            'exam_room': free_exam_room_id,
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
            'date': params['scheduled_datetime'].date().isoformat()
        })

        if office_appointments_response:
            return office_appointments_response.json()['results']

        raise AppointmentException('Could not receive appointments')

    def _get_office(self, office_id: int, session: Session) -> dict:
        office_response = session.get(f'{self.offices_url}/{office_id}')

        if office_response:
            return office_response.json()

        raise AppointmentException('Could not receive office info')

    # pylint: disable=inconsistent-return-statements
    def _get_free_exam_room_id(self,
                               schedule_time: str,
                               exam_rooms: List[dict],
                               appointments: List[dict]) -> int:
        exam_rooms_schedule = self._make_exam_rooms_schedule(appointments)

        for exam_room in exam_rooms:
            exam_room_id = exam_room['index']

            if room_schedule := exam_rooms_schedule.get(exam_room_id):
                # checking if requested time is open for this room
                if schedule_time not in room_schedule:
                    return exam_room_id
            else:
                # if there were no schedule for this room, return it's id
                return exam_room_id

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
    def _make_exam_rooms_schedule(appointments: List[dict]) -> Dict[int, List[str]]:
        exam_rooms_schedule = defaultdict(dict)

        for appointment in appointments:
            exam_room = appointment['exam_room']
            scheduled_time = appointment['scheduled_time'].split('T')[1]

            if not exam_rooms_schedule[exam_room]:
                exam_rooms_schedule[exam_room] = []

            exam_rooms_schedule[exam_room].append(scheduled_time)

        return exam_rooms_schedule


appointment_service = AppointmentService()
