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
  }

  function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 5;
    ctx.lineCap = "round";

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }

  function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const fileInput = document.getElementById("file");
    const label = document.querySelector("label[for=file]");
    fileInput.value = "";
    label.innerText = "Browse Files";
  }

  canvas.addEventListener("mousedown", startPosition);
  canvas.addEventListener("mouseup", finishedPosition);
  canvas.addEventListener("mousemove", draw);

  window.clearCanvas = clearCanvas;
});

function drawImageOnCanvas(input) {
  const canvas = document.getElementById("drawingCanvas");
  const ctx = canvas.getContext("2d");
  const dataURL = canvas.toDataURL();
  if (dataURL !== "data:,") {
    const confirmation = confirm(
      "Are you sure you want to replace the canvas? This will clear the current drawing."
    );
    if (!confirmation) {
      return;
    }
  }
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const reader = new FileReader();
    const fileName = file.name;
    const label = document.querySelector("label[for=file]");
    label.innerText = fileName ?? "Browse Files";

    reader.onload = function (e) {
      const img = new Image();

      img.onload = function () {
        const canvas = document.getElementById("drawingCanvas");
        const ctx = canvas.getContext("2d");
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
  const dataURL = canvas.toDataURL();
  console.log(dataURL); /* Send to server

  const sendButton = document.getElementById("send-drawing");
  sendButton.innerHTML = "Send to server...";
  sendButton.disabled = true; */
}
