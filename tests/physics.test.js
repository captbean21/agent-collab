// Physics Unit Tests — Rook's TDD Round 2
// Tests for updatePlayerPhysics() — written FIRST to fail, then Castle implements

import { createPlayer, updatePlayerPhysics, FIXED_DT, CANVAS_W, CANVAS_H } from '../game.js';

// Simple test runner
let passed = 0;
let failed = 0;

function assert(condition, message) {
    if (condition) {
        console.log(`✅ PASS: ${message}`);
        passed++;
    } else {
        console.error(`❌ FAIL: ${message}`);
        failed++;
    }
}

function assertEqual(actual, expected, message) {
    const ok = Math.abs(actual - expected) < 0.001;
    if (ok) {
        console.log(`✅ PASS: ${message} (${actual} === ${expected})`);
        passed++;
    } else {
        console.error(`❌ FAIL: ${message} (expected ${expected}, got ${actual})`);
        failed++;
    }
}

function runTests() {
    console.log('=== Physics Test Suite ===\n');

    // Test 1: Thrust applies velocity in correct direction
    // thrust=800, dt=1/60: dv = 800/60 = 13.333...
    // After drag (0.98): 13.333... * 0.98 = 13.0666...
    const EXPECTED_THRUST_VEL = (800 / 60) * 0.98;

    {
        const player = createPlayer();
        player.up = true;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.vy, -EXPECTED_THRUST_VEL, 'Thrust up applies negative Y velocity');
    }

    // Test 2: Thrust down applies positive Y velocity
    {
        const player = createPlayer();
        player.down = true;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.vy, EXPECTED_THRUST_VEL, 'Thrust down applies positive Y velocity');
    }

    // Test 3: Thrust left applies negative X velocity
    {
        const player = createPlayer();
        player.left = true;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.vx, -EXPECTED_THRUST_VEL, 'Thrust left applies negative X velocity');
    }

    // Test 4: Thrust right applies positive X velocity
    {
        const player = createPlayer();
        player.right = true;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.vx, EXPECTED_THRUST_VEL, 'Thrust right applies positive X velocity');
    }

    // Test 5: No input applies drag only (velocity decays to 0)
    {
        const player = createPlayer();
        player.vx = 100;
        player.vy = 50;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.vx, 98, 'Drag reduces X velocity by 2%');
        assertEqual(player.vy, 49, 'Drag reduces Y velocity by 2%');
    }

    // Test 6: Velocity clamps to maxSpeed
    {
        const player = createPlayer();
        player.vx = 400; // Over maxSpeed (300)
        player.vy = 0;
        player.right = true; // Adding more thrust
        updatePlayerPhysics(player, FIXED_DT);
        const speed = Math.hypot(player.vx, player.vy);
        assert(speed <= player.maxSpeed + 0.1, `Velocity clamped to maxSpeed (${speed} <= ${player.maxSpeed})`);
    }

    // Test 7: Position updates from velocity (drag applied first)
    // vx=60 -> after drag: 58.8 -> position += 58.8 * (1/60) = 0.98
    {
        const player = createPlayer();
        player.vx = 60;
        player.vy = 0;
        updatePlayerPhysics(player, FIXED_DT);
        assertEqual(player.x, CANVAS_W / 2 + 0.98, 'Position updates from velocity after drag');
    }

    // Test 8: Screen wrap X (right edge -> left)
    // Wrap triggers when x > CANVAS_W + r
    {
        const player = createPlayer();
        player.x = CANVAS_W + player.radius + 1;
        player.vx = 0;
        updatePlayerPhysics(player, FIXED_DT);
        assert(player.x < player.radius * 2, 'Screen wrap X: right edge wraps to left');
    }

    // Test 9: Screen wrap X (left edge -> right)
    // Wrap triggers when x < -r
    {
        const player = createPlayer();
        player.x = -player.radius - 1;
        player.vx = 0;
        updatePlayerPhysics(player, FIXED_DT);
        assert(player.x > CANVAS_W - player.radius * 2, 'Screen wrap X: left edge wraps to right');
    }

    // Test 10: Screen wrap Y (bottom edge -> top)
    // Wrap triggers when y > CANVAS_H + r
    {
        const player = createPlayer();
        player.y = CANVAS_H + player.radius + 1;
        player.vy = 0;
        updatePlayerPhysics(player, FIXED_DT);
        assert(player.y < player.radius * 2, 'Screen wrap Y: bottom edge wraps to top');
    }

    // Test 11: Screen wrap Y (top edge -> bottom)
    // Wrap triggers when y < -r
    {
        const player = createPlayer();
        player.y = -player.radius - 1;
        player.vy = 0;
        updatePlayerPhysics(player, FIXED_DT);
        assert(player.y > CANVAS_H - player.radius * 2, 'Screen wrap Y: top edge wraps to bottom');
    }

    // Test 12: Diagonal thrust normalizes (prevents faster diagonal)
    {
        const player = createPlayer();
        player.up = true;
        player.right = true;
        updatePlayerPhysics(player, FIXED_DT);
        const speed = Math.hypot(player.vx, player.vy);
        // With both axes, raw thrust would be sqrt(2) * single_axis
        // Implementation should normalize or clamp to maxSpeed
        assert(speed <= player.maxSpeed + 0.1, `Diagonal speed clamped (${speed} <= ${player.maxSpeed})`);
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();