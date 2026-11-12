// CPU banger: proper 4/4 structure with kick, hat, bass, arp, chords
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

#define SR 44100
#define PI 3.14159265358979323846f

// === Drum Voices ===
float kick_synth(float t, float trigger) {
    if (!trigger) return 0.0f;
    float pitch = 60.0f * expf(-t * 8.0f) + 30.0f;
    float env = expf(-t * 12.0f);
    return sinf(pitch * t * 2.0f * PI) * env * 1.2f;
}

float hat_synth(float t, float trigger) {
    if (!trigger) return 0.0f;
    float noise = (rand() / (float)RAND_MAX) * 2.0f - 1.0f;
    float env = expf(-t * 80.0f);
    return noise * env * 0.15f;
}

// === Synth Voices ===
float osc_saw(float freq, float t) { return fmodf(freq * t, 1.0f) * 2.0f - 1.0f; }
float osc_square(float freq, float t) { return fmodf(freq * t, 1.0f) < 0.5f ? 1.0f : -1.0f; }

// 4-pole ladder filter
typedef struct { float s1, s2, s3, s4; } Filter;
float ladder(float in, Filter *f, float cutoff, float res) {
    float fc = cutoff / 44100.0f; if (fc < 0.001f) fc = 0.001f; if (fc > 0.49f) fc = 0.49f;
    float fb = res * 4.0f * (1.0f - fc);
    in -= f->s4 * fb;
    f->s1 += fc * (tanhf(in) - tanhf(f->s1));
    f->s2 += fc * (tanhf(f->s1) - tanhf(f->s2));
    f->s3 += fc * (tanhf(f->s2) - tanhf(f->s3));
    f->s4 += fc * (tanhf(f->s3) - tanhf(f->s4));
    return f->s4;
}

// ADSR
float adsr(float t, float a, float d, float s, float r, float on, float off) {
    if (t < on) return 0;
    if (t < off) {
        float dt = t - on;
        if (dt < a) return dt/a;
        dt -= a;
        if (dt < d) return 1.0f - (1.0f-s)*(dt/d);
        return s;
    } else { float dt = t-off; float v = s*(1.0f-dt/r); return v>0?v:0; }
}

// === Sequencer Data ===
#define BPM 120.0f
#define BEAT (60.0f/BPM)
#define BAR (BEAT*4.0f)

