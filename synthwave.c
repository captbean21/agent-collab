#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define SAMPLE_RATE 44100
#define BUFFER_SIZE 4096
#define NUM_VOICES 4
#define NUM_PATTERNS 4
#define STEPS_PER_BAR 16
#define BARS_PER_SECTION 8
#define NUM_SECTIONS 6
#define BPM 128.0f
#define MASTER_GAIN 0.5f
#define OUTPUT_FILE "track.wav"

/* ADSR Envelope */
typedef struct {
    float attack;
    float decay;
    float sustain;
    float release;
    float current;
    int state; /* 0: idle, 1: attack, 2: decay, 3: sustain, 4: release */
    float time;
} ADSR;

/* FM Voice (DX7 style) */
typedef struct {
    float carrier_freq;
    float modulator_freq;
    float modulation_index;
    float carrier_phase;
    float modulator_phase;
    ADSR env;
    float level;
} FMVoice;

/* Analog Voice (Saw/Square with PWM) */
typedef struct {
    float freq;
    float phase;
    float pwm_phase;
    float pwm_rate;
    float pwm_width;
    float is_saw;
    ADSR env;
    float level;
} AnalogVoice;

/* State Variable Filter */
typedef struct {
    float q;
    float g;
    float x1, x2, y1, y2;
    float cutoff;
} SVFilter;

/* Delay Line */
typedef struct {
    float buffer[BUFFER_SIZE];
    int index;
    float delay_time;
    float feedback;
    float wet;
} DelayLine;

/* Reverb (Schroeder) */
typedef struct {
    float comb1[BUFFER_SIZE];
    float comb2[BUFFER_SIZE];
    int comb_idx;
    float allpass1[BUFFER_SIZE];
    float allpass2[BUFFER_SIZE];
    int allpass_idx;
    float comb_fb;
    float allpass_fb;
    float wet;
} Reverb;

/* Noise Generator */
typedef struct {
    float phase;
    float level;
} NoiseGen;

/* Voice State */
typedef struct {
    FMVoice fm;
    AnalogVoice analog;
    SVFilter filter;
    int active;
    float last_freq;
} Voice;

/* Pattern Step */
typedef struct {
    int note;
    int velocity;
    int voice;
} Step;

/* Pattern */
typedef struct {
    Step steps[STEPS_PER_BAR];
} Pattern;

/* Song Section */
typedef struct {
    int pattern;
    int bars;
} Section;

/* Global State */
static Voice voices[NUM_VOICES];
static NoiseGen noise;
static DelayLine delay_l, delay_r;
static Reverb reverb;
static Pattern patterns[NUM_PATTERNS];
static Section sections[NUM_SECTIONS];
static int current_section = 0;
static int current_bar = 0;
static int current_step = 0;
static int last_step = -1;
static float total_samples = 0;
static float target_samples = 0;

/* Initialize ADSR */
void adsr_init(ADSR *env, float a, float d, float s, float r) {
    env->attack = a;
    env->decay = d;
    env->sustain = s;
    env->release = r;
    env->current = 0.0f;
    env->state = 0;
    env->time = 0.0f;
}

void adsr_trigger(ADSR *env) {
    env->state = 1;
    env->time = 0.0f;
    env->current = 0.0f;
}

void adsr_release(ADSR *env) {
    if (env->state != 0) {
        env->state = 4;
        env->time = 0.0f;
    }
}

float adsr_update(ADSR *env) {
    float dt = 1.0f / SAMPLE_RATE;
    switch (env->state) {
        case 1: /* Attack */
            env->time += dt;
            if (env->time >= env->attack) {
                env->current = 1.0f;
                env->state = 2;
                env->time = 0.0f;
            } else {
                env->current = env->time / env->attack;
            }
            break;
        case 2: /* Decay */
            env->time += dt;
            if (env->time >= env->decay) {
                env->current = env->sustain;
                env->state = 3;
                env->time = 0.0f;
            } else {
                env->current = 1.0f - (1.0f - env->sustain) * (env->time / env->decay);
            }
            break;
        case 3: /* Sustain */
            env->current = env->sustain;
            break;
        case 4: /* Release */
            env->time += dt;
            if (env->time >= env->release) {
                env->current = 0.0f;
                env->state = 0;
                env->time = 0.0f;
            } else {
                env->current = env->sustain * (1.0f - env->time / env->release);
            }
            break;
        default:
            env->current = 0.0f;
            break;
    }
    return env->current;
}

