import json
import os
from datetime import datetime, timedelta

CLINIC_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clinic.json')

class ClinicState:
    def __init__(self):
        with open(CLINIC_FILE, 'r') as f:
            self.data = json.load(f)
        
        # Track what has been revealed to the agent to prevent hallucinations
        self.revealed_slots = set()
        self.revealed_patients = set()
        self.revealed_appointments = set()

    def get_patient_by_id(self, patient_id: str):
        for p in self.data['patients']:
            if p['id'] == patient_id:
                return p
        return None

    def get_doctor_by_id(self, doctor_id: str):
        for d in self.data['doctors']:
            if d['id'] == doctor_id:
                return d
        return None

    def get_appointment_by_id(self, appt_id: str):
        for a in self.data['appointments']:
            if a['id'] == appt_id:
                return a
        return None

    def is_holiday(self, date_str: str) -> bool:
        return date_str in self.data.get('holidays', [])

    def _is_authorized(self, caller_id: str, target_patient_id: str) -> bool:
        if caller_id == target_patient_id:
            return True
        caller = self.get_patient_by_id(caller_id)
        if not caller:
            return False
        if target_patient_id in caller.get('guardian_of', []):
            return True
        return False

    def search_slots(self, doctor_id: str, date_str: str):
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            raise ValueError(f"Doctor {doctor_id} not found")

        if self.is_holiday(date_str) or date_str in doctor.get('leave_dates', []):
            return []

        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format, expected YYYY-MM-DD")

        day_of_week = dt.strftime('%a')
        slot_minutes = self.data['clinic']['slot_minutes']
        available_slots = []
        
        for window in doctor.get('windows', []):
            if window['day'] == day_of_week:
                start_time = datetime.strptime(f"{date_str} {window['start']}", '%Y-%m-%d %H:%M')
                end_time = datetime.strptime(f"{date_str} {window['end']}", '%Y-%m-%d %H:%M')
                
                current = start_time
                while current + timedelta(minutes=slot_minutes) <= end_time:
                    slot_start_str = current.strftime('%H:%M')
                    
                    # Race condition / double book check:
                    is_booked = any(
                        appt['doctor_id'] == doctor_id and 
                        appt['date'] == date_str and 
                        appt['start'] == slot_start_str and 
                        appt['status'] == 'booked'
                        for appt in self.data['appointments']
                    )
                    
                    if not is_booked:
                        available_slots.append(slot_start_str)
                        self.revealed_slots.add((doctor_id, date_str, slot_start_str))
                    
                    current += timedelta(minutes=slot_minutes)

        return available_slots

    def book_appointment(self, caller_id: str, patient_id: str, doctor_id: str, date_str: str, start: str):
        if not self._is_authorized(caller_id, patient_id):
            raise ValueError(f"Caller {caller_id} is not authorized to act for patient {patient_id}. Must escalate with 'not_authorised'.")
            
        if (doctor_id, date_str, start) not in self.revealed_slots:
            raise ValueError("Cannot book a slot that was not returned by search_slots (Hallucination check).")
            
        if not self.get_patient_by_id(patient_id):
            raise ValueError("Patient not found")
        if not self.get_doctor_by_id(doctor_id):
            raise ValueError("Doctor not found")
            
        # Re-check availability (race condition prevention at tool layer)
        is_booked = any(
            appt['doctor_id'] == doctor_id and 
            appt['date'] == date_str and 
            appt['start'] == start and 
            appt['status'] == 'booked'
            for appt in self.data['appointments']
        )
        if is_booked:
            raise ValueError("Double booking detected. Slot is already taken.")
            
        slot_minutes = self.data['clinic']['slot_minutes']
        start_time = datetime.strptime(start, '%H:%M')
        end_time = start_time + timedelta(minutes=slot_minutes)
        
        max_id = 0
        for appt in self.data['appointments']:
            try:
                num = int(appt['id'].split('_')[1])
                if num > max_id:
                    max_id = num
            except:
                pass
        
        new_id = f"ap_{max_id + 1:04d}"
        new_appt = {
            "id": new_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": date_str,
            "start": start,
            "end": end_time.strftime('%H:%M'),
            "status": "booked"
        }
        self.data['appointments'].append(new_appt)
        self.revealed_appointments.add(new_id)
        
        # Remove from revealed slots so it can't be booked again
        self.revealed_slots.remove((doctor_id, date_str, start))
        return new_appt

    def cancel_appointment(self, caller_id: str, appointment_id: str):
        appt = self.get_appointment_by_id(appointment_id)
        if not appt:
            raise ValueError("Appointment not found")
        if not self._is_authorized(caller_id, appt['patient_id']):
            raise ValueError(f"Caller {caller_id} is not authorized to cancel this appointment. Must escalate with 'not_authorised'.")
        if appt['status'] == 'cancelled':
            raise ValueError("Appointment is already cancelled")
            
        appt['status'] = 'cancelled'
        return appt
        
    def reschedule_appointment(self, caller_id: str, appointment_id: str, new_date: str, new_start: str):
        appt = self.get_appointment_by_id(appointment_id)
        if not appt:
            raise ValueError("Appointment not found")
        if not self._is_authorized(caller_id, appt['patient_id']):
            raise ValueError(f"Caller {caller_id} is not authorized to reschedule this appointment. Must escalate with 'not_authorised'.")
        if appt['status'] == 'cancelled':
            raise ValueError("Cannot reschedule a cancelled appointment")
            
        if (appt['doctor_id'], new_date, new_start) not in self.revealed_slots:
            raise ValueError("Cannot book a slot that was not returned by search_slots (Hallucination check).")

        # Double book check
        is_booked = any(
            a['doctor_id'] == appt['doctor_id'] and 
            a['date'] == new_date and 
            a['start'] == new_start and 
            a['status'] == 'booked'
            for a in self.data['appointments'] if a['id'] != appointment_id
        )
        if is_booked:
            raise ValueError("Double booking detected. Slot is already taken.")
            
        slot_minutes = self.data['clinic']['slot_minutes']
        start_time = datetime.strptime(new_start, '%H:%M')
        
        appt['date'] = new_date
        appt['start'] = new_start
        appt['end'] = (start_time + timedelta(minutes=slot_minutes)).strftime('%H:%M')
        
        self.revealed_slots.remove((appt['doctor_id'], new_date, new_start))
        return appt

    def lookup_patient(self, search_term: str):
        search_term = search_term.lower()
        results = []
        for p in self.data['patients']:
            if search_term in p['name'].lower() or search_term in p['phone'] or search_term in p['id'].lower():
                results.append(p)
                self.revealed_patients.add(p['id'])
        return results
