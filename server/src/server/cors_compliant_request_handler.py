import time
from http.server import SimpleHTTPRequestHandler
from json import dumps, loads
from random import randint
from threading import Lock
from typing import List

from src.data.data_struct import DataStruct
from src.data.dimension import Dimension
from src.exceptions.invalid_event_exception import InvalidEventException


class CORSCompliantRequestHandler(SimpleHTTPRequestHandler):
    data_structs = []
    session_ids = []
    lock = Lock()

    # Generate numeric session ID in the form XXXXXX-XXXXXX-XXXXXXXXX
    @staticmethod
    def _generate_session_id(session_ids):
        session_id = f"{randint(100000, 999999)}-{randint(100000, 999999)}-{randint(100000000, 999999999)}"
        # Ensure that we don't use the same session ID that someone else is using
        while session_id in session_ids:
            session_id = f"{randint(100000, 999999)}-{randint(100000, 999999)}-{randint(100000000, 999999999)}"
        return session_id

    # Find data_struct with matching session_id value
    @staticmethod
    def _find_data_struct(session_id, data_structs):
        session_data_struct = next(
            data_struct
            for data_struct in data_structs
            if data_struct.session_id == session_id
        )
        return session_data_struct

    # Update data structure based on eventType
    @staticmethod
    def _update_data_struct(session_data_struct, json_body):
        if json_body["eventType"] == "resize":
            session_data_struct.resize_from = Dimension(
                json_body["resizeFrom"]["width"], json_body["resizeFrom"]["height"],
            )
            session_data_struct.resize_to = Dimension(
                json_body["resizeTo"]["width"], json_body["resizeTo"]["height"],
            )
            return session_data_struct
        elif json_body["eventType"] == "copyAndPaste":
            session_data_struct.copy_and_paste[json_body["formId"]] = json_body[
                "pasted"
            ]
            return session_data_struct
        elif json_body["eventType"] == "timeTaken":
            session_data_struct.form_completion_time = json_body["time"]
            print("!!! DATA STRUCT COMPLETE !!!")
            return session_data_struct
        else:
            raise InvalidEventException("Unrecognised 'eventType' value")

    # Add headers to allow requests to occur between domains
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-type"
        )

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/session":
            # Setup headers for response
            self.send_response(200, "OK")
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Send session ID to client
            session_id = self._generate_session_id(self.session_ids)
            response = {}
            response["session_id"] = session_id
            self.wfile.write(bytes(dumps(response), "utf8"))
            print("!!! NEW SESSION GENERATED !!!")
            # Pull website URL from client address tuple provided by client's packet
            new_data_struct = DataStruct(
                self.client_address[0], response["session_id"], None, None, {}, None
            )

            # Ensure no two threads are using data_structs and session_ids
            self.lock.acquire()
            self.session_ids.append(session_id)
            self.data_structs.append(new_data_struct)
            self.lock.release()

            print(new_data_struct)

    def do_POST(self):
        if self.path == "/event":
            # Setup headers for response
            self.send_response(200, "OK")
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Get length of byte stream, decode it, and load it into JSON format
            dataLength = int(self.headers["Content-Length"])
            data = self.rfile.read(dataLength).decode("utf-8")
            json_body = loads(data)

            # Ensure no two threads are using data_structs
            self.lock.acquire()
            try:
                session_data_struct = self._find_data_struct(
                    json_body["sessionId"], self.data_structs
                )
                print(self._update_data_struct(session_data_struct, json_body))
                response = {}
                response["message"] = f"DataStruct {json_body['sessionId']} updated"
                self.wfile.write(bytes(dumps(response), "utf8"))
            except StopIteration:
                print(
                    f"ERROR - No DataStruct found with 'sessionId': {json_body['sessionId']}"
                )
            except InvalidEventException:
                print(f"ERROR - Invalid 'eventType' provided: {json_body['eventType']}")
            self.lock.release()
