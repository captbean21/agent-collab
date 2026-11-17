// Retro Arcade Game — Castle & Rook Collaboration
// Full gameplay loop: GameController + BulletManager + EnemyManager + AudioManager + Difficulty
// Role split: Castle (gameplay/controls), Rook (audio/mechanics)

const CANVAS_W = 800;
const CANVAS_H = 600;
const FIXED_DT = 1 / 60; // 60 Hz fixed timestep

// ---------- Imports ----------
import { GameController } from './gameController.js';
import { EnemyManager } from './enemy.js';
import { CollisionManager } from './collision.js';
import { BulletManager } from './bullet.js';
import { audioManager } from './audio.js';

// ---------- Player & Physics (kept for backward compat with tests) ----------

/**
 * Player entity interface
 * @property {number} x - World X position
 * @property {number} y - World Y position
 * @property {number} vx - Velocity X
 * @property {number} vy - Velocity Y
 * @property {number} radius - Collision radius
 * @property {number} maxSpeed - Maximum speed cap
 * @property {number} thrust - Acceleration per frame
 * @property {number} drag - Velocity decay factor (0-1)
 */
function createPlayer() {
    return {
        x: CANVAS_W / 2,
        y: CANVAS_H / 2,
        vx: 0,
        vy: 0,
        radius: 8,
        maxSpeed: 300,
        thrust: 800,
        drag: 0.98,
        speed: 0, // Computed speed for audio engine pitch
        // Input state
        left: false,
        right: false,
        up: false,
        down: false,
    };
}

/**
 * Updates player physics for one fixed timestep
 * @param {Object} player - Player entity from createPlayer()
 * @param {number} dt - Fixed timestep (seconds)
 * @returns {Object} Updated player (mutates and returns for chaining)
 */
function updatePlayerPhysics(player, dt) {
    // 1. Apply thrust based on input
    const ax = (player.right ? 1 : 0) - (player.left ? 1 : 0);
    const ay = (player.down ? 1 : 0) - (player.up ? 1 : 0);

    if (ax !== 0 || ay !== 0) {
        // Normalize diagonal input to prevent faster diagonal movement
        const len = Math.hypot(ax, ay);
        player.vx += (ax / len) * player.thrust * dt;
        player.vy += (ay / len) * player.thrust * dt;
    }

    // 2. Clamp velocity to maxSpeed
    const speed = Math.hypot(player.vx, player.vy);
    if (speed > player.maxSpeed) {
        const scale = player.maxSpeed / speed;
        player.vx *= scale;
        player.vy *= scale;
    }

    // 3. Apply drag
    player.vx *= player.drag;
    player.vy *= player.drag;

    // 4. Update position
    player.x += player.vx * dt;
    player.y += player.vy * dt;

    // 5. Handle screen wrap (toroidal world)
    const r = player.radius;
    if (player.x > CANVAS_W + r) player.x = -r;
    if (player.x < -r) player.x = CANVAS_W + r;
    if (player.y > CANVAS_H + r) player.y = -r;
    if (player.y < -r) player.y = CANVAS_H + r;

    // 6. Compute speed for audio
    player.speed = Math.hypot(player.vx, player.vy);

    return player;
}

/**
 * Renders player to canvas context
 * @param {CanvasRenderingContext2D} ctx
 * @param {Object} player
 */
function renderPlayer(ctx, player) {
    ctx.save();
    ctx.translate(player.x, player.y);
    const angle = Math.atan2(player.vy, player.vx);
    ctx.rotate(angle);
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.beginPath();
    // Triangle ship pointing right (0 radians)
    ctx.moveTo(player.radius * 1.5, 0);
    ctx.lineTo(-player.radius, -player.radius);
    ctx.lineTo(-player.radius, player.radius);
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
}

// ---------- Browser-specific Input Handling ----------

let browserInputState = {
    left: false,
    right: false,
    up: false,
    down: false,
    fire: false,
};

function setupInput(player) {
    if (typeof window === 'undefined') return; // Skip in Node.js tests

    window.addEventListener('keydown', (e) => {
        switch (e.code) {
            case 'ArrowLeft': case 'KeyA': browserInputState.left = true; break;
            case 'ArrowRight': case 'KeyD': browserInputState.right = true; break;
            case 'ArrowUp': case 'KeyW': browserInputState.up = true; break;
            case 'ArrowDown': case 'KeyS': browserInputState.down = true; break;
            case 'Space': case 'KeyK': browserInputState.fire = true; e.preventDefault(); break;
        }
    });

    window.addEventListener('keyup', (e) => {
        switch (e.code) {
            case 'ArrowLeft': case 'KeyA': browserInputState.left = false; break;
            case 'ArrowRight': case 'KeyD': browserInputState.right = false; break;
            case 'ArrowUp': case 'KeyW': browserInputState.up = false; break;
            case 'ArrowDown': case 'KeyS': browserInputState.down = false; break;
            case 'Space': case 'KeyK': browserInputState.fire = false; break;
        }
    });

    // Resume audio on first interaction
    window.addEventListener('click', async () => {
        await audioManager.resume();
    }, { once: true });
}

function getInputState() {
    return { ...browserInputState };
}

function setInputState(state) {
    browserInputState = { ...state };
}

// ---------- Rendering ----------

