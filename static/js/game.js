const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");
const bg = new Image();
bg.src = "/static/images/bg-pong.png"; 


// Game objects
const paddleWidth = 10, paddleHeight = 100, ballSize = 10;
let player = { x: 0, y: canvas.height / 2 - paddleHeight / 2, dy: 0, score: 0 };
let computer = { x: canvas.width - paddleWidth, y: canvas.height / 2 - paddleHeight / 2, score: 0 };
let ball = { x: canvas.width / 2, y: canvas.height / 2, dx: 4, dy: 4 };

let gameOver = false;
let gameStarted = false;

// Draw helpers
function drawRect(x, y, w, h, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

function drawCircle(x, y, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2, false);
  ctx.closePath();
  ctx.fill();
}

function drawText(text, x, y, size = 24, color = "#fff") {
  ctx.fillStyle = color;
  ctx.font = `${size}px Arial`;
  ctx.fillText(text, x, y);
}

// Controls
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowUp") player.dy = -6;
  else if (e.key === "ArrowDown") player.dy = 6;

  // Start the game or restart
  if (e.code === "Space") {
    if (!gameStarted) {
      gameStarted = true;
    } else if (gameOver) {
      player.score = 0;
      computer.score = 0;
      gameOver = false;
      gameStarted = false;
      resetBall();
    }
  }
});
document.addEventListener("keyup", () => (player.dy = 0));

function resetBall() {
  ball.x = canvas.width / 2;
  ball.y = canvas.height / 2;
  ball.dx = Math.random() > 0.5 ? 4 : -4;
  ball.dy = (Math.random() * 4 + 2) * (Math.random() > 0.5 ? 1 : -1);
}

function update() {
  if (!gameStarted || gameOver) return; // 👈 pause if not started or game over

  // Player movement
  player.y += player.dy;
  if (player.y < 0) player.y = 0;
  if (player.y + paddleHeight > canvas.height)
    player.y = canvas.height - paddleHeight;

  // Computer AI
  let target = ball.y - (computer.y + paddleHeight / 2);
  computer.y += target * 0.08;

  // Ball movement
  ball.x += ball.dx;
  ball.y += ball.dy;

  // Bounce off top/bottom
  if (ball.y < 0 || ball.y + ballSize > canvas.height) ball.dy *= -1;

  // Paddle collisions
  if (
    ball.x < player.x + paddleWidth &&
    ball.y > player.y &&
    ball.y < player.y + paddleHeight
  ) {
    ball.dx *= -1;
    ball.x = player.x + paddleWidth;
  }

  if (
    ball.x + ballSize > computer.x &&
    ball.y > computer.y &&
    ball.y < computer.y + paddleHeight
  ) {
    ball.dx *= -1;
    ball.x = computer.x - ballSize;
  }

  // Scoring
  if (ball.x < 0) {
    computer.score++;
    resetBall();
    gameStarted = false; // 👈 pause until space pressed again
  } else if (ball.x > canvas.width) {
    player.score++;
    resetBall();
    gameStarted = false;
  }

  // Check for win
  if (player.score >= 5 || computer.score >= 5) {
    gameOver = true;
  }
}

function render() {
  ctx.drawImage(bg, 0, 0, canvas.width, canvas.height);

  drawRect(player.x, player.y, paddleWidth, paddleHeight, "#6f42c1");
  drawRect(computer.x, computer.y, paddleWidth, paddleHeight, "#6f42c1");
  drawCircle(ball.x, ball.y, ballSize, "#fff");

  // Center divider
  for (let i = 0; i < canvas.height; i += 20) {
    drawRect(canvas.width / 2 - 1, i, 2, 10, "#444");
  }

  // Scores
  drawText(player.score, canvas.width / 4, 50);
  drawText(computer.score, (3 * canvas.width) / 4, 50);

  // Start screen
  if (!gameStarted && !gameOver) {
    drawText("Press Space to Start", canvas.width / 2 - 140, canvas.height / 2, 24, "#ccc");
  }

  // Game over screen
  if (gameOver) {
    const winner = player.score >= 5 ? "NO HACKING ALLOWED! REEEEEEEEE!!!" : "Skill issue.";
    drawText(winner, canvas.width / 2 - 100, canvas.height / 2 - 20, 36, "#f8f9fa");
    drawText("Press Space to Restart", canvas.width / 2 - 150, canvas.height / 2 + 30, 20, "#ccc");
  }
}

function gameLoop() {
  update();
  render();
}

setInterval(gameLoop, 1000 / 1200);
