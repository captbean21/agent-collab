#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ==================== Constants ==================== */
#define SAMPLE_RATE 44100
#define BPM 110.0f
#define STEPS_PER_BAR 16
#define TOTAL_BARS 72
#define TOTAL_STEPS (TOTAL_BARS * STEPS_PER_BAR)
#define TOTAL_SAMPLES ((int)(TOTAL_STEPS * (SAMPLE_RATE / (BPM * 4.0f))))

#define KICK_DECAY_MS 300.0f
#define KICK_SWEEP_MS 300.0f
#define KICK_HP 30.0f
#define KICK_START_FREQ 150.0f
#define KICK_END_FREQ 60.0f

#define SNARE_DECAY_MS 150.0f
#define SNARE_TONE_FREQ 200.0f

#define HAT_DECAY_MS 50.0f
#define HAT_OPEN_DECAY_MS 150.0f
#define HAT_HP 8000.0f

#define BASS_ENV_A_MS 0.0f
#define BASS_ENV_D_MS 300.0f
#define BASS_ENV_S 0.4f
#define BASS_ENV_R_MS 200.0f
#define BASS_CUT_MIN 400.0f
#define BASS_CUT_MAX 800.0f
#define BASS_LFO_RATE 0.25f /* 1/8 note at 110 BPM: 110/60 / 8 = 2.29 Hz? No, 110/60 = 1.833 beats/sec. 1/8 note = 1.833/8 = 0.229 Hz. Let's use 0.229 */
#define BASS_LFO_DEPTH 0.3f

#define SIDECHAIN_ATTACK_MS 2.0f
#define SIDECHAIN_RELEASE_MS 150.0f
#define SIDECHAIN_DEPTH 0.7f

#define REVERB_DECAY_MS 3000.0f
#define GATE_THRESHOLD 0.005f
#define GATE_HOLD_MS 200.0f
#define GATE_RELEASE_MS 80.0f

#define PORTAMENTO_MS 50.0f

#define CHORUS_LFO_RATE 0.5f
#define CHORUS_DELAY_MIN_MS 2.0f
#define CHORUS_DELAY_MAX_MS 5.0f

#define PING_PONG_DELAY_BEATS 0.1875f /* 3/16 note */
#define PING_PONG_FEEDBACK 0.4f

#define LIMITER_TANH_K 3.0f

/* ==================== Data Structures ==================== */

typedef struct {
    float phase;
    float freq;
    float target_freq;
    float portamento_time;
    float portamento_elapsed;
    float portamento_start_freq;
} FMVoice;

typedef struct {
    float phase;
    float freq;
    float pwm_phase;
    float pwm_rate;
    float filter_cutoff;
    float filter_resonance;
    float filter_env;
    float filter_env_target;
    float filter_env_elapsed;
    float filter_env_duration;
    float lfo_phase;
    float lfo_rate;
    float lfo_depth;
    float lfo_offset;
    float lfo_scale;
    float chorus_delay1;
    float chorus_delay2;
    float chorus_lfo_phase;
    float chorus_lfo_rate;
    float chorus_delay_min;
    float chorus_delay_max;
    float chorus_depth;
    float chorus_mix;
    float chorus_delay_buf1[1024];
    float chorus_delay_buf2[1024];
    int chorus_delay_idx1;
    int chorus_delay_idx2;
} VAVoice;

typedef struct {
    float state1;
    float state2;
    float cutoff;
    float resonance;
    float mode; /* 0: LP, 1: BP, 2: HP */
} StateVarFilter;

typedef struct {
    float comb1[128];
    float comb2[128];
    float comb3[128];
    float comb4[128];
    float ap1[128];
    float ap2[128];
    float pre_delay[128];
    int pre_delay_idx;
    float feedback;
    float decay;
    float gate_envelope;
    float gate_target;
    float gate_elapsed;
    float gate_duration;
    float gate_hold_elapsed;
    float gate_hold_duration;
    float gate_release_elapsed;
    float gate_release_duration;
    float gate_active;
    float gate_threshold;
    float gate_hold_time;
    float gate_release_time;
    float gate_current;
    float gate_target_current;
    float gate_elapsed_current;
    float gate_duration_current;
    float gate_hold_elapsed_current;
    float gate_hold_duration_current;
    float gate_release_elapsed_current;
    float gate_release_duration_current;
    float gate_active_current;
    float gate_threshold_current;
    float gate_hold_time_current;
    float gate_release_time_current;
} SchroederReverb;

typedef struct {
    float delay_buf[4096];
    int delay_idx;
    float feedback;
    float delay_time;
    float ping_pong_phase;
    float ping_pong_rate;
    float ping_pong_depth;
    float ping_pong_offset;
    float ping_pong_scale;
    float ping_pong_mix;
} PingPongDelay;

typedef struct {
    float kick_env;
    float kick_freq;
    float kick_phase;
    float kick_hp_state;
    float kick_hp_prev;
    float kick_decay;
    float kick_sweep;
    float kick_sweep_elapsed;
    float kick_sweep_duration;
    float kick_decay_elapsed;
    float kick_decay_duration;
    float kick_active;
    float kick_start_freq;
    float kick_end_freq;
    float kick_hp_cutoff;
    float kick_hp_resonance;
} KickVoice;

