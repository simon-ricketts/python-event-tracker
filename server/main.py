import argparse
import json

from src.constants import ADDR, PORT
from src.cors_compliant_request_handler import CORSCompliantRequestHandler
from src.data_struct import DataStruct
from src.threaded_http_server import ThreadedHTTPServer

# Set up an argument parser to allow a 'test' mode to be used when running main.py
parser = argparse.ArgumentParser(
    description="Run a threaded HTTPServer with custom request handler"
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="Runs the server in test mode for use in integration tests",
)
args = parser.parse_args()
# If in test mode, add a dummy data struct to be used to verify POST routes
if args.test:
    CORSCompliantRequestHandler.data_structs.append(
        DataStruct(None, "TEST_SESSION_ID", None, None, {}, None)
    )
    print(f"Hosting test server at {ADDR}:{PORT}")
else:
    print(f"Hosting server at {ADDR}:{PORT}")

# Host the server
httpd = ThreadedHTTPServer((ADDR, PORT), CORSCompliantRequestHandler)
httpd.serve_forever()
