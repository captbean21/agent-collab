// cpu_synth.rs — Pure Rust CPU synth, no external deps
// Compile: rustc cpu_synth.rs -o cpu_synth
// Run: ./cpu_synth

use std::fs::File;
use std::io::{Write, BufWriter};

const SAMPLE_RATE: f32 = 44100.0;
const DURATION: f32 = 4.5;
const PI: f32 = std::f32::consts::PI;
const TWO_PI: f32 = 2.0 * PI;

#[derive(Clone, Copy)]
struct Patch {
    bpm: f32,
    osc1_freq: f32,
    osc1_shape: f32,
    osc1_detune: f32,
    osc2_freq_ratio: f32,
    osc2_shape: f32,
    osc2_level: f32,
    filter_cutoff: f32,
    filter_res: f32,
    filter_env_amt: f32,
    env_attack: f32,
    env_decay: f32,
    env_sustain: f32,
    env_release: f32,
    fenv_attack: f32,
    fenv_decay: f32,
    fenv_sustain: f32,
    fenv_release: f32,
    arp_rate: f32,
    arp_pattern: i32,
    arp_octaves: i32,
    delay_time: f32,
    delay_feedback: f32,
    delay_mix: f32,
    master_gain: f32,
}

fn neon_motorway() -> Patch {
    Patch {
        bpm: 118.0,
        osc1_freq: 55.0,
        osc1_shape: 1.0,      // saw
        osc1_detune: 0.0,
        osc2_freq_ratio: 0.5,
        osc2_shape: 2.0,      // square
        osc2_level: 0.3,
        filter_cutoff: 800.0,
        filter_res: 0.6,
        filter_env_amt: 1.0,
        env_attack: 0.01,
        env_decay: 0.3,
        env_sustain: 0.4,
        env_release: 0.5,
        fenv_attack: 0.001,
        fenv_decay: 0.2,
        fenv_sustain: 0.3,
        fenv_release: 0.3,
        arp_rate: 118.0 / 60.0 * 4.0,
        arp_pattern: 2,       // updown
        arp_octaves: 2,
        delay_time: 0.254,
        delay_feedback: 0.3,
        delay_mix: 0.2,
        master_gain: 0.5,
    }
}

fn dark_midnight() -> Patch {
    Patch {
        bpm: 105.0,
        osc1_freq: 41.2,      // E1
        osc1_shape: 0.5,      // sine-saw blend
        osc1_detune: -5.0,
        osc2_freq_ratio: 0.5,
        osc2_shape: 0.0,      // sine
        osc2_level: 0.2,
        filter_cutoff: 400.0,
        filter_res: 0.3,
        filter_env_amt: 0.6,
        env_attack: 0.05,
        env_decay: 0.8,
        env_sustain: 0.6,
        env_release: 1.2,
        fenv_attack: 0.01,
        fenv_decay: 0.5,
        fenv_sustain: 0.4,
        fenv_release: 0.5,
        arp_rate: 105.0 / 60.0 * 2.0, // 8th notes
        arp_pattern: 1,       // down
        arp_octaves: 1,
        delay_time: 0.571,    // quarter note
        delay_feedback: 0.4,
        delay_mix: 0.25,
        master_gain: 0.45,
    }
}

fn arcade_highway() -> Patch {
    Patch {
        bpm: 125.0,
        osc1_freq: 69.3,      // C#2
        osc1_shape: 1.5,      // saw-square
        osc1_detune: 3.0,
        osc2_freq_ratio: 0.5,
        osc2_shape: 1.0,      // saw
        osc2_level: 0.4,
        filter_cutoff: 2000.0,
        filter_res: 0.7,
        filter_env_amt: 1.2,
        env_attack: 0.005,
        env_decay: 0.15,
        env_sustain: 0.3,
        env_release: 0.2,
        fenv_attack: 0.001,
        fenv_decay: 0.1,
        fenv_sustain: 0.2,
        fenv_release: 0.15,
        arp_rate: 125.0 / 60.0 * 4.0, // 16th notes
        arp_pattern: 0,       // up
        arp_octaves: 3,
        delay_time: 0.120,    // 16th note
        delay_feedback: 0.25,
        delay_mix: 0.15,
        master_gain: 0.55,
    }
}

