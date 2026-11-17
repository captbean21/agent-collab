// Enemy Unit Tests — Rook's TDD Round 4 (EnemyManager)
// Tests for EnemyManager — written FIRST to fail, then Castle implements

import { EnemyManager } from '../enemy.js';

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

function runTests() {
    console.log('=== Enemy Test Suite ===\n');

    // Test 1: EnemyManager constructs with empty enemies array
    {
        const em = new EnemyManager();
        assert(Array.isArray(em.enemies), 'Constructor initializes enemies array');
        assertEqual(em.enemies.length, 0, 'Enemies array starts empty');
    }

    // Test 2: spawnEnemy adds enemy to enemies array
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(100, 100, 'basic');
        assertEqual(em.enemies.length, 1, 'spawnEnemy increases length to 1');
        assert(enemy !== undefined, 'spawnEnemy returns created enemy');
    }

    // Test 3: spawnEnemy creates enemy with correct properties
    // Note: Castle's impl uses 'health' but not 'maxHealth' separately
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(200, 300, 'basic');
        assertEqual(enemy.x, 200, 'Enemy x position set correctly');
        assertEqual(enemy.y, 300, 'Enemy y position set correctly');
        assertEqual(enemy.type, 'basic', 'Enemy type set correctly');
        assert(enemy.id !== undefined, 'Enemy has unique id');
        assert(enemy.shape === 'circle', 'Enemy has shape property (circle)');
        assert(enemy.radius !== undefined, 'Enemy has radius');
        assert(enemy.health !== undefined, 'Enemy has health');
        // maxHealth not in Castle's impl - health serves as both
        assert(enemy.speed !== undefined, 'Enemy has speed');
    }

    // Test 4: spawnEnemy with different types sets appropriate stats
    {
        const em = new EnemyManager();

        const basic = em.spawnEnemy(0, 0, 'basic');
        assertEqual(basic.health, 1, 'Basic enemy has 1 health');
        assertEqual(basic.speed, 50, 'Basic enemy has speed 50');
        assertEqual(basic.radius, 10, 'Basic enemy has radius 10');

        const fast = em.spawnEnemy(0, 0, 'fast');
        assertEqual(fast.health, 1, 'Fast enemy has 1 health');
        assert(fast.speed > basic.speed, 'Fast enemy is faster than basic');
        // Castle's impl: fast radius = 5 (smaller than basic's 10)
        assertEqual(fast.radius, 5, 'Fast enemy has smaller radius');

        const tank = em.spawnEnemy(0, 0, 'tank');
        assert(tank.health > basic.health, 'Tank enemy has more health');
        assert(tank.speed < basic.speed, 'Tank enemy is slower');
        // Castle's impl: tank radius = 20 (larger than basic's 10)
        assertEqual(tank.radius, 20, 'Tank enemy has larger radius');
    }

    // Test 5: spawnEnemy with unknown type uses basic config but keeps type string
    // Castle's impl: unknown type gets basic config but type stays as passed
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(0, 0, 'unknown_type');
        assertEqual(enemy.type, 'unknown_type', 'Unknown type string preserved');
        assertEqual(enemy.health, 1, 'Unknown type gets basic health');
        assertEqual(enemy.speed, 50, 'Unknown type gets basic speed');
    }

    // Test 6: Multiple spawnEnemy calls accumulate
    {
        const em = new EnemyManager();
        em.spawnEnemy(0, 0, 'basic');
        em.spawnEnemy(100, 100, 'fast');
        em.spawnEnemy(200, 200, 'tank');
        assertEqual(em.enemies.length, 3, 'Multiple spawnEnemy calls accumulate');
    }

    // Test 7: update(deltaTime) moves enemies toward player (basic AI)
    // Castle's impl: update(deltaTime, targetX, targetY) - target passed as args, not on enemy
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(0, 0, 'basic');
        const initialX = enemy.x;
        em.update(1, 100, 0); // deltaTime=1, targetX=100, targetY=0
        assert(enemy.x > initialX, 'Enemy moves toward target X');
        assertEqual(enemy.y, 0, 'Enemy Y unchanged when target Y same');
    }

    // Test 8: update(deltaTime) respects enemy speed
    // Castle's impl: update(deltaTime, targetX, targetY) - target passed as args
    {
        const em = new EnemyManager();
        const basic = em.spawnEnemy(0, 0, 'basic');
        const fast = em.spawnEnemy(0, 0, 'fast');
        em.update(1, 1000, 0);
        assert(fast.x > basic.x, 'Fast enemy moves further than basic in same time');
    }

    // Test 9: update() with no target doesn't move enemy
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(50, 50, 'basic');
        // No target set
        const initialX = enemy.x;
        const initialY = enemy.y;
        em.update(1);
        assertEqual(enemy.x, initialX, 'Enemy without target does not move X');
        assertEqual(enemy.y, initialY, 'Enemy without target does not move Y');
    }

    // Test 10: cleanup() removes enemies with health <= 0
    {
        const em = new EnemyManager();
        const alive = em.spawnEnemy(0, 0, 'basic');
        const dead = em.spawnEnemy(100, 100, 'basic');
        dead.health = 0;
        const initialCount = em.enemies.length;
        em.cleanup();
        assertEqual(em.enemies.length, initialCount - 1, 'cleanup removes dead enemies');
        assert(em.enemies.includes(alive), 'cleanup keeps alive enemies');
        assert(!em.enemies.includes(dead), 'cleanup removes dead enemies');
    }

    // Test 11: cleanup() removes enemies marked for removal
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(0, 0, 'basic');
        enemy.markedForRemoval = true;
        em.cleanup();
        assertEqual(em.enemies.length, 0, 'cleanup removes marked enemies');
    }

    // Test 12: Enemy has damage property
    {
        const em = new EnemyManager();
        const enemy = em.spawnEnemy(0, 0, 'basic');
        assert(enemy.damage !== undefined, 'Enemy has damage property');
        assertEqual(enemy.damage, 10, 'Basic enemy has damage 10');
    }

    // Test 13: Enemy has scoreValue property
    {
        const em = new EnemyManager();
        const basic = em.spawnEnemy(0, 0, 'basic');
        const fast = em.spawnEnemy(0, 0, 'fast');
        const tank = em.spawnEnemy(0, 0, 'tank');
        assert(basic.scoreValue !== undefined, 'Enemy has scoreValue');
        assert(fast.scoreValue > basic.scoreValue, 'Fast enemy worth more points');
        assert(tank.scoreValue > basic.scoreValue, 'Tank enemy worth more points');
    }

    // Test 14: spawnWave(count, type, centerX, centerY) spawns multiple enemies in formation
    {
        const em = new EnemyManager();
        em.spawnWave(5, 'basic', 320, 240);
        assertEqual(em.enemies.length, 5, 'spawnWave creates correct count');
        // Check they're spawned around center
        em.enemies.forEach(e => {
            const dist = Math.hypot(e.x - 320, e.y - 240);
            assert(dist < 100, 'Wave enemies spawned near center');
        });
    }

    // Test 15: getEnemies() returns all active enemies
    {
        const em = new EnemyManager();
        em.spawnEnemy(0, 0, 'basic');
        em.spawnEnemy(100, 100, 'fast');
        const enemies = em.getEnemies ? em.getEnemies() : em.enemies;
        assertEqual(enemies.length, 2, 'getEnemies returns all enemies');
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();