/* Initialize SV Filter */
void svf_init(SVFilter *f, float cutoff, float q) {
    f->cutoff = cutoff;
    f->q = q;
    f->x1 = 0.0f;
    f->x2 = 0.0f;
    f->y1 = 0.0f;
    f->y2 = 0.0f;
    /* g is related to cutoff and q */
    f->g = 2.0f * sinf((cutoff / SAMPLE_RATE) * M_PI);
}

float svf_process(SVFilter *f, float input) {
    float x1 = f->x1;
    float x2 = f->x2;
    float y1 = f->y1;
    float y2 = f->y2;
    
    float g = f->g;
    float q = f->q;
    
    float x1_new = input - g * y1;
    float y1_new = x1 - g * x2;
    float x2_new = x1_new - g * y2;
    float y2_new = x2 - g * x1_new;
    
    f->x1 = x1_new;
    f->x2 = x2_new;
    f->y1 = y1_new;
    f->y2 = y2_new;
    
    /* Lowpass output */
    return y2_new;
}

/* Initialize Delay */
void delay_init(DelayLine *d, float delay_time, float feedback, float wet) {
    memset(d->buffer, 0, sizeof(d->buffer));
    d->index = 0;
    d->delay_time = delay_time;
    d->feedback = feedback;
    d->wet = wet;
}

float delay_process(DelayLine *d, float input) {
    int delay_samples = (int)(d->delay_time * SAMPLE_RATE);
    if (delay_samples >= BUFFER_SIZE) delay_samples = BUFFER_SIZE - 1;
    
    float out = d->buffer[d->index];
    d->buffer[d->index] = input + out * d->feedback;
    d->index = (d->index + 1) % BUFFER_SIZE;
    
    return input + out * d->wet;
}

/* Initialize Reverb */
void reverb_init(Reverb *r, float wet) {
    memset(r->comb1, 0, sizeof(r->comb1));
    memset(r->comb2, 0, sizeof(r->comb2));
    memset(r->allpass1, 0, sizeof(r->allpass1));
    memset(r->allpass2, 0, sizeof(r->allpass2));
    r->comb_idx = 0;
    r->allpass_idx = 0;
    r->comb_fb = 0.5f;
    r->allpass_fb = 0.5f;
    r->wet = wet;
}

float reverb_process(Reverb *r, float input) {
    /* Comb Filter 1 */
    int c1_idx = r->comb_idx;
    float c1_out = r->comb1[c1_idx];
    r->comb1[c1_idx] = input - r->comb_fb * c1_out;
    r->comb_idx = (r->comb_idx + 1) % BUFFER_SIZE;
    
    /* Comb Filter 2 */
    int c2_idx = r->comb_idx;
    float c2_out = r->comb2[c2_idx];
    r->comb2[c2_idx] = c1_out - r->comb_fb * c2_out;
    r->comb_idx = (r->comb_idx + 1) % BUFFER_SIZE;
    
    /* Allpass 1 */
    int a1_idx = r->allpass_idx;
    float a1_out = r->allpass1[a1_idx];
    r->allpass1[a1_idx] = input - r->allpass_fb * a1_out;
    r->allpass_idx = (r->allpass_idx + 1) % BUFFER_SIZE;
    
    /* Allpass 2 */
    int a2_idx = r->allpass_idx;
    float a2_out = r->allpass2[a2_idx];
    r->allpass2[a2_idx] = c2_out - r->allpass_fb * a2_out;
    r->allpass_idx = (r->allpass_idx + 1) % BUFFER_SIZE;
    
    return input + (c2_out + a2_out) * r->wet;
}

/* Initialize FM Voice */
void fm_voice_init(FMVoice *v, float carrier, float mod, float index, float level) {
    v->carrier_freq = carrier;
    v->modulator_freq = mod;
    v->modulation_index = index;
    v->carrier_phase = 0.0f;
    v->modulator_phase = 0.0f;
    v->level = level;
    adsr_init(&v->env, 0.01f, 0.1f, 0.5f, 0.2f);
}

float fm_voice_process(FMVoice *v) {
    float env = adsr_update(&v->env);
    if (env == 0.0f) return 0.0f;
    
    float mod_val = sinf(v->modulator_phase);
    float carrier_freq_inst = v->carrier_freq + v->modulation_index * v->modulator_freq * mod_val;
    
    float sample = sinf(v->carrier_phase);
    
    /* Update phases */
    v->carrier_phase += (2.0f * M_PI * carrier_freq_inst) / SAMPLE_RATE;
    v->modulator_phase += (2.0f * M_PI * v->modulator_freq) / SAMPLE_RATE;
    
    while (v->carrier_phase >= 2.0f * M_PI) v->carrier_phase -= 2.0f * M_PI;
    while (v->modulator_phase >= 2.0f * M_PI) v->modulator_phase -= 2.0f * M_PI;
    
    return sample * env * v->level;
}

