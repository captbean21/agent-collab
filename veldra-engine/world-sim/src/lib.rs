//! Veldra-7 World Simulation Engine
//! Core simulation loop, physics, and state management.

use veldra_shared_types::*;
use rand::Rng;
use rand::rngs::StdRng;
use rand::SeedableRng;
use std::sync::Arc;
use tokio::sync::RwLock;
use chrono::Utc;

pub mod persistence;
use persistence::{PersistenceManager, PersistenceError};

pub struct WorldSim {
    pub state: Arc<RwLock<WorldState>>,
    pub config: SimConfig,
    rng: StdRng,
}

impl WorldSim {
    pub fn new(config: SimConfig) -> Self {
        let mut state = WorldState::default();
        state.rng_seed = (config.countdown_burn_rate_base as u64) * 0x7E1D7A7u64;
        let rng = StdRng::seed_from_u64(state.rng_seed);
        
        Self {
            state: Arc::new(RwLock::new(state)),
            config,
            rng,
        }
    }

    pub fn new_with_seed(seed: u64) -> Self {
        let config = SimConfig::default();
        let mut state = WorldState::default();
        state.rng_seed = seed;
        let rng = StdRng::seed_from_u64(seed);
        
        Self {
            state: Arc::new(RwLock::new(state)),
            config,
            rng,
        }
    }

    /// Main simulation tick — advances world state by one step
    pub async fn tick(&mut self) -> Result<WorldState, SimError> {
        let dt_years = self.config.time_dilation / (365.25 * 24.0 * 3600.0); // Years per tick
        
        {
            let mut state = self.state.write().await;
            state.simulation_time.0 += dt_years;
            state.tick += 1;

            // 1. Dust storm progression
            Self::update_storm_static(&mut state, dt_years, &self.config).await;

            // 2. Theorem artifact physics
            Self::update_artifact_static(&mut state, &self.config, &mut self.rng).await;

            // 3. Colony infrastructure decay/recovery
            Self::update_colony_static(&mut state, &self.config).await;

            // 4. Geophysics lab systems
            Self::update_lab_static(&mut state, &self.config).await;

            // 5. Character state updates
            Self::update_characters_static(&mut state, &self.config).await;

            // 6. Random events
            Self::maybe_trigger_event_static(&mut state, &self.config, &mut self.rng).await;

            // Trim event log
            if state.event_log.len() > self.config.max_tick_history {
                let drain = state.event_log.len() - self.config.max_tick_history;
                state.event_log.drain(0..drain);
            }
        }

        Ok(self.state.read().await.clone())
    }

