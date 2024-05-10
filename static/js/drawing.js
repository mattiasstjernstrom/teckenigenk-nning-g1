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
    fileInput.value = "";
  }

  canvas.addEventListener("mousedown", startPosition);
  canvas.addEventListener("mouseup", finishedPosition);
  canvas.addEventListener("mousemove", draw);

  window.clearCanvas = clearCanvas;
});

function sendDrawing() {
  const canvas = document.getElementById("drawingCanvas");
  const dataURL = canvas.toDataURL();
  console.log(dataURL); // Send to server
}

function drawImageOnCanvas(input) {
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const reader = new FileReader();

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
