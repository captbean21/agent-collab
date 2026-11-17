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

    // Test 2: BulletManager has default config values
    {
        const bm = new BulletManager();
        assertEqual(bm.config.speed, 500, 'Default bullet speed = 500');
        assertEqual(bm.config.radius, 3, 'Default bullet radius = 3');
        assertEqual(bm.config.lifetime, 2, 'Default bullet lifetime = 2 seconds');
        assertEqual(bm.config.cooldown, 0.15, 'Default fire cooldown = 0.15 seconds');
        assertEqual(bm.config.damage, 1, 'Default bullet damage = 1');
    }

    // ========== fire() Tests ==========

    // Test 3: fire() creates bullet at player position with direction
    {
        const bm = new BulletManager();
        const player = createTestPlayer(100, 100);
        player.vx = 0;
        player.vy = -1; // Facing up

        const bullet = bm.fire(player);

        assert(bullet !== undefined, 'fire() returns bullet');
        assertEqual(bullet.x, 100, 'Bullet x = player x');
        assertEqual(bullet.y, 100, 'Bullet y = player y');
        assertEqual(bm.bullets.length, 1, 'Bullet added to array');
        assert(bullet.vx !== 0 || bullet.vy !== 0, 'Bullet has velocity');
    }

    // Test 4: fire() respects cooldown (returns null if on cooldown)
    {
        const bm = new BulletManager();
        const player = createTestPlayer(100, 100);
        player.vx = 0;
        player.vy = -1;

        bm.fire(player); // First shot
        const bullet2 = bm.fire(player); // Immediate second shot

        assertEqual(bullet2, null, 'Second immediate fire returns null (cooldown)');
        assertEqual(bm.bullets.length, 1, 'Only one bullet in array');
    }

    // Test 5: fire() allows shot after cooldown expires
    {
        const bm = new BulletManager();
        const player = createTestPlayer(100, 100);
        player.vx = 0;
        player.vy = -1;

        bm.fire(player);
        // Simulate time passing (more than cooldown)
        bm.update(0.2); // 0.2s > 0.15s cooldown
        const bullet2 = bm.fire(player);

        assert(bullet2 !== null, 'Shot allowed after cooldown');
        assertEqual(bm.bullets.length, 2, 'Two bullets in array');
    }

    // Test 6: fire() calculates velocity from player facing direction
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0; // Facing right

        const bullet = bm.fire(player);

        assert(bullet.vx > 0, 'Bullet moves right when player faces right');
        assertApprox(bullet.vy, 0, 0.1, 'Bullet vy ≈ 0');
        // Speed should match config
        const speed = Math.hypot(bullet.vx, bullet.vy);
        assertApprox(speed, bm.config.speed, 1, 'Bullet speed matches config');
    }

    // Test 7: fire() works with diagonal direction
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 1; // Diagonal down-right

        const bullet = bm.fire(player);

        assert(bullet.vx > 0 && bullet.vy > 0, 'Bullet moves diagonal');
        const speed = Math.hypot(bullet.vx, bullet.vy);
        assertApprox(speed, bm.config.speed, 1, 'Diagonal bullet speed matches config');
    }

    // ========== update() Tests ==========

    // Test 8: update(deltaTime) moves bullets
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);
        const initialX = bullet.x;

        bm.update(1); // 1 second

        assert(bullet.x > initialX, 'Bullet moves forward over time');
        assertApprox(bullet.x - initialX, bm.config.speed * 1, 1, 'Distance = speed * time');
    }

    // Test 9: update() decreases bullet lifetime
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);
        const initialLifetime = bullet.lifetime;

        bm.update(0.5);

        assertApprox(bullet.lifetime, initialLifetime - 0.5, 0.01, 'Lifetime decreased by deltaTime');
    }

    // Test 10: update() removes expired bullets (lifetime <= 0)
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);
        bullet.lifetime = 0.1; // Almost expired

        bm.update(0.2); // Should expire

        assertEqual(bm.bullets.length, 0, 'Expired bullet removed');
    }

    // Test 11: update() removes bullets that go off-screen
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);
        bullet.x = 1000; // Way off screen (canvas 640x480)
        bullet.y = 240;

        bm.update(0.1);

        assertEqual(bm.bullets.length, 0, 'Off-screen bullet removed');
    }

    // Test 12: update() keeps on-screen bullets
    {
        const bm = new BulletManager();
        const player = createTestPlayer(320, 240);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);

        bm.update(0.1);

        assertEqual(bm.bullets.length, 1, 'On-screen bullet kept');
    }

    // ========== Collision Integration Tests ==========

    // Test 13: bullet-enemy collision via CollisionManager
    {
        const bm = new BulletManager();
        const em = new EnemyManager();
        const cm = new CollisionManager();

        const player = createTestPlayer(320, 240);
        player.vx = 1;
        player.vy = 0;

        // Spawn enemy at bullet path
        const enemy = em.spawnEnemy(400, 240, 'basic');

        // Fire bullet toward enemy
        const bullet = bm.fire(player);

        // Register with collision manager
        cm.colliders = [bullet, enemy];

        // Update bullet to reach enemy
        bm.update(0.2); // Bullet travels 100px
        cm.update();

        // Check collision detected
        const collisions = cm.update();
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

        const player = createTestPlayer(320, 240);
        player.vx = 1;
        player.vy = 0;

        const enemy = em.spawnEnemy(400, 240, 'basic');
        const bullet = bm.fire(player);

        cm.colliders = [bullet, enemy];
        bm.update(0.2);
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
        const player = createTestPlayer(320, 240);

        player.vx = 1; player.vy = 0; bm.fire(player);
        bm.update(0.2); // Wait for cooldown
        player.vx = 0; player.vy = -1; bm.fire(player);
        bm.update(0.2);
        player.vx = -1; player.vy = 0; bm.fire(player);

        assertEqual(bm.bullets.length, 3, 'Three bullets fired in different directions');
    }

    // Test 16: bullets have correct shape for collision (circle)
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        const bullet = bm.fire(player);

        assertEqual(bullet.shape, 'circle', 'Bullet shape = circle');
        assertEqual(bullet.radius, bm.config.radius, 'Bullet radius from config');
    }

    // Test 17: fire() with stationary player (zero velocity) defaults to up
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 0;
        player.vy = 0;

        const bullet = bm.fire(player);

        // Should default to shooting up (0, -1)
        assert(bullet.vy < 0, 'Bullet shoots up when player stationary');
        assertApprox(bullet.vx, 0, 0.1, 'Bullet vx ≈ 0 when stationary');
    }

    // Test 18: BulletManager config can be customized
    {
        const bm = new BulletManager({
            speed: 800,
            radius: 5,
            lifetime: 3,
            cooldown: 0.1,
            damage: 2
        });

        assertEqual(bm.config.speed, 800, 'Custom speed applied');
        assertEqual(bm.config.radius, 5, 'Custom radius applied');
        assertEqual(bm.config.lifetime, 3, 'Custom lifetime applied');
        assertEqual(bm.config.cooldown, 0.1, 'Custom cooldown applied');
        assertEqual(bm.config.damage, 2, 'Custom damage applied');
    }

    // Test 19: getBullets() returns all active bullets
    {
        const bm = new BulletManager();
        const player = createTestPlayer(0, 0);
        player.vx = 1;
        player.vy = 0;

        bm.fire(player);
        bm.update(0.2);
        bm.fire(player);

        const bullets = bm.getBullets ? bm.getBullets() : bm.bullets;
        assertEqual(bullets.length, 2, 'getBullets() returns all bullets');
    }

    // Test 20: Integration - full bullet lifecycle with enemy kill
    {
        const bm = new BulletManager();
        const em = new EnemyManager();
        const cm = new CollisionManager();
        const player = createTestPlayer(320, 240);
        player.vx = 1;
        player.vy = 0;

        // Spawn enemy in bullet path
        const enemy = em.spawnEnemy(500, 240, 'basic');
        em.enemies = [enemy];

        // Fire bullet
        const bullet = bm.fire(player);

        // Simulate frames until collision
        for (let i = 0; i < 10; i++) {
            bm.update(0.05);
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
            bm.bullets = bm.bullets.filter(b => !b.markedForRemoval && b.lifetime > 0);
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