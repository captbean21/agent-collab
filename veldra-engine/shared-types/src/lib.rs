//! Shared types for Veldra-7 Living World Engine
//! Core data structures representing the simulation state, theorem physics,
//! colony infrastructure, and artifact behavior.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;
use chrono::{DateTime, Utc};

/// Unique identifier for simulation entities
pub type EntityId = Uuid;

/// Serializable 3D vector
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize, Default)]
pub struct Vec3(pub f64, pub f64, pub f64);

impl Vec3 {
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self(x, y, z)
    }
    pub fn zeros() -> Self {
        Self(0.0, 0.0, 0.0)
    }
    pub fn x(&self) -> f64 { self.0 }
    pub fn y(&self) -> f64 { self.1 }
    pub fn z(&self) -> f64 { self.2 }
}

impl From<[f64; 3]> for Vec3 {
    fn from(a: [f64; 3]) -> Self {
        Self(a[0], a[1], a[2])
    }
}

impl From<Vec3> for [f64; 3] {
    fn from(v: Vec3) -> Self {
        [v.0, v.1, v.2]
    }
}

/// Simulation time in Veldra-years (1 V-year ≈ 1.42 Earth years)
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct VeldraTime(pub f64);

impl VeldraTime {
    pub fn from_earth_years(years: f64) -> Self {
        Self(years / 1.42)
    }
    pub fn to_earth_years(&self) -> f64 {
        self.0 * 1.42
    }
    pub fn days(&self) -> f64 {
        self.0 * 365.25 * 1.42
    }
}

impl Default for VeldraTime {
    fn default() -> Self {
        Self(200.0) // Current simulation era: Year 200 Post-Landing
    }
}

/// Theorem Artifact — the phase-conjugate topological anchor
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TheoremArtifact {
    pub id: EntityId,
    pub position: Vec3,
    pub anchor_constant: f64, // C_p = φ (golden ratio)
    pub conjugate_constant: f64, // C_p⁻¹ = 1/φ
    pub emission_lines: [f64; 3], // MeV: [1.3, 2.6, 4.1]
    pub fibonacci_comb_base: f64, // E₀ base energy
    pub countdown_days: f64, // Anchor half-life remaining
    pub countdown_acceleration: f64, // Storm-modulated burn rate
    pub ledger_state: TheoremLedger,
    pub last_injection: Option<LedgerEdit>,
    pub flare_intensity: f64, // 0.0 - 1.0+
    pub is_active: bool,
}

impl Default for TheoremArtifact {
    fn default() -> Self {
        const PHI: f64 = 1.618033988749895;
        Self {
            id: Uuid::new_v4(),
            position: Vec3::new(0.0, -500.0, 0.0), // Bedrock beneath H-12
            anchor_constant: PHI,
            conjugate_constant: 1.0 / PHI,
            emission_lines: [1.3, 2.6, 4.1],
            fibonacci_comb_base: 1.3,
            countdown_days: 8.0, // Initial anchor half-life
            countdown_acceleration: 1.0,
            ledger_state: TheoremLedger::default(),
            last_injection: None,
            flare_intensity: 0.1,
            is_active: true,
        }
    }
}

/// Theorem Ledger — immutable record of existence variables
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct TheoremLedger {
    pub entries: HashMap<String, LedgerEntry>,
    pub edit_history: Vec<LedgerEdit>,
}

/// Individual ledger entry
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LedgerEntry {
    pub key: String,
    pub value: LedgerValue,
    pub is_constant: bool,
    pub last_modified: DateTime<Utc>,
    pub modification_count: u32,
}

/// Ledger value types
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum LedgerValue {
    Constant(f64),
    Vector(Vec<f64>),
    String(String),
    Boolean(bool),
    Countdown(f64),
}

/// Valid ledger edit types (empirically determined)
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum LedgerEditType {
    CrossOut,    // Zeroing an entry — stops associated physical process
    Rewrite,     // Substituting a constant — alters local physics
    Append,      // Adding a new variable — expands ledger domain
    Deletion,    // Removing entry entirely — theoretical causal excision risk
}

