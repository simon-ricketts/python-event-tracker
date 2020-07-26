from http.server import HTTPServer
from socketserver import ThreadingMixIn


# Create a ThreadedHTTPServer by inheriting ThreadingMixIn and HTTPServer
# Inherit ThreadingMixIn first to override related methods in HTTPServer
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
