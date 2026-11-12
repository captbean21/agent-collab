#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define SAMPLE_RATE 44100
#define BUFFER_SIZE 44100
#define TOTAL_SECONDS 90
#define TOTAL_SAMPLES (SAMPLE_RATE * TOTAL_SECONDS)
#define BPM 110.0
#define BEATS_PER_BAR 4.0
#define BAR_SECONDS (60.0 / BPM * BEATS_PER_BAR)
#define EIGHTH_SECONDS (BAR_SECONDS / 8.0)
#define SIXTEENTH_SECONDS (BAR_SECONDS / 16.0)
#define DOTTED_EIGHTH_SECONDS (EIGHTH_SECONDS * 1.5)

#define KICK_GAIN 0.8f
#define SNARE_GAIN 0.6f
#define HAT_CLOSED_GAIN 0.3f
#define HAT_OPEN_GAIN 0.4f
#define CLAP_GAIN 0.4f
#define SUB_BASS_GAIN 0.7f
#define MID_BASS_GAIN 0.5f
#define LEAD_GAIN 0.6f
#define PAD1_GAIN 0.4f
#define PAD2_GAIN 0.3f
#define CHORD_GAIN 0.5f
#define DELAY_FEEDBACK_START 0.35f
#define DELAY_FEEDBACK_END 0.50f
#define REVERB_TIME 2.5f
#define REVERB_GAIN 0.3f
#define SOFT_CLIP_THRESHOLD 0.8f
#define LIMITER_THRESHOLD 0.95f

typedef struct {
    float left[BUFFER_SIZE];
    float right[BUFFER_SIZE];
    int write_index;
} AudioBuffer;

typedef struct {
    float delay_buffer[BUFFER_SIZE];
    int write_index;
    float feedback;
} DelayLine;

typedef struct {
    float buffer[BUFFER_SIZE];
    int write_index;
    float decay;
} ReverbLine;

typedef struct {
    float phase;
    float freq;
} Oscillator;

typedef struct {
    float phase;
    float freq;
    float cutoff;
    float resonance;
} Filter;

void init_audio_buffer(AudioBuffer *buf) {
    memset(buf->left, 0, sizeof(buf->left));
    memset(buf->right, 0, sizeof(buf->right));
    buf->write_index = 0;
}

void init_delay_line(DelayLine *dl) {
    memset(dl->delay_buffer, 0, sizeof(dl->delay_buffer));
    dl->write_index = 0;
    dl->feedback = DELAY_FEEDBACK_START;
}

void init_reverb_line(ReverbLine *rl) {
    memset(rl->buffer, 0, sizeof(rl->buffer));
    rl->write_index = 0;
    rl->decay = expf(-1.0f / REVERB_TIME);
}

float sine_wave(float phase) {
    return sinf(phase);
}

float saw_wave(float phase) {
    float normalized = phase / (2.0f * M_PI);
    normalized -= floorf(normalized);
    return 2.0f * normalized - 1.0f;
}

float square_wave(float phase) {
    float normalized = phase / (2.0f * M_PI);
    normalized -= floorf(normalized);
    return (normalized < 0.5f) ? 1.0f : -1.0f;
}

float triangle_wave(float phase) {
    float normalized = phase / (2.0f * M_PI);
    normalized -= floorf(normalized);
    if (normalized < 0.5f) {
        return 4.0f * normalized - 1.0f;
    } else {
        return 3.0f - 4.0f * normalized;
    }
}

float soft_clip(float x) {
    if (x > SOFT_CLIP_THRESHOLD) {
        return SOFT_CLIP_THRESHOLD + (x - SOFT_CLIP_THRESHOLD) * 0.5f;
    } else if (x < -SOFT_CLIP_THRESHOLD) {
        return -SOFT_CLIP_THRESHOLD + (x + SOFT_CLIP_THRESHOLD) * 0.5f;
    }
    return x;
}

float limiter(float x) {
    if (x > LIMITER_THRESHOLD) {
        return LIMITER_THRESHOLD;
    } else if (x < -LIMITER_THRESHOLD) {
        return -LIMITER_THRESHOLD;
    }
    return x;
}

