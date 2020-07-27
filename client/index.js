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
    /*
    Wasn't sure whether the exercise wanted both Copy AND Paste tracking; The example server-side Data
    template shows a map being used for CopyAndPaste with 1-to-1 mappings between a string (fieldId) and a bool which suggests
    only one event should be tracked? I have therefore assumed that we are tracking Paste events.
    */
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
    sessionId: sessionId,
    resizeFrom: { width: initialWidth, height: initialHeight },
    resizeTo: { width: finalWidth, height: finalHeight },
  };
  axios.post(`${serverUrl}/event`, jsonRequest).catch((error) => {
    console.log(error);
  });
}

function postPasteData(elementId) {
  let jsonRequest = {
    eventType: "copyAndPaste",
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
