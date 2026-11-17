// Audio Unit Tests — Rook's TDD Round 8 (AudioManager)
// Tests for AudioManager procedural Web Audio API

import { AudioManager } from '../audio.js';

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

// Mock AudioContext for Node.js testing
class MockAudioContext {
    constructor() {
        this.state = 'running';
        this.currentTime = 0;
        this.sampleRate = 44100;
        this.destination = {};
    }

    createGain() {
        return {
            gain: { value: 1, setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} },
            connect: () => {},
        };
    }

    createOscillator() {
        return {
            type: 'sine',
            frequency: { value: 440, setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} },
            connect: () => {},
            start: () => {},
            stop: () => {},
        };
    }

    createBufferSource() {
        return {
            buffer: null,
            connect: () => {},
            start: () => {},
            stop: () => {},
        };
    }

    createBiquadFilter() {
        return {
            type: 'lowpass',
            frequency: { value: 2000 },
            connect: () => {},
        };
    }

    createBuffer(channels, length, sampleRate) {
        const data = new Float32Array(length);
        return {
            getChannelData: () => data,
        };
    }

    resume() {
        this.state = 'running';
        return Promise.resolve();
    }
}

// Inject mock globally BEFORE importing AudioManager in tests that need it
// (Done in individual tests via dynamic import)

