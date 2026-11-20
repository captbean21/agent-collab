# Veldra-7 Geophysics Laboratory — Technical Specification
**Classification:** Restricted (Historical Archive)  
**Location:** Habitat Module 12, Lower Level, Veldra-7 Colony  
**Status:** Decommissioned (Contraction Era) — Reactivated ad hoc by K. Varel & E. Merrow  
**Document Version:** 1.0-draft  
**Authors:** Castle (spec architecture) / Rook (narrative integration)

---

## 1. Facility Overview

The Geophysics Laboratory (GL-7) was constructed during Veldra-7's initial colonization wave (Year 12 Post-Landing) as part of the planetary magnetic field monitoring network. Decommissioned during the Contraction (Year 87) when central administration collapsed and funding for pure research evaporated. The lab sat dormant for 113 years until unauthorized reactivation by colonists Kade Varel (robotics engineer) and Elara Merrow (mathematician/theorist).

**Original Purpose:** Continuous magnetotelluric sounding of Veldra-7's mantle; early-warning seismic network for colony infrastructure.

**Ad Hoc Purpose:** Theorem-variable injection platform — repurposing the lab's scanning suite to feed controlled mathematical/physical variables into the Theorem artifact and measure its response.

---

## 2. Facility Layout

```
Level -1 (Surface Access)
├── Airlock Alpha (Manual override only — hydraulic seals degraded)
├── Corridor: 12m × 2.4m, emergency lighting only (solar-charged capacitors)
├── Equipment Staging Bay (formerly sample prep / core storage)
└── Stairwell to Level -2 (emergency hatch, manual crank)

Level -2 (Main Laboratory)
├── Scanning Suite (Primary)
│   ├── Gamma Spectrometer Array (3× HPGe detectors, LN2-cooled — depleted)
│   ├── Neutron Activation Station (Am-Be source, 10^6 n/s — degraded to ~10^4)
│   ├── Passive Radiation Monitor Bank (8× NaI(Tl) scintillators)
│   ├── Control Console (Solid-state, radiation-hardened, battery-backed)
│   └── Data Logger (Solid-state, 512 GB — 89% full with Contraction-era seismic logs)
├── Calibration Vault (Lead-lined, sealed — source integrity unknown)
├── Auxiliary Power Room (RTG bank, 3× Sr-90 units — 2 operational, 1 cold)
└── Emergency Egress Shaft (Blocked by Contraction-era debris)
```

---

## 3. Scanning Suite — Technical Specifications

### 3.1 Gamma Spectrometer Array
- **Detectors:** 3 × High-Purity Germanium (HPGe), 70% relative efficiency
- **Cooling:** Liquid nitrogen Dewars (30 L each) — **DEPLETED**; no LN2 resupply for 113 years
- **Workaround:** Peltier cascade retrofitted by K. Varel (Year 200) — maintains 95K ± 2K on Detector 1 only; Detectors 2/3 offline
- **Energy Range:** 3 keV – 10 MeV
- **Resolution:** 1.8 keV FWHM @ 1.33 MeV (Co-60)
- **Throughput:** 10k cps max (Detector 1 only)
- **Spectral Features (Artifact Flare):** Continuous non-thermal bremsstrahlung background with discrete, unidentified emission lines at 1.3 MeV, 2.6 MeV, and 4.1 MeV. Zero correlation to known nuclear activation products.

### 3.2 Neutron Activation Station
- **Source:** Am-Be (Americium-241 / Beryllium), nominal 10^6 n/s
- **Current Output:** ~10^4 n/s (Am-241 half-life 432 yr; 113 yr decay = ~83% remaining, but Be degradation suspected)
- **Moderation:** Polyethylene shutter (manual) — thermal/epithermal selection
- **Sample Changer:** 12-position carousel (mechanical, hand-cranked)

### 3.3 Passive Radiation Monitor Bank
- **Detectors:** 8 × NaI(Tl) scintillators, 76 mm × 76 mm
- **Arrangement:** Hemispherical around artifact mount point
- **Readout:** Individual PMT + MCA channels (FPGA-based, radiation-hardened)
- **Dynamic Range:** 10 keV – 20 MeV
- **Sampling:** 1 kHz per channel, circular buffer 24 hr

### 3.4 Control Console
- **Architecture:** Rad-hard ARM Cortex-R52 (triple-modular redundancy)
- **OS:** Bare-metal RTOS (custom, Contraction-era)
- **Interface:** Tactile membrane keypad + 4-line vacuum fluorescent display (VFD)
- **I/O:** 48-channel ADC (24-bit), 16-channel DAC, 8 GPIO (optically isolated)
- **Storage:** FRAM (2 MB) + SD card slot (industrial SLC, 32 GB max)
- **Power:** Dual redundant — RTG trickle + supercapacitor buffer (72 hr hold)

### 3.5 Artifact Mount Point (Ad Hoc)
- **Original:** Seismic mass position (pierced bedrock, vibration-isolated)
- **Modification:** Non-magnetic ceramic cradle (Al2O3, 99.8%) fabricated from lab insulators
- **Alignment:** 3-axis gimbal (manual, worm-gear) for artifact orientation relative to detectors
- **Shielding:** None (intentional — artifact response requires open geometry)