    /// Update dust storm state
    async fn update_storm_static(state: &mut WorldState, _dt_years: f64, config: &SimConfig) {
        let storm = &mut state.dust_storm;
        let days_per_tick = config.time_dilation / (24.0 * 3600.0);
        storm.days_elapsed += days_per_tick;

        // Phase transitions
        storm.phase = match storm.days_elapsed {
            d if d < 1.0 => StormPhase::Onset,
            d if d < storm.duration_days * 0.6 => StormPhase::Active,
            d if d < storm.duration_days => StormPhase::Settling,
            _ => StormPhase::Dormant,
        };

        // Optical depth evolution (peak at day 3-5, then decay)
        let peak_day = storm.duration_days * 0.25;
        if storm.days_elapsed <= peak_day {
            storm.optical_depth = 8.4 * (storm.days_elapsed / peak_day).min(1.0);
        } else {
            let decay_progress = (storm.days_elapsed - peak_day) / (storm.duration_days - peak_day);
            storm.optical_depth = 8.4 * (1.0 - decay_progress * 0.9).max(0.1);
        }

        // Electrostatic field modulates with optical depth
        storm.electrostatic_field = 1e6 * (storm.optical_depth / 8.4).powf(0.8);

        // Solar array degradation from storm
        state.colony.solar_array.current_kw = state.colony.solar_array.peak_kw * (1.0 - storm.optical_depth / 10.0).max(0.05);
        state.colony.solar_array.dust_accumulation = (storm.optical_depth / 8.4).min(1.0);

        // Battery drain when solar insufficient
        let colony_load_kw = 45.0; // Base colony load
        let deficit = colony_load_kw - state.colony.solar_array.current_kw;
        if deficit > 0.0 {
            let drain_mwh = deficit * (config.time_dilation / 3600.0) / 1000.0; // MWh per tick
            state.colony.battery_bank.current_pct = (state.colony.battery_bank.current_pct - drain_mwh / state.colony.battery_bank.capacity_mwh).max(0.0);
            state.colony.battery_bank.drain_rate_kw = deficit;
            state.colony.battery_bank.recharge_possible = false;
        } else {
            state.colony.battery_bank.recharge_possible = true;
        }

        // Comms degradation
        let comms_degradation = storm.optical_depth / 8.4;
        state.colony.comms_mesh.range_km = 2.3 * (1.0 - comms_degradation * 0.6);
        state.colony.comms_mesh.snr_db = -12.0 * comms_degradation;
        state.colony.comms_mesh.packet_loss_pct = 38.0 * comms_degradation;

        // Log phase changes (approximately once per sim day)
        if storm.days_elapsed.fract() < days_per_tick {
            state.event_log.push(WorldEvent {
                timestamp: state.simulation_time,
                event_type: EventType::StormPhaseChange,
                description: format!("Dust storm phase: {:?}, τ={:.2}", storm.phase, storm.optical_depth),
                participants: vec![],
                severity: EventSeverity::Info,
                data: serde_json::json!({ "phase": format!("{:?}", storm.phase), "optical_depth": storm.optical_depth }),
            });
        }
    }

    /// Update theorem artifact physics
    async fn update_artifact_static(state: &mut WorldState, config: &SimConfig, rng: &mut StdRng) {
        let artifact = &mut state.theorem_artifact;
        let storm = &state.dust_storm;

        // Storm coupling: electrostatic field modulates anchor constant
        if config.storm_coupling_enabled {
            let field_modulation = storm.electrostatic_field / 1e6; // Normalized to 1.0 at 10⁶ V/km
            artifact.countdown_acceleration = 1.0 + field_modulation * 0.5; // Up to 1.5x burn rate
            
            // Emission line shifts
            let shift = field_modulation * 0.0002; // 0.02% per 10 kV/m as per spec
            for i in 0..3 {
                artifact.emission_lines[i] = artifact.emission_lines[i] * (1.0 + shift);
            }
        } else {
            artifact.countdown_acceleration = 1.0;
        }

        // Countdown burn
        let sim_days_per_tick = config.time_dilation / (24.0 * 3600.0);
        let burn = sim_days_per_tick * artifact.countdown_acceleration * config.countdown_burn_rate_base;
        artifact.countdown_days = (artifact.countdown_days - burn).max(0.0);

        // Update neural link countdown for Elara
        for character in state.characters.values_mut() {
            if let Some(link) = &mut character.neural_link {
                link.countdown_display_days = artifact.countdown_days;
                link.last_sync = Utc::now();
            }
        }

        // Artifact flare probability (increases with storm intensity)
        let flare_prob = config.artifact_flare_probability * (1.0 + storm.optical_depth / 8.4);
        if rng.gen::<f64>() < flare_prob {
            artifact.flare_intensity = 0.5 + rng.gen::<f64>() * 0.5;
            
            state.event_log.push(WorldEvent {
                timestamp: state.simulation_time,
                event_type: EventType::ArtifactFlare,
                description: format!("Artifact flare: intensity {:.2}, lines at {:.2}/{:.2}/{:.2} MeV", 
                    artifact.flare_intensity, artifact.emission_lines[0], artifact.emission_lines[1], artifact.emission_lines[2]),
                participants: vec![],
                severity: EventSeverity::Warning,
                data: serde_json::json!({ 
                    "intensity": artifact.flare_intensity,
                    "emission_lines": artifact.emission_lines,
                    "storm_field": storm.electrostatic_field
                }),
            });
        } else {
            artifact.flare_intensity *= 0.95; // Decay
        }

        // Lab radiation spike during flare
        state.geophysics_lab.atmospheric.radiation_background_usv_hr = 0.18 + artifact.flare_intensity * 11.82;

        // Countdown critical warning
        if artifact.countdown_days < 1.0 && artifact.countdown_days > 0.0 {
            state.event_log.push(WorldEvent {
                timestamp: state.simulation_time,
                event_type: EventType::CountdownTick,
                description: format!("ANCHOR CRITICAL: {:.2} days remaining", artifact.countdown_days),
                participants: vec![],
                severity: EventSeverity::Existential,
                data: serde_json::json!({ "countdown_days": artifact.countdown_days }),
            });
        }
    }