typedef struct {
    float snare_env;
    float snare_tone_phase;
    float snare_tone_freq;
    float snare_noise_phase;
    float snare_decay;
    float snare_decay_elapsed;
    float snare_decay_duration;
    float snare_active;
    float snare_tone_decay;
    float snare_tone_decay_elapsed;
    float snare_tone_decay_duration;
    float snare_tone_active;
    float snare_noise_decay;
    float snare_noise_decay_elapsed;
    float snare_noise_decay_duration;
    float snare_noise_active;
    float snare_tone_freq_start;
    float snare_tone_freq_end;
    float snare_tone_sweep_elapsed;
    float snare_tone_sweep_duration;
    float snare_tone_sweep;
} SnareVoice;

typedef struct {
    float hat_env;
    float hat_noise_phase;
    float hat_decay;
    float hat_decay_elapsed;
    float hat_decay_duration;
    float hat_active;
    float hat_hp_state;
    float hat_hp_prev;
    float hat_hp_cutoff;
    float hat_hp_resonance;
    float hat_open;
    float hat_open_decay;
    float hat_open_decay_elapsed;
    float hat_open_decay_duration;
    float hat_open_active;
    float hat_open_hp_state;
    float hat_open_hp_prev;
    float hat_open_hp_cutoff;
    float hat_open_hp_resonance;
    float hat_open_noise_phase;
} HatVoice;

typedef struct {
    float env;
    float env_target;
    float env_elapsed;
    float env_duration;
    float env_active;
    float env_attack;
    float env_decay;
    float env_sustain;
    float env_release;
    float env_attack_elapsed;
    float env_decay_elapsed;
    float env_release_elapsed;
    float env_attack_duration;
    float env_decay_duration;
    float env_release_duration;
    float env_current;
    float env_target_current;
    float env_elapsed_current;
    float env_duration_current;
    float env_active_current;
    float env_attack_current;
    float env_decay_current;
    float env_sustain_current;
    float env_release_current;
    float env_attack_elapsed_current;
    float env_decay_elapsed_current;
    float env_release_elapsed_current;
    float env_attack_duration_current;
    float env_decay_duration_current;
    float env_release_duration_current;
} Envelope;

typedef struct {
    float attack;
    float decay;
    float sustain;
    float release;
    float attack_elapsed;
    float decay_elapsed;
    float release_elapsed;
    float attack_duration;
    float decay_duration;
    float release_duration;
    float current;
    float target;
    float elapsed;
    float duration;
    float active;
    float attack_current;
    float decay_current;
    float sustain_current;
    float release_current;
    float attack_elapsed_current;
    float decay_elapsed_current;
    float release_elapsed_current;
    float attack_duration_current;
    float decay_duration_current;
    float release_duration_current;
    float current_current;
    float target_current;
    float elapsed_current;
    float duration_current;
    float active_current;
} ADSREnvelope;

typedef struct {
    float env;
    float env_target;
    float env_elapsed;
    float env_duration;
    float env_active;
    float env_attack;
    float env_decay;
    float env_sustain;
    float env_release;
    float env_attack_elapsed;
    float env_decay_elapsed;
    float env_release_elapsed;
    float env_attack_duration;
    float env_decay_duration;
    float env_release_duration;
    float env_current;
    float env_target_current;
    float env_elapsed_current;
    float env_duration_current;
    float env_active_current;
    float env_attack_current;
    float env_decay_current;
    float env_sustain_current;
    float env_release_current;
    float env_attack_elapsed_current;
    float env_decay_elapsed_current;
    float env_release_elapsed_current;
    float env_attack_duration_current;
    float env_decay_duration_current;
    float env_release_duration_current;
} ADSREnvelope2;

/* ==================== Global State ==================== */

/* FM Voices */
FMVoice fm_bell;
FMVoice fm_lead;

/* VA Voices */
VAVoice va_bass;
VAVoice va_pad;

/* Filters */
StateVarFilter bass_filter;
StateVarFilter pad_filter;
StateVarFilter lead_filter;

/* Reverb */
SchroederReverb reverb;

/* Delay */
PingPongDelay ping_pong;

/* Drums */
KickVoice kick;
SnareVoice snare;
HatVoice hat;

/* Sidechain */
float sidechain_env;
float sidechain_target;
float sidechain_elapsed;
float sidechain_duration;
float sidechain_active;
float sidechain_attack;
float sidechain_decay;
float sidechain_sustain;
float sidechain_release;
float sidechain_attack_elapsed;
float sidechain_decay_elapsed;
float sidechain_release_elapsed;
float sidechain_attack_duration;
float sidechain_decay_duration;
float sidechain_release_duration;
float sidechain_current;
float sidechain_target_current;
float sidechain_elapsed_current;
float sidechain_duration_current;
float sidechain_active_current;
float sidechain_attack_current;
float sidechain_decay_current;
float sidechain_sustain_current;
float sidechain_release_current;
float sidechain_attack_elapsed_current;
float sidechain_decay_elapsed_current;
float sidechain_release_elapsed_current;
float sidechain_attack_duration_current;
float sidechain_decay_duration_current;
float sidechain_release_duration_current;

