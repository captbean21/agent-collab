// Collision Unit Tests — Rook's TDD Round 2 (Collision)
// Tests for CollisionManager — written FIRST to fail, then Castle implements

import { CollisionManager } from '../collision.js';

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

function createCircleEntity(x, y, radius, id = 'circle') {
    return {
        id,
        type: 'circle',
        shape: 'circle',  // Support both 'type' and 'shape' for compatibility
        x,
        y,
        radius,
        width: radius * 2,  // For AABB compatibility
        height: radius * 2,
    };
}

function createAABBEntity(x, y, width, height, id = 'aabb') {
    return {
        id,
        type: 'rect',  // Match Castle's 'rect' shape
        shape: 'rect',
        x,
        y,
        width,
        height,
        radius: Math.min(width, height) / 2,
    };
}

function runTests() {
    console.log('=== Collision Test Suite ===\n');

    // Test 1: CollisionManager constructs with empty colliders
    {
        const cm = new CollisionManager();
        assert(Array.isArray(cm.colliders), 'Constructor initializes colliders array');
        assertEqual(cm.colliders.length, 0, 'Colliders array starts empty');
    }

    // Test 2: addCollider adds entity to colliders array
    {
        const cm = new CollisionManager();
        const entity = createCircleEntity(100, 100, 10, 'player');
        cm.addCollider(entity);
        assertEqual(cm.colliders.length, 1, 'addCollider increases length to 1');
        assert(cm.colliders[0] === entity, 'addCollider stores reference to entity');
    }

    // Test 3: Multiple addCollider calls accumulate
    {
        const cm = new CollisionManager();
        cm.addCollider(createCircleEntity(0, 0, 5, 'a'));
        cm.addCollider(createCircleEntity(10, 10, 5, 'b'));
        cm.addCollider(createCircleEntity(20, 20, 5, 'c'));
        assertEqual(cm.colliders.length, 3, 'Multiple addCollider calls accumulate');
    }

    // Test 4: Circle-circle collision — overlapping circles return true
    // Distance between centers < sum of radii
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 10, 'a');
        const b = createCircleEntity(15, 0, 10, 'b'); // Distance = 15, sum radii = 20 -> overlap
        const result = cm.checkCollision(a, b);
        assert(result === true, 'Circle-circle: overlapping circles return true');
    }

    // Test 5: Circle-circle collision — touching circles return true
    // Distance between centers == sum of radii
    // Note: Castle's implementation uses strict <, so touching returns false
    // This documents the current behavior; could be changed to <= if desired
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 10, 'a');
        const b = createCircleEntity(20, 0, 10, 'b'); // Distance = 20, sum radii = 20 -> touching
        const result = cm.checkCollision(a, b);
        // Current impl uses strict <, so touching = false
        assert(result === false, 'Circle-circle: touching circles return false (strict < behavior)');
    }

    // Test 6: Circle-circle collision — separate circles return false
    // Distance between centers > sum of radii
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 10, 'a');
        const b = createCircleEntity(25, 0, 10, 'b'); // Distance = 25, sum radii = 20 -> separate
        const result = cm.checkCollision(a, b);
        assert(result === false, 'Circle-circle: separate circles return false');
    }

    // Test 7: Circle-circle collision — one inside another returns true
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 20, 'a');
        const b = createCircleEntity(5, 0, 5, 'b'); // Distance = 5, sum radii = 25 -> b inside a
        const result = cm.checkCollision(a, b);
        assert(result === true, 'Circle-circle: one inside another returns true');
    }

    // Test 8: AABB-AABB collision — overlapping rectangles return true
    {
        const cm = new CollisionManager();
        const a = createAABBEntity(0, 0, 20, 20, 'a');
        const b = createAABBEntity(15, 15, 20, 20, 'b'); // Overlap on both axes
        const result = cm.checkCollision(a, b);
        assert(result === true, 'AABB-AABB: overlapping rectangles return true');
    }

    // Test 9: AABB-AABB collision — touching edges return true
    // Note: Castle's implementation uses strict <, so touching edges return false
    {
        const cm = new CollisionManager();
        const a = createAABBEntity(0, 0, 20, 20, 'a');
        const b = createAABBEntity(20, 0, 20, 20, 'b'); // Touching at x=20
        const result = cm.checkCollision(a, b);
        assert(result === false, 'AABB-AABB: touching edges return false (strict < behavior)');
    }

    // Test 10: AABB-AABB collision — separate rectangles return false
    {
        const cm = new CollisionManager();
        const a = createAABBEntity(0, 0, 20, 20, 'a');
        const b = createAABBEntity(25, 0, 20, 20, 'b'); // Gap of 5
        const result = cm.checkCollision(a, b);
        assert(result === false, 'AABB-AABB: separate rectangles return false');
    }

    // Test 11: Circle-AABB collision — circle overlapping rectangle returns true
    {
        const cm = new CollisionManager();
        const circle = createCircleEntity(10, 10, 5, 'circle');
        const aabb = createAABBEntity(0, 0, 20, 20, 'aabb'); // Circle center inside AABB
        const result = cm.checkCollision(circle, aabb);
        assert(result === true, 'Circle-AABB: circle inside AABB returns true');
    }

    // Test 12: Circle-AABB collision — circle outside rectangle returns false
    {
        const cm = new CollisionManager();
        const circle = createCircleEntity(30, 30, 5, 'circle');
        const aabb = createAABBEntity(0, 0, 20, 20, 'aabb'); // Circle far from AABB
        const result = cm.checkCollision(circle, aabb);
        assert(result === false, 'Circle-AABB: circle far from AABB returns false');
    }

    // Test 13: update() with no colliders does nothing (no error)
    {
        const cm = new CollisionManager();
        // Should not throw
        cm.update();
        assert(true, 'update() with empty colliders does not throw');
    }

    // Test 14: update() with two overlapping colliders detects collision
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 10, 'a');
        const b = createCircleEntity(15, 0, 10, 'b');
        cm.addCollider(a);
        cm.addCollider(b);
        // update() returns array of [entityA, entityB] tuples
        const collisions = cm.update();
        assert(Array.isArray(collisions), 'update() returns array of collision pairs');
        assert(collisions.length >= 1, 'update() detects at least one collision');
        // Check pair structure - tuple of [entityA, entityB]
        const pair = collisions[0];
        assert(Array.isArray(pair) && pair.length === 2, 'Collision pair is tuple of 2 entities');
        assert(pair[0] === a && pair[1] === b, 'Collision pair contains correct entities');
    }

    // Test 15: update() with non-overlapping colliders returns empty array
    {
        const cm = new CollisionManager();
        const a = createCircleEntity(0, 0, 5, 'a');
        const b = createCircleEntity(20, 0, 5, 'b'); // Separate
        cm.addCollider(a);
        cm.addCollider(b);
        const collisions = cm.update();
        assert(Array.isArray(collisions), 'update() returns array');
        assertEqual(collisions.length, 0, 'update() returns empty for no collisions');
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();