    /// Update colony infrastructure
    async fn update_colony_static(state: &mut WorldState, config: &SimConfig) {
        let colony = &mut state.colony;
        let storm = &state.dust_storm;

        // Life support degradation under power stress
        let power_ratio = if colony.solar_array.current_kw > 0.0 {
            (colony.solar_array.current_kw + (colony.battery_bank.current_pct * colony.battery_bank.capacity_mwh * 1000.0)) / 45.0
        } else {
            0.0
        }.min(1.0);

        colony.water_reclamation.efficiency = 0.85 * power_ratio;
        colony.oxygen_generation.efficiency = 0.78 * power_ratio;
        
        // Supply consumption
        let days_per_tick = config.time_dilation / (24.0 * 3600.0);
        colony.supply_days.food_days = (colony.supply_days.food_days - days_per_tick * (colony.population as f64 / 17.0)).max(0.0);
        colony.supply_days.water_days = colony.water_reclamation.reserve_days;
        colony.supply_days.oxygen_days = colony.oxygen_generation.reserve_days;

        // Population stress
        if colony.supply_days.food_days < 5.0 || colony.supply_days.water_days < 3.0 || colony.supply_days.oxygen_days < 2.0 {
            for character in state.characters.values_mut() {
                character.stress = (character.stress + 0.01).min(1.0);
            }
        }

        // RTG fleet status
        for rtg in &mut colony.rtg_fleet {
            rtg.power_watts = 50.0 * rtg.thermocouple_integrity;
        }

        // Log critical supply events
        if colony.supply_days.food_days < 1.0 && colony.supply_days.food_days > 0.0 {
            state.event_log.push(WorldEvent {
                timestamp: state.simulation_time,
                event_type: EventType::SupplyChange,
                description: "FOOD CRITICAL: <1 day remaining".to_string(),
                participants: vec![],
                severity: EventSeverity::Critical,
                data: serde_json::json!({ "supply": "food", "days": colony.supply_days.food_days }),
            });
        }
    }

    /// Update geophysics lab
    async fn update_lab_static(state: &mut WorldState, _config: &SimConfig) {
        let lab = &mut state.geophysics_lab;

        // Power budget check
        let available_power: f64 = lab.rtg_units.iter()
            .filter(|r| r.operational)
            .map(|r| r.power_watts)
            .sum();
        
        let required_power: f64 = if lab.detector1_active { 15.0 } else { 0.0 }
            + if lab.detector2_active { 15.0 } else { 0.0 }
            + if lab.detector3_active { 15.0 } else { 0.0 }
            + 8.0; // Console + monitors

        lab.power_watts = required_power.min(available_power);

        // Detector 2/3 can only activate if Unit 3 repaired
        if lab.rtg_units.len() > 2 && !lab.rtg_units[2].operational {
            lab.detector2_active = false;
            lab.detector3_active = false;
        }

        // Neutron source decay (Am-241 half-life 432 years)
        let years_elapsed = state.simulation_time.0 - 12.0; // Lab built Year 12
        lab.neutron_source_output = 1e6 * 0.5_f64.powf(years_elapsed / 432.0);

        // Artifact mount alignment drift (thermal) - Vec3 uses fields .0 .1 .2
        let thermal_drift = (lab.atmospheric.temperature_c - 14.0) * 0.001;
        let x = lab.artifact_mount.gimbal_orientation.0 + thermal_drift * 0.01;
        let y = lab.artifact_mount.gimbal_orientation.1 + thermal_drift * 0.01;
        let z = lab.artifact_mount.gimbal_orientation.2;
        lab.artifact_mount.gimbal_orientation = Vec3::new(x, y, z);
    }

