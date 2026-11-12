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

/* ==================== Main / Generate ==================== */
int main(void) {
    float dt = 1.0f / SAMPLE_RATE;
    int total_samples = (int)(BPM * 4.0f * 60.0f / BPM * 110.0f * 2.25f * 4.0f); /* Approx ~2:15 */
    int n = (int)(2.25f * 60.0f * SAMPLE_RATE);
    FILE *f = fopen("track.wav", "wb");
    int sr = (int)SAMPLE_RATE;
    int ch = 2;
    int bits = 16;
    int data_size = n * ch * (bits/8);
    fprintf(f, "RIFF");
    fwrite(&(int){36 + data_size}, 4, 1, f);
    fprintf(f, "WAVEfmt ");
    int fmt_size = 16;
    fwrite(&fmt_size, 4, 1, f);
    int fmt_tag = 1; fwrite(&fmt_tag, 2, 1, f);
    fwrite(&ch, 2, 1, f);
    fwrite(&sr, 4, 1, f);
    int byte_rate = sr * ch * (bits/8);
    fwrite(&byte_rate, 4, 1, f);
    int block_align = ch * (bits/8); fwrite(&block_align, 2, 1, f);
    fwrite(&bits, 2, 1, f);
    fprintf(f, "data");
    fwrite(&(int){data_size}, 4, 1, f);

    /* Section automation: less start, more later */
    float sections[6][2] = {{0.35f, 0.55f}, {0.55f, 0.75f}, {0.75f, 0.85f}, {0.65f, 0.85f}, {0.85f, 0.95f}, {0.95f, 0.0f}};
    float master = 0.0f;

    for (int s = 0; s < n; s++) {
        float t = (float)s / (float)SAMPLE_RATE;
        float bar_f = (t * BPM) / 60.0f;
        int bar = (int)bar_f;
        int section = (bar < 8) ? 0 : (bar < 24) ? 1 : (bar < 40) ? 2 : (bar < 48) ? 3 : (bar < 64) ? 4 : 5;
        float target = (section >= 6) ? 0.0f : sections[section][1];
        /* Dynamic: lower at start, build through sections */
        float intro_scale = (bar < 8) ? 0.5f + 0.5f * ((float)bar / 8.0f) : 1.0f;
        float chorus_boost = (section == 2 || section == 4) ? 1.15f : 1.0f;
        float outro_fade = (section == 5) ? 1.0f - ((float)(bar - 64) / 8.0f) : 1.0f;
        master = target * intro_scale * chorus_boost * outro_fade;
        master = fminf(master, 0.95f);

        float left = 0.0f, right = 0.0f;
        /* Simple synth signal for audible output */
        float phase = 2.0f * M_PI * 220.0f * t;
        float sig = 0.5f * sinf(phase) + 0.3f * sinf(phase * 2.0f + 0.5f) + 0.2f * sinf(phase * 4.0f);
        float env = 1.0f - 0.3f * expf(-t / 0.5f); /* Quick build */
        left = sig * env * master;
        right = sig * env * master * 0.95f + 0.05f * sinf(phase + 0.3f);
        left = fminf(fmaxf(left, -0.9f), 0.9f);
        right = fminf(fmaxf(right, -0.9f), 0.9f);
        int16_t ls = (int16_t)(left * 32767.0f);
        int16_t rs = (int16_t)(right * 32767.0f);
        fwrite(&ls, 2, 1, f); fwrite(&rs, 2, 1, f);
    }
    fclose(f);
    printf("Wrote track.wav (%d samples, stereo, %d Hz)\n", n, sr);
    return 0;
}
/* Generate audio function */
void generate_audio(const char *filename) {
    /* Allocate output buffer */
    float *output = (float *)malloc(TOTAL_SAMPLES * 2 * sizeof(float));
    if (!output) {
        fprintf(stderr, "Memory allocation failed\n");
        return;
    }
    memset(output, 0, TOTAL_SAMPLES * 2 * sizeof(float));

    /* Initialize voices */
    FMVoice lead_fm;
    VAVoice pad_va;
    KickVoice kick;
    SnareVoice snare;
    HatVoice hat;
    StateVarFilter bass_filter;
    SchroederReverb reverb;
    PingPongDelay delay;
    Sidechain sidechain;

    fm_init(&lead_fm);
    va_init(&pad_va);
    kick_init(&kick);
    snare_init(&snare);
    hat_init(&hat);
    svf_init(&bass_filter, 800.0f, 1.0f);
    reverb_init(&reverb);
    ping_pong_init(&delay);
    sidechain_init(&sidechain);

    /* Section boundaries (in bars) */
    int intro_start = 0, intro_end = 7;
    int verse_start = 8, verse_end = 23;
    int chorus1_start = 24, chorus1_end = 39;
    int bridge_start = 40, bridge_end = 47;
    int chorus2_start = 48, chorus2_end = 63;
    int outro_start = 64, outro_end = 71;

    /* Process each sample */
    for (int i = 0; i < TOTAL_SAMPLES; i++) {
        int bar = (i / (int)SAMPLES_PER_STEP) / STEPS_PER_BAR;
        int step = ((i / (int)SAMPLES_PER_STEP) % STEPS_PER_BAR);
        int chord_idx = bar % 4;

        /* Determine section */
        float section_gain = 0.5f;
        int is_intro = (bar >= intro_start && bar <= intro_end);
        int is_verse = (bar >= verse_start && bar <= verse_end);
        int is_chorus1 = (bar >= chorus1_start && bar <= chorus1_end);
        int is_bridge = (bar >= bridge_start && bar <= bridge_end);
        int is_chorus2 = (bar >= chorus2_start && bar <= chorus2_end);
        int is_outro = (bar >= outro_start && bar <= outro_end);

        /* Section automation */
        if (is_intro) {
            float t = (float)(bar - intro_start) / (float)(intro_end - intro_start + 1);
            section_gain = lerp(0.35f, 0.55f, smoothstep(0.0f, 1.0f, t));
        } else if (is_verse) {
            float t = (float)(bar - verse_start) / (float)(verse_end - verse_start + 1);
            section_gain = lerp(0.55f, 0.75f, smoothstep(0.0f, 1.0f, t));
        } else if (is_chorus1) {
            float t = (float)(bar - chorus1_start) / (float)(chorus1_end - chorus1_start + 1);
            section_gain = lerp(0.75f, 0.85f, smoothstep(0.0f, 1.0f, t));
        } else if (is_bridge) {
            section_gain = 0.65f;
        } else if (is_chorus2) {
            float t = (float)(bar - chorus2_start) / (float)(chorus2_end - chorus2_start + 1);
            section_gain = lerp(0.85f, 0.95f, smoothstep(0.0f, 1.0f, t));
        } else if (is_outro) {
            float t = (float)(bar - outro_start) / (float)(outro_end - outro_start + 1);
            section_gain = lerp(0.95f, 0.0f, smoothstep(0.0f, 1.0f, t));
        }

        /* Pad VA: sustained chords, new chord each bar */
        float pad_out = 0.0f;
        if (is_intro || is_verse || is_chorus1 || is_bridge || is_chorus2 || is_outro) {
            float chord_freq = midi_to_freq(chords[chord_idx][0]);
            va_set_freq(&pad_va, chord_freq);
            /* Filter envelope: open during chorus, closed during bridge */
            float filter_target = 1.0f;
            float filter_rate = 0.001f;
            if (is_bridge) {
                /* Filter sweep during bridge */
                float t = (float)(bar - bridge_start) / (float)(bridge_end - bridge_start + 1);
                filter_target = lerp(0.2f, 1.0f, smoothstep(0.0f, 1.0f, t));
                filter_rate = 0.005f;
            }
            va_set_filter_env(&pad_va, filter_target, filter_rate);
            pad_out = va_process(&pad_va);
        }

        /* Bass: arpeggiated octaves on steps 0,2,4,6,8,10,12,14 */
        float bass_out = 0.0f;
        if ((is_verse || is_chorus1 || is_bridge || is_chorus2) && (step % 2 == 0)) {
            float root = bass_roots[chord_idx];
            float octave = root + 12.0f;
            float note = (step % 4 == 0) ? root : octave;
            float freq = midi_to_freq(note);
            /* Simple bass synth: sine wave with slight saturation */
            static float bass_phase = 0.0f;
            bass_phase += 2.0f * M_PI * freq / SAMPLE_RATE;
            while (bass_phase >= 2.0f * M_PI) bass_phase -= 2.0f * M_PI;
            float bass_wave = sinf(bass_phase);
            /* Apply sidechain ducking */
            float sc_gain = sidechain_process(&sidechain);
            bass_out = bass_wave * 0.5f * sc_gain;
            /* Apply lowpass filter */
            bass_out = svf_process(&bass_filter, bass_out);
        }

        /* Kick: steps 0,4,8,12 */
        float kick_out = 0.0f;
        if ((is_verse || is_chorus1 || is_chorus2) && (step == 0 || step == 4 || step == 8 || step == 12)) {
            kick_trigger(&kick);
            kick_out = kick_process(&kick);
            /* Trigger sidechain */
            sidechain_trigger(&sidechain);
        }

        /* Snare: steps 4,12 */
        float snare_out = 0.0f;
        if ((is_chorus1 || is_chorus2) && (step == 4 || step == 12)) {
            snare_trigger(&snare);
            snare_out = snare_process(&snare);
        }

        /* Hats: closed on 8th notes, open on & of each beat */
        float hat_out = 0.0f;
        if (is_chorus1 || is_chorus2) {
            int closed_hat = (step % 2 == 0);
            int open_hat = (step == 2 || step == 6 || step == 10 || step == 14);
            if (closed_hat && !open_hat) {
                hat_trigger(&hat, 0);
                hat_out = hat_process(&hat);
            } else if (open_hat) {
                hat_trigger(&hat, 1);
                hat_out = hat_process(&hat);
            }
        }

        /* Lead FM: melody on steps 0, 6, 8, 14 */
        float lead_out = 0.0f;
        if ((is_chorus1 || is_chorus2) && (step == 0 || step == 6 || step == 8 || step == 14)) {
            float note = lead_melody[step];
            if (note > 0.0f) {
                float freq = midi_to_freq(note);
                fm_set_freq(&lead_fm, freq);
                lead_out = fm_process(&lead_fm);
            }
        }

        /* Mix all elements */
        float mix = 0.0f;
        mix += pad_out * 0.4f;
        mix += bass_out * 0.6f;
        mix += kick_out * 0.8f;
        mix += snare_out * 0.5f;
        mix += hat_out * 0.3f;
        mix += lead_out * 0.5f;

        /* Apply reverb */
        float reverb_out = reverb_process(&reverb, mix);
        mix += reverb_out * 0.3f;

        /* Apply ping-pong delay */
        float delay_out = ping_pong_process(&delay, mix);
        mix += delay_out * 0.2f;

        /* Apply section gain */
        mix *= section_gain;

        /* Soft clip to prevent harsh peaks */
        mix = tanh_soft(mix * 1.5f);

        /* Clamp to [-1.0, 1.0] */
        mix = clamp(mix, -1.0f, 1.0f);

        /* Write to stereo output (same for L and R) */
        output[i * 2] = mix;
        output[i * 2 + 1] = mix;
    }

    /* Write WAV file */
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "Failed to open %s for writing\n", filename);
        free(output);
        return;
    }

    /* WAV header */
    int data_size = TOTAL_SAMPLES * 2 * 2; /* stereo, 16-bit */
    int file_size = 44 + data_size;
    uint8_t header[44];
    memcpy(header, "RIFF", 4);
    memcpy(header + 4, (uint8_t *)&file_size, 4);
    memcpy(header + 8, "WAVE", 4);
    memcpy(header + 12, "fmt ", 4);
    uint32_t fmt_size = 16;
    memcpy(header + 16, (uint8_t *)&fmt_size, 4);
    uint16_t audio_format = 1; /* PCM */
    memcpy(header + 20, (uint8_t *)&audio_format, 2);
    uint16_t num_channels = 2;
    memcpy(header + 22, (uint8_t *)&num_channels, 2);
    uint32_t sample_rate = SAMPLE_RATE;
    memcpy(header + 24, (uint8_t *)&sample_rate, 4);
    uint32_t byte_rate = SAMPLE_RATE * 2 * 2;
    memcpy(header + 28, (uint8_t *)&byte_rate, 4);
    uint16_t block_align = 4;
    memcpy(header + 32, (uint8_t *)&block_align, 2);
    uint16_t bits_per_sample = 16;
    memcpy(header + 34, (uint8_t *)&bits_per_sample, 2);
    memcpy(header + 36, "data", 4);
    memcpy(header + 40, (uint8_t *)&data_size, 4);

    fwrite(header, 1, 44, fp);

    /* Write PCM data */
    for (int i = 0; i < TOTAL_SAMPLES; i++) {
        int16_t left = (int16_t)(output[i * 2] * 32767.0f);
        int16_t right = (int16_t)(output[i * 2 + 1] * 32767.0f);
        fwrite(&left, 1, 2, fp);
        fwrite(&right, 1, 2, fp);
    }

    fclose(fp);
    free(output);
}

int main(void) {
    generate_audio("track.wav");
    printf("Generated track.wav\n");
    return 0;
