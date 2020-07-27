import unittest
import unittest.mock
from io import StringIO

from src.data.data_struct import DataStruct
from src.data.dimension import Dimension
from src.exceptions.invalid_event_exception import InvalidEventException
from src.server.cors_compliant_request_handler import CORSCompliantRequestHandler


class TestRequestHandler(unittest.TestCase):
    def test_generate_session_id_matches_regex(self):
        # Check that generated session ID matches regex for XXXXXX-XXXXXX-XXXXXXXXX
        session_id = CORSCompliantRequestHandler._generate_session_id([])
        self.assertRegex(session_id, r"^\d{6}-\d{6}-\d{9}$")

    def test_find_data_struct_returns_data_struct(self):
        # Check that data_struct can be found
        data_structs = [DataStruct(None, "SESSION ID", None, None, {}, None)]
        expected_session_data_struct = DataStruct(
            None, "SESSION ID", None, None, {}, None
        )
        self.assertEqual(
            CORSCompliantRequestHandler._find_data_struct("SESSION ID", data_structs),
            expected_session_data_struct,
        )

    def test_find_data_struct_raises_stop_iteration(self):
        # Check that method throws StopIteration exception on failure to find
        self.assertRaises(
            StopIteration,
            CORSCompliantRequestHandler._find_data_struct,
            "NO SUCH SESSION ID",
            [],
        )

    def test_update_data_struct_for_resize_event(self):
        # Check resize eventType updates correct fields
        session_data_struct = DataStruct(None, None, None, None, {}, None)
        json_body = {
            "eventType": "resize",
            "sessionId": None,
            "resizeFrom": {"width": "1920", "height": "1080"},
            "resizeTo": {"width": "1280", "height": "720"},
        }
        expected_updated_session_data_struct = DataStruct(
            None, None, Dimension("1920", "1080"), Dimension("1280", "720"), {}, None,
        )
        actual_updated_session_data_struct = CORSCompliantRequestHandler._update_data_struct(
            session_data_struct, json_body
        )
        self.assertEqual(
            expected_updated_session_data_struct, actual_updated_session_data_struct
        )

    def test_update_data_struct_for_paste_event(self):
        # Check copyAndPaste eventType updates correct fields
        session_data_struct = DataStruct(None, None, None, None, {}, None)
        json_body = {
            "eventType": "copyAndPaste",
            "sessionId": None,
            "pasted": True,
            "formId": "inputEmail",
        }
        expected_updated_session_data_struct = DataStruct(
            None, None, None, None, {"inputEmail": True}, None,
        )
        actual_updated_session_data_struct = CORSCompliantRequestHandler._update_data_struct(
            session_data_struct, json_body
        )
        self.assertEqual(
            expected_updated_session_data_struct, actual_updated_session_data_struct
        )

    # Create a mock to capture print output, passing it in as the argument 'mock_stdout'
    @unittest.mock.patch("sys.stdout", new_callable=StringIO)
    def test_update_data_struct_for_time_taken_event(self, mock_stdout):
        # Check timeTaken eventType updates correct fields and prints complete message
        session_data_struct = DataStruct(None, None, None, None, {}, None)
        json_body = {
            "eventType": "timeTaken",
            "sessionId": None,
            "time": 10,
        }
        expected_updated_session_data_struct = DataStruct(
            None, None, None, None, {}, 10,
        )
        actual_updated_session_data_struct = CORSCompliantRequestHandler._update_data_struct(
            session_data_struct, json_body
        )
        self.assertEqual(
            expected_updated_session_data_struct, actual_updated_session_data_struct
        )
        self.assertEqual(mock_stdout.getvalue(), "!!! DATA STRUCT COMPLETE !!!\n")

    def test_update_data_struct_raises_for_invalid_event(self):
        # Check that method throws InvalidEventException on incorrect eventType
        session_data_struct = DataStruct(None, None, None, None, {}, None)
        json_body = {
            "eventType": "notAnEvent",
            "sessionId": None,
        }
        self.assertRaises(
            InvalidEventException,
            CORSCompliantRequestHandler._update_data_struct,
            session_data_struct,
            json_body,
        )


if __name__ == "__main__":
    unittest.main()
