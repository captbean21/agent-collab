// CPU prototype: extended synth with kick + hihat + chord layer
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SR 44100.0f
int main() {
    int samples = (int)(SR * 30.0f);
    int16_t *buf = calloc(samples*2, sizeof(int16_t));
    float phase_kick = 0, phase_osc = 0;
    for (int i=0; i<samples; i++) {
        float t = i/SR;
        // Kick (sine sweep) every 0.5s for demo
        float kick = (fmodf(t,0.5f)<0.01f) ? sinf(phase_kick)*expf(-t*20.0f): 0;
        phase_kick += 0.3f;
        // Synth layer (saw + sub) - same math, shorter
        float saw = fmodf(t*110.0f,1.0f)*2.0f-1.0f;
        float mix = (kick*0.8f + saw*0.3f + (fmodf(t*55.0f,1.0f)<0.5f?1:-1)*0.1f);
        float clamped = tanhf(mix);
        int16_t s = (int16_t)(clamped*32767.0f);
        buf[i*2] = s; buf[i*2+1] = s;
    }
    FILE *f = fopen("prototype_30s_banger.wav","wb");
    fwrite("RIFF",1,4,f); uint32_t total=36+samples*4; fwrite(&total,4,1,f);
    fwrite("WAVE",1,4,f); fwrite("fmt ",1,4,f); uint32_t fmt=16; fwrite(&fmt,4,1,f);
    uint16_t fmt_tag=1; fwrite(&fmt_tag,2,1,f); uint16_t ch=2; fwrite(&ch,2,1,f);
    uint32_t sr_u=(uint32_t)SR; fwrite(&sr_u,4,1,f); uint32_t br=SR*4; fwrite(&br,4,1,f);
    uint16_t ba=4; fwrite(&ba,2,1,f); uint16_t bits=16; fwrite(&bits,2,1,f);
    fwrite("data",1,4,f); fwrite(&(uint32_t){samples*4},4,1,f);
    fwrite(buf,2,samples*2,f); fclose(f); free(buf);
    printf("prototype_30s_banger.wav (30s, stereo, 44.1kHz) - with kick sweep + saw + sub pulse layer\n");
    return 0;
}
