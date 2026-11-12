import re

with open('synthwave.c', 'r') as f:
    content = f.read()

# FIX 1: Fix the generate_audio loop - key problems:
# a) Step calculation uses float cast incorrectly
# b) Voices trigger/release every sample - should use last_step tracking
# c) Section tracking resets bar_in_section incorrectly
# d) Need to accumulate signal properly

old_loop_start = 'void generate_audio() {'
new_loop = '''void generate_audio() {
    float dt = 1.0f / SAMPLE_RATE;
    float step_duration_sec = 4.0f * 60.0f / 128.0f / 16.0f;  /* 16th note at 128 BPM */
    int step_samples = (int)(step_duration_sec * SAMPLE_RATE + 0.5f);
    if (step_samples < 1) step_samples = 1;
    
    int samples_per_bar = step_samples * MAX_STEPS; /* 16 steps = 1 bar (4 beats) */
    
    int last_step = -1;  /* Track when we actually change steps */
    int current_voice_states[NUM_VOICES];
    int current_drum_states[NUM_DRUMS];
    
    for (int s = 0; s < max_samples; s++) {
        int total_step = s / step_samples;
        int step_in_song = total_step;
        int step_in_bar = step_in_song % MAX_STEPS;
        int bar = step_in_song / MAX_STEPS;
        
        /* Determine section - accumulate bars */
        int section_idx = 0;
        int bar_offset = bar;
        int running_bar = 0;
        for (int i = 0; i < 6; i++) {
            int section_end = running_bar + sections[i].bars;
            if (bar_offset < section_end) {
                section_idx = i;
                bar_offset = bar_offset - running_bar;
                break;
            }
            running_bar = section_end;
        }
        
        int pattern_idx = sections[section_idx].pattern[bar_offset % 4];
        Step *step = &patterns[pattern_idx].steps[step_in_bar];
        
        float left_mix = 0.0f;
        float right_mix = 0.0f;
        
        /* Only trigger/release on step change */
        if (step_in_song != last_step) {
            /* FM Voices */
            for (int v = 0; v < 2; v++) {
                if (step->voice_active[v] && step->velocity[v] > 0.01f) {
                    adsr_trigger(&fm_voices[v].env);
                } else {
                    adsr_release(&fm_voices[v].env);
                }
            }
            /* VA Oscillators */
            for (int v = 2; v < NUM_VOICES; v++) {
                int va_idx = v - 2;
                if (step->voice_active[v] && step->velocity[v] > 0.01f) {
                    adsr_trigger(&va_osc[va_idx].env);
                } else {
                    adsr_release(&va_osc[va_idx].env);
                }
            }
            /* Drums */
            for (int d = 0; d < NUM_DRUMS; d++) {
                if (step->drum_active[d] && step->drum_velocity[d] > 0.01f) {
                    adsr_trigger(&drums[d].env);
                } else {
                    adsr_release(&drums[d].env);
                }
            }
            last_step = step_in_song;
        }
        
        /* Update all voices (continuous synthesis) */
        for (int v = 0; v < 2; v++) {
            float vel = (step->voice_active[v]) ? step->velocity[v] : 0.0f;
            fm_update(&fm_voices[v], dt, vel);
            left_mix += fm_voices[v].output;
            right_mix += fm_voices[v].output;
        }
        for (int v = 0; v < 2; v++) {
            float vel = (step->voice_active[v+2]) ? step->velocity[v+2] : 0.0f;
            va_update(&va_osc[v], dt, vel);
            left_mix += va_osc[v].output;
            right_mix += va_osc[v].output;
        }
        for (int d = 0; d < NUM_DRUMS; d++) {
            float vel = (step->drum_active[d]) ? step->drum_velocity[d] : 0.0f;
            drum_update(&drums[d], dt, vel);
            left_mix += drums[d].output;
            right_mix += drums[d].output;
        }
        
        /* Effects - run every sample */
        float delay_left_in = left_mix;
        float delay_right_in = right_mix;
        
        /* Simple ping-pong: alternate delay taps */
        static float ping_buf_left[BUFFER_SIZE];
        static float ping_buf_right[BUFFER_SIZE];
        static int ping_idx = 0;
        
        int delay_read_idx = (ping_idx + 1) % BUFFER_SIZE;
        float ping_delayed_l = ping_buf_left[delay_read_idx];
        float ping_delayed_r = ping_buf_right[delay_read_idx];
        
        ping_buf_left[ping_idx] = delay_left_in + 0.4f * ping_delayed_l;
        ping_buf_right[ping_idx] = delay_right_in + 0.4f * ping_delayed_r;
        ping_idx++;
        if (ping_idx >= BUFFER_SIZE) ping_idx = 0;
        
        float delayed_left = delay_left_in * 0.7f + ping_delayed_l * 0.3f;
        float delayed_right = delay_right_in * 0.7f + ping_delayed_r * 0.3f;
        
        /* Reverb - simple comb filter approximation */
        static float rev_buf[BUFFER_SIZE];
        static int rev_idx = 0;
        int rev_read = (rev_idx + 200) % BUFFER_SIZE;
        float rev_delayed = rev_buf[rev_read];
        float rev_input = (delayed_left + delayed_right) * 0.5f;
        rev_buf[rev_idx] = rev_input;
        float reverb_out = rev_input * 0.7f + rev_delayed * 0.3f;
        rev_idx++;
        if (rev_idx >= BUFFER_SIZE) rev_idx = 0;
        
        /* Final mix with reverb added as stereo */
        float final_left = delayed_left + reverb_out * 0.2f;
        float final_right = delayed_right + reverb_out * 0.2f;
        
        /* Hard clamp */
        if (final_left > 1.0f) final_left = 1.0f;
        if (final_left < -1.0f) final_left = -1.0f;
        if (final_right > 1.0f) final_right = 1.0f;
        if (final_right < -1.0f) final_right = -1.0f;
        
        /* Scale up - the signals may be very quiet */
        float scale = 0.8f;
        final_left *= scale;
        final_right *= scale;
        
        if (stereo_buffer) {
            if (s * 2 + 1 < max_samples * 2) {
                stereo_buffer[s * 2] = final_left;
                stereo_buffer[s * 2 + 1] = final_right;
            }
        }
    }
}'''

# Find the old function and replace
content = content.replace('void generate_audio() {', new_loop)

with open('synthwave.c', 'w') as f:
    f.write(content)

print('Fixed generate_audio in synthwave.c')