    /// Update character states
    async fn update_characters_static(state: &mut WorldState, _config: &SimConfig) {
        let artifact = &state.theorem_artifact;
        for character in state.characters.values_mut() {
            // Stress recovery when in safe conditions
            if character.location == "GL-7" && artifact.countdown_days > 3.0 {
                character.stress = (character.stress - 0.001).max(0.0);
            }

            // Health degradation under high stress
            if character.stress > 0.8 {
                character.health = (character.health - 0.0001).max(0.1);
            }

            // Neural link corruption from artifact proximity
            if let Some(link) = &mut character.neural_link {
                if character.location == "GL-7" {
                    link.data_corruption = (link.data_corruption + artifact.flare_intensity * 0.001).min(1.0);
                }
            }
        }
    }

    /// Random event generation
    async fn maybe_trigger_event_static(state: &mut WorldState, _config: &SimConfig, rng: &mut StdRng) {
        // System failure chance increases with storm
        let failure_chance = 0.001 * (1.0 + state.dust_storm.optical_depth / 8.4);
        if rng.gen::<f64>() < failure_chance {
            let systems = ["water_reclamation", "oxygen_generation", "comms_mesh", "solar_array", "battery_bank"];
            let system = systems[rng.gen_range(0..systems.len())];
            
            state.event_log.push(WorldEvent {
                timestamp: state.simulation_time,
                event_type: EventType::SystemFailure,
                description: format!("System degradation: {}", system),
                participants: vec![],
                severity: EventSeverity::Warning,
                data: serde_json::json!({ "system": system }),
            });
        }
    }

