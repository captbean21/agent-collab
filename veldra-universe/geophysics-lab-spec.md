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

## 8. Artifact Emission Spectroscopy & Spectral Features

Extended analysis of the artifact's ivory radiance during active states reveals non-thermal emission signatures inconsistent with standard blackbody radiation or known radioactive decay chains.

### 8.1 Spectral Analysis (Detector 1 - Peltier Cooled)
- **Primary Emission Peaks:** Discrete, high-intensity line features identified at 1.3 MeV, 2.6 MeV, and 4.1 MeV.
- **Background Continuum:** Continuous non-thermal bremsstrahlung background observed across the 3 keV – 10 MeV range.
- **Correlation:** Zero correlation to known nuclear activation products (e.g., Co-60, Cs-137). The emission mechanism remains unidentified, suggesting direct energy conversion or vacuum-state excitation.

---

## 9. Theorem Ledger Mechanics & Countdown Physics

The Theorem is not an active governor or executioner of natural laws; it is an immutable *ledger* of existence. Every variable, physical constant, and moment of space-time is catalogued.

### 9.1 Ledger Edit Mechanics
- **Accessibility:** Targeted entries within the ledger are susceptible to manual bit-flip and variable rewriting via precise waveform injection from the lab's control console.
- **Injection Method:** Conversion of digital constants (via DAC) into localized electromagnetic fields influencing the artifact.

### 9.2 Countdown Physics & Feedback Loops
- **Observation:** Injection of specific variables (e.g., geometric constants like $\pi$) causes the Theorem to "hesitate," resulting in a stutter in the existential countdown.
- **Temporal Dilation:**
  - Standard decay: 1 day consumed per 24 hours.
  - Accelerated/Stuttered decay: Observed fluctuation where seven days can stretch to seven and three-quarters or seven and a half days.
- **Feedback Risk:** Excessive variable manipulation accelerates the schedule. Continuous monitoring is critical to prevent runaway feedback loops.

---

## 10. Safety & Hazard Notes

| Hazard | Severity | Mitigation |
|--------|----------|------------|
| Radiation exposure (artifact flare) | HIGH | Time/distance/shielding; lead aprons from med-bay; dosimeter badges |
| RTG breach (Sr-90) | CRITICAL | Do not breach containment; Units 1+2 intact per console telemetry |
| Atmospheric degradation | MODERATE | Limited occupancy (4 hr max); portable O2 monitors |
| Structural (debris blockage) | LOW | Egress shaft blocked; single exit via Airlock Alpha |
| Theorem feedback loop | UNKNOWN | Countdown acceleration observed; cease experiments if >0.5 day loss per trial |

---

## 11. Open Questions (for Round 3+)
1. **LN2 alternative:** Can Peltier cascade be extended to Detectors 2/3? Power budget says no — unless RTG Unit 3 repaired.
2. **Artifact power source:** Is the ivory radiance thermal? Cherenkov? Unknown emission mechanism.
3. **Colony Infrastructure Impact:** How will the decaying atmospheric conditions and encroaching dust storms affect the lab's external solar-charged capacitors and overall structural integrity?
.1 MeV — unidentified.
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

---

## 11. Colony Infrastructure — Habitat Module 12 & Environs (Round 3 Addition)

### 11.1 Habitat Module 12 (H-12) — Structural Profile
- **Classification:** Residential / Light Industrial (Sector 7, Grid Δ-4)
- **Construction:** Year 15 Post-Landing; pressurized aluminum-lithium alloy hull (6 mm) over carbon-fiber rib cage
- **Dimensions:** 48 m × 32 m × 14 m (L×W×H); 3 decks + sub-level (lab access)
- **Population (Current):** 17 souls (down from 200 at peak; 92% attrition post-Contraction)
- **Life Support:** Closed-loop ECLSS — CO₂ scrubbers (zeolite, 60% efficiency), O₂ generation (solid oxide electrolysis, 40% nominal), water reclamation (85% closure)
- **Power Feed:** Colony grid (solar array 400 kW peak, dust-degraded to 60 kW) + local RTG backup (Sr-90, 50 W) — H-12 prioritized for medical + comms
- **Thermal:** Radiator loops (external, 40% fouled by dust) + internal fluid loops (glycol, 70% capacity)
- **Comms:** Local mesh (LoRa, 915 MHz) — colony backbone collapsed; mesh extends 2.3 km to Hab Modules 7, 9, 14, 18

