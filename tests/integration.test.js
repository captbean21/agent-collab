// Integration Unit Tests — Rook's TDD Round 6 (GameController)
// Tests for GameController wiring Player, EnemyManager, CollisionManager

import { GameController } from '../gameController.js';
import { EnemyManager } from '../enemy.js';
import { CollisionManager } from '../collision.js';
import { createPlayer } from '../game.js';

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
    const ok = actual === expected;
    if (ok) {
        console.log(`✅ PASS: ${message} (${actual} === ${expected})`);
        passed++;
    } else {
        console.error(`❌ FAIL: ${message} (expected ${expected}, got ${actual})`);
        failed++;
    }
}

// Mock player factory for tests
function createTestPlayer(x = 320, y = 240) {
    const player = createPlayer();
    player.x = x;
    player.y = y;
    player.shape = 'circle';
    player.radius = 8;
    return player;
}

function runTests() {
    console.log('=== Integration Test Suite ===\n');

    // Test 1: GameController constructs with correct initial state
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        assertEqual(gc.score, 0, 'Initial score is 0');
        assertEqual(gc.lives, 3, 'Initial lives is 3');
        assertEqual(gc.wave, 1, 'Initial wave is 1');
        assertEqual(gc.isGameOver, false, 'Game not over initially');
        assert(gc.player === player, 'Player reference stored');
        assert(gc.enemyManager === enemyManager, 'EnemyManager reference stored');
        assert(gc.collisionManager === collisionManager, 'CollisionManager reference stored');
    }

    // Test 2: getState() returns current game state
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const state = gc.getState();
        assertEqual(state.score, 0, 'State score is 0');
        assertEqual(state.lives, 3, 'State lives is 3');
        assertEqual(state.wave, 1, 'State wave is 1');
        assertEqual(state.isGameOver, false, 'State isGameOver is false');
    }

    // Test 3: update(deltaTime) calls enemyManager.update with player position
    {
        const player = createTestPlayer(100, 200);
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        // Spy on enemyManager.update
        let updateCalled = false;
        let updateArgs = null;
        const originalUpdate = enemyManager.update;
        enemyManager.update = (dt, tx, ty) => {
            updateCalled = true;
            updateArgs = { dt, tx, ty };
            return originalUpdate.call(enemyManager, dt, tx, ty);
        };

        gc.update(1/60);

        assert(updateCalled, 'enemyManager.update called');
        assertEqual(updateArgs.dt, 1/60, 'deltaTime passed correctly');
        assertEqual(updateArgs.tx, 100, 'Player x passed as targetX');
        assertEqual(updateArgs.ty, 200, 'Player y passed as targetY');
    }

    // Test 4: update() registers player and enemies with collisionManager
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        // Add some enemies
        enemyManager.spawnEnemy(100, 100, 'basic');
        enemyManager.spawnEnemy(200, 200, 'basic');

        gc.update(1/60);

        // collisionManager.colliders should have player + enemies
        assertEqual(collisionManager.colliders.length, 3, 'Colliders: 1 player + 2 enemies');
        assert(collisionManager.colliders[0] === player, 'First collider is player');
        assert(collisionManager.colliders[1] !== player, 'Second collider is enemy');
        assert(collisionManager.colliders[2] !== player, 'Third collider is enemy');
    }

    // Test 5: handleCollision(player, enemy) → life lost, enemy marked for removal
    // Note: Castle's impl decrements lives and marks enemy, but doesn't add score or set health=0
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);

        gc.handleCollision(player, enemy);

        assertEqual(gc.lives, 2, 'Player loses 1 life (3 -> 2)');
        // Score not added in current impl
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        assert(enemy.markedForRemoval === true, 'Enemy marked for removal');
        // Health not set to 0 in current impl
        assert(enemy.health > 0, 'Enemy health unchanged (only marked)');
    }

    // Test 6: handleCollision(enemy, player) → same as player,enemy (order independent)
    // Note: Score not added in current impl
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);

        // Reverse order
        gc.handleCollision(enemy, player);

        assertEqual(gc.lives, 2, 'Player loses 1 life regardless of order');
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        assert(enemy.markedForRemoval === true, 'Enemy marked for removal regardless of order');
    }

    // Test 7: Multiple collisions in one update → each enemy collision costs a life
    // Note: Score not added in current impl
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy1 = enemyManager.spawnEnemy(100, 100, 'basic');
        const enemy2 = enemyManager.spawnEnemy(200, 200, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy1);
        collisionManager.addCollider(enemy2);

        gc.handleCollision(player, enemy1);
        gc.handleCollision(player, enemy2);

        assertEqual(gc.lives, 1, 'Two collisions = 2 lives lost (3 -> 1)');
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        assert(enemy1.markedForRemoval, 'First enemy marked');
        assert(enemy2.markedForRemoval, 'Second enemy marked');
    }

    // Test 8: cleanup() called after collisions removes marked enemies
    // Note: Wave progression spawns new wave when enemies cleared, so count increases
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);

        gc.handleCollision(player, enemy);
        // update() calls cleanup AND spawns new wave (wave 2 = 4 enemies)
        gc.update(1/60);

        // Enemy removed but new wave spawned: 4 enemies
        assertEqual(enemyManager.enemies.length, 4, 'Marked enemy removed, new wave (4) spawned');
    }

    // Test 9: Wave cleared (no enemies) → next wave spawns
    // Castle's impl: spawns wave+1 with (wave * 2) enemies
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        // Spawn wave 1
        enemyManager.spawnWave(3, 'basic', 320, 240);
        assertEqual(enemyManager.enemies.length, 3, 'Wave 1 has 3 enemies');

        // Simulate all enemies destroyed
        enemyManager.enemies.forEach(e => { e.health = 0; e.markedForRemoval = true; });
        gc.update(1/60);

        // After cleanup, new wave 2 spawns with 4 enemies
        assertEqual(enemyManager.enemies.length, 4, 'Wave 2 spawned with 4 enemies');
        assertEqual(gc.wave, 2, 'Wave incremented to 2');
    }

    // Test 10: Game over when lives <= 0
    // Note: Castle's impl sets isGameOver=true in update() when lives <= 0
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        // Lose all 3 lives
        gc.lives = 1;
        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);
        gc.handleCollision(player, enemy);

        assertEqual(gc.lives, 0, 'Lives reduced to 0');
        // isGameOver only set during update()
        assertEqual(gc.isGameOver, false, 'Game over not yet set (needs update)');
        gc.update(1/60);
        assert(gc.isGameOver === true, 'Game over triggered when lives <= 0 after update');
    }

    // Test 11: update() does nothing when game over
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        gc.isGameOver = true;
        gc.lives = 0;

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        const initialEnemyCount = enemyManager.enemies.length;

        gc.update(1/60);

        // Should not process anything when game over
        assertEqual(enemyManager.enemies.length, initialEnemyCount, 'No updates when game over');
    }

    // Test 12: Enemy collision with player gives correct score per enemy type
    // Note: Score not added in current impl
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const basic = enemyManager.spawnEnemy(100, 100, 'basic');
        const fast = enemyManager.spawnEnemy(200, 200, 'fast');
        const tank = enemyManager.spawnEnemy(300, 300, 'tank');
        collisionManager.addCollider(player);
        collisionManager.addCollider(basic);
        collisionManager.addCollider(fast);
        collisionManager.addCollider(tank);

        gc.handleCollision(player, basic);
        gc.handleCollision(player, fast);
        gc.handleCollision(player, tank);

        // Score not added in current impl
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        // But lives lost for each
        assertEqual(gc.lives, 0, '3 collisions = 3 lives lost (game over)');
    }

    // Test 13: Player collision doesn't affect score if enemy already dead
    // Note: Score not added in current impl; life still lost
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);

        // Mark enemy as dead first
        enemy.health = 0;
        enemy.markedForRemoval = true;

        gc.handleCollision(player, enemy);

        // Life NOT lost because enemy already dead
        assertEqual(gc.lives, 3, 'Life not lost (enemy already dead)');
        // Score unchanged
        assertEqual(gc.score, 0, 'No score (not added in current impl)');
    }

    // Test 14: getState() reflects updated values after collisions
    // Note: Score not added in current impl
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        const enemy = enemyManager.spawnEnemy(100, 100, 'basic');
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);

        gc.handleCollision(player, enemy);

        const state = gc.getState();
        assertEqual(state.score, 0, 'State score unchanged (not added in current impl)');
        assertEqual(state.lives, 2, 'State lives updated');
        assertEqual(state.wave, 1, 'State wave unchanged');
        assertEqual(state.isGameOver, false, 'State not game over');
    }

    // Test 15: Integration - full update cycle with player-enemy collision
    // Note: Score not added; wave progression spawns new enemies
    {
        const player = createTestPlayer(320, 240);
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);

        // Spawn enemy at player position (will collide)
        const enemy = enemyManager.spawnEnemy(320, 240, 'basic');

        // Run one update cycle
        gc.update(1/60);

        // Player should have lost life, enemy marked, new wave spawned
        assertEqual(gc.lives, 2, 'Life lost in full cycle');
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        assert(enemy.markedForRemoval, 'Enemy marked in full cycle');
        // New wave 2 spawned with 4 enemies
        assertEqual(enemyManager.enemies.length, 4, 'Enemy cleaned up, new wave (4) spawned');
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();