// moody_driving_60s.c — 60s moody synth driving track with full production
// gcc moody_driving_60s.c -o moody_driving_60s -lm -O3
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SR 44100
#define PI 3.14159265f
#define TAU 6.2831853f
// Oscillators
float osc_sin(float f,float t){ return sinf(f*t*TAU); }
float osc_saw(float f,float t){ float p=fmodf(f*t,1.0f); return p*2-1; }
float osc_sq(float f,float t){ float p=fmodf(f*t,1.0f); return p<0.5f?1:-1; }
float osc_tri(float f,float t){ float p=fmodf(f*t,1.0f); return 1-2*fabsf(p-0.5f); }
// ADSR
float adsr(float t,float a,float d,float s,float r,float on,float off){
  if(t<on) return 0; if(t<off){ float dt=t-on; if(dt<a) return dt/a; dt-=a; if(dt<d) return 1-(1-s)*(dt/d); return s; }
  float dt=t-off; float v=s*(1-dt/r); return v>0?v:0; }
// 4-pole ladder filter
typedef struct{float s1,s2,s3,s4;}F;
float ladder(float in,F*f,float c,float r){ float fc=c/SR; if(fc<0.001)fc=0.001; if(fc>0.49)fc=0.49; float fb=r*4*(1-fc); in-=f->s4*fb; f->s1+=fc*(tanhf(in)-tanhf(f->s1)); f->s2+=fc*(tanhf(f->s1)-tanhf(f->s2)); f->s3+=fc*(tanhf(f->s2)-tanhf(f->s3)); f->s4+=fc*(tanhf(f->s3)-tanhf(f->s4)); return f->s4; }
// One-pole for sidechain
float onepole(float in,float*state,float coeff){ *state+=coeff*(in-*state); return *state; }
// Noise
float randf(){ return (rand()/(float)RAND_MAX)*2-1; }
int main(){ srand(42); int sec=60; int N=SR*sec; int16_t*buf=calloc(N*2,sizeof(int16_t));
  // Delay buffers (2 sec)
  static float dl[SR*2]={0}, dr[SR*2]={0}; int dpos=0;
  // Reverb (simple allpass+comb)
  static float rv_l[SR]={0}, rv_r[SR]={0}; int rpos=0;
  // Filters
  F f_bass={0}, f_arp={0}, f_pad1={0}, f_pad2={0}, f_chord={0};
  // Sidechain envelope state
  float sc_env=0; const float sc_coeff_atk=1-expf(-1/(0.001f*SR)), sc_coeff_rel=1-expf(-1/(0.15f*SR));
  // Section timing
  float sec_t[]={0,8,20,32,44,56}; int nsec=6;
  float sec_bpm[]={105,115,120,95,120,100};
  float sec_cut[]={200,800,2000,300,1800,400};
  float sec_res[]={0.2f,0.4f,0.6f,0.3f,0.5f,0.2f};
  float sec_dly[]={0.15f,0.25f,0.30f,0.55f,0.30f,0.40f};
  // Patterns
  float bass_pat[]={55,55,0,55, 61.7f,61.7f,0,61.7f, 49,49,0,49, 55,55,0,55};
  float arp_pat[]={55,65.4f,73.4f,82.4f, 98,82.4f,73.4f,65.4f};
  float chord_pat[]={55,0,61.7f,0, 49,0,51.9f,0, 55,0,73.4f,0};
  // Velocity humanization tables (precomputed)
  float vel_kick[16], vel_hat[32], vel_arp[16];
  for(int i=0;i<16;i++) vel_kick[i]=0.9f+randf()*0.2f;
  for(int i=0;i<32;i++) vel_hat[i]=0.7f+randf()*0.6f;
  for(int i=0;i<16;i++) vel_arp[i]=0.6f+randf()*0.5f;
  for(int i=0;i<N;i++){
    float t=(float)i/SR;
    // Section detection
    int sec=0; for(int s=nsec-1;s>=0;s--) if(t>=sec_t[s]){sec=s;break;}
    float bpm=sec_bpm[sec]; float B=60/bpm; float B4=B/4; float B2=B/2; float B8=B/8;
    int beat16=(int)(t/B4)%16; int beat8=(int)(t/B2)%8; int beat4=(int)(t/B)%4;
    float bar_pos=fmodf(t,B*4);
    // KICK trigger
    float kick_trig = bar_pos<0.01f;
    if(kick_trig){ sc_env=1.0f; }
    // Sidechain envelope
    float sc_target = kick_trig ? 1.0f : 0.0f;
    float sc_coeff = sc_target>sc_env ? sc_coeff_atk : sc_coeff_rel;
    sc_env += sc_coeff*(sc_target-sc_env);
    float sc_duck = 1.0f - sc_env*0.25f; // -12dB ≈ 0.25 linear
    // HAT trigger (8th notes)
    float hat_phase=fmodf(t,B8); float hat_trig=hat_phase<0.005f;
    // CLAP trigger (beats 2&4, chorus only)
    float clap_trig=0; if(sec==2||sec==4){ clap_trig = (beat4==1||beat4==3) && bar_pos<0.01f; }
    // Note frequencies
    float bass_f = bass_pat[beat16];
    float arp_f = arp_pat[beat8%8];
    float chord_f = chord_pat[beat4*2];
    // Envelopes per 16th
    float n16_pos=fmodf(t,B4);
    float bass_env=adsr(n16_pos,0.002f,0.08f,0.35f,0.25f,0,B4*0.9f);
    float arp_env=adsr(fmodf(t,B2),0.001f,0.04f,0.15f,0.08f,0,B2*0.85f);
    float chord_env=adsr(fmodf(t,B2),0.01f,0.3f,0.5f,0.4f,0,B2*0.8f);
    float pad_env=adsr(t,2.0f,8.0f,0.7f,4.0f,0,55);
    // Filter cutoff automation per section
    float bass_cut = sec_cut[sec] + bass_env*1200;
    float arp_cut = sec_cut[sec]*1.5f + arp_env*2000;
    float pad1_cut = 200 + t*30 + (sec==2?1500:0); // slow sweep
    float pad2_cut = 400 + t*20;
    float chord_cut = sec_cut[sec]*0.4f;
    float res = sec_res[sec];
    float mix=0;
    // KICK
    if(kick_trig){
      float kick_t = fmodf(t,0.01f);
      float pitch = 60*expf(-kick_t*15) + 30;
      float kick_env = expf(-kick_t*20);
      mix += osc_sin(pitch,t)*kick_env*1.4f*vel_kick[beat16%16];
    }
    // HAT
    if(hat_trig){
      float hat_env = expf(-hat_phase*150);
      float hp = randf() - randf(); // crude HP
      mix += hp*hat_env*0.1f*vel_hat[beat8%32];
    }
    // CLAP
    if(clap_trig){
      float clap_t = fmodf(t,0.01f);
      float clap_env = expf(-clap_t*30);
      mix += (randf()*0.7f + osc_sin(200,t)*0.3f)*clap_env*0.5f;
    }
    // SUB BASS (sidechained)
    float sub = osc_sin(27.5f,t)*0.6f*pad_env*sc_duck;
    mix += sub;
    // MID BASS
    if(bass_f>0){
      float raw = osc_saw(bass_f,t) + osc_sq(bass_f*0.5f,t)*0.3f;
      float filt = ladder(raw*bass_env*sc_duck, &f_bass, bass_cut, 0.55f);
      mix += filt*0.7f;
    }
    // ARP (velocity humanized)
    if(sec!=0){ // no arp in intro
      float arp_v = vel_arp[beat8%16];
      float raw = osc_saw(arp_f,t)*arp_v + osc_tri(arp_f*2,t)*0.15f;
      float filt = ladder(raw*arp_env, &f_arp, arp_cut, 0.4f);
      mix += filt*0.22f;
    }
    // PAD 1 (wide, slow attack, sidechained)
    if(sec<4){ // no pad in bridge/outro
      float p1 = osc_saw(55*0.5f,t)*0.5f + osc_sq(55*0.7f,t)*0.3f;
      float p1f = ladder(p1*pad_env*sc_duck*0.5f, &f_pad1, pad1_cut, 0.3f);
      // Haas stereo
      float p1l = p1f*0.8f; float p1r = p1f*0.8f;
      mix += (p1l+p1r)*0.12f;
    }
    // PAD 2 (shimmer on chorus)
    if(sec==2||sec==4){
      float p2 = osc_sin(55*1.5f,t) + osc_sin(55*2.5f,t)*0.5f;
      float p2f = ladder(p2*pad_env*0.3f, &f_pad2, pad2_cut, 0.2f);
      mix += p2f*0.18f;
    }
    // CHORD STABS (chorus only)
    if((sec==2||sec==4) && chord_f>0){
      float raw = osc_saw(chord_f,t) + osc_saw(chord_f*1.189f,t) + osc_saw(chord_f*1.498f,t);
      float filt = ladder(raw*chord_env, &f_chord, chord_cut, 0.25f);
      mix += filt*0.3f;
    }
    // DELAY (ping-pong, tempo-synced dotted 8th)
    float dly_t = 0.75f*B; // dotted 8th
    int ds = (int)(dly_t*SR);
    float fb = 0.3f + sec*0.05f;
    float dmx = sec_dly[sec];
    float dl_o = dl[(dpos+2*SR-ds)%(2*SR)];
    float dr_o = dr[(dpos+2*SR-ds)%(2*SR)];
    dl[dpos] = mix*(1-dmx) + dr_o*fb;
    dr[dpos] = mix*(1-dmx) + dl_o*fb;
    mix += (dl_o+dr_o)*dmx;
    dpos = (dpos+1)%(2*SR);
    // REVERB (pads only, simple)
    float rv_in = (sec<4) ? mix*0.3f : 0;
    float rv_l_o = rv_l[rpos]; float rv_r_o = rv_r[rpos];
    rv_l[rpos] = rv_in + rv_r_o*0.7f;
    rv_r[rpos] = rv_in + rv_l_o*0.7f;
    mix += (rv_l_o+rv_r_o)*0.08f;
    rpos = (rpos+1)%SR;
    // MASTER
    float out = tanhf(mix*0.8f);
    // Soft limiter
    if(out>0.9f) out=0.9f+(out-0.9f)*0.1f;
    if(out<-0.9f) out=-0.9f+(out+0.9f)*0.1f;
    int16_t s=(int16_t)(out*32767); if(s>32767)s=32767; if(s<-32768)s=-32768;
    buf[i*2]=s; buf[i*2+1]=s;
  }
  FILE*f=fopen("moody_driving_60s.wav","wb");
  uint32_t tot=36+N*4; fwrite("RIFF",1,4,f); fwrite(&tot,4,1,f); fwrite("WAVE",1,4,f);
  fwrite("fmt ",1,4,f); uint32_t fmt=16; fwrite(&fmt,4,1,f); uint16_t ft=1, ch=2; fwrite(&ft,2,1,f); fwrite(&ch,2,1,f);
  uint32_t sru=SR; fwrite(&sru,4,1,f); uint32_t br=SR*4; fwrite(&br,4,1,f); uint16_t ba=4, bits=16; fwrite(&ba,2,1,f); fwrite(&bits,2,1,f);
  fwrite("data",1,4,f); uint32_t data_len=tot-36; fwrite(&data_len,4,1,f); fwrite(buf,2,N*2,f); fclose(f); free(buf);
  printf("moody_driving_60s.wav — 60s (intro/verse/chorus/bridge/chorus/outro)\n"); return 0; }