int main() {
    srand(42);
    int samples = (int)(44100.0f * 30.0f);
    int16_t *buf = calloc(samples*2, sizeof(int16_t));
    
    Filter bass_f = {0}, arp_f = {0}, chord_f = {0};
    float kick_phase = 0, hat_phase = 0;
    
    // Bass pattern: 16th notes, 2 bars repeating
    float bass_notes[32] = {
        55.0f, 55.0f, 0, 55.0f,  61.7f, 61.7f, 0, 61.7f,
        49.0f, 49.0f, 0, 49.0f,  55.0f, 55.0f, 0, 55.0f,
        55.0f, 55.0f, 0, 55.0f,  61.7f, 61.7f, 0, 61.7f,
        49.0f, 49.0f, 0, 49.0f,  51.9f, 51.9f, 0, 51.9f
    };
    // Chord stabs on beat 1 and 3
    float chord_root[8] = {55.0f, 0, 61.7f, 0, 49.0f, 0, 51.9f, 0};
    
    // Delay buffers (1 second each)
    static float delay_l[44100] = {0}, delay_r[44100] = {0};
    int dl = 0;
    
    for (int i=0; i<samples; i++) {
        float t = i / 44100.0f;
        float beat_pos = fmodf(t, BEAT);
        float bar_pos = fmodf(t, BAR);
        int beat16 = (int)(bar_pos / (BEAT/4.0f)) % 32;
        int beat_idx = (int)(bar_pos / BEAT) % 8;
        
        float mix = 0.0f;
        
        // KICK: every beat
        if (beat_pos < 0.005f) kick_phase = 0;
        mix += kick_synth(kick_phase, beat_pos < 0.02f);
        kick_phase += 1.0f/44100.0f;
        
        // HAT: off-beats (8ths)
        float hat_trigger = (fmodf(bar_pos, BEAT/2.0f) < 0.005f);
        if (hat_trigger) hat_phase = 0;
        mix += hat_synth(hat_phase, hat_trigger);
        hat_phase += 1.0f/44100.0f;
        
        // BASS: 16th note pattern
        float bass_freq = bass_notes[beat16];
        if (bass_freq > 0) {
            float note_t = fmodf(t, BEAT/4.0f);
            float env = adsr(note_t, 0.001f, 0.08f, 0.3f, 0.05f, 0, BEAT/4.0f*0.9f);
            float raw = osc_saw(bass_freq, t) + osc_square(bass_freq*0.5f, t)*0.3f;
            float filt = ladder(raw * env, &bass_f, 500.0f + env*2000.0f, 0.5f);
            mix += filt * 0.6f;
        }
        
        // ARP: 8th notes, minor pent up-down
        float arp_notes[16] = {55,65.4,73.4,82.4,98,82.4,73.4,65.4,  49,58.3,65.4,73.4,82.4,73.4,65.4,58.3};
        float arp_freq = arp_notes[(int)(bar_pos/(BEAT/2.0f))%16];
        float arp_t = fmodf(t, BEAT/2.0f);
        float arp_env = adsr(arp_t, 0.001f, 0.05f, 0.1f, 0.05f, 0, BEAT/2.0f*0.8f);
        float arp_raw = osc_saw(arp_freq, t) * 0.5f;
        float arp_filt = ladder(arp_raw * arp_env, &arp_f, 2000.0f + arp_env*3000.0f, 0.3f);
        mix += arp_filt * 0.3f;
        
        // CHORD STABS: beats 1 & 3
        float chord_freq = chord_root[beat_idx];
        if (chord_freq > 0) {
            float chord_t = fmodf(t, BAR/2.0f);
            float chord_env = adsr(chord_t, 0.01f, 0.3f, 0.4f, 0.5f, 0, BAR/2.0f*0.7f);
            float chord = osc_saw(chord_freq, t) + osc_saw(chord_freq*1.189f, t) + osc_saw(chord_freq*1.498f, t);
            float chord_filt = ladder(chord * chord_env, &chord_f, 800.0f, 0.2f);
            mix += chord_filt * 0.25f;
        }
        
        // DELAY (ping-pong)
        float dtime = 0.375f;
        int ds = (int)(dtime * 44100.0f);
        float fb = 0.35f;
        float dry = mix;
        float dl_out = delay_l[(dl + 44100 - ds) % 44100];
        float dr_out = delay_r[(dl + 44100 - ds) % 44100];
        delay_l[dl] = dry + dr_out * fb;
        delay_r[dl] = dry + dl_out * fb;
        mix += (dl_out + dr_out) * 0.15f;
        dl = (dl + 1) % 44100;
        
        // Master
        float out = tanhf(mix * 0.7f);
        int16_t s = (int16_t)(out * 32767.0f);
        buf[i*2] = s; buf[i*2+1] = s;
    }
    
    FILE *f = fopen("banger_30s.wav","wb");
    fwrite("RIFF",1,4,f); uint32_t total=36+samples*4; fwrite(&total,4,1,f);
    fwrite("WAVE",1,4,f); fwrite("fmt ",1,4,f); uint32_t fmt=16; fwrite(&fmt,4,1,f);
    uint16_t ft=1; fwrite(&ft,2,1,f); uint16_t ch=2; fwrite(&ch,2,1,f);
    uint32_t sru=44100; fwrite(&sru,4,1,f); uint32_t br=44100*4; fwrite(&br,4,1,f);
    uint16_t ba=4; fwrite(&ba,2,1,f); uint16_t bits=16; fwrite(&bits,2,1,f);
    fwrite("data",1,4,f); fwrite(&(uint32_t){samples*4},4,1,f);
    fwrite(buf,2,samples*2,f); fclose(f); free(buf);
    printf("banger_30s.wav - 120 BPM, kick/hat/bass/arp/chords/delay\n");
    return 0;
}