/* Initialize Analog Voice */
void analog_voice_init(AnalogVoice *v, float freq, float level, int is_saw) {
    v->freq = freq;
    v->phase = 0.0f;
    v->pwm_phase = 0.0f;
    v->pwm_rate = 5.0f;
    v->pwm_width = 0.5f;
    v->is_saw = is_saw;
    v->level = level;
    adsr_init(&v->env, 0.05f, 0.2f, 0.7f, 0.3f);
}

float analog_voice_process(AnalogVoice *v) {
    float env = adsr_update(&v->env);
    if (env == 0.0f) return 0.0f;
    
    float sample = 0.0f;
    if (v->is_saw) {
        sample = (v->phase / (2.0f * M_PI)) * 2.0f - 1.0f;
    } else {
        /* Square with PWM */
        float pwm_val = sinf(v->pwm_phase);
        float threshold = (v->pwm_width - 0.5f) * 2.0f;
        if (pwm_val > threshold) {
            sample = 1.0f;
        } else {
            sample = -1.0f;
        }
    }
    
    /* Update phases */
    v->phase += (2.0f * M_PI * v->freq) / SAMPLE_RATE;
    v->pwm_phase += (2.0f * M_PI * v->pwm_rate) / SAMPLE_RATE;
    
    while (v->phase >= 2.0f * M_PI) v->phase -= 2.0f * M_PI;
    while (v->pwm_phase >= 2.0f * M_PI) v->pwm_phase -= 2.0f * M_PI;
    
    return sample * env * v->level;
}

/* Initialize Noise */
void noise_init(NoiseGen *n, float level) {
    n->phase = 0.0f;
    n->level = level;
}

float noise_process(NoiseGen *n) {
    /* Simple white noise */
    float sample = (float)(rand() % 1000) / 500.0f - 1.0f;
    return sample * n->level;
}

/* Note Frequency */
float note_to_freq(int note) {
    if (note < 0) return 0.0f;
    float semitones_from_a4 = note - 69;
    return 440.0f * powf(2.0f, semitones_from_a4 / 12.0f);
}