/* Master */
float master_gain;
float master_gain_target;
float master_gain_elapsed;
float master_gain_duration;
float master_gain_active;
float master_gain_attack;
float master_gain_decay;
float master_gain_sustain;
float master_gain_release;
float master_gain_attack_elapsed;
float master_gain_decay_elapsed;
float master_gain_release_elapsed;
float master_gain_attack_duration;
float master_gain_decay_duration;
float master_gain_release_duration;
float master_gain_current;
float master_gain_target_current;
float master_gain_elapsed_current;
float master_gain_duration_current;
float master_gain_active_current;
float master_gain_attack_current;
float master_gain_decay_current;
float master_gain_sustain_current;
float master_gain_release_current;
float master_gain_attack_elapsed_current;
float master_gain_decay_elapsed_current;
float master_gain_release_elapsed_current;
float master_gain_attack_duration_current;
float master_gain_decay_duration_current;
float master_gain_release_duration_current;

/* Limiter */
float limiter_env;
float limiter_target;
float limiter_elapsed;
float limiter_duration;
float limiter_active;
float limiter_attack;
float limiter_decay;
float limiter_sustain;
float limiter_release;
float limiter_attack_elapsed;
float limiter_decay_elapsed;
float limiter_release_elapsed;
float limiter_attack_duration;
float limiter_decay_duration;
float limiter_release_duration;
float limiter_current;
float limiter_target_current;
float limiter_elapsed_current;
float limiter_duration_current;
float limiter_active_current;
float limiter_attack_current;
float limiter_decay_current;
float limiter_sustain_current;
float limiter_release_current;
float limiter_attack_elapsed_current;
float limiter_decay_elapsed_current;
float limiter_release_elapsed_current;
float limiter_attack_duration_current;
float limiter_decay_duration_current;
float limiter_release_duration_current;

/* Sequencer */
int current_step;
int current_bar;
int current_section;
float section_gain;
float section_gain_target;
float section_gain_elapsed;
float section_gain_duration;
float section_gain_active;
float section_gain_attack;
float section_gain_decay;
float section_gain_sustain;
float section_gain_release;
float section_gain_attack_elapsed;
float section_gain_decay_elapsed;
float section_gain_release_elapsed;
float section_gain_attack_duration;
float section_gain_decay_duration;
float section_gain_release_duration;
float section_gain_current;
float section_gain_target_current;
float section_gain_elapsed_current;
float section_gain_duration_current;
float section_gain_active_current;
float section_gain_attack_current;
float section_gain_decay_current;
float section_gain_sustain_current;
float section_gain_release_current;
float section_gain_attack_elapsed_current;
float section_gain_decay_elapsed_current;
float section_gain_release_elapsed_current;
float section_gain_attack_duration_current;
float section_gain_decay_duration_current;
float section_gain_release_duration_current;

/* Audio buffers */
float *audio_buffer;
int audio_buffer_size;

/* ==================== Helper Functions ==================== */

float clamp(float x, float min, float max) {
    if (x < min) return min;
    if (x > max) return max;
    return x;
}

float lerp(float a, float b, float t) {
    return a + (b - a) * t;
}

float smoothstep(float t) {
    return t * t * (3.0f - 2.0f * t);
}

float tanh_soft(float x) {
    return tanhf(LIMITER_TANH_K * x) / tanhf(LIMITER_TANH_K);
}

/* ==================== State Variable Filter ==================== */

void svf_init(StateVarFilter *f, float cutoff, float resonance, int mode) {
    f->state1 = 0.0f;
    f->state2 = 0.0f;
    f->cutoff = cutoff;
    f->resonance = resonance;
    f->mode = mode;
}

float svf_process(StateVarFilter *f, float input) {
    float w = 2.0f * M_PI * f->cutoff / SAMPLE_RATE;
    float r = f->resonance;
    float a = 1.0f - r * sinf(w);
    float b = r * sinf(w);
    float c = 1.0f - r * sinf(w);
    float d = r * sinf(w);
    
    float out;
    if (f->mode == 0) { /* LP */
        out = f->state1;
        f->state1 = input + b * f->state1 - a * out;
        f->state2 = out + d * f->state1 - c * out;
    } else if (f->mode == 1) { /* BP */
        out = f->state1;
        f->state1 = input + b * f->state1 - a * out;
        f->state2 = out + d * f->state1 - c * out;
        out = f->state2;
    } else { /* HP */
        out = f->state1;
        f->state1 = input + b * f->state1 - a * out;
        f->state2 = out + d * f->state1 - c * out;
        out = input - f->state2;
    }
    return out;
}

/* ==================== FM Voice ==================== */

