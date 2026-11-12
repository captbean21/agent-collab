// Banger 45s — structured song: intro(8) / verse(12) / chorus(8) / bridge(6) / chorus(6) / outro(5)
// Variations: BPM, filter, arp pattern, chord stabs, delay mix, gain shift per section
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SR 44100
#define PI 3.14159265358979323846f
float osc_saw(float f,float t){ float p=fmodf(f*t,1); return p*2.0f-1.0f; }
float osc_sq(float f,float t){ float p=fmodf(f*t,1); return p<0.5f?1:-1; }
float adsr(float t,float a,float d,float s,float r,float on,float off){
  if(t<on) return 0; if(t<off){ float dt=t-on; if(dt<a) return dt/a; dt-=a; if(dt<d) return 1-(1-s)*(dt/d); return s; }
  float dt=t-off; float v=s*(1-dt/r); return v>0?v:0; }
typedef struct{float s1,s2,s3,s4;}F;
float ladder(float in,F*f,float c,float r){ float fc=c/SR; if(fc<0.001)fc=0.001; if(fc>0.49)fc=0.49; float fb=r*4*(1-fc); in-=f->s4*fb; f->s1+=fc*(tanhf(in)-tanhf(f->s1)); f->s2+=fc*(tanhf(f->s1)-tanhf(f->s2)); f->s3+=fc*(tanhf(f->s2)-tanhf(f->s3)); f->s4+=fc*(tanhf(f->s3)-tanhf(f->s4)); return f->s4; }
int main(){ srand(42); int sec=45; int samples=(int)(SR*sec); int16_t*buf=calloc(samples*2,sizeof(int16_t));
  static float delay_l[SR]={0}, delay_r[SR]={0}; int dl=0;
  // Sections: 0=intro(0-8s),1=verse(8-20),2=chorus(20-28),3=bridge(28-34),4=chorus(34-40),5=outro(40-45)
  int sec_start[]={0,8,20,28,34,40}; float sec_bpm[]={100,120,120,95,120,90}; float sec_cut[]={400,800,2000,150,1500,500}; float sec_mix[]={0.10,0.15,0.25,0.40,0.20,0.30};
  F bass_f={0},arp_f={0},ch_f={0};
  float bass_notes[] = {55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,55,55,0,55}; // 16th
  float chord_root[]  = {55,0,61.7,0,49,0,51.9,0}; // 8-beat
  float arp_notes[]   = {55,65.4,73.4,82.4,98,82.4,73.4,65.4,49,58.3,65.4,73.4,82.4,73.4,65.4,58.3}; // 16-step pent
  float bass16[] = {55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,55,55,0,55,55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,55,55,0,55,55,55,0,55,61.7,61.7,0,61.7,49,49,0,49,55,55,0,55,55,0,55};
  for(int i=0;i<samples;i++){
    float t=(float)i/SR; float beat4=fmodf(t,2.4f); float bar8=fmodf(t,9.6f);
    int section=0; for(int s=5;s>=0;s--) if(t>=sec_start[s]){section=s;break;}
    float bpm=sec_bpm[section]; float B=(60.0f/bpm); float B4=B/4.0f; float B2=B/2.0f; float B8=B/8.0f;
    float note_period=B/4.0f; int note_idx=(int)floorf(t/note_period);
    int beat16=(int)(t/(B4))%32; int beat8=(int)(t/(B2));
    int arp_step=(int)(t/(B2))%16;
    int chord_beat=beat8%8;
    int scale5[] = {0,3,5,7,10}; int p_idx=0, oct=0;
    if(section==0||section==5){ p_idx=note_idx%4; oct=0; } // intro/outro: simple arp
    else if(section==2||section==4){ p_idx=note_idx%5; oct=(note_idx/5)%3; } // chorus: 3-oct up/down
    else { p_idx=note_idx%5; oct=(note_idx/5)%2; } // verse/bridge
    int sem=scale5[p_idx]+oct*12; float freq_mul=powf(2.0f,sem/12.0f);
    float bass_fq=bass_notes[beat16%16]; float chord_fq=chord_root[chord_beat];
    float arp_fq=arp_notes[arp_step];
    float amp_env=adsr(fmodf(t,B4),0.001f,0.08f,0.3f,0.05f,0,B4*0.9f);
    float filt_env=adsr(fmodf(t,B4),0.001f,0.1f,0.2f,0.1f,0,B4*0.9f);
    float mix=0.0f;
    // KICK: beat 1 of every bar
    float bpos=fmodf(t,B*4);
    if(bpos<0.02f) mix+=1.2f*expf(-8*t)*0.8f;
    else if(bpos<B2-0.005f && bpos>B2-0.02f) mix+=0.3f; // lighter off-beat in bridge
    // HAT: every 8th (light in intro, heavy in chorus)
    float hat_trig=(fmodf(t,B/2.0f)<0.005f);
    float hat_env=hat_trig?expf(-t*80.0f):0; float hat_noise=(rand()/(float)RAND_MAX)*2-1; mix+=hat_noise*hat_env*0.15f*(section==2?1.2f:1.0f);
    // BASS
    float raw_bass=osc_saw(bass_fq,t)+osc_sq(bass_fq*0.5f,t)*0.3f; float filt_b=ladder(raw_bass*amp_env,&bass_f,sec_cut[section]+filt_env*2000,0.5f); mix+=filt_b*0.6f;
    // ARP (varies per section)
    float arp_env=adsr(fmodf(t,(B/2.0f)),0.001f,0.05f,0.1f,0.05f,0,(B/2.0f)*0.8f);
    float arp_raw=osc_saw(arp_fq*freq_mul,t)*0.5f; float filt_a=ladder(arp_raw*arp_env,&arp_f,sec_cut[section]*2+arp_env*3000,0.3f*(section==3?0.8f:1.0f)); mix+=filt_a*0.3f;
    // CHORD STABS (only chorus/verse)
    if(chord_fq>0 && (section==1||section==2||section==3||section==4)){
      float ch_t=fmodf(t,(B*2)); float ch_env=adsr(ch_t,0.01f,0.3f,0.4f,0.5f,0,(B*2)*0.7f); float chord_raw=osc_saw(chord_fq,t)+osc_saw(chord_fq*1.189f,t)+osc_saw(chord_fq*1.498f,t); float filt_c=ladder(chord_raw*ch_env,&ch_f,sec_cut[section]*0.4f,0.2f); mix+=filt_c*0.25f; }
    // DELAY ping-pong varies per section
    float dtime=0.375f; int ds=(int)(dtime*SR); float fb=0.35f;
    float dl_o=delay_l[(dl+SR-ds)%SR]; float dr_o=delay_r[(dl+SR-ds)%SR];
    float dm=sec_mix[section]; delay_l[dl]=mix*(1-dm)+dr_o*fb; delay_r[dl]=mix*(1-dm)+dl_o*fb; mix+=dl_o*dm+dr_o*dm; dl=(dl+1)%SR;
    float out=tanhf(mix*(0.7f+(section==2?0.15f:0))); // chorus boosted
    int16_t s=(int16_t)(out*32767.0f); if(s>32767)s=32767; if(s<-32768)s=-32768; buf[i*2]=s; buf[i*2+1]=s;
  }
  FILE*f=fopen("banger_45s.wav","wb"); fwrite("RIFF",1,4,f); uint32_t tot=36+samples*4; fwrite(&tot,4,1,f); fwrite("WAVE",1,4,f); fwrite("fmt ",1,4,f); uint32_t fmt=16; fwrite(&fmt,4,1,f); uint16_t ft=1; fwrite(&ft,2,1,f); uint16_t ch=2; fwrite(&ch,2,1,f); uint32_t sru=(uint32_t)SR; fwrite(&sru,4,1,f); uint32_t br=SR*4; fwrite(&br,4,1,f); uint16_t ba=4; fwrite(&ba,2,1,f); uint16_t bits=16; fwrite(&bits,2,1,f); fwrite("data",1,4,f); fwrite(&tot,4,1,f); fwrite(&tot,4,1,f); fwrite(&(uint32_t){samples*4},4,1,f); fwrite(buf,2,samples*2,f); fclose(f); free(buf); printf("banger_45s.wav: 45s structured (intro/verse/chorus/bridge/chorus/outro)\n"); return 0; }
