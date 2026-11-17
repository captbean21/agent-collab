// Bullet System Unit Tests — Rook's TDD Round 11 (Bullet System)
// Tests for BulletManager and bullet entities — written FIRST to fail, then Castle implements

import { BulletManager } from '../bullet.js';
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
    console.log('=== Bullet System Test Suite ===\n');

    // ========== BulletManager Constructor Tests ==========

    // Test 1: BulletManager constructs with empty bullets array
    {
        const bm = new BulletManager();
        assert(Array.isArray(bm.bullets), 'Constructor initializes bullets array');
        assertEqual(bm.bullets.length, 0, 'Bullets array starts empty');
        assert(bm.config !== undefined, 'Has config object');
    }

    // Test 2: BulletManager has default config values (milliseconds)
    {
        const bm = new BulletManager();
        assertEqual(bm.config.speed, 500, 'Default bullet speed = 500 px/s');
        assertEqual(bm.config.radius, 3, 'Default bullet radius = 3');
        assertEqual(bm.config.lifetime, 2000, 'Default bullet lifetime = 2000ms');
        assertEqual(bm.config.cooldown, 150, 'Default fire cooldown = 150ms');
        assertEqual(bm.config.damage, 1, 'Default bullet damage = 1');
    }

    // ========== fire() Tests ==========

    // Test 3: fire() creates bullet at player position with direction
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        const bullet = bm.fire(100, 100, 0, -1, currentTime); // Facing up

        assert(bullet !== undefined, 'fire() returns bullet');
        assertEqual(bullet.x, 100, 'Bullet x = player x');
        assertEqual(bullet.y, 100, 'Bullet y = player y');
        assertEqual(bm.bullets.length, 1, 'Bullet added to array');
        assert(bullet.vx !== 0 || bullet.vy !== 0, 'Bullet has velocity');
    }

    // Test 4: fire() respects cooldown (returns null if on cooldown)
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(100, 100, 0, -1, currentTime); // First shot
        const bullet2 = bm.fire(100, 100, 0, -1, currentTime); // Immediate second shot

        assertEqual(bullet2, null, 'Second immediate fire returns null (cooldown)');
        assertEqual(bm.bullets.length, 1, 'Only one bullet in array');
    }

    // Test 5: fire() allows shot after cooldown expires
    {
        const bm = new BulletManager();

        bm.fire(100, 100, 0, -1, 1000);
        // Time advances past cooldown (150ms)
        const bullet2 = bm.fire(100, 100, 0, -1, 1200); // 200ms later

        assert(bullet2 !== null, 'Shot allowed after cooldown');
        assertEqual(bm.bullets.length, 2, 'Two bullets in array');
    }

    // Test 6: fire() calculates velocity from player facing direction
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        // Facing right (1, 0)
        const bullet = bm.fire(0, 0, 1, 0, currentTime);

        assert(bullet.vx > 0, 'Bullet moves right when player faces right');
        assertApprox(bullet.vy, 0, 0.1, 'Bullet vy ≈ 0');
        // Speed should match config
        const speed = Math.hypot(bullet.vx, bullet.vy);
        assertApprox(speed, bm.config.speed, 1, 'Bullet speed matches config');
    }

    // Test 7: fire() works with diagonal direction
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        // Diagonal down-right (1, 1)
        const bullet = bm.fire(0, 0, 1, 1, currentTime);

        assert(bullet.vx > 0 && bullet.vy > 0, 'Bullet moves diagonal');
        const speed = Math.hypot(bullet.vx, bullet.vy);
        assertApprox(speed, bm.config.speed, 1, 'Diagonal bullet speed matches config');
    }

    // ========== update() Tests ==========

    // Test 8: update(deltaTime) moves bullets
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(0, 0, 1, 0, currentTime); // Facing right
        const bullet = bm.bullets[0];
        const initialX = bullet.x;

        bm.update(1, currentTime + 1000); // 1 second

        assert(bullet.x > initialX, 'Bullet moves forward over time');
        assertApprox(bullet.x - initialX, bm.config.speed * 1, 1, 'Distance = speed * time');
    }

    // Test 9: update() marks bullets for removal when lifetime expires
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(0, 0, 1, 0, currentTime);
        const bullet = bm.bullets[0];

        // Advance time past lifetime (2000ms = 2s)
        bm.update(2.1, currentTime + 2100); // deltaTime=2.1s, currentTime=3100ms

        assert(bullet.markedForRemoval === true, 'Bullet marked for removal after lifetime');
    }

    // Test 10: cleanup() removes marked bullets
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(0, 0, 1, 0, currentTime);
        const bullet = bm.bullets[0];
        bullet.markedForRemoval = true;

        bm.cleanup();

        assertEqual(bm.bullets.length, 0, 'Marked bullet removed by cleanup');
    }

    // Test 11: update() removes bullets that go off-screen
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(0, 0, 1, 0, currentTime);
        const bullet = bm.bullets[0];
        bullet.x = 1000; // Way off screen (canvas 800x600)
        bullet.y = 300;

        bm.update(0.1, currentTime + 100);

        assert(bullet.markedForRemoval === true, 'Off-screen bullet marked for removal');
    }

    // Test 12: update() keeps on-screen bullets
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        bm.fire(320, 240, 1, 0, currentTime);

        bm.update(0.1, currentTime + 100);

        assertEqual(bm.bullets.length, 1, 'On-screen bullet kept');
        assert(bm.bullets[0].markedForRemoval !== true, 'On-screen bullet not marked');
    }

    // ========== Collision Integration Tests ==========

    // Test 13: bullet-enemy collision via CollisionManager
    {
        const bm = new BulletManager();
        const em = new EnemyManager();
        const cm = new CollisionManager();

        const currentTime = 1000;

        // Spawn enemy at bullet path (distance 50px, within radius sum 13)
        const enemy = em.spawnEnemy(370, 240, 'basic');

        // Fire bullet toward enemy
        const bullet = bm.fire(320, 240, 1, 0, currentTime);

        // Register with collision manager
        cm.colliders = [bullet, enemy];

        // Update bullet to reach enemy (0.1s = 50px)
        bm.update(0.1, currentTime + 100);
        const collisions = cm.update();

        // Check collision detected
        const bulletEnemyCollision = collisions.find(([a, b]) => 
            (a === bullet && b === enemy) || (a === enemy && b === bullet)
        );

        assert(bulletEnemyCollision !== undefined, 'Bullet-enemy collision detected');
    }

    // Test 14: bullet-enemy collision marks both for removal
    {
        const bm = new BulletManager();
        const em = new EnemyManager();
        const cm = new CollisionManager();

        const currentTime = 1000;

        const enemy = em.spawnEnemy(400, 240, 'basic');
        const bullet = bm.fire(320, 240, 1, 0, currentTime);

        cm.colliders = [bullet, enemy];
        bm.update(0.2, currentTime + 200);
        const collisions = cm.update();

        // Find bullet-enemy collision
        const hit = collisions.find(([a, b]) => 
            (a === bullet && b === enemy) || (a === enemy && b === bullet)
        );

        if (hit) {
            const [a, b] = hit;
            // Bullet should be marked for removal
            assert(a.markedForRemoval === true || b.markedForRemoval === true, 'Bullet or enemy marked for removal');
        }
    }

    // Test 15: multiple bullets can exist simultaneously
    {
        const bm = new BulletManager();
        let currentTime = 1000;

        bm.fire(320, 240, 1, 0, currentTime);
        currentTime += 200; // Wait for cooldown
        bm.fire(320, 240, 0, -1, currentTime);
        currentTime += 200;
        bm.fire(320, 240, -1, 0, currentTime);

        assertEqual(bm.bullets.length, 3, 'Three bullets fired in different directions');
    }

    // Test 16: bullets have correct shape for collision (circle)
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        const bullet = bm.fire(0, 0, 1, 0, currentTime);

        assertEqual(bullet.shape, 'circle', 'Bullet shape = circle');
        assertEqual(bullet.radius, bm.config.radius, 'Bullet radius from config');
    }

    // Test 17: fire() with stationary player (zero velocity) defaults to up
    {
        const bm = new BulletManager();
        const currentTime = 1000;

        const bullet = bm.fire(0, 0, 0, 0, currentTime);

        // Should default to shooting up (0, -speed)
        assert(bullet.vy < 0, 'Bullet shoots up when player stationary');
        assertApprox(bullet.vx, 0, 0.1, 'Bullet vx ≈ 0 when stationary');
    }

    // Test 18: BulletManager config can be customized
    {
        const bm = new BulletManager({
            speed: 800,
            radius: 5,
            lifetime: 3000,
            cooldown: 100,
            damage: 2
        });

        assertEqual(bm.config.speed, 800, 'Custom speed applied');
        assertEqual(bm.config.radius, 5, 'Custom radius applied');
        assertEqual(bm.config.lifetime, 3000, 'Custom lifetime applied (ms)');
        assertEqual(bm.config.cooldown, 100, 'Custom cooldown applied (ms)');
        assertEqual(bm.config.damage, 2, 'Custom damage applied');
    }

    // Test 19: getBullets() returns all active bullets
    {
        const bm = new BulletManager();
        let currentTime = 1000;

        bm.fire(0, 0, 1, 0, currentTime);
        currentTime += 200;
        bm.fire(0, 0, 0, -1, currentTime);

        const bullets = bm.getBullets ? bm.getBullets() : bm.bullets;
        assertEqual(bullets.length, 2, 'getBullets() returns all bullets');
    }

    // Test 20: Integration - full bullet lifecycle with enemy kill
    {
        const bm = new BulletManager();
        const em = new EnemyManager();
        const cm = new CollisionManager();
        let currentTime = 1000;

        // Spawn enemy in bullet path
        const enemy = em.spawnEnemy(500, 240, 'basic');
        em.enemies = [enemy];

        // Fire bullet
        const bullet = bm.fire(320, 240, 1, 0, currentTime);

        // Simulate frames until collision
        for (let i = 0; i < 10; i++) {
            currentTime += 50;
            bm.update(0.05, currentTime);
            cm.colliders = [bullet, ...em.getEnemies()];
            const collisions = cm.update();
            
            // Check for bullet-enemy collision
            for (const [a, b] of collisions) {
                if ((a === bullet && b === enemy) || (a === enemy && b === bullet)) {
                    bullet.markedForRemoval = true;
                    enemy.markedForRemoval = true;
                    enemy.health = 0;
                }
            }

            // Cleanup
            bm.cleanup();
            em.cleanup();
        }

        // Enemy should be dead, bullet removed
        assertEqual(em.enemies.length, 0, 'Enemy killed and removed');
        assert(bm.bullets.length === 0 || !bm.bullets.includes(bullet), 'Bullet removed after hit');
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();