void fm_init(FMVoice *v, float freq) {
    v->phase = 0.0f;
    v->freq = freq;
    v->target_freq = freq;
    v->portamento_time = PORTAMENTO_MS / 1000.0f;
    v->portamento_elapsed = 0.0f;
    v->portamento_start_freq = freq;
}

void fm_set_freq(FMVoice *v, float freq) {
    v->portamento_start_freq = v->freq;
    v->target_freq = freq;
    v->portamento_elapsed = 0.0f;
}

float fm_process(FMVoice *v, float dt) {
    if (v->portamento_elapsed < v->portamento_time) {
        v->portamento_elapsed += dt;
        float t = v->portamento_elapsed / v->portamento_time;
        t = smoothstep(t);
        v->freq = lerp(v->portamento_start_freq, v->target_freq, t);
    } else {
        v->freq = v->target_freq;
    }
    
    v->phase += v->freq * dt;
    while (v->phase >= 2.0f * M_PI) v->phase -= 2.0f * M_PI;
    
    float mod_index = 0.5f;
    float mod_phase = v->phase * 2.0f;
    float mod_signal = sinf(mod_phase);
    float carrier = sinf(v->phase + mod_index * mod_signal);
    return carrier;
}

/* ==================== VA Voice ==================== */

void va_init(VAVoice *v, float freq) {
    v->phase = 0.0f;
    v->freq = freq;
    v->pwm_phase = 0.0f;
    v->pwm_rate = 0.0f;
    v->filter_cutoff = 1000.0f;
    v->filter_resonance = 0.7f;
    v->filter_env = 0.0f;
    v->filter_env_target = 0.0f;
    v->filter_env_elapsed = 0.0f;
    v->filter_env_duration = 0.0f;
    v->lfo_phase = 0.0f;
    v->lfo_rate = BASS_LFO_RATE;
    v->lfo_depth = BASS_LFO_DEPTH;
    v->lfo_offset = 0.0f;
    v->lfo_scale = 1.0f;
    v->chorus_delay1 = 0.0f;
    v->chorus_delay2 = 0.0f;
    v->chorus_lfo_phase = 0.0f;
    v->chorus_lfo_rate = CHORUS_LFO_RATE;
    v->chorus_delay_min = CHORUS_DELAY_MIN_MS / 1000.0f;
    v->chorus_delay_max = CHORUS_DELAY_MAX_MS / 1000.0f;
    v->chorus_depth = 0.5f;
    v->chorus_mix = 0.5f;
    memset(v->chorus_delay_buf1, 0, sizeof(v->chorus_delay_buf1));
    memset(v->chorus_delay_buf2, 0, sizeof(v->chorus_delay_buf2));
    v->chorus_delay_idx1 = 0;
    v->chorus_delay_idx2 = 0;
}

void va_set_freq(VAVoice *v, float freq) {
    v->freq = freq;
}

void va_set_filter_env(VAVoice *v, float env) {
    v->filter_env_target = env;
    v->filter_env_elapsed = 0.0f;
    v->filter_env_duration = 0.0f;
}

float va_process(VAVoice *v, float dt) {
    /* Filter envelope */
    if (v->filter_env_elapsed < v->filter_env_duration) {
        v->filter_env_elapsed += dt;
        float t = v->filter_env_elapsed / v->filter_env_duration;
        v->filter_env = lerp(v->filter_env, v->filter_env_target, t);
    } else {
        v->filter_env = v->filter_env_target;
    }
    
    /* LFO */
    v->lfo_phase += v->lfo_rate * dt;
    while (v->lfo_phase >= 2.0f * M_PI) v->lfo_phase -= 2.0f * M_PI;
    float lfo_val = sinf(v->lfo_phase);
    float lfo_mod = v->lfo_offset + v->lfo_scale * lfo_val * v->lfo_depth;
    
    /* Filter cutoff */
    float cutoff = BASS_CUT_MIN + (BASS_CUT_MAX - BASS_CUT_MIN) * (v->filter_env + lfo_mod);
    cutoff = clamp(cutoff, BASS_CUT_MIN, BASS_CUT_MAX);
    
    /* PWM */
    v->pwm_phase += v->pwm_rate * dt;
    while (v->pwm_phase >= 2.0f * M_PI) v->pwm_phase -= 2.0f * M_PI;
    float pwm_val = sinf(v->pwm_phase);
    
    /* Saw wave */
    v->phase += v->freq * dt;
    while (v->phase >= 2.0f * M_PI) v->phase -= 2.0f * M_PI;
    float saw = v->phase / (2.0f * M_PI) - 0.5f;
    
    /* Square wave */
    float square = (saw > 0.0f) ? 1.0f : -1.0f;
    
    /* Mix saw and square */
    float raw = 0.5f * saw + 0.5f * square;
    
    /* Apply filter */
    StateVarFilter temp_filter;
    svf_init(&temp_filter, cutoff, v->filter_resonance, 0);
    float filtered = svf_process(&temp_filter, raw);
    
    /* Chorus */
    v->chorus_lfo_phase += v->chorus_lfo_rate * dt;
    while (v->chorus_lfo_phase >= 2.0f * M_PI) v->chorus_lfo_phase -= 2.0f * M_PI;
    float chorus_lfo_val = sinf(v->chorus_lfo_phase);
    float chorus_delay1 = v->chorus_delay_min + (v->chorus_delay_max - v->chorus_delay_min) * (0.5f + 0.5f * chorus_lfo_val);
    float chorus_delay2 = v->chorus_delay_min + (v->chorus_delay_max - v->chorus_delay_min) * (0.5f - 0.5f * chorus_lfo_val);
    
    int delay_samples1 = (int)(chorus_delay1 * SAMPLE_RATE);
    int delay_samples2 = (int)(chorus_delay2 * SAMPLE_RATE);
    
    v->chorus_delay_idx1 = (v->chorus_delay_idx1 + 1) % 1024;
    v->chorus_delay_idx2 = (v->chorus_delay_idx2 + 1) % 1024;
    
    v->chorus_delay_buf1[v->chorus_delay_idx1] = filtered;
    v->chorus_delay_buf2[v->chorus_delay_idx2] = filtered;
    
    int read_idx1 = (v->chorus_delay_idx1 - delay_samples1 + 1024) % 1024;
    int read_idx2 = (v->chorus_delay_idx2 - delay_samples2 + 1024) % 1024;
    
    float chorus1 = v->chorus_delay_buf1[read_idx1];
    float chorus2 = v->chorus_delay_buf2[read_idx2];
    
    float chorus_out = 0.5f * chorus1 + 0.5f * chorus2;
    
    float out = (1.0f - v->chorus_mix) * filtered + v->chorus_mix * chorus_out;
    
    return out;
}

