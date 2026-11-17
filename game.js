// Retro Arcade Game — Castle & Rook Collaboration
// Scaffold: Castle (gameplay/controls), Rook (audio/mechanics)
// Role split per PROJECT_IDEAS.md

const CANVAS_W = 640;
const CANVAS_H = 480;
const FIXED_DT = 1 / 60; // 60 Hz fixed timestep

// ---------- Types / Interfaces (Round 1: Castle defines, Rook tests) ----------

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
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.beginPath();
    // Simple triangle ship
    ctx.moveTo(0, -player.radius * 1.5);
    ctx.lineTo(player.radius, player.radius);
    ctx.lineTo(-player.radius, player.radius);
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
}

// ---------- Browser-specific Input Handling (only runs in browser) ----------

let browserInputState = {
    left: false,
    right: false,
    up: false,
    down: false,
};

function setupInput(player) {
    if (typeof window === 'undefined') return; // Skip in Node.js tests

    window.addEventListener('keydown', (e) => {
        switch (e.code) {
            case 'ArrowLeft': case 'KeyA': browserInputState.left = true; break;
            case 'ArrowRight': case 'KeyD': browserInputState.right = true; break;
            case 'ArrowUp': case 'KeyW': browserInputState.up = true; break;
            case 'ArrowDown': case 'KeyS': browserInputState.down = true; break;
        }
    });

    window.addEventListener('keyup', (e) => {
        switch (e.code) {
            case 'ArrowLeft': case 'KeyA': browserInputState.left = false; break;
            case 'ArrowRight': case 'KeyD': browserInputState.right = false; break;
            case 'ArrowUp': case 'KeyW': browserInputState.up = false; break;
            case 'ArrowDown': case 'KeyS': browserInputState.down = false; break;
        }
    });
}

function getInputState() {
    return { ...browserInputState };
}

function setInputState(state) {
    browserInputState = { ...state };
}

// ---------- Game State & Loop (for browser) ----------

function createGameState() {
    return {
        player: createPlayer(),
        score: 0,
        lives: 3,
        wave: 1,
        lastTime: 0,
        accumulator: 0,
    };
}

function gameStep(state, timestamp) {
    const frameTime = (timestamp - state.lastTime) / 1000;
    state.lastTime = timestamp;

    const clampedFrameTime = Math.min(frameTime, 0.1);
    state.accumulator += clampedFrameTime;

    // Sync input to player
    state.player.left = browserInputState.left;
    state.player.right = browserInputState.right;
    state.player.up = browserInputState.up;
    state.player.down = browserInputState.down;

    while (state.accumulator >= FIXED_DT) {
        updatePlayerPhysics(state.player, FIXED_DT);
        state.accumulator -= FIXED_DT;
    }

    return state;
}

function renderGame(ctx, state) {
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

    renderPlayer(ctx, state.player);
}

function initGame() {
    if (typeof window === 'undefined') return null; // Skip in Node.js tests

    const state = createGameState();
    setupInput(state.player);

    function loop(timestamp) {
        gameStep(state, timestamp);
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        renderGame(ctx, state);

        // Update HUD
        document.getElementById('score').textContent = state.score;
        document.getElementById('lives').textContent = state.lives;
        document.getElementById('wave').textContent = state.wave;

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
};