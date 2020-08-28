# Python Event Tracker

A Python HTTPServer primed to receive tracking/logging events from an example client's webpage alongside other requests such as:

* Session ID Requests
* Resize events
* Paste events
* Form submission
* Time taken to submit form

Session IDs are requested by the client and granted by the server on page load in order to ensure events can be attributed to unique users and therefore properly tracked.

## Setup

A Python installation of 3.7 is required.

The client relies on the [Web Server](#web-server) to be running first so that it can fetch a `session_id` from it, ensure that this is the case

A [makefile](/makefile) has been provided with all the necessary commands needed to run the code, though explanations are provided below for manual operation

### Web Server

```
cd server
python3 main.py
```

The server uses the constants `ADDR` and `PORT` in [constant.py](server/src/constants.py) to determine its web address, their default values will host the web server at http://127.0.0.1:8000

## Testing

### Unit Tests

```
cd server
python3 -m unittest discover -v test/unit
```

### Integration Tests

Integration tests rely on a test version of the server with dummy data to be running first.

In a separate terminal run the following commands to open a server in test mode:

```
cd server
python3 main.py -t
```

Following this, in your original terminal run:

```
cd server
python3 -m unittest discover -v test/integration
```
