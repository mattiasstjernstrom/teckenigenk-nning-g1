document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('drawingCanvas');
  const ctx = canvas.getContext('2d');

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
      ctx.lineCap = 'round';

      ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }

  canvas.addEventListener('mousedown', startPosition);
  canvas.addEventListener('mouseup', finishedPosition);
  canvas.addEventListener('mousemove', draw);
});

function sendDrawing() {
  const canvas = document.getElementById('drawingCanvas');
  const dataURL = canvas.toDataURL();
  console.log(dataURL); // Send here, console log for now
}
