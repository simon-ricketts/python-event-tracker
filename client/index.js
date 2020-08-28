const serverUrl = "http://127.0.0.1:8000"; // Placeholder
const sessionId = generateSessionId();
const initialHeight = window.innerWidth;
const initialWidth = window.innerHeight;

let hasResized = false;
let startTime;

// Wait until DOM has fully loaded before attempting to apply event listeners to it
document.addEventListener("DOMContentLoaded", function (event) {
  const inputFields = document.getElementsByClassName("form-control");
  addEventListenersToInputFields(inputFields);
});

function addEventListenersToInputFields(inputFields) {
  document
    .getElementsByClassName("form-details")[0]
    .addEventListener("submit", postTimerData);

  let resizeTimeout;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimeout);
    // Assuming only one resize occurs
    if (hasResized === false) {
      resizeTimeout = setTimeout(postResizeData, 300);
    }
  });

  for (i = 0; i < inputFields.length; i++) {
    let inputFieldId = inputFields[i].id;
    inputFields[i].addEventListener("input", startTimer);
    inputFields[i].addEventListener("paste", function () {
      postPasteData(inputFieldId);
    });
  }

  function startTimer() {
    startTime = Date.now();
    for (i = 0; i < inputFields.length; i++) {
      inputFields[i].removeEventListener("input", startTimer);
    }
  }
}

// Generate numeric session IDs in the form XXXXXX-XXXXXX-XXXXXXXXX

function generateSessionId() {
  return `${Math.floor(100000 + Math.random() * 900000)}-${Math.floor(
    100000 + Math.random() * 900000
  )}-${Math.floor(100000000 + Math.random() * 900000000)}`;
}

// POST REQUESTS

function postResizeData() {
  hasResized = true;
  let jsonRequest = {
    eventType: "resize",
    websiteUrl: window.location.href,
    sessionId: sessionId,
    initialDimensions: { height: initialHeight, width: initialWidth },
    finalDimensions: { height: window.innerHeight, width: innerWidth },
  };
  console.log(jsonRequest);
  axios.post(serverUrl, jsonRequest).then((error) => {
    console.log(error);
  });
}

function postPasteData(elementId) {
  let jsonRequest = {
    eventType: "copyAndPaste",
    websiteUrl: window.location.href,
    sessionId: sessionId,
    pasted: true,
    formId: elementId,
  };
  console.log(jsonRequest);
  axios.post(serverUrl, jsonRequest).then((error) => {
    console.log(error);
  });
}

function postTimerData(event) {
  event.preventDefault();
  let jsonRequest = {
    eventType: "timeTaken",
    websiteUrl: window.location.href,
    sessionId: sessionId,
    time: Math.floor((Date.now() - startTime) / 1000),
  };
  console.log(jsonRequest);
  axios
    .post(serverUrl, jsonRequest)
    .then((response) => location.reload)
    .catch((error) => {
      console.log(error);
    });
}