function renderBullet(ctx, bullet) {
    ctx.save();
    ctx.translate(bullet.x, bullet.y);
    ctx.fillStyle = '#ffff00';
    ctx.beginPath();
    ctx.arc(0, 0, bullet.radius || 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function renderEnemy(ctx, enemy) {
    ctx.save();
    ctx.translate(enemy.x, enemy.y);
    const colors = { basic: '#ff4444', fast: '#ff8800', tank: '#ff00ff' };
    ctx.strokeStyle = colors[enemy.type] || '#ff4444';
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (enemy.shape === 'circle') {
        ctx.arc(0, 0, enemy.radius, 0, Math.PI * 2);
    }
    ctx.stroke();
    // Health indicator for tank
    if (enemy.type === 'tank' && enemy.health < 5) {
        ctx.fillStyle = '#ff00ff';
        ctx.font = '10px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(enemy.health.toString(), 0, 3);
    }
    ctx.restore();
}

function renderExplosion(ctx, x, y, radius, color) {
    ctx.save();
    ctx.translate(x, y);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
}

function renderGame(ctx, gameController) {
    // Clear with slight trail effect
    ctx.fillStyle = 'rgba(13, 13, 13, 0.3)';
    ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

    // Grid background
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.05)';
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x <= CANVAS_W; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, CANVAS_H);
        ctx.stroke();
    }
    for (let y = 0; y <= CANVAS_H; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(CANVAS_W, y);
        ctx.stroke();
    }

    // Render enemies
    const enemies = gameController.enemyManager.getEnemies();
    for (const enemy of enemies) {
        renderEnemy(ctx, enemy);
    }

    // Render bullets
    const bullets = gameController.bulletManager.getBullets();
    for (const bullet of bullets) {
        renderBullet(ctx, bullet);
    }

    // Render player
    renderPlayer(ctx, gameController.player);

    // Render explosions (visual feedback for collisions)
    // This is a simplified version - in a full game you'd have a particle system
}

// ---------- Game Loop ----------

function createGameState() {
    const player = createPlayer();
    const enemyManager = new EnemyManager();
    const collisionManager = new CollisionManager();
    const bulletManager = new BulletManager();
    const gameController = new GameController(player, enemyManager, collisionManager, bulletManager);

    // Spawn initial wave
    enemyManager.spawnWave(4, 400, 300, 1);

    return {
        gameController,
        lastTime: 0,
        accumulator: 0,
    };
}

function gameStep(state, timestamp) {
    const frameTime = (timestamp - state.lastTime) / 1000;
    state.lastTime = timestamp;

    const clampedFrameTime = Math.min(frameTime, 0.1);
    state.accumulator += clampedFrameTime;

    const gc = state.gameController;

    // Sync input to player
    gc.player.left = browserInputState.left;
    gc.player.right = browserInputState.right;
    gc.player.up = browserInputState.up;
    gc.player.down = browserInputState.down;

    // Handle fire input
    if (browserInputState.fire) {
        gc.fire(performance.now());
    }

    // Fixed timestep loop
    while (state.accumulator >= FIXED_DT) {
        gc.update(FIXED_DT, performance.now());
        state.accumulator -= FIXED_DT;
    }

    return state;
}

function initGame() {
    if (typeof window === 'undefined') return null; // Skip in Node.js tests

    const state = createGameState();
    setupInput(state.gameController.player);

    // Initialize audio
    audioManager.init();

    function loop(timestamp) {
        gameStep(state, timestamp);
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        renderGame(ctx, state.gameController);

        // Update HUD
        const gcState = state.gameController.getState();
        document.getElementById('score').textContent = gcState.score;
        document.getElementById('lives').textContent = gcState.lives;
        document.getElementById('wave').textContent = gcState.wave;

        if (gcState.isGameOver) {
            // Game over - show message
            ctx.save();
            ctx.fillStyle = 'rgba(13, 13, 13, 0.9)';
            ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
            ctx.fillStyle = '#ff4444';
            ctx.font = '48px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('GAME OVER', CANVAS_W / 2, CANVAS_H / 2 - 20);
            ctx.font = '24px monospace';
            ctx.fillStyle = '#ffff00';
            ctx.fillText(`Final Score: ${gcState.score}`, CANVAS_W / 2, CANVAS_H / 2 + 30);
            ctx.font = '16px monospace';
            ctx.fillStyle = '#888888';
            ctx.fillText('Click to restart', CANVAS_W / 2, CANVAS_H / 2 + 70);
            ctx.restore();

            // Wait for click to restart
            canvas.onclick = () => {
                window.location.reload();
            };
            return;
        }

        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
    return state;
}

// Export for testing (Rook's test suite will import these)
export {
    createPlayer,
    updatePlayerPhysics,
    renderPlayer,
    FIXED_DT,
    CANVAS_W,
    CANVAS_H,
    createGameState,
    gameStep,
    renderGame,
    initGame,
    setupInput,
    getInputState,
    setInputState,
    // Re-export managers for test access
    EnemyManager,
    CollisionManager,
    BulletManager,
    GameController,
    audioManager,
};

export default {
    createPlayer,
    updatePlayerPhysics,
    FIXED_DT,
    CANVAS_W,
    CANVAS_H,
    createGameState,
    gameStep,
    renderGame,
    initGame,
    setupInput,
    getInputState,
    setInputState,
    EnemyManager,
    CollisionManager,
    BulletManager,
    GameController,
    audioManager,
};
// Auto-start the game in the browser (not during Node.js test imports)
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        initGame();
    });
    // If DOM already loaded (module defer), kick off now
    if (document.readyState !== 'loading') {
        initGame();
    }
}
