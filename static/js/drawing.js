let hasDrawn = false;
document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("drawingCanvas");
  const ctx = canvas.getContext("2d");
  let painting = false;
  
  function startPosition(e) {
    painting = true;
    draw(e);
  }

  function finishedPosition() {
    painting = false;
    ctx.beginPath();
    if (!hasDrawn) hasDrawn = true;  // Update hasDrawn when the user has drawn
  }

  function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 30;
    ctx.lineCap = "round";
    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }

  function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    hasDrawn = false;  // Reset hasDrawn when canvas is cleared
    const fileInput = document.getElementById("file");
    const label = document.querySelector("label[for=file]");
    fileInput.value = "";
    label.innerText = "Browse Files";

    // Rensa prediktionsnotisen
    const predictionMessage = document.getElementById("prediction-message");
    predictionMessage.innerHTML = '';
  }

  canvas.addEventListener("mousedown", startPosition);
  canvas.addEventListener("mouseup", finishedPosition);
  canvas.addEventListener("mousemove", draw);

  window.clearCanvas = clearCanvas;

  const label = document.querySelector("label[for=file]");
  label.addEventListener("click", function(event) {
    if (hasDrawn && !confirm("Are you sure you want to replace the canvas? This will clear the current drawing.")) {
      event.preventDefault();  // Prevent the file dialog from continuing
      label.value = "";    // Reset the file input
    } else {
      loadImage(event.target);
    }
  });
});

function loadImage(input) {
  const canvas = document.getElementById("drawingCanvas");
  const ctx = canvas.getContext("2d");
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const reader = new FileReader();
    const label = document.querySelector("label[for=file]");
    label.innerHTML = "Uploaded file: <strong class='whitebg'>" + file.name + "</strong>" ?? "Browse Files";

    reader.onload = function (e) {
      const img = new Image();

      img.onload = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };

      img.src = e.target.result;
    };

    reader.readAsDataURL(file);
  }
}

function sendDrawing() {
  const canvas = document.getElementById("drawingCanvas");
  const dataURL = canvas.toDataURL("image/png");
  
  const sendButton = document.getElementById("send-drawing");
  sendButton.innerHTML = "Sending...";
  sendButton.disabled = true;

  // AJAX request to send dataURL to the server
  fetch('/upload-drawing', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: dataURL })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    sendButton.innerHTML = "Check Letter";
    sendButton.disabled = false;

    // Get the RF and KNN predictions from the server response
    const prediction_RF = data.prediction_RF;
    const prediction_KNN_EMNIST = data.prediction_KNN_EMNIST;

    // Update the page with the predicted numbers
    const predictionMessage = document.getElementById("prediction-message");
    predictionMessage.innerHTML = `Predicted letter/number with RF: ${prediction_RF}<br>Predicted letter/number with KNN EMNIST: ${prediction_KNN_EMNIST}`;
  })
  .catch((error) => {
    console.error('Error:', error);
    sendButton.innerHTML = "Check Letter";
    sendButton.disabled = false;
  });
}