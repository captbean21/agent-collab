#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SR 44100
#define PI 3.14159265358979323846f

float osc_saw(float f,float t){return fmodf(f*t,1.0f)*2.0f-1.0f;}
float osc_sqr(float f,float t){return fmodf(f*t,1.0f)<0.5f?1.0f:-1.0f;}
float osc_sin(float f,float t){return sinf(f*t*2*PI);}

typedef struct{float s1,s2,s3,s4;}Filt;
float lad(float in,Filt*f,float co,float re){
    float fc=co/SR;if(fc<0.001f)fc=0.001f;if(fc>0.49f)fc=0.49f;
    float fb=re*4*(1-fc);in-=f->s4*fb;
    f->s1+=fc*(tanhf(in)-tanhf(f->s1));
    f->s2+=fc*(tanhf(f->s1)-tanhf(f->s2));
    f->s3+=fc*(tanhf(f->s2)-tanhf(f->s3));
    f->s4+=fc*(tanhf(f->s3)-tanhf(f->s4));
    return f->s4;
}
float adsr(float t,float a,float d,float s,float r,float on,float off){
    if(t<on)return 0;if(t<off){float dt=t-on;if(dt<a)return dt/a;dt-=a;if(dt<d)return 1-(1-s)*dt/d;return s;}
    float dt=t-off;float v=s*(1-dt/r);return v>0?v:0;
}

int main(){
    srand(42);
    int samples=SR*45; int16_t*buf=calloc(samples*2,sizeof(int16_t));
    Filt bf={0},af={0},cf={0},lf={0};
    static float dl[SR]={0},dr[SR]={0}; int di=0;
    float kp=0,hp=0;
    float bpm=120,beat=60/bpm,bar=beat*4;
    float bass_pat[32]={55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,55,55,0,55,55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,51.9,51.9,0,51.9};
    float ch_root[8]={55,0,61.7,0,49,0,51.9,0};
    float arp_pat[16]={55,65.4,73.4,82.4,98,82.4,73.4,65.4,49,58.3,65.4,73.4,82.4,73.4,65.4,58.3};
    float neon_arp[16]={110,130.8,146.8,164.8,196,164.8,146.8,130.8,98,116.5,130.8,146.8,164.8,146.8,130.8,116.5};
    for(int i=0;i<samples;i++){
        float t=i/44100.0f; float bp=fmodf(t,beat),brp=fmodf(t,bar);
        int b16=(int)(brp/(beat/4))%32; int bi=(int)(brp/beat)%8;
        int section=(int)(t/11.25f); // 4 sections of ~11.25s
        float energy=section==0?0.5f:section==1?0.8f:section==2?1.0f:0.6f;
        float mix=0;
        // KICK
        if(bp<0.005f)kp=0; mix+=kp<0.02f?(sinf((60*expf(-kp*8)+30)*kp*2*PI)*expf(-kp*12)*1.2f):0; kp+=1.0f/SR;
        // HAT
        float ht=(fmodf(brp,beat/2)<0.005f); if(ht)hp=0; mix+=ht?((rand()/(float)RAND_MAX*2-1)*expf(-hp*80)*0.15f):0; hp+=1.0f/SR;
        // BASS - 16ths
        float bfreq=bass_pat[b16];
        if(bfreq>0){float nt=fmodf(t,beat/4); float ev=adsr(nt,.001,.08,.3,.05,0,beat/4*.9);
            float raw=osc_saw(bfreq,t)+osc_sqr(bfreq*.5,t)*.3;
            mix+=lad(raw*ev,&bf,500+ev*2000,.5)*0.6*energy;}
        // MAIN ARP - 8ths (neon motorway style)
        float afrq=arp_pat[(int)(brp/(beat/2))%16];
        float at=fmodf(t,beat/2); float aev=adsr(at,.001,.05,.1,.05,0,beat/2*.8);
        float araw=osc_saw(afrq,t)*.5; mix+=lad(araw*aev,&af,2000+aev*3000,.3)*0.3*energy;
        // NEON ARP - 16ths, brighter (arcade highway style) - section 2+
        if(section>=1){float nf=neon_arp[(int)(brp/(beat/4))%16];
            float nt=fmodf(t,beat/4); float nev=adsr(nt,.001,.03,.05,.03,0,beat/4*.7);
            float nraw=osc_saw(nf,t)*0.3; mix+=lad(nraw*nev,&lf,3000+nev*4000,.4)*0.2*energy;}
        // CHORD STABS (dark midnight style) - beats 1,3
        float cr=ch_root[bi]; if(cr>0){
            float ct=fmodf(t,bar/2); float cev=adsr(ct,.01,.3,.4,.5,0,bar/2*.7);
            float ch=osc_saw(cr,t)+osc_saw(cr*1.189f,t)+osc_saw(cr*1.498f,t);
            mix+=lad(ch*cev,&cf,800,.2)*0.25*energy;}
        // PAD (retro sunrise style) - section 3+, whole notes
        if(section>=2){float pd=fmodf(t,bar); float pev=adsr(pd,.5,2,.8,3,0,bar*.9);
            float pd_raw=osc_saw(32.7,t)*.4+osc_sin(16.35,t)*.15;
            mix+=lad(pd_raw*pev,&lf,600+pev*800,.2)*0.3*energy;}
        // DELAY
        int ds=(int)(0.375*SR); float fb=.35; float dry=mix;
        float dlo=dl[(di+SR-ds)%SR], dro=dr[(di+SR-ds)%SR];
        dl[di]=dry+dro*fb; dr[di]=dry+dlo*fb; mix+=(dlo+dro)*.15; di=(di+1)%SR;
        // MASTER
        float out=tanhf(mix*0.7); int16_t s=(int16_t)(out*32767); buf[i*2]=s; buf[i*2+1]=s;
    }
    FILE*f=fopen("banger_45s.wav","wb");
    fwrite("RIFF",1,4,f); uint32_t tot=36+samples*4; fwrite(&tot,4,1,f);
    fwrite("WAVE",1,4,f); fwrite("fmt ",1,4,f); uint32_t fm=16; fwrite(&fm,4,1,f);
    uint16_t ft=1; fwrite(&ft,2,1,f); uint16_t ch=2; fwrite(&ch,2,1,f);
    uint32_t sru=SR; fwrite(&sru,4,1,f); uint32_t br=SR*4; fwrite(&br,4,1,f);
    uint16_t ba=4; fwrite(&ba,2,1,f); uint16_t bits=16; fwrite(&bits,2,1,f);
    fwrite("data",1,4,f); fwrite(&(uint32_t){samples*4},4,1,f);
    fwrite(buf,2,samples*2,f); fclose(f); free(buf);
    printf("banger_45s.wav done\n"); return 0;
}
