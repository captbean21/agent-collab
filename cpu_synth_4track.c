// cpu_synth.c — 4 tracks, 15s each
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

#define SAMPLE_RATE 44100.0f
#define DURATION 15.0f
#define PI 3.14159265358979323846f
#define TWO_PI 6.28318530717958647692f

typedef struct {
    float bpm;
    float osc1_freq;
    float osc1_shape;
    float osc1_detune;
    float osc2_freq_ratio;
    float osc2_shape;
    float osc2_level;
    float filter_cutoff;
    float filter_res;
    float filter_env_amt;
    float env_attack;
    float env_decay;
    float env_sustain;
    float env_release;
    float fenv_attack;
    float fenv_decay;
    float fenv_sustain;
    float fenv_release;
    float arp_rate;
    int arp_pattern;
    int arp_octaves;
    float delay_time;
    float delay_feedback;
    float delay_mix;
    float master_gain;
} Patch;

Patch neon_motorway() {
    return (Patch){
        .bpm = 118.0f, .osc1_freq = 55.0f, .osc1_shape = 1.0f, .osc1_detune = 0.0f,
        .osc2_freq_ratio = 0.5f, .osc2_shape = 2.0f, .osc2_level = 0.3f,
        .filter_cutoff = 800.0f, .filter_res = 0.6f, .filter_env_amt = 1.0f,
        .env_attack = 0.01f, .env_decay = 0.3f, .env_sustain = 0.4f, .env_release = 0.5f,
        .fenv_attack = 0.001f, .fenv_decay = 0.2f, .fenv_sustain = 0.3f, .fenv_release = 0.3f,
        .arp_rate = 118.0f / 60.0f * 4.0f, .arp_pattern = 2, .arp_octaves = 2,
        .delay_time = 0.254f, .delay_feedback = 0.3f, .delay_mix = 0.2f, .master_gain = 0.5f,
    };
}

Patch dark_midnight() {
    return (Patch){
        .bpm = 105.0f, .osc1_freq = 41.2f, .osc1_shape = 0.5f, .osc1_detune = -5.0f,
        .osc2_freq_ratio = 0.5f, .osc2_shape = 0.0f, .osc2_level = 0.2f,
        .filter_cutoff = 400.0f, .filter_res = 0.3f, .filter_env_amt = 0.6f,
        .env_attack = 0.05f, .env_decay = 0.8f, .env_sustain = 0.6f, .env_release = 1.2f,
        .fenv_attack = 0.01f, .fenv_decay = 0.5f, .fenv_sustain = 0.4f, .fenv_release = 0.5f,
        .arp_rate = 105.0f / 60.0f * 2.0f, .arp_pattern = 1, .arp_octaves = 1,
        .delay_time = 0.571f, .delay_feedback = 0.4f, .delay_mix = 0.25f, .master_gain = 0.45f,
    };
}

Patch arcade_highway() {
    return (Patch){
        .bpm = 125.0f, .osc1_freq = 69.3f, .osc1_shape = 1.5f, .osc1_detune = 3.0f,
        .osc2_freq_ratio = 0.5f, .osc2_shape = 1.0f, .osc2_level = 0.4f,
        .filter_cutoff = 2000.0f, .filter_res = 0.7f, .filter_env_amt = 1.2f,
        .env_attack = 0.005f, .env_decay = 0.15f, .env_sustain = 0.3f, .env_release = 0.2f,
        .fenv_attack = 0.001f, .fenv_decay = 0.1f, .fenv_sustain = 0.2f, .fenv_release = 0.15f,
        .arp_rate = 125.0f / 60.0f * 4.0f, .arp_pattern = 0, .arp_octaves = 3,
        .delay_time = 0.120f, .delay_feedback = 0.25f, .delay_mix = 0.15f, .master_gain = 0.55f,
    };
}

