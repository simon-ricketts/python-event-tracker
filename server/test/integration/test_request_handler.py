import json
import threading
import time
import unittest
from http.server import HTTPServer

import requests

from src.constants.constants import ADDR, PORT


class TestRequestHandler(unittest.TestCase):
    def test_get_session_route_provides_ok_response_and_regex_compliant_session_id(
        self,
    ) -> None:
        response = requests.get(f"http://{ADDR}:{PORT}/session")
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.json()["session_id"], r"^\d{6}-\d{6}-\d{9}$")

    def test_post_event_route_provides_ok_response_and_updates_struct(self) -> None:
        response = requests.post(
            f"http://{ADDR}:{PORT}/event",
            json={
                "eventType": "copyAndPaste",
                "sessionId": "TEST_SESSION_ID",
                "pasted": True,
                "formId": "inputEmail",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "DataStruct TEST_SESSION_ID updated"
        )


if __name__ == "__main__":
    unittest.main()
