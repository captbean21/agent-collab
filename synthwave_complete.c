#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define SAMPLE_RATE 44100
#define BPM 110.0f
#define STEPS_PER_BAR 16
#define TOTAL_BARS 72
#define SAMPLES_PER_STEP (SAMPLE_RATE * 60.0f / BPM / STEPS_PER_BAR)
#define TOTAL_SAMPLES ((int)(SAMPLES_PER_STEP * STEPS_PER_BAR * TOTAL_BARS))

/* Existing types and function declarations */
typedef struct {
    float phase;
    float freq;
    float mod_ratio;
    float mod_depth;
    float amp;
    float env;
    float env_target;
    float env_rate;
} FMVoice;

typedef struct {
    float phase;
    float freq;
    float filter_freq;
    float filter_env;
    float filter_env_target;
    float filter_env_rate;
    float lfo_phase;
    float lfo_freq;
    float lfo_depth;
    float chorus_depth;
    float amp;
    float env;
    float env_target;
    float env_rate;
} VAVoice;

typedef struct {
    float phase;
    float freq;
    float start_freq;
    float end_freq;
    float env;
    float env_target;
    float env_rate;
    float hpf_phase;
    float hpf_freq;
} KickVoice;

typedef struct {
    float phase;
    float freq;
    float noise_phase;
    float env;
    float env_target;
    float env_rate;
    float noise_env;
    float noise_env_target;
    float noise_env_rate;
} SnareVoice;

typedef struct {
    float noise_phase;
    float env;
    float env_target;
    float env_rate;
    float hpf_phase;
    float hpf_freq;
    float open;
} HatVoice;

typedef struct {
    float y1, y2;
    float x1, x2;
    float a;
    float b;
} StateVarFilter;

typedef struct {
    float delay_buf[256];
    int delay_idx;
    float feedback;
    float mix;
    float noise_gate;
    float noise_gate_target;
    float noise_gate_rate;
} SchroederReverb;

typedef struct {
    float delay_buf[1024];
    int delay_idx;
    float feedback;
    float mix;
    float ping;
    float pong;
} PingPongDelay;

/* Existing function declarations */
void fm_init(FMVoice *v);
void fm_set_freq(FMVoice *v, float freq);
float fm_process(FMVoice *v);

void va_init(VAVoice *v);
void va_set_freq(VAVoice *v, float freq);
void va_set_filter_env(VAVoice *v, float target, float rate);
float va_process(VAVoice *v);

void kick_init(KickVoice *v);
void kick_trigger(KickVoice *v);
float kick_process(KickVoice *v);

void snare_init(SnareVoice *v);
void snare_trigger(SnareVoice *v);
float snare_process(SnareVoice *v);

void hat_init(HatVoice *v);
void hat_trigger(HatVoice *v, int open);
float hat_process(HatVoice *v);

void svf_init(StateVarFilter *f, float freq, float q);
float svf_process(StateVarFilter *f, float input);

void reverb_init(SchroederReverb *r);
float reverb_process(SchroederReverb *r, float input);

void ping_pong_init(PingPongDelay *d);
float ping_pong_process(PingPongDelay *d, float input);

float clamp(float x, float min, float max);
float lerp(float a, float b, float t);
float smoothstep(float edge0, float edge1, float x);
float tanh_soft(float x);

/* Helper: frequency from MIDI note */
static float midi_to_freq(float midi) {
    return 440.0f * powf(2.0f, (midi - 69.0f) / 12.0f);
}

/* Chord progression: Am - F - C - G (i - VI - III - VII in A minor) */
/* Each chord: 3 notes (root, 3rd, 5th) */
static const float chords[4][3] = {
    {57.0f, 60.0f, 64.0f},  /* A3, C4, E4 */
    {53.0f, 57.0f, 60.0f},  /* F3, A3, C4 */
    {48.0f, 52.0f, 55.0f},  /* C3, E3, G3 */
    {55.0f, 59.0f, 62.0f}   /* G3, B3, D4 */
};

/* Bass root notes (one octave below chord root) */
static const float bass_roots[4] = {
    45.0f,  /* A2 */
    41.0f,  /* F2 */
    36.0f,  /* C2 */
    43.0f   /* G2 */
};

/* Lead melody notes (sparse, on steps 0, 6, 8, 14) */
/* Simple synthwave melody in A minor */
static const float lead_melody[16] = {
    69.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, 72.0f, -1.0f,
    74.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, 71.0f, -1.0f
};

/* Sidechain envelope follower */
typedef struct {
    float env;
    float attack_rate;
    float release_rate;
    float depth;
} Sidechain;

static void sidechain_init(Sidechain *sc) {
    sc->env = 0.0f;
    sc->attack_rate = 1.0f / (0.002f * SAMPLE_RATE); /* 2ms attack */
    sc->release_rate = 1.0f / (0.150f * SAMPLE_RATE); /* 150ms release */
    sc->depth = 0.7f;
}

static void sidechain_trigger(Sidechain *sc) {
    sc->env = 1.0f;
}

static float sidechain_process(Sidechain *sc) {
    if (sc->env > 0.0f) {
        sc->env -= sc->release_rate;
        if (sc->env < 0.0f) sc->env = 0.0f;
    }
    return 1.0f - (sc->env * sc->depth);
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
}