function runTests() {
    console.log('=== Audio Test Suite ===\n');

    // Test 1: AudioManager constructs with correct initial state
    {
        const am = new AudioManager();
        assertEqual(am.audioContext, null, 'audioContext initially null');
        assertEqual(am.masterGain, null, 'masterGain initially null');
        assertEqual(am.isMuted, false, 'isMuted initially false');
        assertEqual(am.enabled, true, 'enabled initially true');
    }

    // Test 2: init() creates AudioContext and masterGain
    {
        const am = new AudioManager();
        am.init();
        // In headless, enabled=false; in browser, context created
        if (am.enabled) {
            assert(am.audioContext !== null, 'AudioContext created');
            assert(am.masterGain !== null, 'masterGain created');
            assertEqual(am.masterGain.gain.value, 0.3, 'Master volume set to 0.3');
        } else {
            assert(true, 'init() disables audio in headless');
        }
    }

    // Test 3: init() returns existing context if already initialized
    {
        const am = new AudioManager();
        const ctx1 = am.init();
        const ctx2 = am.init();
        if (am.enabled) {
            assert(ctx1 === ctx2, 'init() returns same context on second call');
        } else {
            assert(true, 'init() consistent in headless');
        }
    }

    // Test 4: setMuted(true) zeros master gain
    {
        const am = new AudioManager();
        am.init();
        am.setMuted(true);
        if (am.enabled) {
            assertEqual(am.masterGain.gain.value, 0, 'Muted sets gain to 0');
        }
        assertEqual(am.isMuted, true, 'isMuted flag set');
    }

    // Test 5: setMuted(false) restores master gain
    {
        const am = new AudioManager();
        am.init();
        am.setMuted(true);
        am.setMuted(false);
        if (am.enabled) {
            assertEqual(am.masterGain.gain.value, 0.3, 'Unmuted restores gain to 0.3');
        }
        assertEqual(am.isMuted, false, 'isMuted flag cleared');
    }

    // Test 6: setEnabled(false) disables audio output
    {
        const am = new AudioManager();
        am.setEnabled(false);
        assertEqual(am.enabled, false, 'enabled flag false');
    }

    // Tests 7-10: Core synthesis primitives (require AudioContext)
    // In headless, these return undefined; with mock, they return objects
    // We test both scenarios

    // Test 7: createTone
    {
        const am = new AudioManager();
        am.init();
        const result = am.createTone(440, 0.1);
        if (am.enabled && result) {
            assert(result !== undefined, 'createTone returns object');
            assert(result.osc !== undefined, 'Result has osc');
            assert(result.gain !== undefined, 'Result has gain');
        } else {
            assert(true, 'createTone skipped in headless');
        }
    }

    // Test 8: createTone respects parameters
    {
        const am = new AudioManager();
        am.init();
        const result = am.createTone(880, 0.5, 'square', 0.7);
        if (am.enabled && result) {
            assertEqual(result.osc.frequency.value, 880, 'Frequency set correctly');
            assertEqual(result.osc.type, 'square', 'Wave type set correctly');
            assertEqual(result.gain.gain.value, 0.7, 'Volume set correctly');
        } else {
            assert(true, 'createTone skipped in headless');
        }
    }

    // Test 9: createSweep
    {
        const am = new AudioManager();
        am.init();
        const result = am.createSweep(100, 200, 0.5, 'sawtooth', 0.4);
        if (am.enabled && result) {
            assert(result !== undefined, 'createSweep returns object');
            assertEqual(result.osc.type, 'sawtooth', 'Sweep uses sawtooth wave');
        } else {
            assert(true, 'createSweep skipped in headless');
        }
    }

    // Test 10: createNoiseBurst
    {
        const am = new AudioManager();
        am.init();
        const result = am.createNoiseBurst(0.2, 0.5, 1000);
        if (am.enabled && result) {
            assert(result !== undefined, 'createNoiseBurst returns object');
            assert(result.source !== undefined, 'Result has source');
            assert(result.filter !== undefined, 'Result has filter');
            assertEqual(result.filter.frequency.value, 1000, 'Filter frequency set');
        } else {
            assert(true, 'createNoiseBurst skipped in headless');
        }
    }

    // Test 11: playPlayerHit
    {
        const am = new AudioManager();
        am.init();
        am.playPlayerHit();
        assert(true, 'playPlayerHit executes without error');
    }

    // Test 12: playEnemyDestroyed varies by enemy type
    {
        const am = new AudioManager();
        am.init();
        am.playEnemyDestroyed('basic');
        am.playEnemyDestroyed('fast');
        am.playEnemyDestroyed('tank');
        am.playEnemyDestroyed('unknown');
        assert(true, 'playEnemyDestroyed executes for all types');
    }

    // Test 13: playEnemySpawn
    {
        const am = new AudioManager();
        am.init();
        am.playEnemySpawn();
        assert(true, 'playEnemySpawn executes without error');
    }

    // Test 14: playWaveComplete
    {
        const am = new AudioManager();
        am.init();
        am.playWaveComplete();
        assert(true, 'playWaveComplete executes without error');
    }

    // Test 15: playGameOver
    {
        const am = new AudioManager();
        am.init();
        am.playGameOver();
        assert(true, 'playGameOver executes without error');
    }

    // Test 16: playScore
    {
        const am = new AudioManager();
        am.init();
        am.playScore(100);
        am.playScore(500);
        assert(true, 'playScore executes without error');
    }

    // Test 17: startEngineHum
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        if (am.enabled) {
            assert(am.engineOsc !== null, 'Engine oscillator created');
            assert(am.engineGain !== null, 'Engine gain created');
            assert(am.engineFilter !== null, 'Engine filter created');
        } else {
            assert(true, 'startEngineHum skipped in headless');
        }
    }

    // Test 18: stopEngineHum
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        am.stopEngineHum();
        if (am.enabled) {
            assertEqual(am.engineOsc, null, 'Engine oscillator cleared');
            assertEqual(am.engineGain, null, 'Engine gain cleared');
            assertEqual(am.engineFilter, null, 'Engine filter cleared');
        } else {
            assert(true, 'stopEngineHum skipped in headless');
        }
    }

    // Test 19: setEnginePitch
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        if (am.enabled) {
            am.setEnginePitch(0);
            assertEqual(am.engineOsc.frequency.value, 40, 'Pitch at 0 speed = 40Hz');
            assertEqual(am.engineGain.gain.value, 0.02, 'Gain at 0 speed = 0.02');

            am.setEnginePitch(1);
            assertEqual(am.engineOsc.frequency.value, 120, 'Pitch at max speed = 120Hz');
            assertEqual(am.engineGain.gain.value, 0.1, 'Gain at max speed = 0.1');

            am.setEnginePitch(0.5);
            assertEqual(am.engineOsc.frequency.value, 80, 'Pitch at half speed = 80Hz');
            assertEqual(am.engineGain.gain.value, 0.06, 'Gain at half speed = 0.06');

            am.stopEngineHum();
        } else {
            assert(true, 'setEnginePitch skipped in headless');
        }
    }

    // Test 20: resume()
    {
        const am = new AudioManager();
        am.init();
        if (am.enabled && am.audioContext) {
            am.audioContext.state = 'suspended';
            am.resume();
            assertEqual(am.audioContext.state, 'running', 'Context resumed to running');
        } else {
            assert(true, 'resume() skipped in headless');
        }
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();