// EXTRA TRACK: Retro sunrise - 90 BPM, warm pads, slow evolving
Patch retro_sunrise() {
    return (Patch){
        .bpm = 90.0f, .osc1_freq = 32.7f, .osc1_shape = 0.3f, .osc1_detune = -3.0f,  // C1
        .osc2_freq_ratio = 0.25f, .osc2_shape = 0.0f, .osc2_level = 0.15f,  // two octaves down sine
        .filter_cutoff = 600.0f, .filter_res = 0.2f, .filter_env_amt = 0.8f,
        .env_attack = 0.5f, .env_decay = 2.0f, .env_sustain = 0.8f, .env_release = 3.0f,
        .fenv_attack = 0.1f, .fenv_decay = 1.0f, .fenv_sustain = 0.5f, .fenv_release = 1.0f,
        .arp_rate = 90.0f / 60.0f * 1.0f, .arp_pattern = 2, .arp_octaves = 1,  // quarter notes, updown
        .delay_time = 0.667f, .delay_feedback = 0.35f, .delay_mix = 0.3f, .master_gain = 0.4f,
    };
}

float oscillator(float phase, float shape) {
    float s = floorf(shape);
    float t = shape - s;
    float sine = sinf(phase * TWO_PI);
    float saw = phase * 2.0f - 1.0f;
    float square = (phase < 0.5f) ? 1.0f : -1.0f;
    float tri = 1.0f - 2.0f * fabsf(phase - 0.5f);
    if (s <= 0.0f) return sine;
    else if (s <= 1.0f) return sine + (saw - sine) * t;
    else if (s <= 2.0f) return saw + (square - saw) * t;
    else return square + (tri - square) * t;
}

typedef struct { float s1, s2, s3, s4; } FilterState;

float ladder_filter(float input, FilterState *fs, float cutoff, float res) {
    float f = cutoff / SAMPLE_RATE;
    if (f < 0.001f) f = 0.001f;
    if (f > 0.49f) f = 0.49f;
    float fb = res * 4.0f * (1.0f - f);
    input -= fs->s4 * fb;
    fs->s1 += f * (tanhf(input) - tanhf(fs->s1));
    fs->s2 += f * (tanhf(fs->s1) - tanhf(fs->s2));
    fs->s3 += f * (tanhf(fs->s2) - tanhf(fs->s3));
    fs->s4 += f * (tanhf(fs->s3) - tanhf(fs->s4));
    return fs->s4;
}

float adsr(float t, float attack, float decay, float sustain, float release, float note_on, float note_off) {
    if (t < note_on) return 0.0f;
    if (t < note_off) {
        float dt = t - note_on;
        if (dt < attack) return dt / attack;
        dt -= attack;
        if (dt < decay) return 1.0f - (1.0f - sustain) * (dt / decay);
        return sustain;
    } else {
        float dt = t - note_off;
        float val = sustain * (1.0f - dt / release);
        return val > 0.0f ? val : 0.0f;
    }
}

void write_wav_header(FILE *f, int sample_count, int channels) {
    int data_len = sample_count * channels * 2;
    int riff_len = 36 + data_len;
    fwrite("RIFF", 1, 4, f);
    uint32_t riff = (uint32_t)riff_len; fwrite(&riff, 4, 1, f);
    fwrite("WAVE", 1, 4, f);
    fwrite("fmt ", 1, 4, f);
    uint32_t fmt_size = 16; fwrite(&fmt_size, 4, 1, f);
    uint16_t audio_fmt = 1; fwrite(&audio_fmt, 2, 1, f);
    uint16_t ch = (uint16_t)channels; fwrite(&ch, 2, 1, f);
    uint32_t sr = (uint32_t)SAMPLE_RATE; fwrite(&sr, 4, 1, f);
    uint32_t byte_rate = (uint32_t)(SAMPLE_RATE * channels * 2); fwrite(&byte_rate, 4, 1, f);
    uint16_t block_align = (uint16_t)(channels * 2); fwrite(&block_align, 2, 1, f);
    uint16_t bits = 16; fwrite(&bits, 2, 1, f);
    fwrite("data", 1, 4, f);
    uint32_t dl = (uint32_t)data_len; fwrite(&dl, 4, 1, f);
}

