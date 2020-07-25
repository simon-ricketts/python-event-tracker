from http.server import SimpleHTTPRequestHandler
from json import dumps, loads
from random import randint
from typing import List
from threading import Lock
import time
from data_struct import DataStruct
from dimension import Dimension


class CORSCompliantRequestHandler(SimpleHTTPRequestHandler):
    struct_dataset = []
    session_ids = []
    lock = Lock()

    # Generate numeric session ID in the form XXXXXX-XXXXXX-XXXXXXXXX
    def _generate_session_id(self):
        session_id = f"{randint(0, 999999)}-{randint(0, 999999)}-{randint(0, 999999999)}"
        # Ensure that we don't use the same session ID that someone else is using
        while(session_id in self.session_ids):
            session_id = f"{randint(0, 999999)}-{randint(0, 999999)}-{randint(0, 999999999)}"
        return session_id

    def _update_data_struct(self, session_struct_data, json_body):
        if json_body["eventType"] == "resize":
            session_struct_data.resize_from = Dimension(
                json_body["initialDimensions"]["width"], json_body["initialDimensions"]["height"])
            session_struct_data.resize_to = Dimension(
                json_body["finalDimensions"]["width"], json_body["finalDimensions"]["height"])
            print(session_struct_data)
        elif json_body["eventType"] == "copyAndPaste":
            session_struct_data.copy_and_paste[json_body["formId"]] = True
            print(session_struct_data)
        elif json_body["eventType"] == "timeTaken":
            session_struct_data.form_completion_time = json_body["time"]
            print(session_struct_data)
            print("!!! DATA_STRUCT COMPLETE !!!")
        else:
            print("Unrecognised 'eventType' value")

    # Add headers to allow requests to occur between domains
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers",
                         "X-Requested-With, Content-type")

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
            session_id = self._generate_session_id()
            response = {}
            response["session_id"] = session_id
            self.wfile.write(bytes(dumps(response), "utf8"))
            new_struct_dataset = DataStruct(
                self.client_address[0], response["session_id"], None, None, {}, None)

            # Ensure no two threads are using struct_dataset and session_ids
            self.lock.acquire()
            self.session_ids.append(session_id)
            self.struct_dataset.append(new_struct_dataset)
            self.lock.release()

            print(new_struct_dataset)

    def do_POST(self):
        if self.path == "/event":
            # Setup headers for response
            self.send_response(201, "CREATED")
            self._send_cors_headers()
            self.end_headers()

            # Get length of byte stream, decode it, and load it into JSON format
            dataLength = int(self.headers["Content-Length"])
            data = self.rfile.read(dataLength).decode('utf-8')
            json_body = loads(data)
            try:
                # Ensure no two threads are using struct_dataset
                self.lock.acquire()
                session_data_struct = next(
                    data_struct for data_struct in self.struct_dataset if data_struct.session_id == json_body["sessionId"])
                self._update_data_struct(session_data_struct, json_body)
                self.lock.release()
            except StopIteration:
                print(
                    f"ERROR - No DataStruct found with session_id: {json_body['sessionId']}")
