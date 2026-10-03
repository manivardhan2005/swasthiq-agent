import unittest
import threading
import json
import os
from backend.clinic_state import ClinicState
from backend.agent import run_agent
from unittest.mock import patch, MagicMock
from google.genai import types

class TestToolLayer(unittest.TestCase):
    def setUp(self):
        self.state = ClinicState()
        
    def test_mutation_invariant(self):
        """Test that booking an unrevealed slot fails (anti-hallucination)."""
        # User tries to book 09:00 without searching first
        with self.assertRaises(ValueError) as context:
            self.state.book_appointment(
                caller_id="pt_0001",
                patient_id="pt_0001", 
                doctor_id="dr_rao", 
                date_str="2026-10-01", 
                start="11:15"
            )
        self.assertTrue("not returned by search_slots" in str(context.exception))
        
        # Now search first
        slots = self.state.search_slots("dr_rao", "2026-10-01")
        self.assertIn("11:15", slots)
        
        # Booking should now succeed
        appt = self.state.book_appointment(
            caller_id="pt_0001",
            patient_id="pt_0001", 
            doctor_id="dr_rao", 
            date_str="2026-10-01", 
            start="11:15"
        )
        self.assertEqual(appt["status"], "booked")

    def test_authorization(self):
        """Test authorization logic."""
        # Caller = patient (allowed)
        self.assertTrue(self.state._is_authorized("pt_0001", "pt_0001"))
        
        # Caller = unrelated person (not allowed)
        self.assertFalse(self.state._is_authorized("pt_0001", "pt_0002"))
        
        # Caller = guardian (allowed)
        # pt_0008 (Sunita Gupta) is guardian of pt_0006 and pt_0007
        self.assertTrue(self.state._is_authorized("pt_0008", "pt_0006"))
        
        # Target is guardian but caller is dependent (not allowed typically)
        self.assertFalse(self.state._is_authorized("pt_0006", "pt_0008"))

    def test_concurrency(self):
        """Test that concurrent bookings for the same slot result in exactly one success."""
        # We need a shared state for this test to simulate threads accessing the same ClinicState instance
        shared_state = ClinicState()
        
        # Reveal the slot first
        shared_state.search_slots("dr_rao", "2026-10-06")
        
        results = []
        def book_thread(caller, target):
            try:
                res = shared_state.book_appointment(
                    caller_id=caller,
                    patient_id=target,
                    doctor_id="dr_rao",
                    date_str="2026-10-06",
                    start="10:00"
                )
                results.append("success")
            except ValueError as e:
                results.append("failure")
                
        t1 = threading.Thread(target=book_thread, args=("pt_0001", "pt_0001"))
        t2 = threading.Thread(target=book_thread, args=("pt_0002", "pt_0002"))
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # Exactly one should succeed, one should fail
        self.assertEqual(results.count("success"), 1)
        self.assertEqual(results.count("failure"), 1)

if __name__ == "__main__":
    unittest.main()