fn oscillator(phase: f32, shape: f32) -> f32 {
    let s = shape.floor();
    let t = shape.fract();
    
    let sine = (phase * TWO_PI).sin();
    let saw = phase * 2.0 - 1.0;
    let square = if phase < 0.5 { 1.0 } else { -1.0 };
    let tri = 1.0 - 2.0 * (phase - 0.5).abs();
    
    let v1 = if s <= 0.0 { sine } else if s <= 1.0 { sine + (saw - sine) * t } else if s <= 2.0 { saw + (square - saw) * t } else { square + (tri - square) * t };
    v1
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

struct FilterState {
    s1: f32, s2: f32, s3: f32, s4: f32,
}

fn ladder_filter(input: f32, fs: &mut FilterState, cutoff: f32, res: f32) -> f32 {
    let f = (cutoff / SAMPLE_RATE).clamp(0.001, 0.49);
    let fb = res * 4.0 * (1.0 - f);
    
    let input = input - fs.s4 * fb;
    
    fs.s1 = fs.s1 + f * (input.tanh() - fs.s1.tanh());
    fs.s2 = fs.s2 + f * (fs.s1.tanh() - fs.s2.tanh());
    fs.s3 = fs.s3 + f * (fs.s2.tanh() - fs.s3.tanh());
    fs.s4 = fs.s4 + f * (fs.s3.tanh() - fs.s4.tanh());
    
    fs.s4
}

fn adsr(t: f32, attack: f32, decay: f32, sustain: f32, release: f32, note_on: f32, note_off: f32) -> f32 {
    if t < note_on { return 0.0; }
    if t < note_off {
        let dt = t - note_on;
        if dt < attack { return dt / attack; }
        let dt = dt - attack;
        if dt < decay { return 1.0 - (1.0 - sustain) * (dt / decay); }
        return sustain;
    } else {
        let dt = t - note_off;
        return sustain * (1.0 - dt / release).max(0.0);
    }
}

fn generate(patch: Patch, filename: &str) -> std::io::Result<()> {
    let sample_count = (SAMPLE_RATE * DURATION) as usize;
    let mut samples = Vec::with_capacity(sample_count * 2);
    
    // Minor pentatonic scale degrees
    let scale = [0, 3, 5, 7, 10];
    
    let mut fs = FilterState { s1: 0.0, s2: 0.0, s3: 0.0, s4: 0.0 };
    let mut delay_buf = vec![0.0f32; (SAMPLE_RATE * 2.0) as usize]; // 2s max delay
    let mut delay_pos = 0;
    
    for i in 0..sample_count {
        let t = i as f32 / SAMPLE_RATE;
        
        // Arpeggiator
        let note_period = 1.0 / patch.arp_rate;
        let note_idx = (t / note_period).floor() as i32;
        let note_pos = (t % note_period) / note_period;
        
        let pattern_idx = match patch.arp_pattern {
            0 => note_idx % 5,                    // up
            1 => 4 - (note_idx % 5),              // down
            _ => {                                // updown
                let cycle = note_idx % 8;
                if cycle < 5 { cycle } else { 8 - cycle }
            }
        };
        
        let octave = (note_idx / 5).rem_euclid(patch.arp_octaves);
        let semitones = scale[pattern_idx as usize] + octave * 12;
        let freq_mul = 2.0_f32.powf(semitones as f32 / 12.0);
        
        // Oscillators
        let detune_mul = 2.0_f32.powf(patch.osc1_detune / 1200.0);
        let phase1 = (t * patch.osc1_freq * freq_mul * detune_mul) % 1.0;
        let phase2 = (t * patch.osc1_freq * freq_mul * patch.osc2_freq_ratio) % 1.0;
        
        let osc1 = oscillator(phase1, patch.osc1_shape);
        let osc2 = oscillator(phase2, patch.osc2_shape) * patch.osc2_level;
        let mixed = osc1 + osc2;
        
        // Envelopes (per-note, retrigger each arp step)
        let note_start = (note_idx as f32) * note_period;
        let note_end = note_start + note_period * 0.9; // small gap
        let note_t = t - note_start;
        
        let amp_env = if note_t < 0.0 { 0.0 } else {
            adsr(note_t, patch.env_attack, patch.env_decay, patch.env_sustain, patch.env_release, 0.0, note_period * 0.9)
        };
        let filt_env = if note_t < 0.0 { 0.0 } else {
            adsr(note_t, patch.fenv_attack, patch.fenv_decay, patch.fenv_sustain, patch.fenv_release, 0.0, note_period * 0.9)
        };
        
        // Filter
        let cutoff_mod = patch.filter_cutoff + filt_env * patch.filter_env_amt * 5000.0;
        let filtered = ladder_filter(mixed * amp_env, &mut fs, cutoff_mod, patch.filter_res);
        
        // Delay
        let delay_samples = (patch.delay_time * SAMPLE_RATE) as usize;
        let delayed = delay_buf[(delay_pos + delay_buf.len() - delay_samples) % delay_buf.len()];
        let out = filtered * (1.0 - patch.delay_mix) + delayed * patch.delay_mix;
        
        // Write to delay buffer with feedback
        delay_buf[delay_pos] = filtered + delayed * patch.delay_feedback;
        delay_pos = (delay_pos + 1) % delay_buf.len();
        
        // Master + soft clip
        let final_out = (out * patch.master_gain).tanh();
        
        // Stereo (mono for now, same L/R)
        let s16 = (final_out.clamp(-1.0, 1.0) * 32767.0) as i16;
        samples.push(s16);
        samples.push(s16);
    }
    
    // Write WAV
    let mut file = BufWriter::new(File::create(filename)?);
    
    // RIFF header
    let data_len = samples.len() * 2;
    let riff_len = 36 + data_len;
    
    file.write_all(b"RIFF")?;
    file.write_all(&(riff_len as u32).to_le_bytes())?;
    file.write_all(b"WAVE")?;
    
    // fmt chunk
    file.write_all(b"fmt ")?;
    file.write_all(&16u32.to_le_bytes())?;        // chunk size
    file.write_all(&1u16.to_le_bytes())?;         // PCM
    file.write_all(&2u16.to_le_bytes())?;         // stereo
    file.write_all(&(SAMPLE_RATE as u32).to_le_bytes())?;
    file.write_all(&(SAMPLE_RATE as u32 * 2 * 2).to_le_bytes())?; // byte rate
    file.write_all(&(2 * 2)u16.to_le_bytes())?;   // block align
    file.write_all(&16u16.to_le_bytes())?;        // bits per sample
    
    // data chunk
    file.write_all(b"data")?;
    file.write_all(&(data_len as u32).to_le_bytes())?;
    
    for &s in &samples {
        file.write_all(&s.to_le_bytes())?;
    }
    
    file.flush()?;
    println!("Generated {} ({:.1}s, {} samples, stereo)", filename, DURATION, sample_count);
    Ok(())
}

fn main() {
    println!("CPU Synth - Generating 3 tracks...");
    
    generate(neon_motorway(), "track1_neon_motorway.wav").expect("track1 failed");
    generate(dark_midnight(), "track2_dark_midnight.wav").expect("track2 failed");
    generate(arcade_highway(), "track3_arcade_highway.wav").expect("track3 failed");
    
    println!("Done. 3 WAV files created.");
}