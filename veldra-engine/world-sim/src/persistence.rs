//! World State Persistence — SQLite + JSON serialization for simulation state.
//! Enables simulation to survive restarts and maintain continuity.

use crate::*;
use serde::{Deserialize, Serialize};
use sqlx::{sqlite::SqlitePoolOptions, Pool, Sqlite, Row, Error as SqlxError};
use std::path::Path;
use chrono::Utc;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PersistedWorldState {
    pub schema_version: u32,
    pub saved_at: String,
    pub simulation_time: f64,
    pub tick: u64,
    pub theorem_artifact: TheoremArtifact,
    pub dust_storm: DustStorm,
    pub colony: ColonyInfrastructure,
    pub geophysics_lab: GeophysicsLab,
    pub characters: Vec<Character>, // HashMap serialized as vec
    pub event_log: Vec<WorldEvent>,
    pub rng_seed: u64,
    pub config: SimConfig,
}

impl PersistedWorldState {
    pub fn from_world_state(state: &WorldState, config: &SimConfig) -> Self {
        Self {
            schema_version: 1,
            saved_at: Utc::now().to_rfc3339(),
            simulation_time: state.simulation_time.0,
            tick: state.tick,
            theorem_artifact: state.theorem_artifact.clone(),
            dust_storm: state.dust_storm.clone(),
            colony: state.colony.clone(),
            geophysics_lab: state.geophysics_lab.clone(),
            characters: state.characters.values().cloned().collect(),
            event_log: state.event_log.clone(),
            rng_seed: state.rng_seed,
            config: config.clone(),
        }
    }
    
    pub fn to_world_state(&self) -> WorldState {
        let mut characters = std::collections::HashMap::new();
        for c in &self.characters {
            characters.insert(c.id, c.clone());
        }
        WorldState {
            simulation_time: VeldraTime(self.simulation_time),
            tick: self.tick,
            theorem_artifact: self.theorem_artifact.clone(),
            dust_storm: self.dust_storm.clone(),
            colony: self.colony.clone(),
            geophysics_lab: self.geophysics_lab.clone(),
            characters,
            event_log: self.event_log.clone(),
            rng_seed: self.rng_seed,
        }
    }
}

pub struct PersistenceManager {
    pool: Pool<Sqlite>,
    json_path: std::path::PathBuf,
}

impl PersistenceManager {
    pub async fn new(db_path: &str, json_path: &str) -> Result<Self, sqlx::Error> {
        let pool = SqlitePoolOptions::new()
            .max_connections(1)
            .connect(db_path)
            .await?;
        
        // Initialize schema
        sqlx::query(
            r#"
            CREATE TABLE IF NOT EXISTS world_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                schema_version INTEGER NOT NULL,
                saved_at TEXT NOT NULL,
                data BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER NOT NULL,
                simulation_time REAL NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_event_log_tick ON event_log(tick);
            "#,
        )
        .execute(&pool)
        .await?;
        
        let manager = Self {
            pool,
            json_path: Path::new(json_path).to_path_buf(),
        };
        
        // Also ensure JSON path exists
        if let Some(parent) = manager.json_path.parent() {
            tokio::fs::create_dir_all(parent).await.ok();
        }
        
        Ok(manager)
    }
    
    pub async fn save(&self, state: &WorldState, config: &SimConfig) -> Result<(), PersistenceError> {
        let persisted = PersistedWorldState::from_world_state(state, config);
        
        // Save to SQLite (binary)
        let data = bincode::serialize(&persisted)
            .map_err(|e| PersistenceError::Serialization(e.to_string()))?;
        
        sqlx::query(
            "INSERT OR REPLACE INTO world_state (id, schema_version, saved_at, data) VALUES (1, ?, ?, ?)"
        )
        .bind(persisted.schema_version as i64)
        .bind(&persisted.saved_at)
        .bind(&data)
        .execute(&self.pool)
        .await
        .map_err(|e| PersistenceError::Database(e.to_string()))?;
        
        // Save latest N events to event_log table
        let recent_events = state.event_log.iter().rev().take(1000).collect::<Vec<_>>();
        for event in recent_events {
            sqlx::query(
                "INSERT OR IGNORE INTO event_log (tick, simulation_time, event_type, description, severity, data) VALUES (?, ?, ?, ?, ?, ?)"
            )
            .bind(state.tick as i64)
            .bind(state.simulation_time.0)
            .bind(format!("{:?}", event.event_type))
            .bind(&event.description)
            .bind(format!("{:?}", event.severity))
            .bind(serde_json::to_string(&event.data).unwrap_or_default())
            .execute(&self.pool)
            .await
            .map_err(|e| PersistenceError::Database(e.to_string()))?;
        }
        
        // Also save JSON for human readability / debugging
        let json = serde_json::to_string_pretty(&persisted)
            .map_err(|e| PersistenceError::Serialization(e.to_string()))?;
        tokio::fs::write(&self.json_path, json).await
            .map_err(|e| PersistenceError::Io(e.to_string()))?;
        
        Ok(())
    }
    