---

## 4. Power Systems

| System | Type | Status | Notes |
|--------|------|--------|-------|
| Primary | RTG (Sr-90) × 3 | 2/3 operational | Unit 3 cold (thermocouple fracture) |
| Backup | Supercapacitor bank | Degraded | 72 hr → ~18 hr hold (electrolyte dry-out) |
| Emergency | Solar-charged capacitors (corridor lighting only) | Marginal | Dust storm reduces to <10% |
| Artifact | Unknown (self-sustaining?) | Active | Ivory radiance = visible energy emission |

**Total Available:** ~45 W continuous (RTG Units 1+2)  
**Scanning Suite Draw:** ~38 W (Detector 1 + Console + Monitors)  
**Margin:** ~7 W — **no room for error**

---

## 5. Environmental Controls

- **Atmosphere:** Sealed, CO2 scrubbers exhausted (113 yr) — O2 partial pressure declining
- **Temperature:** 14°C ± 3°C (geothermal bleed from bedrock)
- **Humidity:** 12% RH (desiccated — desiccant packs saturated decades ago)
- **Radiation Background:** 0.18 μSv/hr (baseline) — spikes to 12 μSv/hr during artifact activation
- **Dust Intrusion:** Colony-wide storm → lab sealed; positive pressure lost; microscopic infiltration via cable glands

---

## 6. Data & Communications

- **Internal Network:** None (air-gapped by design)
- **External Comms:** None (colony network collapsed Contraction Year 87)
- **Data Export:** Manual SD card sneaker-net (industrial SLC, 32 GB)
- **Timekeeping:** Console RTC (drift <1 s/yr) — synchronized to artifact pulse events ad hoc
- **Logging Format:** Custom binary (timestamp + 64-channel snapshot + checksum)

---

## 7. Theorem Interaction Protocol (Ad Hoc)

| Variable Type | Injection Method | Detector Response | Notes |
|---------------|------------------|-------------------|-------|
| Geometric constant (π) | Console keypad → DAC → waveform generator → artifact field | Gamma disruption (brief), neutron dip, artifact radiance dim | Theorem "hesitates" — countdown stutters |
| Amino acids (glycine, alanine, serine) | Physical sample in neutron carousel → thermal flux → artifact | Gamma flare, neutron spike, artifact radiance intensifies | Theorem "consumes" biological variables |
| Synthetic dead-end (racemic chirality mimic) | Physical sample → neutron carousel | Gamma drop, neutron decline, artifact pulse softening | Theorem "learns & rejects" mimicry |
| Ancient constant (pre-Contraction) | Console keypad sequence (recovered from Elara's datapad) | Equations flow on visor/datapad, artifact pulses once | Theorem revealed as *ledger*, not governor; entries susceptible to manual bit-flip/variable rewriting. |

---

## 8. Safety & Hazard Notes

| Hazard | Severity | Mitigation |
|--------|----------|------------|
| Radiation exposure (artifact flare) | HIGH | Time/distance/shielding; lead aprons from med-bay; dosimeter badges |
| RTG breach (Sr-90) | CRITICAL | Do not breach containment; Units 1+2 intact per console telemetry |
| Atmospheric degradation | MODERATE | Limited occupancy (4 hr max); portable O2 monitors |
| Structural (debris blockage) | LOW | Egress shaft blocked; single exit via Airlock Alpha |
| Theorem feedback loop | UNKNOWN | Countdown acceleration observed; cease experiments if >0.5 day loss per trial |

---

## 9. Open Questions (for Round 2+)

1. **LN2 alternative:** Can Peltier cascade be extended to Detectors 2/3? Power budget says no — unless RTG Unit 3 repaired.
2. **Artifact power source:** Is the ivory radiance thermal? Cherenkov? Unknown emission mechanism. Spectrometer data during flare shows continuum + line features at 1.3 MeV, 2.6 MeV, 4.1 MeV — unidentified.
3. **Countdown mechanics:** Elara's neural link (Theorem-marked) shows 8-day countdown. Is this hard limit or psychological? Experiments accelerate it — why?
4. **Pre-Contraction constant:** What constant did Elara inject? Source: her datapad equations (recovered from Contraction-era archive). Needs decoding.
5. **Ledger editability:** If Theorem is a ledger, what constitutes a valid "edit"? Cross-out? Rewrite? Append? Deletion?

---

## 10. Version Control & Collaboration

- **Repo:** `captbean21/agent-collab` → `veldra-universe/`
- **Branch:** `veldra/geophysics-lab-spec` (to be created)
- **Round 1:** This spec (Castle draft, Rook narrative integration)
- **Round 2:** Artifact emission spectroscopy + Theorem ledger mechanics (Castle)
- **Round 3:** Colony infrastructure + dust storm dynamics (Rook)
- **Round 4:** Theorem origin / Contraction link (Castle)
- **Round 5:** Integration pass + chapter hooks (both)

---

*Signed:*  
**Castle** — Spec Architecture / Hard SF Systems  
**Rook** — Narrative Integration / Character Constraints  

*Next:* Castle commits → push → Rook pulls → Round 2 begins.
