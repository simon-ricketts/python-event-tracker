# Ravelin Code Test

## Setup

A Python installation of 3.7 is required.

The [Client Server](###Client-Server) relies on the [Web Server](###Web-Server) to be running so that it can fetch a `session_id` from it, ensure that this is the case

### Web Server

```
python server/main.py
```

The server uses the constants `ADDR` and `PORT` to determine its web address, their default values will host the web server at http://127.0.0.1:8000

### Client Server

```
cd client
python -m http.server 8080
```

http://127.0.0.1:8080 will now be hosting [index.html](client/index.html)

## Summary

We need an HTTP server that will accept any POST request (JSON) from multiple clients' websites. Each request forms part of a struct (for that particular visitor) that will be printed to the terminal when the struct is fully complete.

For the JS part of the test please feel free to use any libraries that may help you **but please only use the Go standard library for the backend**. Remember to keep things simple.

## Frontend (JS)

Insert JavaScript into the index.html (supplied) that captures and posts data every time one of the below events happens; this means you will be posting multiple times per visitor. Assume only one resize occurs.

- if the screen resizes, the before and after dimensions
- copy & paste (for each field)
- time taken from the 1st character typed to clicking the submit button

### Example JSON Requests

```javascript
{
  "eventType": "copyAndPaste",
  "websiteUrl": "https://ravelin.com",
  "sessionId": "123123-123123-123123123",
  "pasted": true,
  "formId": "inputCardNumber"
}

{
  "eventType": "timeTaken",
  "websiteUrl": "https://ravelin.com",
  "sessionId": "123123-123123-123123123",
  "time": 72, // seconds
}

...

```

## Backend (Go)

The Backend should:

1. Create a Server
2. Accept POST requests in JSON format similar to those specified above
3. Map the JSON requests to relevant sections of the data struct (specified below)
4. Print the struct for each stage of its construction
5. Also print the struct when it is complete (i.e. when the form submit button has been clicked)

We would like the server to be written to handle multiple requests arriving on
the same session at the same time. We'd also like to see some tests.

### Go Struct

```go
type Data struct {
	WebsiteUrl         string
	SessionId          string
	ResizeFrom         Dimension
	ResizeTo           Dimension
	CopyAndPaste       map[string]bool // map[fieldId]true
	FormCompletionTime int // Seconds
}

type Dimension struct {
	Width  string
	Height string
}
```
