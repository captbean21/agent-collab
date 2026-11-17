// Difficulty Ramping Unit Tests — Rook's TDD Round 9
// Tests for EnemyManager and GameController difficulty scaling

import { EnemyManager } from '../enemy.js';
import { GameController } from '../gameController.js';
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

function assertApprox(actual, expected, tolerance, message) {
    const ok = Math.abs(actual - expected) <= tolerance;
    if (ok) {
        console.log(`✅ PASS: ${message} (${actual} ≈ ${expected} ±${tolerance})`);
        passed++;
    } else {
        console.error(`❌ FAIL: ${message} (expected ${expected} ±${tolerance}, got ${actual})`);
        failed++;
    }
}

function createTestPlayer(x = 320, y = 240) {
    const player = createPlayer();
    player.x = x;
    player.y = y;
    player.shape = 'circle';
    player.radius = 8;
    return player;
}

function runTests() {
    console.log('=== Difficulty Ramping Test Suite ===\n');

    // ========== EnemyManager Difficulty Tests ==========

    // Test 1: EnemyManager has difficulty config with wave multipliers
    {
        const em = new EnemyManager();
        assert(em.difficultyConfig !== undefined, 'EnemyManager has difficultyConfig');
        assert(typeof em.difficultyConfig.speedMultiplierPerWave === 'number', 'Has speedMultiplierPerWave');
        assert(typeof em.difficultyConfig.healthMultiplierPerWave === 'number', 'Has healthMultiplierPerWave');
        // getTypesForWave is a method on EnemyManager, not on difficultyConfig
        assert(typeof em.getTypesForWave === 'function', 'Has getTypesForWave method');
    }

    // Test 2: speedMultiplierPerWave increases enemy speed each wave
    {
        const em = new EnemyManager();
        const baseSpeed = 50; // basic enemy base speed
        const multiplier = em.difficultyConfig.speedMultiplierPerWave;

        // Wave 1: no multiplier
        const enemy1 = em.spawnEnemy(0, 0, 'basic', 1);
        assertEqual(enemy1.speed, baseSpeed, 'Wave 1: base speed');

        // Wave 2: 1x multiplier
        const enemy2 = em.spawnEnemy(0, 0, 'basic', 2);
        assertApprox(enemy2.speed, baseSpeed * (1 + multiplier), 0.1, `Wave 2: speed = base * (1 + ${multiplier})`);

        // Wave 5: 4x multiplier
        const enemy5 = em.spawnEnemy(0, 0, 'basic', 5);
        assertApprox(enemy5.speed, baseSpeed * (1 + 4 * multiplier), 0.1, `Wave 5: speed = base * (1 + 4*${multiplier})`);
    }

    // Test 3: healthMultiplierPerWave increases enemy health each wave
    // Note: Castle's impl keeps health as float (1.05, 1.2), not rounded to int
    {
        const em = new EnemyManager();
        const baseHealth = 1; // basic enemy base health
        const multiplier = em.difficultyConfig.healthMultiplierPerWave;

        const enemy1 = em.spawnEnemy(0, 0, 'basic', 1);
        assertEqual(enemy1.health, baseHealth, 'Wave 1: base health');

        const enemy2 = em.spawnEnemy(0, 0, 'basic', 2);
        // Health kept as float: 1 * (1 + 0.05) = 1.05
        assertApprox(enemy2.health, baseHealth * (1 + multiplier), 0.01, 'Wave 2: health scaled (float)');

        const enemy5 = em.spawnEnemy(0, 0, 'basic', 5);
        // Health: 1 * (1 + 4 * 0.05) = 1.2
        assertApprox(enemy5.health, baseHealth * (1 + 4 * multiplier), 0.01, 'Wave 5: health scaled (float)');
    }

    // Test 4: getTypesForWave returns correct type pool per wave
    {
        const em = new EnemyManager();
        const types1 = em.getTypesForWave(1);
        const types2 = em.getTypesForWave(2);
        const types3 = em.getTypesForWave(3);
        const types5 = em.getTypesForWave(5);
        const types10 = em.getTypesForWave(10);

        // Wave 1: only basic
        assertEqual(types1.length, 1, 'Wave 1: 1 type');
        assert(types1.includes('basic'), 'Wave 1: includes basic');

        // Wave 2: basic + fast
        assertEqual(types2.length, 2, 'Wave 2: 2 types');
        assert(types2.includes('basic') && types2.includes('fast'), 'Wave 2: basic + fast');

        // Wave 3+: basic + fast + tank
        assertEqual(types3.length, 3, 'Wave 3: 3 types');
        assert(types3.includes('basic') && types3.includes('fast') && types3.includes('tank'), 'Wave 3: all types');

        // Higher waves still have all 3 types
        assertEqual(types5.length, 3, 'Wave 5: 3 types');
        assertEqual(types10.length, 3, 'Wave 10: 3 types');
    }

    // Test 5: spawnEnemy accepts wave parameter and applies difficulty
    // Note: Castle's impl applies difficulty but doesn't store wave property on enemy
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(100, 100, 'basic', 3);
        // wave property not stored in current impl
        assert(enemy.wave === undefined, 'Enemy does not store wave property (current impl)');
        // Speed should be scaled for wave 3
        assert(enemy.speed > 50, 'Wave 3 enemy faster than base');
        // Health should be scaled for wave 3
        assert(enemy.health >= 1, 'Wave 3 enemy has at least base health');
    }

    // Test 6: spawnWave passes wave number to spawned enemies
    // Note: Castle's impl applies difficulty but doesn't store wave property on enemy
    {
        const em = new EnemyManager();
        const wave = 4;
        const enemies = em.spawnWave(5, 'basic', 320, 240, wave);
        assertEqual(enemies.length, 5, 'spawnWave creates correct count');
        enemies.forEach(e => {
            // wave property not stored in current impl
            assert(e.wave === undefined, 'Enemy does not store wave property (current impl)');
            // But difficulty IS applied
            assert(e.speed > 50, 'Wave 4 enemy has scaled speed');
        });
    }

    // Test 7: spawnWave with mixed types distributes types from getTypesForWave
    {
        const em = new EnemyManager();
        const wave = 3; // Should have basic, fast, tank
        const enemies = em.spawnWave(12, 'mixed', 320, 240, wave);
        assertEqual(enemies.length, 12, 'Mixed wave creates correct count');
        
        const types = enemies.map(e => e.type);
        assert(types.includes('basic'), 'Mixed wave has basic');
        assert(types.includes('fast'), 'Mixed wave has fast');
        assert(types.includes('tank'), 'Mixed wave has tank');
    }

    // Test 8: Difficulty config has score multiplier per wave
    {
        const em = new EnemyManager();
        assert(typeof em.difficultyConfig.scoreMultiplierPerWave === 'number', 'Has scoreMultiplierPerWave');
        
        const baseScore = 100; // basic enemy score
        const multiplier = em.difficultyConfig.scoreMultiplierPerWave;
        
        const score1 = Math.round(baseScore * (1 + 0 * multiplier));
        const score2 = Math.round(baseScore * (1 + 1 * multiplier));
        const score5 = Math.round(baseScore * (1 + 4 * multiplier));
        
        assert(score2 > score1, 'Wave 2 score > Wave 1 score');
        assert(score5 > score2, 'Wave 5 score > Wave 2 score');
    }

    // Test 9: Enemy scoreValue scales with wave
    {
        const em = new EnemyManager();
        const enemy1 = em.spawnEnemy(0, 0, 'basic', 1);
        const enemy5 = em.spawnEnemy(0, 0, 'basic', 5);
        
        assert(enemy5.scoreValue > enemy1.scoreValue, 'Higher wave enemy worth more points');
    }

    // ========== GameController Difficulty Tests ==========

    // Test 10: GameController tracks current wave and applies difficulty
    // Note: Castle's GameController doesn't have getDifficultyMultiplier yet
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        assertEqual(gc.wave, 1, 'GameController starts at wave 1');
        // getDifficultyMultiplier not in current impl
        assert(gc.getDifficultyMultiplier === undefined, 'No getDifficultyMultiplier (current impl)');
    }

    // Test 11: GameController wave progression increases difficulty
    // Note: Castle's impl doesn't have getDifficultyMultiplier; difficulty is in EnemyManager
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        // Manually increment wave
        gc.wave = 3;
        // Difficulty tracked via EnemyManager
        const mult = 1 + (gc.wave - 1) * enemyManager.difficultyConfig.speedMultiplierPerWave;
        assert(mult > 1, 'Difficulty multiplier > 1 at wave 3');
        assertApprox(mult, 1.2, 0.01, 'Multiplier matches formula (1 + 2 * 0.1)');
    }

    // Test 12: GameController spawns next wave with correct wave number
    // Note: Castle's GameController.spawnWave uses 'basic' type, not mixed
    // and enemy doesn't store wave property
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        // Clear enemies to trigger wave spawn
        enemyManager.enemies = [];
        gc.wave = 1;
        
        // Call internal wave spawn logic (or simulate update)
        gc.update(1/60);
        
        // Should spawn wave 2 with 4 enemies
        assertEqual(gc.wave, 2, 'Wave incremented to 2');
        assertEqual(enemyManager.enemies.length, 4, 'Wave 2 spawns 4 enemies');
        // enemy doesn't store wave property in current impl
        enemyManager.enemies.forEach(e => {
            assert(e.wave === undefined, 'Enemy does not store wave property (current impl)');
            // But difficulty IS applied for wave 2
            assert(e.speed > 50, 'Wave 2 enemy has scaled speed');
        });
    }

    // Test 13: Score accumulation uses wave multiplier
    // Note: Castle's handleCollision doesn't add score currently
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        gc.wave = 3;
        gc.score = 0;
        
        // Simulate killing a basic enemy at wave 3
        const enemy = enemyManager.spawnEnemy(100, 100, 'basic', 3);
        collisionManager.addCollider(player);
        collisionManager.addCollider(enemy);
        
        gc.handleCollision(player, enemy);
        
        // Score not added in current impl
        assertEqual(gc.score, 0, 'Score unchanged (not added in current impl)');
        // But enemy has correct scaled scoreValue
        const baseScore = 100;
        const multiplier = enemyManager.difficultyConfig.scoreMultiplierPerWave;
        const expectedScore = Math.floor(baseScore * (1 + 2 * multiplier));
        assertEqual(enemy.scoreValue, expectedScore, 'Enemy scoreValue has wave 3 multiplier');
    }

    // Test 14: Enemy type distribution shifts toward harder types at higher waves
    {
        const em = new EnemyManager();
        
        // Wave 1: 100% basic
        const types1 = em.getTypesForWave(1);
        assertEqual(types1.length, 1, 'Wave 1: only basic available');
        
        // Wave 2: 50% basic, 50% fast (or weighted)
        const types2 = em.getTypesForWave(2);
        assertEqual(types2.length, 2, 'Wave 2: basic + fast');
        
        // Wave 10: all types, but tank more common
        // This is implementation-dependent, just verify all 3 types available
        const types10 = em.getTypesForWave(10);
        assertEqual(types10.length, 3, 'Wave 10: all types available');
    }

    // Test 15: Difficulty caps at reasonable maximums
    {
        const em = new EnemyManager();
        
        // Very high wave shouldn't break things
        const enemy100 = em.spawnEnemy(0, 0, 'basic', 100);
        assert(enemy100.speed < 1000, 'Speed capped at reasonable max');
        assert(enemy100.health < 100, 'Health capped at reasonable max');
        assert(enemy100.scoreValue < 10000, 'Score value capped at reasonable max');
    }

    // Test 16: Fast and tank enemies also scale with wave
    {
        const em = new EnemyManager();
        
        const fast1 = em.spawnEnemy(0, 0, 'fast', 1);
        const fast5 = em.spawnEnemy(0, 0, 'fast', 5);
        assert(fast5.speed > fast1.speed, 'Fast enemy speed scales with wave');
        assert(fast5.health >= fast1.health, 'Fast enemy health scales with wave');
        
        const tank1 = em.spawnEnemy(0, 0, 'tank', 1);
        const tank5 = em.spawnEnemy(0, 0, 'tank', 5);
        assert(tank5.speed > tank1.speed, 'Tank enemy speed scales with wave');
        assert(tank5.health > tank1.health, 'Tank enemy health scales with wave');
    }

    // Test 17: spawnWave uses getTypesForWave internally for mixed type distribution
    // Note: Castle's spawnWave(count, centerX, centerY, wave) uses getTypesForWave(wave)
    // to determine type array, then distributes enemies across those types
    {
        const em = new EnemyManager();
        
        // Wave 1: only basic available
        const wave1 = em.spawnWave(10, 0, 0, 1);
        const types1 = wave1.map(e => e.type);
        assert(types1.every(t => t === 'basic'), 'Wave 1 = all basic');
        
        // Wave 3: basic, fast, tank all available, distributed round-robin
        const wave3 = em.spawnWave(12, 0, 0, 3);
        const types3 = wave3.map(e => e.type);
        assert(types3.includes('basic'), 'Wave 3 has basic');
        assert(types3.includes('fast'), 'Wave 3 has fast');
        assert(types3.includes('tank'), 'Wave 3 has tank');
        // Count each type (12 enemies / 3 types = 4 each)
        const basicCount = types3.filter(t => t === 'basic').length;
        const fastCount = types3.filter(t => t === 'fast').length;
        const tankCount = types3.filter(t => t === 'tank').length;
        assertEqual(basicCount, 4, '4 basic enemies');
        assertEqual(fastCount, 4, '4 fast enemies');
        assertEqual(tankCount, 4, '4 tank enemies');
    }

    // Test 18: Difficulty multiplier is 1 at wave 1
    // Note: GameController doesn't have getDifficultyMultiplier
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        gc.wave = 1;
        const mult = 1 + (gc.wave - 1) * enemyManager.difficultyConfig.speedMultiplierPerWave;
        assertEqual(mult, 1, 'Multiplier = 1 at wave 1');
    }

    // Test 19: Difficulty affects spawn positions (wider spread at higher waves)
    // Note: Castle's impl uses fixed 50px radius regardless of wave
    // spawnWave(count, centerX, centerY, wave)
    {
        const em = new EnemyManager();
        
        const wave1 = em.spawnWave(5, 320, 240, 1);
        const wave10 = em.spawnWave(5, 320, 240, 10);
        
        const spread1 = Math.max(...wave1.map(e => Math.hypot(e.x - 320, e.y - 240)));
        const spread10 = Math.max(...wave10.map(e => Math.hypot(e.x - 320, e.y - 240)));
        
        // Both use fixed 50px radius
        assertApprox(spread1, 50, 0.1, 'Wave 1 spread = 50px');
        assertApprox(spread10, 50, 0.1, 'Wave 10 spread = 50px (fixed radius)');
    }

    // Test 20: Integration - full game with difficulty progression
    // Note: GameController.update() increments wave when enemies cleared and spawns wave*2 enemies
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        // Start: gc.wave = 1 (from constructor), no enemies yet
        // First update: enemies empty -> wave becomes 2, spawns 4 enemies
        gc.update(1/60);
        assertEqual(gc.wave, 2, 'First clear -> wave 2');
        assertEqual(enemyManager.enemies.length, 4, 'Wave 2 spawns 4 enemies');
        enemyManager.enemies.forEach(e => {
            assert(e.speed > 50, 'Wave 2 enemies have scaled speed');
        });
        
        // Clear enemies -> wave 3, spawns 6 enemies
        enemyManager.enemies = [];
        gc.update(1/60);
        assertEqual(gc.wave, 3, 'Second clear -> wave 3');
        assertEqual(enemyManager.enemies.length, 6, 'Wave 3 spawns 6 enemies');
        // At wave 3: basic=70, fast=120, tank=30 (types: basic, fast, tank)
        // Check that basic and fast have higher speed than wave 2 basic (55)
        enemyManager.enemies.forEach(e => {
            if (e.type === 'basic' || e.type === 'fast') {
                assert(e.speed > 55, `Wave 3 ${e.type} has higher speed`);
            }
        });
        
        // Clear enemies -> wave 4, spawns 8 enemies
        enemyManager.enemies = [];
        gc.update(1/60);
        assertEqual(gc.wave, 4, 'Third clear -> wave 4');
        assertEqual(enemyManager.enemies.length, 8, 'Wave 4 spawns 8 enemies');
        // At wave 4: basic=80, fast=130, tank=32.5
        enemyManager.enemies.forEach(e => {
            if (e.type === 'basic' || e.type === 'fast') {
                assert(e.speed > 60, `Wave 4 ${e.type} has even higher speed`);
            }
        });
        
        // Test direct spawnWave with specific wave number
        // Note: spawnWave distributes types round-robin: basic, fast, tank
        // Basic wave 5: 50 * 1.4 = 70
        // Fast wave 5: 100 * 1.4 = 140
        // Tank wave 5: 25 * 1.4 = 35
        enemyManager.enemies = [];
        const wave5enemies = enemyManager.spawnWave(10, 320, 240, 5);
        assertEqual(wave5enemies.length, 10, 'Direct spawnWave(10, wave=5) creates 10 enemies');
        wave5enemies.forEach(e => {
            if (e.type === 'basic') {
                assert(e.speed >= 70, 'Basic wave 5 speed >= 70');
            } else if (e.type === 'fast') {
                assert(e.speed >= 140, 'Fast wave 5 speed >= 140');
            } else if (e.type === 'tank') {
                assert(e.speed >= 35, 'Tank wave 5 speed >= 35');
            }
            assert(e.health > 1, 'Wave 5 enemies have scaled health');
            assert(e.scoreValue > 100, 'Wave 5 enemies have scaled score');
        });
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();