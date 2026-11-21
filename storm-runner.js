/**
 * Veldra Storm Runner - Game Logic Module
 * Handles player physics, debris/shard spawning, collision, scoring, game state.
 */
import { audioManager } from './audio.js';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let player = {
  x: 400,
  y: 420,
  w: 30,
  h: 30,
  speed: 6,
  dx: 0
};

let debris = [];
let shards = [];
let score = 0;
let shardCount = 0;
let health = 100;
let gameOver = false;
let lastShardCollectTime = 0;
let difficultyLevel = 1;
let spawnRateMultiplier = 1;

let keys = {};
window.addEventListener('keydown', e => keys[e.key] = true);
window.addEventListener('keyup', e => keys[e.key] = false);

// Initialize audio on first user interaction
let audioInitialized = false;
function initAudio() {
  if (!audioInitialized) {
    audioManager.init();
    audioManager.resume();
    audioManager.startEngineHum();
    audioInitialized = true;
  }
}

// Attach audio init to any key press
window.addEventListener('keydown', initAudio, { once: true });
window.addEventListener('click', initAudio, { once: true });
window.addEventListener('touchstart', initAudio, { once: true });

function spawnObjects() {
  const debrisSpawnChance = 0.04 * spawnRateMultiplier;
  const shardSpawnChance = 0.02 * spawnRateMultiplier;

  if (Math.random() < debrisSpawnChance) {
    debris.push({
      x: Math.random() * (canvas.width - 30),
      y: -30,
      w: 25 + Math.random() * 25,
      h: 25 + Math.random() * 25,
      speed: 3 + Math.random() * 4 * spawnRateMultiplier
    });
  }
  if (Math.random() < shardSpawnChance) {
    shards.push({
      x: Math.random() * (canvas.width - 20),
      y: -20,
      size: 15,
      speed: 2 + Math.random() * 2 * spawnRateMultiplier
    });
  }
}

function updateDifficulty() {
  // Increase difficulty every 1000 points
  const newLevel = Math.floor(score / 1000) + 1;
  if (newLevel > difficultyLevel) {
    difficultyLevel = newLevel;
    spawnRateMultiplier = 1 + (difficultyLevel - 1) * 0.3;
    player.speed = Math.min(6 + difficultyLevel * 0.5, 12);
    audioManager.playWaveComplete();
  }
}

function update() {
  if (gameOver) return;

  // Player input
  if (keys['ArrowLeft'] || keys['a'] || keys['A']) player.x -= player.speed;
  if (keys['ArrowRight'] || keys['d'] || keys['D']) player.x += player.speed;

  // Engine pitch based on horizontal speed
  const speedRatio = Math.abs(player.dx) / player.speed;
  audioManager.setEnginePitch(speedRatio);

  // Bounds
  if (player.x < 0) player.x = 0;
  if (player.x + player.w > canvas.width) player.x = canvas.width - player.w;

  // Debris update & collision
  for (let i = debris.length - 1; i >= 0; i--) {
    let d = debris[i];
    d.y += d.speed;

    // Simple AABB collision
    if (player.x < d.x + d.w && player.x + player.w > d.x &&
        player.y < d.y + d.h && player.y + player.h > d.y) {
      health -= 15;
      debris.splice(i, 1);
      audioManager.playPlayerHit();
      if (health <= 0) {
        health = 0;
        gameOver = true;
        audioManager.playGameOver();
        audioManager.stopEngineHum();
      }
    } else if (d.y > canvas.height) {
      debris.splice(i, 1);
      score += 10;
      audioManager.playScore(10);
    }
  }

  // Shards update & collection
  for (let i = shards.length - 1; i >= 0; i--) {
    let s = shards[i];
    s.y += s.speed;

    // Circle/Box approx collision
    if (player.x < s.x + s.size && player.x + player.w > s.x - s.size &&
        player.y < s.y + s.size && player.y + player.h > s.y - s.size) {
      shardCount += 1;
      score += 50;
      audioManager.playScore(50);
      shards.splice(i, 1);
      lastShardCollectTime = Date.now();
    } else if (s.y > canvas.height) {
      shards.splice(i, 1);
    }
  }

  score += 1;
  if (score % 50 === 0) {
    audioManager.playScore(1);
  }

  spawnObjects();
  updateDifficulty();

  document.getElementById('scoreVal').innerText = score;
  document.getElementById('shardsVal').innerText = shardCount;
  document.getElementById('healthVal').innerText = health;
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player probe
  ctx.fillStyle = '#58a6ff';
  ctx.fillRect(player.x, player.y, player.w, player.h);

  // Draw debris
  ctx.fillStyle = '#f85149';
  for (let d of debris) {
    ctx.fillRect(d.x, d.y, d.w, d.h);
  }

  // Draw shards
  ctx.fillStyle = '#3fb950';
  for (let s of shards) {
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
    ctx.fill();
  }

  if (gameOver) {
    ctx.fillStyle = 'rgba(22, 27, 34, 0.85)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#f85149';
    ctx.font = '32px monospace';
    ctx.fillText('CRITICAL METRIC FAILURE', canvas.width / 2 - 200, canvas.height / 2 - 20);
    ctx.fillStyle = '#c9d1d9';
    ctx.font = '18px monospace';
    ctx.fillText('Final Score: ' + score, canvas.width / 2 - 70, canvas.height / 2 + 20);
    ctx.fillText('Press R to restart', canvas.width / 2 - 80, canvas.height / 2 + 50);
  }
}

// Restart handler
window.addEventListener('keydown', e => {
  if (e.key === 'r' || e.key === 'R') {
    if (gameOver) {
      resetGame();
    }
  }
});

function resetGame() {
  player.x = 400;
  player.y = 420;
  player.speed = 6;
  debris = [];
  shards = [];
  score = 0;
  shardCount = 0;
  health = 100;
  gameOver = false;
  difficultyLevel = 1;
  spawnRateMultiplier = 1;
  audioManager.startEngineHum();
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();

export { resetGame };