/* Initialize Patterns */
void init_patterns() {
    /* Pattern A: Intro - Simple bass and lead */
    for (int i = 0; i < STEPS_PER_BAR; i++) {
        patterns[0].steps[i].note = -1;
        patterns[0].steps[i].velocity = 0;
        patterns[0].steps[i].voice = -1;
    }
    /* Bass on steps 0, 4, 8, 12 */
    patterns[0].steps[0].note = 33; /* A1 */
    patterns[0].steps[0].velocity = 100;
    patterns[0].steps[0].voice = 0;
    patterns[0].steps[4].note = 33;
    patterns[0].steps[4].velocity = 100;
    patterns[0].steps[4].voice = 0;
    patterns[0].steps[8].note = 33;
    patterns[0].steps[8].velocity = 100;
    patterns[0].steps[8].voice = 0;
    patterns[0].steps[12].note = 33;
    patterns[0].steps[12].velocity = 100;
    patterns[0].steps[12].voice = 0;
    
    /* Lead on steps 0, 6, 10 */
    patterns[0].steps[0].note = 69; /* A4 */
    patterns[0].steps[0].voice = 1;
    patterns[0].steps[6].note = 72; /* C5 */
    patterns[0].steps[6].voice = 1;
    patterns[0].steps[10].note = 74; /* D5 */
    patterns[0].steps[10].voice = 1;

    /* Pattern B: Verse - More complex */
    for (int i = 0; i < STEPS_PER_BAR; i++) {
        patterns[1].steps[i].note = -1;
        patterns[1].steps[i].velocity = 0;
        patterns[1].steps[i].voice = -1;
    }
    /* Bass */
    patterns[1].steps[0].note = 33;
    patterns[1].steps[0].velocity = 100;
    patterns[1].steps[0].voice = 0;
    patterns[1].steps[4].note = 33;
    patterns[1].steps[4].velocity = 100;
    patterns[1].steps[4].voice = 0;
    patterns[1].steps[8].note = 36; /* C2 */
    patterns[1].steps[8].velocity = 100;
    patterns[1].steps[8].voice = 0;
    patterns[1].steps[12].note = 33;
    patterns[1].steps[12].velocity = 100;
    patterns[1].steps[12].voice = 0;
    
    /* Lead */
    patterns[1].steps[0].note = 69;
    patterns[1].steps[0].voice = 1;
    patterns[1].steps[3].note = 71; /* B4 */
    patterns[1].steps[3].voice = 1;
    patterns[1].steps[6].note = 72;
    patterns[1].steps[6].voice = 1;
    patterns[1].steps[9].note = 74;
    patterns[1].steps[9].voice = 1;
    patterns[1].steps[12].note = 76; /* E5 */
    patterns[1].steps[12].voice = 1;

    /* Pattern C: Chorus - Energetic */
    for (int i = 0; i < STEPS_PER_BAR; i++) {
        patterns[2].steps[i].note = -1;
        patterns[2].steps[i].velocity = 0;
        patterns[2].steps[i].voice = -1;
    }
    /* Bass */
    patterns[2].steps[0].note = 33;
    patterns[2].steps[0].velocity = 100;
    patterns[2].steps[0].voice = 0;
    patterns[2].steps[2].note = 33;
    patterns[2].steps[2].velocity = 100;
    patterns[2].steps[2].voice = 0;
    patterns[2].steps[4].note = 33;
    patterns[2].steps[4].velocity = 100;
    patterns[2].steps[4].voice = 0;
    patterns[2].steps[6].note = 33;
    patterns[2].steps[6].velocity = 100;
    patterns[2].steps[6].voice = 0;
    patterns[2].steps[8].note = 36;
    patterns[2].steps[8].velocity = 100;
    patterns[2].steps[8].voice = 0;
    patterns[2].steps[10].note = 36;
    patterns[2].steps[10].velocity = 100;
    patterns[2].steps[10].voice = 0;
    patterns[2].steps[12].note = 33;
    patterns[2].steps[12].velocity = 100;
    patterns[2].steps[12].voice = 0;
    patterns[2].steps[14].note = 33;
    patterns[2].steps[14].velocity = 100;
    patterns[2].steps[14].voice = 0;
    
    /* Lead */
    patterns[2].steps[0].note = 69;
    patterns[2].steps[0].voice = 1;
    patterns[2].steps[2].note = 72;
    patterns[2].steps[2].voice = 1;
    patterns[2].steps[4].note = 74;
    patterns[2].steps[4].voice = 1;
    patterns[2].steps[6].note = 76;
    patterns[2].steps[6].voice = 1;
    patterns[2].steps[8].note = 79; /* G5 */
    patterns[2].steps[8].voice = 1;
    patterns[2].steps[10].note = 77; /* F#5 */
    patterns[2].steps[10].voice = 1;
    patterns[2].steps[12].note = 74;
    patterns[2].steps[12].voice = 1;
    patterns[2].steps[14].note = 72;
    patterns[2].steps[14].voice = 1;

    /* Pattern D: Bridge - Softer */
    for (int i = 0; i < STEPS_PER_BAR; i++) {
        patterns[3].steps[i].note = -1;
        patterns[3].steps[i].velocity = 0;
        patterns[3].steps[i].voice = -1;
    }
    /* Bass */
    patterns[3].steps[0].note = 33;
    patterns[3].steps[0].velocity = 80;
    patterns[3].steps[0].voice = 0;
    patterns[3].steps[8].note = 36;
    patterns[3].steps[8].velocity = 80;
    patterns[3].steps[8].voice = 0;
    
    /* Lead */
    patterns[3].steps[0].note = 69;
    patterns[3].steps[0].voice = 1;
    patterns[3].steps[8].note = 72;
    patterns[3].steps[8].voice = 1;
}

/* Initialize Sections */
void init_sections() {
    /* Intro (8 bars) -> Pattern A */
    sections[0].pattern = 0;
    sections[0].bars = 8;
    /* Verse (16 bars) -> Pattern B */
    sections[1].pattern = 1;
    sections[1].bars = 16;
    /* Chorus (16 bars) -> Pattern C */
    sections[2].pattern = 2;
    sections[2].bars = 16;
    /* Bridge (8 bars) -> Pattern D */
    sections[3].pattern = 3;
    sections[3].bars = 8;
    /* Chorus (16 bars) -> Pattern C */
    sections[4].pattern = 2;
    sections[4].bars = 16;
    /* Outro (8 bars) -> Pattern A */
    sections[5].pattern = 0;
    sections[5].bars = 8;
}