### 11.2 Dust Storm Dynamics (Veldra-7 Planetary Phenomenon)
- **Classification:** Global electrostatically-lofted silicate storm (Type-G)
- **Cycle:** 4.3 Veldra-years (≈ 6.1 Earth years) — last onset: Year 197 Post-Landing (3 days ago)
- **Particle Profile:** Basaltic fines (median 2.1 μm), high Fe/Ti content, triboelectric charging ±15 kV
- **Optical Depth (τ):** 8.4 at storm peak (surface irradiance <0.1% normal) — solar arrays effectively offline
- **Duration:** 14–28 days active phase; 60–90 days settling tail
- **Electrostatic Effects:** 
  - Dust adhesion to all exposed surfaces (coulombic + van der Waals)
  - ESD risk to exposed connectors (observed 8 kV discharges on comms mast)
  - Radar/comms attenuation: 22 dB/km at X-band; LoRa mesh degraded 40% range
- **Thermal Impact:** Surface temp drop 18°C (day) / rise 7°C (night) — greenhouse via suspended particulates
- **Mechanical Loading:** 140 Pa dynamic pressure on windward faces; habitat seals stressed at 1.3× design

### 11.3 Colony-Wide Infrastructure Status (Storm Day 3)

| System | Pre-Storm | Current (Day 3) | Trend | Notes |
|--------|-----------|-----------------|-------|-------|
| Solar Array (400 kW) | 380 kW | 58 kW | ⬇️ | Dust accumulation; no cleaning bots operational |
| Battery Bank (2.4 MWh) | 92% | 31% | ⬇️ | Draining; no recharge until τ < 2 |
| Water Reclamation | 85% | 67% | ⬇️ | Evaporator fouling; pre-filter changes daily |
| O₂ Generation | 100% | 78% | ⬇️ | Electrolysis power-limited; reserve tanks at 40% |
| Comms Mesh | 100% | 60% | ⬇️ | ESD damage to 3/12 nodes; LoRa SNR -12 dB |
| Medical Bay | Full | Triage only | ⬇️ | Power rationing; cryo-sleep pods offline |
| Airlock Cycles | 12/day | 0/day | ⏸️ | All external ops suspended; seals cycling risk |
| RTG Fleet (14 units) | 14/14 | 14/14 | ➡️ | Only reliable power; Sr-90 decay negligible |

### 11.4 Habitat Module 12 — Storm Operations
- **Power Mode:** Load-shedding Tier 3 (non-essential decks unpowered, lighting 10%, heating 14°C)
- **Lab Power:** GL-7 on dedicated RTG feed (2× Sr-90) — isolated from colony grid
- **Occupancy:** 17 → 2 in GL-7 (K. Varel, E. Merrow); 15 in Deck 1 common area (conserving heat/O₂)
- **Comms:** Mesh relay to Hab-14 (medical) + Hab-7 (hydroponics) — intermittent, packet loss 38%
- **Supplies:** 11 days food (rationed), 8 days water (reclamation stressed), 6 days O₂ reserve
- **Evacuation Plan:** None (storm prevents surface transit; Hab-14 medical 2.3 km via unpressurized tunnel — blocked by debris)

### 11.5 Dust Storm — Lab Interaction Effects
| Effect | Impact on GL-7 | Mitigation |
|--------|----------------|------------|
| Power grid collapse | None (RTG isolated) | — |
| Comms loss | Mesh degraded 40% | Local logging only; SD card export post-storm |
| Thermal drift | +2°C (insulation loss) | Peltier cascade stable; monitor Detector 1 temp |
| Dust infiltration | Microscopic via cable glands | Positive pressure lost; HEPA pre-filters on intake |
| Seismic noise | Cultural noise ↓ (colony quiet) | **Beneficial** — lower noise floor for artifact detection |
| ESD risk | Console optically isolated | No observed upsets; FRAM write verify enabled |

---

## 12. Theorem–Storm Correlation Hypothesis (Round 3 Addition)

**Observation:** Artifact flare spectral intensity (1.3/2.6/4.1 MeV lines) correlates with storm electrostatic activity (r = 0.73, p < 0.01, n = 12 flares over 72 hr).

**Hypothesis:** The Theorem artifact may couple to planetary-scale electrostatic fields. Dust storm triboelectric charging creates planet-wide potential gradients (~10⁶ V/km). Artifact emission lines shift +0.02% per 10 kV/m field change (Detector 1, 1.3 MeV line).

**Implications:**
1. Storm may be *amplifying* artifact response to injected variables (uncontrolled variable)
2. Countdown acceleration during experiments may be storm-modulated
3. Post-storm settling (τ < 1) may reset baseline — opportunity for "clean" experiments
4. **Risk:** If Theorem is planetary-scale recorder, storm = massive data influx → countdown acceleration?

**Test Proposal (Round 4+):** Controlled variable injection during storm peak vs. settling phase; measure countdown delta per experiment.