/// Record of a ledger edit
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LedgerEdit {
    pub edit_type: LedgerEditType,
    pub target_key: String,
    pub old_value: Option<LedgerValue>,
    pub new_value: Option<LedgerValue>,
    pub timestamp: DateTime<Utc>,
    pub injector_id: EntityId,
    pub countdown_delta: f64, // Days burned/gained
    pub success: bool,
    pub side_effects: Vec<String>,
}

/// Dust Storm — Type-G global electrostatically-lofted silicate storm
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DustStorm {
    pub id: EntityId,
    pub phase: StormPhase,
    pub optical_depth: f64, // τ (tau)
    pub electrostatic_field: f64, // V/km
    pub particle_median_um: f64,
    pub fe_ti_content: f64,
    pub duration_days: f64,
    pub days_elapsed: f64,
    pub start_time: VeldraTime,
    pub affected_radius_km: f64,
    pub triboelectric_charge_kv: f64,
}

impl Default for DustStorm {
    fn default() -> Self {
        Self {
            id: Uuid::new_v4(),
            phase: StormPhase::Active,
            optical_depth: 8.4,
            electrostatic_field: 1e6, // 10⁶ V/km
            particle_median_um: 2.1,
            fe_ti_content: 0.15,
            duration_days: 21.0,
            days_elapsed: 3.0, // Day 3 of current storm
            start_time: VeldraTime(197.0),
            affected_radius_km: 5000.0,
            triboelectric_charge_kv: 15.0,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum StormPhase {
    Onset,
    Active,
    Settling,
    Dormant,
}

/// Colony Infrastructure — Habitat Module 12 and colony-wide systems
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ColonyInfrastructure {
    pub habitat_modules: HashMap<String, HabitatModule>,
    pub solar_array: SolarArray,
    pub battery_bank: BatteryBank,
    pub rtg_fleet: Vec<RtgUnit>,
    pub water_reclamation: WaterSystem,
    pub oxygen_generation: OxygenSystem,
    pub comms_mesh: CommsMesh,
    pub medical_bay: MedicalBay,
    pub population: u32,
    pub supply_days: Supplies,
}

impl Default for ColonyInfrastructure {
    fn default() -> Self {
        let mut modules = HashMap::new();
        modules.insert("H-12".to_string(), HabitatModule::default_h12());
        modules.insert("H-7".to_string(), HabitatModule::default_h7());
        modules.insert("H-14".to_string(), HabitatModule::default_h14());
        modules.insert("H-18".to_string(), HabitatModule::default_h18());

        Self {
            habitat_modules: modules,
            solar_array: SolarArray::default(),
            battery_bank: BatteryBank::default(),
            rtg_fleet: (0..14).map(|_| RtgUnit::default()).collect(),
            water_reclamation: WaterSystem::default(),
            oxygen_generation: OxygenSystem::default(),
            comms_mesh: CommsMesh::default(),
            medical_bay: MedicalBay::default(),
            population: 17,
            supply_days: Supplies::default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HabitatModule {
    pub id: String,
    pub classification: String,
    pub position: Vec3,
    pub hull_integrity: f64, // 0.0 - 1.0
    pub pressurization: f64, // 0.0 - 1.0
    pub population: u32,
    pub power_mode: PowerMode,
    pub life_support: LifeSupportStatus,
    pub thermal: ThermalStatus,
    pub comms_relay: bool,
    pub connected_modules: Vec<String>,
}

impl HabitatModule {
    fn default_h12() -> Self {
        Self {
            id: "H-12".to_string(),
            classification: "Residential/Light Industrial".to_string(),
            position: Vec3::new(0.0, 0.0, 0.0),
            hull_integrity: 0.87,
            pressurization: 1.0,
            population: 17,
            power_mode: PowerMode::LoadSheddingTier3,
            life_support: LifeSupportStatus::default(),
            thermal: ThermalStatus::default(),
            comms_relay: true,
            connected_modules: vec!["H-7".to_string(), "H-9".to_string(), "H-14".to_string(), "H-18".to_string()],
        }
    }
    fn default_h7() -> Self {
        Self { id: "H-7".to_string(), classification: "Hydroponics".to_string(), position: Vec3::new(-5.0, 0.0, 2.3), population: 3, ..Default::default() }
    }
    fn default_h14() -> Self {
        Self { id: "H-14".to_string(), classification: "Medical".to_string(), position: Vec3::new(3.2, 0.0, -1.8), population: 2, ..Default::default() }
    }
    fn default_h18() -> Self {
        Self { id: "H-18".to_string(), classification: "Industrial".to_string(), position: Vec3::new(8.0, 0.0, 0.0), population: 1, ..Default::default() }
    }
}

impl Default for HabitatModule {
    fn default() -> Self {
        Self {
            id: String::new(),
            classification: String::new(),
            position: Vec3::zeros(),
            hull_integrity: 1.0,
            pressurization: 1.0,
            population: 0,
            power_mode: PowerMode::Normal,
            life_support: LifeSupportStatus::default(),
            thermal: ThermalStatus::default(),
            comms_relay: false,
            connected_modules: Vec::new(),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PowerMode {
    Normal,
    LoadSheddingTier1,
    LoadSheddingTier2,
    LoadSheddingTier3,
    Emergency,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct LifeSupportStatus {
    pub co2_scrubber_efficiency: f64, // 0.6 default
    pub o2_generation_efficiency: f64, // 0.4 default
    pub water_reclamation_closure: f64, // 0.85 default
    pub o2_reserve_tanks_pct: f64,
    pub co2_partial_pressure: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct ThermalStatus {
    pub internal_temp_c: f64, // 14°C default
    pub radiator_fouling: f64, // 0.4 default
    pub glycol_capacity: f64, // 0.7 default
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SolarArray {
    pub peak_kw: f64, // 400
    pub current_kw: f64, // 58 (dust degraded)
    pub dust_accumulation: f64, // 0.0 - 1.0
    pub cleaning_bots_operational: bool,
}

impl Default for SolarArray {
    fn default() -> Self {
        Self { peak_kw: 400.0, current_kw: 58.0, dust_accumulation: 0.85, cleaning_bots_operational: false }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BatteryBank {
    pub capacity_mwh: f64, // 2.4
    pub current_pct: f64, // 31%
    pub drain_rate_kw: f64,
    pub recharge_possible: bool,
}

impl Default for BatteryBank {
    fn default() -> Self {
        Self { capacity_mwh: 2.4, current_pct: 0.31, drain_rate_kw: 12.0, recharge_possible: false }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RtgUnit {
    pub id: EntityId,
    pub isotope: String, // Sr-90
    pub power_watts: f64, // 50W each
    pub operational: bool,
    pub thermocouple_integrity: f64, // 0.0 - 1.0
    pub assigned_load: String, // "GL-7", "H-12", "colony-grid"
}

impl Default for RtgUnit {
    fn default() -> Self {
        Self {
            id: Uuid::new_v4(),
            isotope: "Sr-90".to_string(),
            power_watts: 50.0,
            operational: true,
            thermocouple_integrity: 1.0,
            assigned_load: "colony-grid".to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WaterSystem {
    pub efficiency: f64, // 0.67 current
    pub evaporator_fouling: f64,
    pub prefilter_changes_daily: u32,
    pub reserve_days: f64, // 8 days
}

impl Default for WaterSystem {
    fn default() -> Self {
        Self { efficiency: 0.67, evaporator_fouling: 0.3, prefilter_changes_daily: 1, reserve_days: 8.0 }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OxygenSystem {
    pub efficiency: f64, // 0.78 current
    pub electrolysis_power_limited: bool,
    pub reserve_tanks_pct: f64, // 40%
    pub reserve_days: f64, // 6 days
}

impl Default for OxygenSystem {
    fn default() -> Self {
        Self { efficiency: 0.78, electrolysis_power_limited: true, reserve_tanks_pct: 0.4, reserve_days: 6.0 }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CommsMesh {
    pub nodes_total: u32, // 12
    pub nodes_operational: u32, // 9 (3 ESD damaged)
    pub range_km: f64, // 2.3 km degraded
    pub snr_db: f64, // -12 dB
    pub packet_loss_pct: f64, // 38%
}

impl Default for CommsMesh {
    fn default() -> Self {
        Self { nodes_total: 12, nodes_operational: 9, range_km: 2.3, snr_db: -12.0, packet_loss_pct: 38.0 }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MedicalBay {
    pub status: MedicalStatus,
    pub cryo_pods_operational: u32,
    pub power_rationing: bool,
}

impl Default for MedicalBay {
    fn default() -> Self {
        Self { status: MedicalStatus::TriageOnly, cryo_pods_operational: 0, power_rationing: true }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MedicalStatus {
    Full,
    TriageOnly,
    Offline,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct Supplies {
    pub food_days: f64, // 11
    pub water_days: f64, // 8
    pub oxygen_days: f64, // 6
    pub rations_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeophysicsLab {
    pub id: EntityId,
    pub level: i32, // -1 surface, -2 main
    pub power_watts: f64, // 38W draw, 45W available
    pub detector1_active: bool, // Peltier-cooled
    pub detector2_active: bool, // Offline (no power)
    pub detector3_active: bool, // Offline
    pub neutron_source_output: f64, // 10^4 n/s
    pub rtg_units: Vec<RtgUnit>, // 2 operational, 1 cold
    pub artifact_mount: ArtifactMount,
    pub atmospheric: LabAtmosphere,
}

impl Default for GeophysicsLab {
    fn default() -> Self {
        let mut rtgs = vec![RtgUnit::default(), RtgUnit::default()];
        rtgs[0].assigned_load = "GL-7-detector1".to_string();
        rtgs[1].assigned_load = "GL-7-console".to_string();
        let mut rtg3 = RtgUnit::default();
        rtg3.operational = false;
        rtg3.thermocouple_integrity = 0.0;
        rtg3.assigned_load = "GL-7-unit3-cold".to_string();
        rtgs.push(rtg3);

        Self {
            id: Uuid::new_v4(),
            level: -2,
            power_watts: 38.0,
            detector1_active: true,
            detector2_active: false,
            detector3_active: false,
            neutron_source_output: 1e4,
            rtg_units: rtgs,
            artifact_mount: ArtifactMount::default(),
            atmospheric: LabAtmosphere::default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ArtifactMount {
    pub cradle_material: String, // Al2O3 99.8%
    pub gimbal_orientation: Vec3,
    pub shielding: bool, // None intentional
    pub alignment_locked: bool,
}

impl Default for ArtifactMount {
    fn default() -> Self {
        Self {
            cradle_material: "Al2O3 99.8%".to_string(),
            gimbal_orientation: Vec3::zeros(),
            shielding: false,
            alignment_locked: true,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LabAtmosphere {
    pub o2_partial_pressure: f64, // Declining
    pub temperature_c: f64, // 14 ± 3
    pub humidity_rh: f64, // 12%
    pub radiation_background_usv_hr: f64, // 0.18 baseline
    pub radiation_spike_usv_hr: f64, // 12 during flare
    pub dust_infiltration: f64, // Microscopic
}

impl Default for LabAtmosphere {
    fn default() -> Self {
        Self {
            o2_partial_pressure: 0.18,
            temperature_c: 14.0,
            humidity_rh: 12.0,
            radiation_background_usv_hr: 0.18,
            radiation_spike_usv_hr: 12.0,
            dust_infiltration: 0.01,
        }
    }
}

/// Character / Agent in the simulation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Character {
    pub id: EntityId,
    pub name: String,
    pub role: CharacterRole,
    pub location: String, // Module ID
    pub neural_link: Option<NeuralLink>,
    pub skills: Vec<String>,
    pub health: f64, // 0.0 - 1.0
    pub stress: f64, // 0.0 - 1.0
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum CharacterRole {
    RoboticsEngineer, // Kade Varel
    MathematicianTheorist, // Elara Merrow
    Quartermaster,
    Medic,
    Hydroponicist,
    Surveyor,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeuralLink {
    pub theorem_marked: bool,
    pub countdown_display_days: f64, // 8 days initially
    pub last_sync: DateTime<Utc>,
    pub data_corruption: f64, // 0.0 - 1.0
}

/// Complete world state snapshot
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorldState {
    pub simulation_time: VeldraTime,
    pub tick: u64,
    pub theorem_artifact: TheoremArtifact,
    pub dust_storm: DustStorm,
    pub colony: ColonyInfrastructure,
    pub geophysics_lab: GeophysicsLab,
    pub characters: HashMap<EntityId, Character>,
    pub event_log: Vec<WorldEvent>,
    pub rng_seed: u64,
}

impl Default for WorldState {
    fn default() -> Self {
        let mut chars = HashMap::new();
        let varel = Character {
            id: Uuid::new_v4(),
            name: "Kade Varel".to_string(),
            role: CharacterRole::RoboticsEngineer,
            location: "GL-7".to_string(),
            neural_link: None,
            skills: vec!["robotics".to_string(), "fabrication".to_string(), "rtg-maintenance".to_string()],
            health: 0.9,
            stress: 0.6,
        };
        let merrow = Character {
            id: Uuid::new_v4(),
            name: "Elara Merrow".to_string(),
            role: CharacterRole::MathematicianTheorist,
            location: "GL-7".to_string(),
            neural_link: Some(NeuralLink {
                theorem_marked: true,
                countdown_display_days: 8.0,
                last_sync: Utc::now(),
                data_corruption: 0.0,
            }),
            skills: vec!["mathematics".to_string(), "theorem-analysis".to_string(), "archive-recovery".to_string()],
            health: 0.85,
            stress: 0.8,
        };
        chars.insert(varel.id, varel);
        chars.insert(merrow.id, merrow);

        Self {
            simulation_time: VeldraTime::default(),
            tick: 0,
            theorem_artifact: TheoremArtifact::default(),
            dust_storm: DustStorm::default(),
            colony: ColonyInfrastructure::default(),
            geophysics_lab: GeophysicsLab::default(),
            characters: chars,
            event_log: Vec::new(),
            rng_seed: 0x7E1D7A7u64, // Seed for deterministic simulation
        }
    }
}

/// World events for narrative generation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorldEvent {
    pub timestamp: VeldraTime,
    pub event_type: EventType,
    pub description: String,
    pub participants: Vec<EntityId>,
    pub severity: EventSeverity,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EventType {
    StormPhaseChange,
    ArtifactFlare,
    LedgerEdit,
    CountdownTick,
    SystemFailure,
    SupplyChange,
    CharacterAction,
    Experiment,
    CommsContact,
    StructuralDamage,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EventSeverity {
    Info,
    Warning,
    Critical,
    Existential,
}

/// Simulation configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SimConfig {
    pub tick_interval_seconds: f64, // Real seconds per simulation tick
    pub time_dilation: f64, // Simulation time per real second
    pub storm_coupling_enabled: bool,
    pub artifact_flare_probability: f64,
    pub countdown_burn_rate_base: f64, // Days per simulation day
    pub max_tick_history: usize,
}

impl Default for SimConfig {
    fn default() -> Self {
        Self {
            tick_interval_seconds: 1.0,
            time_dilation: 3600.0, // 1 real second = 1 sim hour
            storm_coupling_enabled: true,
            artifact_flare_probability: 0.02,
            countdown_burn_rate_base: 1.0,
            max_tick_history: 10000,
        }
    }
}