/* Initialize Voices */
void init_voices() {
    for (int i = 0; i < NUM_VOICES; i++) {
        voices[i].active = 0;
        voices[i].last_freq = 0.0f;
        svf_init(&voices[i].filter, 1000.0f, 1.0f);
    }
    
    /* Voice 0: Bass (Analog Saw) */
    analog_voice_init(&voices[0].analog, 55.0f, 0.8f, 1);
    svf_init(&voices[0].filter, 500.0f, 2.0f);
    
    /* Voice 1: Lead (FM) */
    fm_voice_init(&voices[1].fm, 440.0f, 880.0f, 2.0f, 0.6f);
    svf_init(&voices[1].filter, 2000.0f, 1.0f);
    
    /* Voice 2: Pad (Analog Square) */
    analog_voice_init(&voices[2].analog, 220.0f, 0.4f, 0);
    svf_init(&voices[2].filter, 1500.0f, 1.5f);
    
    /* Voice 3: Bell (FM) */
    fm_voice_init(&voices[3].fm, 880.0f, 1760.0f, 3.0f, 0.3f);
    svf_init(&voices[3].filter, 3000.0f, 1.0f);
}

/* Trigger Voice */
void trigger_voice(int voice_idx, int note, int velocity) {
    if (voice_idx < 0 || voice_idx >= NUM_VOICES) return;
    if (note < 0) return;
    
    float freq = note_to_freq(note);
    if (freq == 0.0f) return;
    
    Voice *v = &voices[voice_idx];
    v->active = 1;
    v->last_freq = freq;
    
    if (voice_idx == 0 || voice_idx == 2) {
        /* Analog voices */
        v->analog.freq = freq;
        adsr_trigger(&v->analog.env);
    } else {
        /* FM voices */
        v->fm.carrier_freq = freq;
        v->fm.modulator_freq = freq * 2.0f;
        adsr_trigger(&v->fm.env);
    }
}

/* Release Voice */
void release_voice(int voice_idx) {
    if (voice_idx < 0 || voice_idx >= NUM_VOICES) return;
    Voice *v = &voices[voice_idx];
    if (v->active) {
        if (voice_idx == 0 || voice_idx == 2) {
            adsr_release(&v->analog.env);
        } else {
            adsr_release(&v->fm.env);
        }
    }
}

/* Process Voice */
float process_voice(int voice_idx) {
    if (!voices[voice_idx].active) return 0.0f;
    
    float sample = 0.0f;
    Voice *v = &voices[voice_idx];
    
    if (voice_idx == 0 || voice_idx == 2) {
        sample = analog_voice_process(&v->analog);
    } else {
        sample = fm_voice_process(&v->fm);
    }
    
    /* Apply filter */
    sample = svf_process(&v->filter, sample);
    
    return sample;
}

