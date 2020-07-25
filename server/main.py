import json
from http.server import HTTPServer
from socketserver import ThreadingMixIn

from cors_compliant_request_handler import CORSCompliantRequestHandler

ADDR = "127.0.0.1"
PORT = 8000


# Create a ThreadedHTTPServer by inheriting ThreadingMixIn and HTTPServer
# Inherit ThreadingMixIn first to override related methods in HTTPServer
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':
    httpd = ThreadedHTTPServer((ADDR, PORT), CORSCompliantRequestHandler)
    print(f"Hosting server at {ADDR}:{PORT}")
    httpd.serve_forever()
