import os
import sys

# Add parent dir to path so backend module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.clinic_state import ClinicState

def test_state():
    state = ClinicState()
    # search slots
    slots = state.search_slots("dr_rao", "2026-10-01")
    print("Available slots for Dr. Rao on 2026-10-01:", slots)
    
    # lookup patient
    patients = state.lookup_patient("Sharma")
    print("Patients matching 'Sharma':", [p['name'] for p in patients])
    
if __name__ == "__main__":
    test_state()
