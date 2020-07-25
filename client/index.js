const serverUrl = "http://127.0.0.1:8000"; // Placeholder
const initialHeight = window.innerHeight;
const initialWidth = window.innerWidth;

let sessionId;
let hasResized = false;
let startTime;

// Wait until DOM has fully loaded before attempting to apply event listeners to it
document.addEventListener("DOMContentLoaded", async function (event) {
  sessionId = await getSessionId();
  addEventListenersToDOM();
});

function addEventListenersToDOM() {
  document
    .getElementsByClassName("form-details")[0]
    .addEventListener("submit", function () {
      postTimerData(event, Math.floor((Date.now() - startTime) / 1000));
    });

  let resizeTimeout;

  window.addEventListener("resize", function () {
    clearTimeout(resizeTimeout);
    // Assuming only one resize occurs
    if (hasResized === false) {
      // Add 300ms idle buffer to help ensure data is sent when resize is actually complete
      resizeTimeout = setTimeout(function () {
        postResizeData(window.innerHeight, window.innerWidth);
      }, 300);
    }
  });

  const inputFields = document.getElementsByClassName("form-control");

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

// POST REQUESTS

function postResizeData(finalHeight, finalWidth) {
  hasResized = true;
  let jsonRequest = {
    eventType: "resize",
    websiteUrl: window.location.href,
    sessionId: sessionId,
    initialDimensions: { height: initialHeight, width: initialWidth },
    finalDimensions: { height: finalHeight, width: finalWidth },
  };
  axios.post(`${serverUrl}/event`, jsonRequest).catch((error) => {
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
  axios.post(`${serverUrl}/event`, jsonRequest).catch((error) => {
    console.log(error);
  });
}

async function postTimerData(event, totalTime) {
  event.preventDefault();
  let jsonRequest = {
    eventType: "timeTaken",
    websiteUrl: window.location.href,
    sessionId: sessionId,
    time: totalTime,
  };
  // Ensure data is sent before reloading the page
  await axios.post(`${serverUrl}/event`, jsonRequest).catch((error) => {
    console.log(error);
  });
  location.reload(true);
}

// GET REQUESTS

function getSessionId() {
  return axios
    .get(`${serverUrl}/session`)
    .then((response) => response.data["session_id"])
    .catch((error) => {
      console.log(error);
    });
}
