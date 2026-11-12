// Late Night Driving — 35s structured synth track
// Sections: intro(6) / verse(10) / pre-chorus(5) / chorus(9) / outro(5)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SR 44100
#define PI 3.14159265f
float osc_saw(float f,float t){ float p=fmodf(f*t,1); return p*2-1; }
float osc_sq(float f,float t){ float p=fmodf(f*t,1); return p<0.5f?1:-1; }
float osc_sin(float f,float t){ return sinf(f*t*2*PI); }
float adsr(float t,float a,float d,float s,float r,float on,float off){
  if(t<on) return 0; if(t<off){ float dt=t-on; if(dt<a) return dt/a; dt-=a; if(dt<d) return 1-(1-s)*(dt/d); return s; }
  float dt=t-off; float v=s*(1-dt/r); return v>0?v:0; }
typedef struct{float s1,s2,s3,s4;}F;
float ladder(float in,F*f,float c,float r){ float fc=c/SR; if(fc<0.001)fc=0.001; if(fc>0.49)fc=0.49; float fb=r*4*(1-fc); in-=f->s4*fb; f->s1+=fc*(tanhf(in)-tanhf(f->s1)); f->s2+=fc*(tanhf(f->s1)-tanhf(f->s2)); f->s3+=fc*(tanhf(f->s2)-tanhf(f->s3)); f->s4+=fc*(tanhf(f->s3)-tanhf(f->s4)); return f->s4; }
int main(){ srand(123); int sec=35; int samples=(int)(SR*sec); int16_t*buf=calloc(samples*2,sizeof(int16_t));
  float dl[SR]={0}; float dr[SR]={0}; int dpos=0;
  float bass_note[]={55,49,55,61.7, 55,49,55,73.4, 55,49,55,61.7, 55,49,55,73.4};
  float chord_note[]={55,0,61.7,0, 49,0,51.9,0, 55,0,73.4,0};
  float arp_note[]={55,65.4,73.4,82.4, 49,58.3,65.4,73.4};
  float sec_bpm[]={85,110,100,115,90};
  float sec_cutoff[]={300,1200,600,2000,400};
  float sec_mix[]={0.12,0.22,0.15,0.35,0.18};
  int sec_start[]={0,6,16,21,30};
  F bass_f={0},arp_f={0},ch_f={0};
  for(int i=0;i<samples;i++){
    float t=(float)i/SR; int sec_idx=0; for(int s=4;s>=0;s--){if(t>=sec_start[s]){sec_idx=s;break;}}
    float bpm=sec_bpm[sec_idx]; float B=60.0f/bpm; float B4=B/4; float B2=B/2; float B8=B/8;
    int beat4=(int)(t/B4)%16; int beat2=(int)(t/B2)%8; int step8=(int)(t/B8)%8;
    float note_fq=bass_note[beat4%16]; float chord_fq=chord_note[beat2%12]; float arp_fq=arp_note[step8%8];
    float amp_env=adsr(fmodf(t,B4),0.002f,0.06f,0.35f,0.3f,0,B4*0.9f);
    float filt_env=adsr(fmodf(t,B4),0.01f,0.3f,0.5f,1.0f,0,B4*0.9f);
    float mix=0.0f;
    // KICK: beat 1 of 4
    float bpos=fmodf(t,B*4);
    if(bpos<0.015f){ mix+=1.5f*expf(-t*12)*0.7f; }
    // HAT: 8th notes
    float hat_t=fmodf(t,B/8); float hat_trig=hat_t<0.01f; float hat_n=(rand()/(float)RAND_MAX)*2-1; float hat_env=hat_trig?expf(-hat_t*100):0; mix+=hat_n*hat_env*0.12f*(sec_idx==3?1.4f:1.0f);
    // BASS: 16th pattern
    float raw_b=osc_saw(note_fq,t)+osc_sq(note_fq*0.5f,t)*0.35f; float filt_b=ladder(raw_b*amp_env,&bass_f,sec_cutoff[sec_idx]+filt_env*1500,0.55f); mix+=filt_b*0.65f;
    // ARP: 8th note up-down pent minor
    float arp_env=adsr(fmodf(t,B2),0.001f,0.03f,0.15f,0.05f,0,B2*0.85f);
    float arp_raw=osc_saw(arp_fq,t)+osc_sin(arp_fq*2,t)*0.2f; float filt_a=ladder(arp_raw*arp_env,&arp_f,sec_cutoff[sec_idx]*1.5f+arp_env*1000,0.35f); mix+=filt_a*0.25f;
    // CHORD STABS: chorus and verse
    if(chord_fq>0 && (sec_idx==1||sec_idx==3||sec_idx==4)){
      float ch_t=fmodf(t,B2); float ch_env=adsr(ch_t,0.02f,0.4f,0.5f,0.6f,0,B2*0.8f);
      float ch_raw=osc_saw(chord_fq,t)+osc_saw(chord_fq*1.189f,t)+osc_sq(chord_fq*1.498f,t)*0.3f;
      float filt_c=ladder(ch_raw*ch_env,&ch_f,sec_cutoff[sec_idx]*0.3f,0.2f); mix+=filt_c*0.28f; }
    // SUB BASS: intro + bridge only
    if(sec_idx==0||sec_idx==4){ mix+=osc_sin(27.5f,t)*0.35f*amp_env; }
    // DELAY ping-pong (longer in chorus for space)
    float dtime=sec_idx==3?0.55f:0.30f; int ds=(int)(dtime*SR); float fb=0.32f;
    float dl_o=dl[(dpos+SR-ds)%SR]; float dr_o=dr[(dpos+SR-ds)%SR];
    float dm=sec_mix[sec_idx]; dl[dpos]=mix*(1-dm)+dr_o*fb; dr[dpos]=mix*(1-dm)+dl_o*fb;
    mix+=(dl_o+dr_o)*dm; dpos=(dpos+1)%SR;
    float out=tanhf(mix*0.75f*(sec_idx==3?1.15f:1.0f));
    int16_t s=(int16_t)(out*32767); if(s>32767)s=32767; if(s<-32768)s=-32768; buf[i*2]=s; buf[i*2+1]=s;
  }
  FILE*f=fopen("late_night_35s.wav","wb");
  fwrite("RIFF",1,4,f); uint32_t tot=36+samples*4; fwrite(&tot,4,1,f); fwrite("WAVE",1,4,f); fwrite("fmt ",1,4,f); uint32_t fmt=16; fwrite(&fmt,4,1,f); uint16_t ft=1; fwrite(&ft,2,1,f); uint16_t ch=2; fwrite(&ch,2,1,f); uint32_t sru=SR; fwrite(&sru,4,1,f); uint32_t br=SR*4; fwrite(&br,4,1,f); uint16_t ba=4; fwrite(&ba,2,1,f); uint16_t bits=16; fwrite(&bits,2,1,f); fwrite("data",1,4,f); uint32_t data_len=tot-36; fwrite(&data_len,4,1,f); fwrite(buf,2,samples*2,f); fclose(f); free(buf);
  printf("late_night_35s.wav — 35s (intro/verse/pre-chorus/chorus/outro)\n"); return 0; }
