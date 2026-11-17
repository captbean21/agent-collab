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
        assert(typeof em.difficultyConfig.getTypesForWave === 'function', 'Has getTypesForWave function');
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
    {
        const em = new EnemyManager();
        const baseHealth = 1; // basic enemy base health
        const multiplier = em.difficultyConfig.healthMultiplierPerWave;

        const enemy1 = em.spawnEnemy(0, 0, 'basic', 1);
        assertEqual(enemy1.health, baseHealth, 'Wave 1: base health');

        const enemy2 = em.spawnEnemy(0, 0, 'basic', 2);
        // Health should be integer, so Math.floor or Math.ceil
        const expectedHealth = Math.max(1, Math.round(baseHealth * (1 + multiplier)));
        assertEqual(enemy2.health, expectedHealth, `Wave 2: health scaled`);

        const enemy5 = em.spawnEnemy(0, 0, 'basic', 5);
        const expectedHealth5 = Math.max(1, Math.round(baseHealth * (1 + 4 * multiplier)));
        assertEqual(enemy5.health, expectedHealth5, `Wave 5: health scaled`);
    }

    // Test 4: getTypesForWave returns correct type pool per wave
    {
        const em = new EnemyManager();
        const types1 = em.difficultyConfig.getTypesForWave(1);
        const types2 = em.difficultyConfig.getTypesForWave(2);
        const types3 = em.difficultyConfig.getTypesForWave(3);
        const types5 = em.difficultyConfig.getTypesForWave(5);
        const types10 = em.difficultyConfig.getTypesForWave(10);

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
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(100, 100, 'basic', 3);
        assert(enemy.wave === 3, 'Enemy stores wave number');
        // Speed should be scaled for wave 3
        assert(enemy.speed > 50, 'Wave 3 enemy faster than base');
        // Health should be scaled for wave 3
        assert(enemy.health >= 1, 'Wave 3 enemy has at least base health');
    }

    // Test 6: spawnWave passes wave number to spawned enemies
    {
        const em = new EnemyManager();
        const wave = 4;
        const enemies = em.spawnWave(5, 'basic', 320, 240, wave);
        assertEqual(enemies.length, 5, 'spawnWave creates correct count');
        enemies.forEach(e => {
            assertEqual(e.wave, wave, 'Each enemy has wave number');
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
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        assertEqual(gc.wave, 1, 'GameController starts at wave 1');
        assert(gc.getDifficultyMultiplier !== undefined, 'Has getDifficultyMultiplier');
    }

    // Test 11: GameController wave progression increases difficulty
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        // Manually increment wave
        gc.wave = 3;
        
        const mult = gc.getDifficultyMultiplier();
        assert(mult > 1, 'Difficulty multiplier > 1 at wave 3');
        assertEqual(mult, 1 + 2 * enemyManager.difficultyConfig.speedMultiplierPerWave, 'Multiplier matches formula');
    }

    // Test 12: GameController spawns next wave with correct wave number
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
        enemyManager.enemies.forEach(e => {
            assertEqual(e.wave, 2, 'Spawned enemies have wave 2');
        });
    }

    // Test 13: Score accumulation uses wave multiplier
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
        
        // Score should include wave multiplier
        const baseScore = 100;
        const multiplier = enemyManager.difficultyConfig.scoreMultiplierPerWave;
        const expectedScore = Math.round(baseScore * (1 + 2 * multiplier));
        assertEqual(gc.score, expectedScore, `Score includes wave 3 multiplier`);
    }

    // Test 14: Enemy type distribution shifts toward harder types at higher waves
    {
        const em = new EnemyManager();
        
        // Wave 1: 100% basic
        const types1 = em.difficultyConfig.getTypesForWave(1);
        assertEqual(types1.length, 1, 'Wave 1: only basic available');
        
        // Wave 2: 50% basic, 50% fast (or weighted)
        const types2 = em.difficultyConfig.getTypesForWave(2);
        assertEqual(types2.length, 2, 'Wave 2: basic + fast');
        
        // Wave 10: all types, but tank more common
        // This is implementation-dependent, just verify all 3 types available
        const types10 = em.difficultyConfig.getTypesForWave(10);
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

    // Test 17: spawnWave with 'mixed' type uses weighted distribution
    {
        const em = new EnemyManager();
        
        // Wave 1 mixed = all basic
        const wave1 = em.spawnWave(10, 'mixed', 0, 0, 1);
        const types1 = wave1.map(e => e.type);
        assert(types1.every(t => t === 'basic'), 'Wave 1 mixed = all basic');
        
        // Wave 3 mixed = all three types present
        const wave3 = em.spawnWave(30, 'mixed', 0, 0, 3);
        const types3 = wave3.map(e => e.type);
        assert(types3.includes('basic'), 'Wave 3 mixed has basic');
        assert(types3.includes('fast'), 'Wave 3 mixed has fast');
        assert(types3.includes('tank'), 'Wave 3 mixed has tank');
    }

    // Test 18: getDifficultyMultiplier returns 1 at wave 1
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        gc.wave = 1;
        assertEqual(gc.getDifficultyMultiplier(), 1, 'Multiplier = 1 at wave 1');
    }

    // Test 19: Difficulty affects spawn positions (wider spread at higher waves)
    {
        const em = new EnemyManager();
        
        const wave1 = em.spawnWave(5, 'basic', 320, 240, 1);
        const wave10 = em.spawnWave(5, 'basic', 320, 240, 10);
        
        const spread1 = Math.max(...wave1.map(e => Math.hypot(e.x - 320, e.y - 240)));
        const spread10 = Math.max(...wave10.map(e => Math.hypot(e.x - 320, e.y - 240)));
        
        // Higher wave could have wider spawn radius (optional feature)
        // Just verify both work
        assert(spread1 > 0, 'Wave 1 has spread');
        assert(spread10 > 0, 'Wave 10 has spread');
    }

    // Test 20: Integration - full game with difficulty progression
    {
        const player = createTestPlayer();
        const enemyManager = new EnemyManager();
        const collisionManager = new CollisionManager();
        const gc = new GameController(player, enemyManager, collisionManager);
        
        // Simulate several waves
        for (let w = 1; w <= 5; w++) {
            gc.wave = w;
            enemyManager.enemies = [];
            gc.update(1/60);
            
            assertEqual(gc.wave, w, `Wave ${w} tracked correctly`);
            assertEqual(enemyManager.enemies.length, w * 2, `Wave ${w} spawns ${w * 2} enemies`);
            
            // Enemies should have correct wave number
            enemyManager.enemies.forEach(e => {
                assertEqual(e.wave, w, `Enemy wave = ${w}`);
            });
        }
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();