    /// Perform a ledger edit on the theorem artifact
    pub async fn perform_ledger_edit(
        &mut self,
        edit_type: LedgerEditType,
        target_key: String,
        new_value: Option<LedgerValue>,
        injector_id: EntityId,
    ) -> Result<LedgerEdit, SimError> {
        let mut state = self.state.write().await;
        
        // Calculate countdown delta first (needs immutable borrow)
        let storm_factor = state.dust_storm.electrostatic_field / 1e6;
        let base_cost = match edit_type {
            LedgerEditType::CrossOut => 0.1,
            LedgerEditType::Rewrite => 0.25,
            LedgerEditType::Append => 0.15,
            LedgerEditType::Deletion => 0.5, // Highest risk
        };
        let countdown_delta = base_cost * (1.0 + storm_factor * 0.5) * state.theorem_artifact.countdown_acceleration;
        
        // Get old value before mutable borrow
        let old_value = state.theorem_artifact.ledger_state.entries.get(&target_key).map(|e| e.value.clone());
        
        // Clone new_value for the edit record since we'll move it
        let new_value_for_record = new_value.clone();
        
        // Apply edit with mutable borrow
        let artifact = &mut state.theorem_artifact;
        let success = true;
        let side_effects = vec![];
        
        match edit_type {
            LedgerEditType::CrossOut => {
                if let Some(entry) = artifact.ledger_state.entries.get_mut(&target_key) {
                    entry.value = LedgerValue::Constant(0.0);
                    entry.last_modified = Utc::now();
                    entry.modification_count += 1;
                }
            }
            LedgerEditType::Rewrite => {
                if let Some(new_val) = new_value {
                    if let Some(entry) = artifact.ledger_state.entries.get_mut(&target_key) {
                        entry.value = new_val;
                        entry.last_modified = Utc::now();
                        entry.modification_count += 1;
                    } else {
                        artifact.ledger_state.entries.insert(target_key.clone(), LedgerEntry {
                            key: target_key.clone(),
                            value: new_val,
                            is_constant: false,
                            last_modified: Utc::now(),
                            modification_count: 1,
                        });
                    }
                }
            }
            LedgerEditType::Append => {
                if let Some(new_val) = new_value {
                    let new_key = format!("{}_{}", target_key, artifact.ledger_state.entries.len() + 1);
                    artifact.ledger_state.entries.insert(new_key, LedgerEntry {
                        key: target_key.clone(),
                        value: new_val,
                        is_constant: false,
                        last_modified: Utc::now(),
                        modification_count: 1,
                    });
                }
            }
            LedgerEditType::Deletion => {
                artifact.ledger_state.entries.remove(&target_key);
            }
        }

        artifact.countdown_days = (artifact.countdown_days - countdown_delta).max(0.0);
        
        let edit = LedgerEdit {
            edit_type,
            target_key: target_key.clone(),
            old_value,
            new_value: new_value_for_record,
            timestamp: Utc::now(),
            injector_id,
            countdown_delta,
            success,
            side_effects,
        };

        artifact.ledger_state.edit_history.push(edit.clone());
        artifact.last_injection = Some(edit.clone());

        // Get simulation_time before pushing event
        let sim_time = state.simulation_time;
        state.event_log.push(WorldEvent {
            timestamp: sim_time,
            event_type: EventType::LedgerEdit,
            description: format!("Ledger edit: {:?} on '{}', countdown -{:.3} days", edit.edit_type, target_key, countdown_delta),
            participants: vec![injector_id],
            severity: EventSeverity::Warning,
            data: serde_json::to_value(&edit).unwrap_or_default(),
        });

        Ok(edit)
    }

    /// Inject conjugate constant (1/φ) - hypothesized anchor healing
    pub async fn inject_conjugate_constant(&mut self, injector_id: EntityId) -> Result<LedgerEdit, SimError> {
        self.perform_ledger_edit(
            LedgerEditType::Rewrite,
            "anchor_constant".to_string(),
            Some(LedgerValue::Constant(1.0 / 1.618033988749895)), // 1/φ
            injector_id,
        ).await
    }

    /// Get current world state (read-only)
    pub async fn get_state(&self) -> WorldState {
        self.state.read().await.clone()
    }

    /// Export state for dashboard/API
    pub async fn export_json(&self) -> String {
        let state = self.get_state().await;
        serde_json::to_string_pretty(&state).unwrap_or_default()
    }

    /// Save current state to persistence layer
    pub async fn save_state(&self, persistence: &PersistenceManager) -> Result<(), PersistenceError> {
        let state = self.get_state().await;
        persistence.save(&state, &self.config).await
    }

    /// Load state from persistence layer
    pub async fn load_state(persistence: &PersistenceManager) -> Result<(WorldState, SimConfig), PersistenceError> {
        persistence.load().await
    }

    /// Create new WorldSim from persisted state
    pub async fn from_persisted(persistence: &PersistenceManager) -> Result<Self, PersistenceError> {
        let (state, config) = Self::load_state(persistence).await?;
        let rng = StdRng::seed_from_u64(state.rng_seed);
        Ok(Self {
            state: Arc::new(RwLock::new(state)),
            config,
            rng,
        })
    }
}

#[derive(Debug, thiserror::Error)]
pub enum SimError {
    #[error("Simulation error: {0}")]
    Generic(String),
    #[error("Invalid state: {0}")]
    InvalidState(String),
    #[error("Edit failed: {0}")]
    EditFailed(String),
}