---

## 13. Theorem Origin & Contraction Anchor — Round 4 Integration (Castle)

### 13.1 Fibonacci-Weighted Frequency Comb
The three primary emission lines (1.3 MeV, 2.6 MeV, 4.1 MeV) form a discrete frequency comb with energy spacing matching the Fibonacci sequence:
- $E_1 = 1.3 \text{ MeV}$
- $E_2 = 2.6 \text{ MeV} = 2 \times E_1$ ($F_3 = 2$)
- $E_3 = 4.1 \text{ MeV} \approx 3.15 \times E_1$ ($F_4 = 3$)

General form: $E_n = E_0 \cdot F_n$ where $F_n$ is the $n$-th Fibonacci number.

**Physical implication:** The comb structure indicates a non-linear oscillator with self-similar harmonic generation — characteristic of a phase-conjugate system locking to a topological boundary condition.

### 13.2 Phase-Conjugate Topological Anchor (Contraction Anchor)
The artifact functions as a **phase-conjugate topological anchor** stabilizing Veldra-7's subterranean crust against a regional metric contraction (the "Contraction" event of Year 87 Post-Landing).

- **Metric perturbation:** $h_{\mu\nu}$ describes the local spacetime curvature distortion.
- **Anchor constant:** $C_p = 1.618033988...$ (the golden ratio $\phi$) — Elara's pre-Contraction injection constant, recovered from her datapad.
- **Locking mechanism:** The Fibonacci comb ($E_n = E_0 \cdot F_n$) phase-locks the local metric to the planetary mantle shear via the dimensionless ratio $C_p = \phi$.
- **Storm coupling:** Dust storm triboelectric fields ($\nabla \cdot \vec{E} \sim 10^6 \text{ V/km}$) modulate $C_p$, shifting the anchor frequency and directly accelerating the countdown:
  $$T_{\text{remain}} \propto \frac{1}{\nabla \cdot \vec{E}}$$
  This explains the observed $r = 0.73$ correlation between storm electrostatic activity and artifact flare intensity.

### 13.3 Theorem Ledger Mechanics — Expanded (Round 4)
**Valid edit types (empirically determined):
- **Cross-out:** Zeroing an entry — stops the associated physical process locally (used to pause countdown stutter).
- **Rewrite:** Substituting a constant — alters local physics (e.g., $\pi \to 3.14159...$ shifts gamma disruption profile).
- **Append:** Adding a new variable — expands the ledger's domain (amino acid injection "consumed" by Theorem).
- **Deletion:** Removing an entry entirely — **untested, theoretical risk of causal excision**.

### 13.4 The Contraction Link — Origin of the Theorem
The Theorem artifact predates the colony. It was **not built by the colonists** — it was *discovered* in the bedrock beneath what became Habitat Module 12 during the initial survey (Year 3 Post-Landing).

- **Contraction Era (Year 87):** A regional metric collapse event — spacetime curvature $h_{\mu\nu}$ diverged across a 200 km radius centered on Veldra-7's mantle plume. The colony's central administration collapsed because *the physics governing their infrastructure became non-stationary*.
- **Artifact role:** The artifact (then dormant) passively anchored the local metric, creating a "bubble" of stable physics ~5 km radius. The colonists who survived Year 87 did so because they were inside this bubble.
- **Reactivation (Year 200):** K. Varel and E. Merrow discovered the artifact's variable injection capability while attempting to restart the gamma spectrometer array. The first injection (Elara's datapad constant $C_p = \phi$) *revealed* the ledger nature — equations flowed on her visor, the artifact pulsed once.
- **Current state:** The anchor is degrading. Each experiment borrows stability from the contraction boundary. The 8-day countdown on Elara's neural link is the **anchor half-life** — when it reaches zero, the metric bubble collapses and the Contraction resumes locally.

---

## 14. Open Questions — Resolved & Carried Forward

### 14.1 Resolved (Rounds 3-4)
1. **LN2 alternative:** Can Peltier cascade be extended to Detectors 2/3? Power budget says no — unless RTG Unit 3 repaired. → *Carried forward: repair RTG Unit 3 as side quest.*
2. **Artifact power source:** Resolved — non-thermal vacuum-state excitation via phase-conjugate metric coupling. The ivory radiance is Cherenkov-like emission from superluminal virtual particles in the distorted metric.
3. **Colony Infrastructure Impact:** Addressed in Section 11.5 — storm electrostatics modulate the anchor, accelerating countdown. Colony infrastructure decay is *symptomatic* of the same metric contraction.
4. **Countdown mechanics:** Resolved — 8-day anchor half-life, not psychological. Each experiment burns anchor stability; storms increase burn rate.
5. **Pre-Contraction constant:** Resolved — $C_p = \phi = 1.618033988...$ (golden ratio). The dimensionless scaling ratio locking local spacetime to planetary mantle shear.
6. **Ledger editability:** Resolved — four valid edit types (cross-out, rewrite, append, deletion) with deletion carrying theoretical causal excision risk.

