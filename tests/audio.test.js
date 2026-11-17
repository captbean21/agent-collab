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

// Inject mock globally for tests
global.AudioContext = MockAudioContext;
global.webkitAudioContext = MockAudioContext;

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
        assert(am.audioContext !== null, 'AudioContext created');
        assert(am.masterGain !== null, 'masterGain created');
        assertEqual(am.masterGain.gain.value, 0.3, 'Master volume set to 0.3');
    }

    // Test 3: init() returns existing context if already initialized
    {
        const am = new AudioManager();
        const ctx1 = am.init();
        const ctx2 = am.init();
        assert(ctx1 === ctx2, 'init() returns same context on second call');
    }

    // Test 4: setMuted(true) zeros master gain
    {
        const am = new AudioManager();
        am.init();
        am.setMuted(true);
        assertEqual(am.masterGain.gain.value, 0, 'Muted sets gain to 0');
        assertEqual(am.isMuted, true, 'isMuted flag set');
    }

    // Test 5: setMuted(false) restores master gain
    {
        const am = new AudioManager();
        am.init();
        am.setMuted(true);
        am.setMuted(false);
        assertEqual(am.masterGain.gain.value, 0.3, 'Unmuted restores gain to 0.3');
        assertEqual(am.isMuted, false, 'isMuted flag cleared');
    }

    // Test 6: setEnabled(false) disables audio output
    {
        const am = new AudioManager();
        am.setEnabled(false);
        assertEqual(am.enabled, false, 'enabled flag false');
    }

    // Test 7: createTone returns oscillator and gain objects
    {
        const am = new AudioManager();
        const result = am.createTone(440, 0.1);
        assert(result !== undefined, 'createTone returns object');
        assert(result.osc !== undefined, 'Result has osc');
        assert(result.gain !== undefined, 'Result has gain');
    }

    // Test 8: createTone respects frequency and duration parameters
    {
        const am = new AudioManager();
        const result = am.createTone(880, 0.5, 'square', 0.7);
        assertEqual(result.osc.frequency.value, 880, 'Frequency set correctly');
        assertEqual(result.osc.type, 'square', 'Wave type set correctly');
        assertEqual(result.gain.gain.value, 0.7, 'Volume set correctly');
    }

    // Test 9: createSweep creates frequency sweep
    {
        const am = new AudioManager();
        const result = am.createSweep(100, 200, 0.5, 'sawtooth', 0.4);
        assert(result !== undefined, 'createSweep returns object');
        assertEqual(result.osc.type, 'sawtooth', 'Sweep uses sawtooth wave');
    }

    // Test 10: createNoiseBurst creates noise buffer
    {
        const am = new AudioManager();
        const result = am.createNoiseBurst(0.2, 0.5, 1000);
        assert(result !== undefined, 'createNoiseBurst returns object');
        assert(result.source !== undefined, 'Result has source');
        assert(result.filter !== undefined, 'Result has filter');
        assertEqual(result.filter.frequency.value, 1000, 'Filter frequency set');
    }

    // Test 11: playPlayerHit creates hit sound (tone + noise)
    {
        const am = new AudioManager();
        am.init();
        // Should not throw
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

    // Test 13: playEnemySpawn creates spawn sound
    {
        const am = new AudioManager();
        am.init();
        am.playEnemySpawn();
        assert(true, 'playEnemySpawn executes without error');
    }

    // Test 14: playWaveComplete creates ascending arpeggio
    {
        const am = new AudioManager();
        am.init();
        am.playWaveComplete();
        assert(true, 'playWaveComplete executes without error');
    }

    // Test 15: playGameOver creates descending tones
    {
        const am = new AudioManager();
        am.init();
        am.playGameOver();
        assert(true, 'playGameOver executes without error');
    }

    // Test 16: playScore creates blip based on points
    {
        const am = new AudioManager();
        am.init();
        am.playScore(100);
        am.playScore(500);
        assert(true, 'playScore executes without error');
    }

    // Test 17: startEngineHum creates continuous oscillator
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        assert(am.engineOsc !== null, 'Engine oscillator created');
        assert(am.engineGain !== null, 'Engine gain created');
        assert(am.engineFilter !== null, 'Engine filter created');
    }

    // Test 18: stopEngineHum stops and cleans up engine oscillator
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        am.stopEngineHum();
        assertEqual(am.engineOsc, null, 'Engine oscillator cleared');
        assertEqual(am.engineGain, null, 'Engine gain cleared');
        assertEqual(am.engineFilter, null, 'Engine filter cleared');
    }

    // Test 19: setEnginePitch adjusts frequency and gain based on speed
    {
        const am = new AudioManager();
        am.init();
        am.startEngineHum();
        am.setEnginePitch(0); // Stopped
        assertEqual(am.engineOsc.frequency.value, 40, 'Pitch at 0 speed = 40Hz');
        assertEqual(am.engineGain.gain.value, 0.02, 'Gain at 0 speed = 0.02');

        am.setEnginePitch(1); // Max speed
        assertEqual(am.engineOsc.frequency.value, 120, 'Pitch at max speed = 120Hz');
        assertEqual(am.engineGain.gain.value, 0.1, 'Gain at max speed = 0.1');

        am.setEnginePitch(0.5); // Half speed
        assertEqual(am.engineOsc.frequency.value, 80, 'Pitch at half speed = 80Hz');
        assertEqual(am.engineGain.gain.value, 0.06, 'Gain at half speed = 0.06');

        am.stopEngineHum();
    }

    // Test 20: resume() resumes suspended context
    {
        const am = new AudioManager();
        am.init();
        am.audioContext.state = 'suspended';
        // Should not throw
        am.resume();
        assertEqual(am.audioContext.state, 'running', 'Context resumed to running');
    }

    // Summary
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
    if (failed > 0) {
        process.exitCode = 1;
    }
}

runTests();