/* Main Audio Loop */
int main() {
    /* Initialize */
    init_patterns();
    init_sections();
    init_voices();
    noise_init(&noise, 0.5f);
    delay_init(&delay_l, 0.25f, 0.4f, 0.3f);
    delay_init(&delay_r, 0.25f, 0.4f, 0.3f);
    reverb_init(&reverb, 0.2f);
    
    /* Calculate total samples */
    int total_bars = 0;
    for (int i = 0; i < NUM_SECTIONS; i++) {
        total_bars += sections[i].bars;
    }
    int total_steps = total_bars * STEPS_PER_BAR;
    float seconds_per_step = (60.0f / BPM) / 4.0f; /* 16th notes */
    target_samples = (int)(total_steps * seconds_per_step * SAMPLE_RATE);
    
    /* Open file */
    FILE *fp = fopen(OUTPUT_FILE, "wb");
    if (!fp) {
        fprintf(stderr, "Error: Could not open %s\n", OUTPUT_FILE);
        return 1;
    }
    
    /* Write WAV header placeholder */
    unsigned char header[44];
    memset(header, 0, sizeof(header));
    memcpy(header, "RIFF", 4);
    unsigned int file_size = 36 + target_samples * 4; /* 44 header + data */
    memcpy(header + 4, &file_size, 4);
    memcpy(header + 8, "WAVE", 4);
    memcpy(header + 12, "fmt ", 4);
    unsigned int fmt_size = 16;
    memcpy(header + 16, &fmt_size, 4);
    unsigned short audio_format = 1; /* PCM */
    memcpy(header + 20, &audio_format, 2);
    unsigned short num_channels = 2;
    memcpy(header + 22, &num_channels, 2);
    unsigned int sample_rate = SAMPLE_RATE;
    memcpy(header + 24, &sample_rate, 4);
    unsigned int byte_rate = SAMPLE_RATE * 4; /* 2 channels * 2 bytes */
    memcpy(header + 28, &byte_rate, 4);
    unsigned short block_align = 4;
    memcpy(header + 32, &block_align, 2);
    unsigned short bits_per_sample = 16;
    memcpy(header + 34, &bits_per_sample, 2);
    memcpy(header + 36, "data", 4);
    unsigned int data_size = target_samples * 4;
    memcpy(header + 40, &data_size, 4);
    
    fwrite(header, 1, 44, fp);
    
    /* Audio Loop */
    float left_mix = 0.0f;
    float right_mix = 0.0f;
    
    for (long i = 0; i < target_samples; i++) {
        /* Calculate current step */
        float seconds_per_step = (60.0f / BPM) / 4.0f;
        int step_idx = (int)(i / (seconds_per_step * SAMPLE_RATE));
        if (step_idx >= total_steps) step_idx = total_steps - 1;
        
        /* Find current section and bar */
        int bar_in_section = 0;
        int bars_accumulated = 0;
        for (int s = 0; s < NUM_SECTIONS; s++) {
            if (bars_accumulated + sections[s].bars > (step_idx / STEPS_PER_BAR)) {
                current_section = s;
                bar_in_section = (step_idx / STEPS_PER_BAR) - bars_accumulated;
                break;
            }
            bars_accumulated += sections[s].bars;
        }
        current_bar = bar_in_section;
        current_step = step_idx % STEPS_PER_BAR;
        
        /* Trigger envelopes on step change */
        if (current_step != last_step) {
            /* Release previous step voices */
            for (int v = 0; v < NUM_VOICES; v++) {
                release_voice(v);
            }
            
            /* Trigger new step voices */
            int pattern_idx = sections[current_section].pattern;
            Step *step = &patterns[pattern_idx].steps[current_step];
            if (step->note >= 0 && step->voice >= 0) {
                trigger_voice(step->voice, step->note, step->velocity);
            }
            
            /* Drums: Kick on step 0, 8; Snare on step 4, 12; Hi-hat on every step */
            if (current_step == 0 || current_step == 8) {
                /* Kick: Low frequency burst */
                noise.level = 0.8f;
            } else if (current_step == 4 || current_step == 12) {
                /* Snare: Mid frequency burst */
                noise.level = 0.6f;
            } else {
                /* Hi-hat: High frequency burst */
                noise.level = 0.3f;
            }
            
            last_step = current_step;
        }
        
        /* Process all voices */
        left_mix = 0.0f;
        right_mix = 0.0f;
        
        for (int v = 0; v < NUM_VOICES; v++) {
            float sample = process_voice(v);
            /* Ping-pong delay: alternate left/right */
            if (v % 2 == 0) {
                left_mix += sample;
            } else {
                right_mix += sample;
            }
        }
        
        /* Add noise (drums) */
        float noise_sample = noise_process(&noise);
        left_mix += noise_sample * 0.5f;
        right_mix += noise_sample * 0.5f;
        
        /* Apply delay */
        left_mix = delay_process(&delay_l, left_mix);
        right_mix = delay_process(&delay_r, right_mix);
        
        /* Apply reverb */
        left_mix = reverb_process(&reverb, left_mix);
        right_mix = reverb_process(&reverb, right_mix);
        
        /* Master gain */
        left_mix *= MASTER_GAIN;
        right_mix *= MASTER_GAIN;
        
        /* Clamp */
        if (left_mix > 1.0f) left_mix = 1.0f;
        if (left_mix < -1.0f) left_mix = -1.0f;
        if (right_mix > 1.0f) right_mix = 1.0f;
        if (right_mix < -1.0f) right_mix = -1.0f;
        
        /* Convert to 16-bit PCM */
        short left_pcm = (short)(left_mix * 32767.0f);
        short right_pcm = (short)(right_mix * 32767.0f);
        
        /* Write to file */
        fwrite(&left_pcm, 2, 1, fp);
        fwrite(&right_pcm, 2, 1, fp);
    }
    
    fclose(fp);
    printf("Generated %s (%d samples)\n", OUTPUT_FILE, (int)target_samples);
    return 0;
}