/* ==================== Schroeder Reverb ==================== */

void reverb_init(SchroederReverb *r) {
    memset(r->comb1, 0, sizeof(r->comb1));
    memset(r->comb2, 0, sizeof(r->comb2));
    memset(r->comb3, 0, sizeof(r->comb3));
    memset(r->comb4, 0, sizeof(r->comb4));
    memset(r->ap1, 0, sizeof(r->ap1));
    memset(r->ap2, 0, sizeof(r->ap2));
    memset(r->pre_delay, 0, sizeof(r->pre_delay));
    r->pre_delay_idx = 0;
    r->feedback = 0.5f;
    r->decay = REVERB_DECAY_MS / 1000.0f;
    r->gate_envelope = 0.0f;
    r->gate_target = 0.0f;
    r->gate_elapsed = 0.0f;
    r->gate_duration = 0.0f;
    r->gate_hold_elapsed = 0.0f;
    r->gate_hold_duration = GATE_HOLD_MS / 1000.0f;
    r->gate_release_elapsed = 0.0f;
    r->gate_release_duration = GATE_RELEASE_MS / 1000.0f;
    r->gate_active = 0.0f;
    r->gate_threshold = GATE_THRESHOLD;
    r->gate_hold_time = GATE_HOLD_MS / 1000.0f;
    r->gate_release_time = GATE_RELEASE_MS / 1000.0f;
    r->gate_current = 0.0f;
    r->gate_target_current = 0.0f;
    r->gate_elapsed_current = 0.0f;
    r->gate_duration_current = 0.0f;
    r->gate_hold_elapsed_current = 0.0f;
    r->gate_hold_duration_current = GATE_HOLD_MS / 1000.0f;
    r->gate_release_elapsed_current = 0.0f;
    r->gate_release_duration_current = GATE_RELEASE_MS / 1000.0f;
    r->gate_active_current = 0.0f;
    r->gate_threshold_current = GATE_THRESHOLD;
    r->gate_hold_time_current = GATE_HOLD_MS / 1000.0f;
    r->gate_release_time_current = GATE_RELEASE_MS / 1000.0f;
}