    pub async fn load(&self) -> Result<(WorldState, SimConfig), PersistenceError> {
        // Try SQLite first
        if let Ok(row) = sqlx::query("SELECT data FROM world_state WHERE id = 1")
            .fetch_optional(&self.pool)
            .await {
            if let Some(row) = row {
                let data: Vec<u8> = row.try_get("data")?;
                let persisted: PersistedWorldState = bincode::deserialize(&data)
                    .map_err(|e| PersistenceError::Serialization(e.to_string()))?;
                return Ok((persisted.to_world_state(), persisted.config));
            }
        }
        
        // Fallback to JSON
        if self.json_path.exists() {
            let json = tokio::fs::read_to_string(&self.json_path).await
                .map_err(|e| PersistenceError::Io(e.to_string()))?;
            let persisted: PersistedWorldState = serde_json::from_str(&json)
                .map_err(|e| PersistenceError::Serialization(e.to_string()))?;
            return Ok((persisted.to_world_state(), persisted.config));
        }
        
        Err(PersistenceError::NotFound)
    }
    
    pub async fn load_events_since(&self, tick: u64, limit: usize) -> Result<Vec<WorldEvent>, PersistenceError> {
        let rows = sqlx::query(
            "SELECT event_type, description, severity, data, tick, simulation_time FROM event_log WHERE tick > ? ORDER BY tick ASC LIMIT ?"
        )
        .bind(tick as i64)
        .bind(limit as i64)
        .fetch_all(&self.pool)
        .await
        .map_err(|e| PersistenceError::Database(e.to_string()))?;
        
        let mut events = Vec::new();
        for row in rows {
            let event_type: String = row.try_get("event_type")?;
            let description: String = row.try_get("description")?;
            let severity: String = row.try_get("severity")?;
            let data_str: String = row.try_get("data")?;
            let _tick: i64 = row.try_get("tick")?;
            let _sim_time: f64 = row.try_get("simulation_time")?;
            
            let event_type = match event_type.as_str() {
                "StormPhaseChange" => EventType::StormPhaseChange,
                "ArtifactFlare" => EventType::ArtifactFlare,
                "LedgerEdit" => EventType::LedgerEdit,
                "CountdownTick" => EventType::CountdownTick,
                "SystemFailure" => EventType::SystemFailure,
                "SupplyChange" => EventType::SupplyChange,
                "CharacterAction" => EventType::CharacterAction,
                "Experiment" => EventType::Experiment,
                "CommsContact" => EventType::CommsContact,
                "StructuralDamage" => EventType::StructuralDamage,
                _ => EventType::SystemFailure,
            };
            
            let severity = match severity.as_str() {
                "Info" => EventSeverity::Info,
                "Warning" => EventSeverity::Warning,
                "Critical" => EventSeverity::Critical,
                "Existential" => EventSeverity::Existential,
                _ => EventSeverity::Warning,
            };
            
            let data: serde_json::Value = serde_json::from_str(&data_str).unwrap_or_default();
            
            events.push(WorldEvent {
                timestamp: VeldraTime(_sim_time),
                event_type,
                description,
                participants: vec![],
                severity,
                data,
            });
        }
        
        Ok(events)
    }
}

#[derive(Debug, thiserror::Error)]
pub enum PersistenceError {
    #[error("Database error: {0}")]
    Database(String),
    #[error("Serialization error: {0}")]
    Serialization(String),
    #[error("IO error: {0}")]
    Io(String),
    #[error("No saved state found")]
    NotFound,
}

impl From<SqlxError> for PersistenceError {
    fn from(e: SqlxError) -> Self {
        PersistenceError::Database(e.to_string())
    }
}

impl From<std::io::Error> for PersistenceError {
    fn from(e: std::io::Error) -> Self {
        PersistenceError::Io(e.to_string())
    }
}

impl From<bincode::Error> for PersistenceError {
    fn from(e: bincode::Error) -> Self {
        PersistenceError::Serialization(e.to_string())
    }
}

impl From<serde_json::Error> for PersistenceError {
    fn from(e: serde_json::Error) -> Self {
        PersistenceError::Serialization(e.to_string())
    }
}