float clamp(float x) {
    if (x > 1.0f) return 1.0f;
    if (x < -1.0f) return -1.0f;
    return x;
}

int main() {
    AudioBuffer audio;
    init_audio_buffer(&audio);

    DelayLine delay;
    init_delay_line(&delay);

    ReverbLine reverb;
    init_reverb_line(&reverb);

    Oscillator sub_bass;
    sub_bass.phase = 0.0f;
    sub_bass.freq = 35.0f;

    Oscillator mid_bass_saw;
    mid_bass_saw.phase = 0.0f;
    mid_bass_saw.freq = 110.0f;

    Oscillator mid_bass_square;
    mid_bass_square.phase = 0.0f;
    mid_bass_square.freq = 110.0f;

    Filter mid_bass_filter;
    mid_bass_filter.phase = 0.0f;
    mid_bass_filter.freq = 110.0f;
    mid_bass_filter.cutoff = 500.0f;
    mid_bass_filter.resonance = 0.7f;

    Oscillator lead_osc;
    lead_osc.phase = 0.0f;
    lead_osc.freq = 440.0f;

    Filter lead_filter;
    lead_filter.phase = 0.0f;
    lead_filter.freq = 440.0f;
    lead_filter.cutoff = 2000.0f;
    lead_filter.resonance = 0.5f;

    Oscillator pad1_saw;
    pad1_saw.phase = 0.0f;
    pad1_saw.freq = 220.0f;

    Oscillator pad1_square;
    pad1_square.phase = 0.0f;
    pad1_square.freq = 220.0f;

    Filter pad1_filter;
    pad1_filter.phase = 0.0f;
    pad1_filter.freq = 220.0f;
    pad1_filter.cutoff = 150.0f;
    pad1_filter.resonance = 0.3f;

    Oscillator pad2_sine;
    pad2_sine.phase = 0.0f;
    pad2_sine.freq = 880.0f;

    Oscillator pad2_triangle;
    pad2_triangle.phase = 0.0f;
    pad2_triangle.freq = 880.0f;

    // Minor pentatonic scale: A, C, D, E, G (relative to A minor)
    // Frequencies for A minor pentatonic (A3, C4, D4, E4, G4)
    float pentatonic[5] = {220.0f, 261.63f, 293.66f, 329.63f, 392.0f};
    // 2 octaves up-down pattern: A3, C4, D4, E4, G4, A4, G4, E4, D4, C4, A3, G3, E3, D3, C3, A2
    // Simplified: just use the 5 notes and cycle up-down
    int pentatonic_index = 0;
    int pentatonic_direction = 1;

    // Chord frequencies for minor 7 and major 7 stabs
    // Am7: A, C, E, G
    float am7[4] = {220.0f, 261.63f, 329.63f, 392.0f};
    // Cmaj7: C, E, G, B
    float cmaj7[4] = {261.63f, 329.63f, 392.0f, 493.88f};

    int current_bar = 0;
    float bar_time = 0.0f;
    float total_time = 0.0f;

    // Structure: intro(10)/verse(15)/chorus(15)/bridge(15)/chorus(15)/outro(20)
    int section = 0; // 0: intro, 1: verse, 2: chorus, 3: bridge, 4: chorus, 5: outro
    float section_start_time = 0.0f;
    float section_duration = 10.0f;

    for (int i = 0; i < TOTAL_SAMPLES; i++) {
        float sample_left = 0.0f;
        float sample_right = 0.0f;

        // Update time and section
        total_time = (float)i / SAMPLE_RATE;
        if (total_time >= section_start_time + section_duration) {
            section_start_time += section_duration;
            section++;
            if (section == 1) section_duration = 15.0f;
            else if (section == 2) section_duration = 15.0f;
            else if (section == 3) section_duration = 15.0f;
            else if (section == 4) section_duration = 15.0f;
            else if (section == 5) section_duration = 20.0f;
        }

        float section_time = total_time - section_start_time;
        float bar_in_section = section_time / BAR_SECONDS;
        int current_bar_in_section = (int)bar_in_section;
        float bar_fraction = bar_in_section - current_bar_in_section;
        int beat_in_bar = (int)(bar_fraction * BEATS_PER_BAR);
        float beat_fraction = (bar_fraction * BEATS_PER_BAR) - beat_in_bar;
        int eighth_in_bar = (int)(bar_fraction * 8.0f);
        float eighth_fraction = (bar_fraction * 8.0f) - eighth_in_bar;
        int sixteenth_in_bar = (int)(bar_fraction * 16.0f);
        float sixteenth_fraction = (bar_fraction * 16.0f) - sixteenth_in_bar;

        // Update delay feedback
        float progress = total_time / TOTAL_SECONDS;
        delay.feedback = DELAY_FEEDBACK_START + (DELAY_FEEDBACK_END - DELAY_FEEDBACK_START) * progress;

        // Update pad1 filter sweep (150Hz -> 2500Hz over 60s)
        if (section >= 1 && section <= 4) {
            float sweep_progress = section_time / 60.0f;
            if (sweep_progress > 1.0f) sweep_progress = 1.0f;
            pad1_filter.cutoff = 150.0f + (2500.0f - 150.0f) * sweep_progress;
        }

        // DRUMS
        if (section >= 1 && section <= 4) {
            // Kick on beat 1
            if (beat_in_bar == 0 && beat_fraction < 0.1f) {
                float kick_env = 1.0f - beat_fraction / 0.1f;
                float kick_sample = sine_wave(sub_bass.phase) * kick_env * KICK_GAIN;
                sample_left += kick_sample;
                sample_right += kick_sample;
            }

            // Snare on beats 2 & 4
            if ((beat_in_bar == 1 || beat_in_bar == 3) && beat_fraction < 0.1f) {
                float snare_env = 1.0f - beat_fraction / 0.1f;
                float snare_sample = (rand() % 2 == 0 ? 1.0f : -1.0f) * snare_env * SNARE_GAIN;
                sample_left += snare_sample;
                sample_right += snare_sample;

                // Clap layer on snare
                float clap_env = 1.0f - beat_fraction / 0.1f;
                float clap_sample = (rand() % 2 == 0 ? 1.0f : -1.0f) * clap_env * CLAP_GAIN;
                sample_left += clap_sample;
                sample_right += clap_sample;
            }

            // Hats on 8ths with closed/open variation
            if (eighth_fraction < 0.05f) {
                float hat_env = 1.0f - eighth_fraction / 0.05f;
                float hat_gain = (eighth_in_bar % 2 == 0) ? HAT_CLOSED_GAIN : HAT_OPEN_GAIN;
                float hat_sample = (rand() % 2 == 0 ? 1.0f : -1.0f) * hat_env * hat_gain;
                sample_left += hat_sample;
                sample_right += hat_sample;
            }
        }

        // BASS
        if (section >= 1 && section <= 4) {
            // Sub sine 35Hz sidechained to kick (-12dB)
            float kick_level = 0.0f;
            if (beat_in_bar == 0 && beat_fraction < 0.1f) {
                kick_level = 1.0f - beat_fraction / 0.1f;
            }
            float sidechain_gain = 1.0f - (kick_level * 0.5f); // -12dB approx
            float sub_sample = sine_wave(sub_bass.phase) * SUB_BASS_GAIN * sidechain_gain;
            sample_left += sub_sample;
            sample_right += sub_sample;

            // Mid saw+square 16th pattern with filter envelope
            if (sixteenth_fraction < 0.1f) {
                float bass_env = 1.0f - sixteenth_fraction / 0.1f;
                float saw_sample = saw_wave(mid_bass_saw.phase) * bass_env;
                float square_sample = square_wave(mid_bass_square.phase) * bass_env;
                float mid_bass_sample = (saw_sample + square_sample) * 0.5f * MID_BASS_GAIN;
                sample_left += mid_bass_sample;
                sample_right += mid_bass_sample;
            }
        }

        // LEAD: minor pentatonic arp 8th notes, 2 octaves up-down, velocity humanized ±30%
        if (section >= 1 && section <= 4) {
            if (eighth_fraction < 0.1f) {
                float velocity = 1.0f + (rand() % 60 - 30) / 100.0f; // ±30%
                float lead_freq = pentatonic[pentatonic_index];
                lead_osc.freq = lead_freq;
                float lead_sample = sine_wave(lead_osc.phase) * LEAD_GAIN * velocity;
                sample_left += lead_sample;
                sample_right += lead_sample;

                // Update pentatonic index
                pentatonic_index += pentatonic_direction;
                if (pentatonic_index >= 5) {
                    pentatonic_index = 4;
                    pentatonic_direction = -1;
                } else if (pentatonic_index <= 0) {
                    pentatonic_index = 0;
                    pentatonic_direction = 1;
                }
            }
        }

        // PADS
        if (section >= 1 && section <= 4) {
            // Pad1 wide saw+sq (Haas 25ms), slow attack 3s, filter sweep
            float pad1_attack = section_time / 3.0f;
            if (pad1_attack > 1.0f) pad1_attack = 1.0f;
            float pad1_sample_left = (saw_wave(pad1_saw.phase) + square_wave(pad1_square.phase)) * 0.5f * PAD1_GAIN * pad1_attack;
            float pad1_sample_right = (saw_wave(pad1_saw.phase + 0.1f) + square_wave(pad1_square.phase + 0.1f)) * 0.5f * PAD1_GAIN * pad1_attack; // Haas 25ms approx
            sample_left += pad1_sample_left;
            sample_right += pad1_sample_right;
        }

        // Pad2 shimmer sine+triangle on chorus
        if (section == 2 || section == 4) {
            float pad2_sample_left = (sine_wave(pad2_sine.phase) + triangle_wave(pad2_triangle.phase)) * 0.5f * PAD2_GAIN;
            float pad2_sample_right = (sine_wave(pad2_sine.phase + 0.2f) + triangle_wave(pad2_triangle.phase + 0.2f)) * 0.5f * PAD2_GAIN;
            sample_left += pad2_sample_left;
            sample_right += pad2_sample_right;
        }

        // CHORDS: minor 7 / major 7 stabs on beats 1&3 (chorus only)
        if (section == 2 || section == 4) {
            if ((beat_in_bar == 0 || beat_in_bar == 2) && beat_fraction < 0.1f) {
                float chord_env = 1.0f - beat_fraction / 0.1f;
                float chord_sample = 0.0f;
                for (int j = 0; j < 4; j++) {
                    chord_sample += sine_wave(beat_fraction * 100.0f + j * 0.1f) * chord_env;
                }
                chord_sample *= CHORD_GAIN;
                sample_left += chord_sample;
                sample_right += chord_sample;
            }
        }

        // FX: ping-pong delay dotted 8th (35%→50% feedback)
        int delay_samples = (int)(DOTTED_EIGHTH_SECONDS * SAMPLE_RATE);
        int delay_read_index = (delay.write_index - delay_samples + BUFFER_SIZE) % BUFFER_SIZE;
        float delayed_sample = delay.delay_buffer[delay_read_index % BUFFER_SIZE];
        sample_left += delayed_sample * delay.feedback;
        sample_right += delayed_sample * delay.feedback;

        // Reverb on pads (2.5s)
        float reverb_sample = reverb.buffer[reverb.write_index % BUFFER_SIZE] * reverb.decay;
        sample_left += reverb_sample * REVERB_GAIN;
        sample_right += reverb_sample * REVERB_GAIN;

        // Update oscillators
        sub_bass.phase += 2.0f * M_PI * sub_bass.freq / SAMPLE_RATE;
        if (sub_bass.phase >= 2.0f * M_PI) sub_bass.phase -= 2.0f * M_PI;

        mid_bass_saw.phase += 2.0f * M_PI * mid_bass_saw.freq / SAMPLE_RATE;
        if (mid_bass_saw.phase >= 2.0f * M_PI) mid_bass_saw.phase -= 2.0f * M_PI;

        mid_bass_square.phase += 2.0f * M_PI * mid_bass_square.freq / SAMPLE_RATE;
        if (mid_bass_square.phase >= 2.0f * M_PI) mid_bass_square.phase -= 2.0f * M_PI;

        lead_osc.phase += 2.0f * M_PI * lead_osc.freq / SAMPLE_RATE;
        if (lead_osc.phase >= 2.0f * M_PI) lead_osc.phase -= 2.0f * M_PI;

        pad1_saw.phase += 2.0f * M_PI * pad1_saw.freq / SAMPLE_RATE;
        if (pad1_saw.phase >= 2.0f * M_PI) pad1_saw.phase -= 2.0f * M_PI;

        pad1_square.phase += 2.0f * M_PI * pad1_square.freq / SAMPLE_RATE;
        if (pad1_square.phase >= 2.0f * M_PI) pad1_square.phase -= 2.0f * M_PI;

        pad2_sine.phase += 2.0f * M_PI * pad2_sine.freq / SAMPLE_RATE;
        if (pad2_sine.phase >= 2.0f * M_PI) pad2_sine.phase -= 2.0f * M_PI;

        pad2_triangle.phase += 2.0f * M_PI * pad2_triangle.freq / SAMPLE_RATE;
        if (pad2_triangle.phase >= 2.0f * M_PI) pad2_triangle.phase -= 2.0f * M_PI;

        // MASTER: soft clip + limiter
        sample_left = soft_clip(sample_left);
        sample_right = soft_clip(sample_right);
        sample_left = limiter(sample_left);
        sample_right = limiter(sample_right);

        // Clamp to -1.0f to 1.0f
        sample_left = clamp(sample_left);
        sample_right = clamp(sample_right);

        // Write to audio buffer
        int write_idx = audio.write_index % BUFFER_SIZE;
        audio.left[write_idx] = sample_left;
        audio.right[write_idx] = sample_right;
        audio.write_index++;

        // Update delay line
        delay.delay_buffer[delay.write_index % BUFFER_SIZE] = sample_left;
        delay.write_index++;

        // Update reverb line
        reverb.buffer[reverb.write_index % BUFFER_SIZE] = sample_left;
        reverb.write_index++;
    }

    // Write WAV file
    FILE *fp = fopen("night_drive_90s.wav", "wb");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    // WAV header

    fwrite("RIFF", 1, 4, fp);
    fwrite(&(int){44 + TOTAL_SAMPLES * 2 * sizeof(int16_t)}, 1, 4, fp);
    fwrite("WAVE", 1, 4, fp);
    fwrite("fmt ", 1, 4, fp);
    int32_t fmt_chunk_size = 16;
    fwrite(&fmt_chunk_size, 1, 4, fp);
    int16_t audio_format = 1;
    fwrite(&audio_format, 1, 2, fp);
    int16_t channels = 2;
    fwrite(&channels, 1, 2, fp);
    fwrite(&(int32_t){SAMPLE_RATE}, 1, 4, fp); // fixed: use macro value directly
    int32_t byte_rate = SAMPLE_RATE * 2 * 16 / 8;
    fwrite(&byte_rate, 1, 4, fp);
    int16_t block_align = 2 * 16 / 8;
    fwrite(&block_align, 1, 2, fp);
    int16_t bits = 16;
    fwrite(&bits, 1, 2, fp);
    fwrite("data", 1, 4, fp);
    int32_t data_size = TOTAL_SAMPLES * 2 * sizeof(int16_t);
    fwrite(&data_size, 1, 4, fp);

    for (int i = 0; i < TOTAL_SAMPLES; i++) {
        int idx = i % BUFFER_SIZE;
        int16_t left = (int16_t)(audio.left[idx] * 32767.0f);
        int16_t right = (int16_t)(audio.right[idx] * 32767.0f);
        fwrite(&left, 1, 2, fp);
        fwrite(&right, 1, 2, fp);
    }
    fclose(fp);




















    printf("Wrote night_drive_90s.wav\n");
    return 0;
}