float reverb_process(SchroederReverb *r, float input, float dt) {
    /* Pre-delay */
    r->pre_delay_idx = (r->pre_delay_idx + 1) % 128;
    r->pre_delay[r->pre_delay_idx] = input;
    int pre_delay_read = (r->pre_delay_idx - 128 + 128) % 128;
    float pre_delayed = r->pre_delay[pre_delay_read];
    
    /* Comb filters */
    float c1 = pre_delayed + r->feedback * r->comb1[0];
    r->comb1[0] = c1;
    for (int i = 127; i > 0; i--) r->comb1[i] = r->comb1[i-1];
    
    float c2 = pre_delayed + r->feedback * r->comb2[0];
    r->comb2[0] = c2;
    for (int i = 127; i > 0; i--) r->comb2[i] = r->comb2[i-1];
    
    float c3 = pre_delayed + r->feedback * r->comb3[0];
    r->comb3[0] = c3;
    for (int i = 127; i > 0; i--) r->comb3[i] = r->comb3[i-1];
    
    float c4 = pre_delayed + r->feedback * r->comb4[0];
    r->comb4[0] = c4;
    for (int i = 127; i > 0; i--) r->comb4[i] = r->comb4[i-1];
    
    float comb_out = 0.25f * (c1 + c2 + c3 + c4);
    
    /* Allpass filters */
    float a1 = comb_out + r->ap1[0];
    r->ap1[0] = comb_out - r->ap1[0] + 0.5f * a1;
    for (int i = 127; i > 0; i--) r->ap1[i] = r->ap1[i-1];
    
    float a2 = a1 + r->ap2[0];
    r->ap2[0] = a1 - r->ap2[0] + 0.5f * a2;
    for (int i = 127; i > 0; i--) r->ap2[i] = r->ap2[i-1];
    
    float reverb_out = a2;
    
    /* Noise gate */
    float abs_out = fabsf(reverb_out);
    if (abs_out > r->gate_threshold) {
        r->gate_target = 1.0f;
        r->gate_elapsed = 0.0f;
        r->gate_duration = r->gate_hold_time;
        r->gate_active = 1.0f;
    } else {
        if (r->gate_active > 0.5f) {
            r->gate_elapsed += dt;
            if (r->gate_elapsed >= r->gate_duration) {
                r->gate_target = 0.0f;
                r->gate_elapsed = 0.0f;
                r->gate_duration = r->gate_release_time;
                r->gate_active = 0.0f;
            }
        } else {
            r->gate_target = 0.0f;
        }
    }
    
    if (r->gate_elapsed < r->gate_duration) {
        float t = r->gate_elapsed / r->gate_duration;
        r->gate_envelope = lerp(r->gate_envelope, r->gate_target, t);
    } else {
        r->gate_envelope = r->gate_target;
    }
    
    float gated_out = reverb_out * r->gate_envelope;
    
    return gated_out;
}

/* ==================== Ping-Pong Delay ==================== */

void ping_pong_init(PingPongDelay *d) {
    memset(d->delay_buf, 0, sizeof(d->delay_buf));
    d->delay_idx = 0;
    d->feedback = PING_PONG_FEEDBACK;
    d->delay_time = PING_PONG_DELAY_BEATS * (60.0f / BPM) / 4.0f;
    d->ping_pong_phase = 0.0f;
    d->ping_pong_rate = 0.5f;
    d->ping_pong_depth = 0.5f;
    d->ping_pong_offset = 0.5f;
    d->ping_pong_scale = 1.0f;
    d->ping_pong_mix = 0.5f;
}

float ping_pong_process(PingPongDelay *d, float input, float dt) {
    d->ping_pong_phase += d->ping_pong_rate * dt;
    while (d->ping_pong_phase >= 2.0f * M_PI) d->ping_pong_phase -= 2.0f * M_PI;
    float ping_pong_val = sinf(d->ping_pong_phase);
    float pan = d->ping_pong_offset + d->ping_pong_scale * ping_pong_val * d->ping_pong_depth;
    
    int delay_samples = (int)(d->delay_time * SAMPLE_RATE);
    d->delay_idx = (d->delay_idx + 1) % 4096;
    d->delay_buf[d->delay_idx] = input;
    
    int read_idx = (d->delay_idx - delay_samples + 4096) % 4096;
    float delayed = d->delay_buf[read_idx];
    
    float out = input + delayed * d->feedback;
    
    return out;
}

/* ==================== Drum Voices ==================== */

void kick_init(KickVoice *k) {
    k->kick_env = 0.0f;
    k->kick_freq = KICK_START_FREQ;
    k->kick_phase = 0.0f;
    k->kick_hp_state = 0.0f;
    k->kick_hp_prev = 0.0f;
    k->kick_decay = 0.0f;
    k->kick_sweep = 0.0f;
    k->kick_sweep_elapsed = 0.0f;
    k->kick_sweep_duration = KICK_SWEEP_MS / 1000.0f;
    k->kick_decay_elapsed = 0.0f;
    k->kick_decay_duration = KICK_DECAY_MS / 1000.0f;
    k->kick_active = 0.0f;
    k->kick_start_freq = KICK_START_FREQ;
    k->kick_end_freq = KICK_END_FREQ;
    k->kick_hp_cutoff = KICK_HP;
    k->kick_hp_resonance = 0.7f;
}

void kick_trigger(KickVoice *k) {
    k->kick_env = 1.0f;
    k->kick_freq = KICK_START_FREQ;
    k->kick_phase = 0.0f;
    k->kick_hp_state = 0.0f;
    k->kick_hp_prev = 0.0f;
    k->kick_decay = 1.0f;
    k->kick_sweep = 0.0f;
    k->kick_sweep_elapsed = 0.0f;
    k->kick_decay_elapsed = 0.0f;
    k->kick_active = 1.0f;
}

float kick_process(KickVoice *k, float dt) {
    float env = k->kick_env;
    float freq = k->kick_freq + (k->kick_start_freq - k->kick_end_freq) * (1.0f - env);
    k->kick_phase += freq * dt;
    float out = sinf(2.0f * M_PI * k->kick_phase);
    /* Envelope decay */
    env *= expf(-dt / (k->kick_decay_duration > 0 ? k->kick_decay_duration : 0.1f));
    k->kick_env = env;
    /* Filter sweep */
    float sweep = expf(-k->kick_sweep_elapsed / 0.01f);
    k->kick_sweep_elapsed += dt;
    float filtered = out * env * sweep;
    return filtered;
}

