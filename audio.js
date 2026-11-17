/**
 * AudioManager - Procedural Audio via Web Audio API
 * Generates retro arcade sound effects and background loops programmatically.
 */
class AudioManager {
  constructor() {
    this.audioContext = null;
    this.masterGain = null;
    this.isMuted = false;
    this.enabled = true;
  }

  // Initialize Web Audio API context (must be called after user interaction)
  init() {
    if (this.audioContext) return this.audioContext;

    // Support both browser (window) and Node.js (global) environments
    const AudioContextClass = (typeof window !== 'undefined' && (window.AudioContext || window.webkitAudioContext))
      || (typeof global !== 'undefined' && global.AudioContext)
      || (typeof self !== 'undefined' && (self.AudioContext || self.webkitAudioContext));

    if (!AudioContextClass) {
      throw new Error('AudioContext not available in this environment');
    }

    this.audioContext = new AudioContextClass();
    this.masterGain = this.audioContext.createGain();
    this.masterGain.connect(this.audioContext.destination);
    this.masterGain.gain.value = 0.3; // Master volume
    return this.audioContext;
  }

  // Resume context if suspended (browser autoplay policy)
  async resume() {
    if (this.audioContext && this.audioContext.state === 'suspended') {
      await this.audioContext.resume();
    }
  }

  // Toggle mute
  setMuted(muted) {
    this.isMuted = muted;
    if (this.masterGain) {
      this.masterGain.gain.value = muted ? 0 : 0.3;
    }
  }

  // Enable/disable audio entirely
  setEnabled(enabled) {
    this.enabled = enabled;
  }

  // ---------- Core Synthesis Primitives ----------

  // Generate a simple tone (sine wave)
  createTone(frequency, duration, type = 'sine', volume = 0.5) {
    if (!this.enabled || this.isMuted) return;
    if (!this.audioContext) this.init();

    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();

    osc.type = type;
    osc.frequency.value = frequency;
    gain.gain.value = volume;

    osc.connect(gain);
    gain.connect(this.masterGain);

    const now = this.audioContext.currentTime;
    osc.start(now);
    osc.stop(now + duration);

    return { osc, gain, stop: () => osc.stop() };
  }

  // Generate a frequency sweep (for thrust/engine sounds)
  createSweep(startFreq, endFreq, duration, type = 'sawtooth', volume = 0.3) {
    if (!this.enabled || this.isMuted) return;
    if (!this.audioContext) this.init();

    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();

    osc.type = type;
    gain.gain.value = volume;

    osc.connect(gain);
    gain.connect(this.masterGain);

    const now = this.audioContext.currentTime;
    osc.frequency.setValueAtTime(startFreq, now);
    osc.frequency.exponentialRampToValueAtTime(endFreq, now + duration);
    gain.gain.setValueAtTime(volume, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

    osc.start(now);
    osc.stop(now + duration);

    return { osc, gain, stop: () => osc.stop() };
  }

  // Generate noise burst (for explosions/hits)
  createNoiseBurst(duration, volume = 0.5, filterFreq = 2000) {
    if (!this.enabled || this.isMuted) return;
    if (!this.audioContext) this.init();

    const bufferSize = this.audioContext.sampleRate * duration;
    const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
    const data = buffer.getChannelData(0);

    // White noise
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }

    const source = this.audioContext.createBufferSource();
    const gain = this.audioContext.createGain();
    const filter = this.audioContext.createBiquadFilter();

    source.buffer = buffer;
    filter.type = 'lowpass';
    filter.frequency.value = filterFreq;
    gain.gain.value = volume;

    source.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    const now = this.audioContext.currentTime;
    gain.gain.setValueAtTime(volume, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

    source.start(now);
    source.stop(now + duration);

    return { source, gain, filter, stop: () => source.stop() };
  }

  // ---------- Game Sound Effects ----------

  // Player thrust (engine hum with subtle modulation)
  playThrust(isActive) {
    if (!this.enabled || this.isMuted) return;
    // For continuous thrust, we'd use a long-running oscillator
    // This is a placeholder - real impl would maintain state
    if (isActive) {
      this.createSweep(80, 120, 0.1, 'square', 0.1);
    }
  }

  // Player collision/hit
  playPlayerHit() {
    if (!this.enabled || this.isMuted) return;
    this.createTone(150, 0.3, 'sawtooth', 0.4);
    this.createNoiseBurst(0.2, 0.3, 800);
  }

  // Enemy destroyed
  playEnemyDestroyed(enemyType = 'basic') {
    if (!this.enabled || this.isMuted) return;
    const freqMap = { basic: 440, fast: 660, tank: 220 };
    const freq = freqMap[enemyType] || 440;
    this.createTone(freq, 0.15, 'square', 0.3);
    this.createTone(freq * 1.5, 0.1, 'square', 0.2);
  }

  // Enemy spawned
  playEnemySpawn() {
    if (!this.enabled || this.isMuted) return;
    this.createSweep(200, 100, 0.2, 'sine', 0.2);
  }

  // Wave complete / level up
  playWaveComplete() {
    if (!this.enabled || this.isMuted) return;
    // Ascending arpeggio
    const notes = [261.63, 329.63, 392.00, 523.25]; // C4, E4, G4, C5
    notes.forEach((freq, i) => {
      setTimeout(() => this.createTone(freq, 0.2, 'sine', 0.3), i * 80);
    });
  }

  // Game over
  playGameOver() {
    if (!this.enabled || this.isMuted) return;
    // Descending sad tones
    const notes = [392.00, 349.23, 329.63, 293.66]; // G4, F4, E4, D4
    notes.forEach((freq, i) => {
      setTimeout(() => this.createTone(freq, 0.4, 'sine', 0.3), i * 150);
    });
  }

  // Score increment (tiny blip)
  playScore(points) {
    if (!this.enabled || this.isMuted) return;
    const freq = Math.min(440 + points, 1200);
    this.createTone(freq, 0.05, 'sine', 0.15);
  }

  // Background engine hum (looped)
  startEngineHum() {
    if (!this.enabled || this.isMuted) return;
    if (!this.audioContext) this.init();

    // Create a subtle continuous drone
    if (this.engineOsc) return; // Already playing

    this.engineOsc = this.audioContext.createOscillator();
    this.engineGain = this.audioContext.createGain();
    this.engineFilter = this.audioContext.createBiquadFilter();

    this.engineOsc.type = 'sawtooth';
    this.engineOsc.frequency.value = 60;
    this.engineFilter.type = 'lowpass';
    this.engineFilter.frequency.value = 200;
    this.engineGain.gain.value = 0.05;

    this.engineOsc.connect(this.engineFilter);
    this.engineFilter.connect(this.engineGain);
    this.engineGain.connect(this.masterGain);

    this.engineOsc.start();
  }

  stopEngineHum() {
    if (this.engineOsc) {
      this.engineOsc.stop();
      this.engineOsc = null;
      this.engineGain = null;
      this.engineFilter = null;
    }
  }

  // Set engine pitch based on player speed
  setEnginePitch(speedRatio) {
    // speedRatio: 0 (stopped) to 1 (max speed)
    if (this.engineOsc) {
      this.engineOsc.frequency.value = 40 + speedRatio * 80; // 40-120 Hz
      this.engineGain.gain.value = 0.02 + speedRatio * 0.08; // 0.02-0.1
    }
  }
}

// Singleton instance for easy import
export const audioManager = new AudioManager();
export { AudioManager };