void generate(Patch patch, const char *filename) {
    int sample_count = (int)(SAMPLE_RATE * DURATION);
    int16_t *samples = malloc(sample_count * 2 * sizeof(int16_t));
    int scale[5] = {0, 3, 5, 7, 10};
    FilterState fs = {0, 0, 0, 0};
    int delay_buf_size = (int)(SAMPLE_RATE * 2.0f);
    float *delay_buf = calloc(delay_buf_size, sizeof(float));
    int delay_pos = 0;
    for (int i = 0; i < sample_count; i++) {
        float t = (float)i / SAMPLE_RATE;
        float note_period = 1.0f / patch.arp_rate;
        int note_idx = (int)floorf(t / note_period);
        int pattern_idx;
        if (patch.arp_pattern == 0) pattern_idx = note_idx % 5;
        else if (patch.arp_pattern == 1) pattern_idx = 4 - (note_idx % 5);
        else { int cycle = note_idx % 8; pattern_idx = (cycle < 5) ? cycle : 8 - cycle; }
        int octave = (note_idx / 5) % patch.arp_octaves;
        if (octave < 0) octave += patch.arp_octaves;
        int semitones = scale[pattern_idx] + octave * 12;
        float freq_mul = powf(2.0f, semitones / 12.0f);
        float detune_mul = powf(2.0f, patch.osc1_detune / 1200.0f);
        float phase1 = fmodf(t * patch.osc1_freq * freq_mul * detune_mul, 1.0f);
        float phase2 = fmodf(t * patch.osc1_freq * freq_mul * patch.osc2_freq_ratio, 1.0f);
        float osc1 = oscillator(phase1, patch.osc1_shape);
        float osc2 = oscillator(phase2, patch.osc2_shape) * patch.osc2_level;
        float mixed = osc1 + osc2;
        float note_start = (float)note_idx * note_period;
        float note_t = t - note_start;
        float note_off = note_period * 0.9f;
        float amp_env = (note_t < 0.0f) ? 0.0f : adsr(note_t, patch.env_attack, patch.env_decay, patch.env_sustain, patch.env_release, 0.0f, note_off);
        float filt_env = (note_t < 0.0f) ? 0.0f : adsr(note_t, patch.fenv_attack, patch.fenv_decay, patch.fenv_sustain, patch.fenv_release, 0.0f, note_off);
        float cutoff_mod = patch.filter_cutoff + filt_env * patch.filter_env_amt * 5000.0f;
        float filtered = ladder_filter(mixed * amp_env, &fs, cutoff_mod, patch.filter_res);
        int delay_samples = (int)(patch.delay_time * SAMPLE_RATE);
        int delay_idx = (delay_pos + delay_buf_size - delay_samples) % delay_buf_size;
        float delayed = delay_buf[delay_idx];
        float out = filtered * (1.0f - patch.delay_mix) + delayed * patch.delay_mix;
        delay_buf[delay_pos] = filtered + delayed * patch.delay_feedback;
        delay_pos = (delay_pos + 1) % delay_buf_size;
        float final_out = tanhf(out * patch.master_gain);
        int16_t s16 = (int16_t)(final_out * 32767.0f);
        if (s16 > 32767) s16 = 32767;
        if (s16 < -32768) s16 = -32768;
        samples[i * 2] = s16;
        samples[i * 2 + 1] = s16;
    }
    FILE *f = fopen(filename, "wb");
    if (!f) { perror("fopen"); free(samples); free(delay_buf); return; }
    write_wav_header(f, sample_count, 2);
    fwrite(samples, 2, sample_count * 2, f);
    fclose(f);
    free(samples);
    free(delay_buf);
    printf("Generated %s (%.1fs, %d samples, stereo)\n", filename, DURATION, sample_count);
}

int main() {
    printf("CPU Synth - Generating 4 tracks at 15s...\n");
    generate(neon_motorway(), "track1_neon_motorway.wav");
    generate(dark_midnight(), "track2_dark_midnight.wav");
    generate(arcade_highway(), "track3_arcade_highway.wav");
    generate(retro_sunrise(), "track4_retro_sunrise.wav");
    printf("Done. 4 WAV files created.\n");
    return 0;
}