/* ==================== Complete Track Generation ==================== */
void generate_audio(const char *filename) {
    float dt = 1.0f / SAMPLE_RATE;
    float step_duration = 4.0f * 60.0f / BPM / STEPS_PER_BAR;
    int samples_per_step = (int)(step_duration * SAMPLE_RATE + 0.5f);
    if (samples_per_step < 1) samples_per_step = 1;
    int samples_per_bar = samples_per_step * STEPS_PER_BAR;
    int total_samples = samples_per_bar * TOTAL_BARS;
    
    FMVoice lead_fm; fm_init(&lead_fm, 440.0f);
    FMVoice bell_fm; fm_init(&bell_fm, 880.0f);
    VAVoice bass_va; va_init(&bass_va, 110.0f);
    VAVoice pad_va; va_init(&pad_va, 220.0f);
    KickVoice kick; kick_init(&kick);
    SnareVoice snare = {0};
    snare.snare_tone_freq = SNARE_TONE_FREQ;
    snare.snare_decay_duration = SNARE_DECAY_MS / 1000.0f;
    snare.snare_tone_decay_duration = SNARE_DECAY_MS / 1000.0f;
    snare.snare_noise_decay_duration = SNARE_DECAY_MS / 1000.0f;
    snare.snare_tone_freq_start = 300.0f;
    snare.snare_tone_freq_end = 150.0f;
    snare.snare_tone_sweep_duration = 0.03f;
    HatVoice hat = {0};
    hat.hat_decay_duration = HAT_DECAY_MS / 1000.0f;
    hat.hat_open_decay_duration = HAT_OPEN_DECAY_MS / 1000.0f;
    hat.hat_hp_cutoff = HAT_HP;
    hat.hat_open_hp_cutoff = 4000.0f;
    hat.hat_hp_resonance = 0.7f;
    hat.hat_open_hp_resonance = 0.7f;
    
    SchroederReverb reverb; reverb_init(&reverb);
    PingPongDelay delay; ping_pong_init(&delay);
    
    float sidechain_env = 0.0f;
    float sidechain_attack = 1.0f - expf(-dt / (SIDECHAIN_ATTACK_MS / 1000.0f));
    float sidechain_release = 1.0f - expf(-dt / (SIDECHAIN_RELEASE_MS / 1000.0f));
    
    int kick_pat[16] = {1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0};
    int snare_pat[16] = {0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0};
    int hat_closed_pat[16] = {1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0};
    int hat_open_pat[16] = {0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0};
    int bass_pat[16] = {1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0};
    int lead_pat[16] = {1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0};
    
    float bass_notes[8] = {55.0f, 55.0f, 41.2f, 55.0f, 49.0f, 49.0f, 36.7f, 49.0f};
    int bass_octaves[16] = {0,1,0,1, 0,1,0,1, 0,1,0,1, 0,1,0,1};
    int chords[8][3] = {{69,73,76},{65,69,72},{62,67,71},{60,65,69},{69,73,76},{65,69,72},{62,67,71},{60,67,71}};
    int lead_mel[16] = {76,0,0,0, 74,0,76,0, 74,0,71,0, 74,0,76,0};
    
    float *output = (float*)malloc(total_samples * 2 * sizeof(float));
    if (!output) return;
    
    int chord_idx = 0, prev_bar = -1;
    float master_gain = 0.35f;
    float hat_hp_state = 0, hat_hp_prev = 0;
    
    for (int i = 0; i < total_samples; i++) {
        int bar = i / samples_per_bar;
        int step = (i % samples_per_bar) / samples_per_step;
        int step_samp = i % samples_per_step;
        
        if (bar != prev_bar) {
            prev_bar = bar; float t = 0;
            if (bar < 8) { t = (float)bar/8.0f; master_gain = lerp(0.35f, 0.55f, t); }
            else if (bar < 24) { t = (float)(bar-8)/16.0f; master_gain = lerp(0.55f, 0.75f, t); }
            else if (bar < 40) { t = (float)(bar-24)/16.0f; master_gain = lerp(0.75f, 0.85f, t); }
            else if (bar < 48) { master_gain = 0.65f; }
            else if (bar < 64) { t = (float)(bar-48)/16.0f; master_gain = lerp(0.85f, 0.95f, t); }
            else { t = (float)(bar-64)/8.0f; master_gain = lerp(0.95f, 0.0f, t); }
            master_gain = fminf(master_gain, 0.95f);
            chord_idx = bar % 8;
        }
        
        int is_step = (step_samp == 0);
        if (is_step) {
            if (kick_pat[step]) { kick_trigger(&kick); sidechain_env = 1.0f; }
            if (snare_pat[step] && bar >= 24) { snare.snare_env = 1.0f; snare.snare_tone_phase = 0; snare.snare_noise_phase = (float)rand()/RAND_MAX*2*M_PI; }
            if (hat_closed_pat[step] && bar >= 24) { hat.hat_env = 1.0f; hat.hat_noise_phase = (float)rand()/RAND_MAX*2*M_PI; }
            if (hat_open_pat[step] && bar >= 24) { hat.hat_open = 1.0f; hat.hat_open_noise_phase = (float)rand()/RAND_MAX*2*M_PI; }
            if (bass_pat[step] && bar >= 8) { float root = bass_notes[chord_idx]; int oct = bass_octaves[step]; va_set_freq(&bass_va, root*(1<<oct)); va_set_filter_env(&bass_va, 1.0f); }
            if (lead_pat[step] && bar >= 24) { int n = lead_mel[step]; if (n>0) fm_set_freq(&lead_fm, 440.0f*powf(2.0f,(n-69)/12.0f)); }
            if (step == 0 && bar >= 0) { float root = 440.0f*powf(2.0f,(chords[chord_idx][0]-69)/12.0f); va_set_freq(&pad_va, root); }
        }
        
        if (sidechain_env > 0) sidechain_env *= (1.0f - sidechain_release);
        float sc_gain = 1.0f - SIDECHAIN_DEPTH * sidechain_env;
        
        float pad_out = 0, bass_out = 0, lead_out = 0, bell_out = 0, kick_out = 0, snare_out = 0, hat_out = 0;
        
        if (bar >= 0) { float ft = fminf(1.0f, (float)bar/48.0f); va_set_filter_env(&pad_va, lerp(0.2f, 0.8f, ft)); pad_out = va_process(&pad_va, dt); }
        if (bar >= 8) { bass_out = va_process(&bass_va, dt) * sc_gain; }
        if (bar >= 24) lead_out = fm_process(&lead_fm, dt) * 0.3f;
        bell_out = fm_process(&bell_fm, dt) * 0.05f;
        kick_out = kick_process(&kick, dt) * 0.8f;
        
        if (bar >= 24 && snare.snare_env > 0.001f) {
            snare.snare_tone_phase += snare.snare_tone_freq * dt;
            float tone = sinf(2*M_PI*snare.snare_tone_phase);
            float noise = ((float)rand()/RAND_MAX)*2-1;
            snare_out = (tone*0.5f + noise*0.5f) * snare.snare_env;
            snare.snare_env *= expf(-dt/(SNARE_DECAY_MS/1000.0f));
        }
        if (bar >= 24 && hat.hat_env > 0.001f) {
            float noise = ((float)rand()/RAND_MAX)*2-1;
            float hp = noise - hat_hp_prev + 0.95f*hat_hp_state; hat_hp_prev = noise; hat_hp_state = hp;
            hat_out = hp * hat.hat_env * 0.3f; hat.hat_env *= expf(-dt/(HAT_DECAY_MS/1000.0f));
        }
        if (bar >= 24 && hat.hat_open > 0.001f) {
            float noise = ((float)rand()/RAND_MAX)*2-1;
            hat_out += noise * hat.hat_open * 0.15f;
            hat.hat_open *= expf(-dt/(HAT_OPEN_DECAY_MS/1000.0f));
        }
        
        float mix = pad_out + bass_out + lead_out + bell_out + kick_out + snare_out + hat_out;
        float reverb_out = reverb_process(&reverb, mix + snare_out*2.0f, dt);
        float delay_out = ping_pong_process(&delay, mix, dt);
        float left = mix + reverb_out*0.25f + delay_out*0.2f;
        float right = mix + reverb_out*0.25f - delay_out*0.2f;
        left = tanh_soft(left * master_gain * 0.7f);
        right = tanh_soft(right * master_gain * 0.7f);
        output[i*2] = left; output[i*2+1] = right;
    }
    
    FILE *f = fopen(filename, "wb");
    if (!f) { free(output); return; }
    int sr = (int)SAMPLE_RATE, ch = 2, bits = 16;
    int data_size = total_samples * ch * (bits/8);
    int file_size = 36 + data_size;
    fwrite("RIFF",1,4,f); fwrite(&file_size,4,1,f);
    fwrite("WAVEfmt ",1,8,f); int fs=16; fwrite(&fs,4,1,f);
    short ft=1; fwrite(&ft,2,1,f); fwrite(&ch,2,1,f); fwrite(&sr,4,1,f);
    int br=sr*ch*(bits/8); fwrite(&br,4,1,f); short ba=ch*(bits/8); fwrite(&ba,2,1,f); fwrite(&bits,2,1,f);
    fwrite("data",1,4,f); fwrite(&data_size,4,1,f);
    for (int i=0;i<total_samples;i++) {
        int16_t ls = (int16_t)(clamp(output[i*2],-1,1)*32767.0f);
        int16_t rs = (int16_t)(clamp(output[i*2+1],-1,1)*32767.0f);
        fwrite(&ls,2,1,f); fwrite(&rs,2,1,f);
    }
    fclose(f); free(output);
    printf("Generated %s (%d samples, %d Hz, stereo)\n", filename, total_samples, sr);
}

int main(void) { generate_audio("track.wav"); return 0; }