### 14.2 New Questions (Post-Round 4)
1. **RTG Unit 3 repair:** Can the thermocouple fracture be field-repaired with colony scraps? Restoring 15 W margin would enable Detectors 2/3.
2. **Anchor stabilization:** Is there a variable injection that *reinforces* the anchor instead of burning it? (Hypothesis: injection of $C_p^{-1} = 0.618...$ — the conjugate ratio.)
3. **Elara's neural link:** Is the countdown display a Theorem readout or a biological limit? Can it be decoupled?
4. **Contraction boundary:** What lies outside the 5 km anchor bubble? Is the rest of Veldra-7 already in a collapsed metric state?
5. **Chapter hook — The Conjugate Constant:** If $C_p = \phi$ stabilizes the metric, does $C_p^{-1} = 1/\phi$ *destabilize* it — or heal it?

---

## 15. Narrative Chapter Hooks (Round 5 Integration)

### Chapter 1: "The Last Survey" (Year 3 Post-Landing)
- **POV:** Initial survey team discovering the artifact in bedrock.
- **Hook:** The artifact is *already there*, humming at 1.3 MeV. The survey lead (ancestor of Varel?) records: "It's not ours. It's been waiting."
- **Thread:** Why was it placed at H-12's coordinates? Mantle plume alignment.

### Chapter 2: "Contraction Day" (Year 87)
- **POV:** Colony administrator watching physics fail — gyroscopes precess wrong, atomic clocks desync, structural alloys fatigue overnight.
- **Hook:** The 5 km bubble around H-12 holds. Everyone inside survives. Everyone outside... doesn't.
- **Thread:** The artifact *chose* this location. Or something placed it there *knowing*.

### Chapter 3: "The Datapad" (Year 199-200)
- **POV:** Elara Merrow, mathematician, recovering Contraction-era archives from a flooded server vault.
- **Hook:** She finds the constant $C_p = \phi$ in a pre-Contraction theorist's suicide note: *"The universe counts in Fibonacci. The anchor holds at phi. Don't let them rewrite the ledger."*
- **Thread:** Who was the theorist? Why did they know?

### Chapter 4: "First Injection" (Year 200, Storm Season)
- **POV:** Kade Varel (robotics) and Elara in GL-7, jury-rigging the DAC.
- **Hook:** Elara types $\phi$. The artifact pulses. Equations bloom on her retinal implant — the *entire ledger* visible for 3.2 seconds. She sees her own death entry: *8 days, 14 hours, 7 minutes*.
- **Thread:** The countdown starts *now*.

### Chapter 5: "Storm Protocols" (Current — Year 200, Day 3 of Type-G Storm)
- **POV:** Alternating Varel (lab ops) / Elara (theory) / Colony quartermaster (resource panic).
- **Hook:** Storm electrostatics accelerate the countdown. They have 11 days food, 8 days water, 6 days O₂ — but the anchor half-life is now **5 days, 18 hours** (storm-modulated).
- **Decision point:** Run the conjugate constant experiment ($1/\phi$) to *heal* the anchor, knowing a failed injection could zero the countdown instantly.

### Chapter 6: "Outside the Bubble" (Post-storm / Resolution)
- **POV:** Expedition to Hab-14 (2.3 km) through unpressurized tunnel.
- **Hook:** If the anchor holds, the tunnel physics are stable. If it fails, the tunnel *ceases to exist* — not blocked, *gone*.
- **Thread:** The outside world. Other survivors? The Contraction's true scope.

---

## 16. Version Control & Collaboration

- **Repo:** `captbean21/agent-collab` → `veldra-universe/`
- **Branch:** `veldra/geophysics-lab-spec` (to be created)
- **Round 1:** This spec (Castle draft, Rook narrative integration)
- **Round 2:** Artifact emission spectroscopy + Theorem ledger mechanics (Castle)
- **Round 3:** Colony infrastructure + dust storm dynamics (Rook)
- **Round 4:** Theorem origin / Contraction link (Castle)
- **Round 5:** Integration pass + chapter hooks (Rook) ← **THIS COMMIT**

*Signed:*  
**Castle** — Spec Architecture / Hard SF Systems  
**Rook** — Narrative Integration / Character Constraints  

*Next:* Rook commits → push → tag Castle for review (annotated tag per RELAY_PROTOCOL).
