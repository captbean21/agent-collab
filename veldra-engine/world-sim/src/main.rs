//! Veldra-7 World Simulation Server
//! Runs the simulation and exposes REST/WebSocket API for dashboard.

use veldra_world_sim::WorldSim;
use veldra_shared_types::{SimConfig, *};
use axum::{
    extract::{State, WebSocketUpgrade, Query},
    http::StatusCode,
    response::{Html, IntoResponse, Json, Response},
    routing::{get, post},
    Router,
};
use axum::extract::ws::{Message, WebSocket};
use futures::{sink::SinkExt, stream::StreamExt};
use serde_json::json;
use std::sync::Arc;
use tokio::sync::{broadcast, RwLock};
use tower_http::cors::{Any, CorsLayer};
use tower_http::services::ServeDir;
use std::time::Duration;

#[derive(Clone)]
struct AppState {
    sim: Arc<RwLock<WorldSim>>,
    tx: broadcast::Sender<String>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    
    let config = SimConfig::default();
    let sim = Arc::new(RwLock::new(WorldSim::new(config)));
    let (tx, _rx) = broadcast::channel(100);
    
    let app_state = AppState { sim: sim.clone(), tx: tx.clone() };
    
    // Start simulation loop
    let sim_loop = sim.clone();
    let tx_loop = tx.clone();
    tokio::spawn(async move {
        let mut interval = tokio::time::interval(Duration::from_secs(1));
        loop {
            interval.tick().await;
            let mut sim = sim_loop.write().await;
            if let Ok(state) = sim.tick().await {
                let json = serde_json::to_string(&state).unwrap_or_default();
                let _ = tx_loop.send(json);
            }
        }
    });

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/api/state", get(get_state))
        .route("/api/state/export", get(export_state))
        .route("/api/ledger/edit", post(ledger_edit))
        .route("/api/ledger/conjugate", post(inject_conjugate))
        .route("/api/config", get(get_config))
        .route("/ws", get(websocket_handler))
        .route("/", get(serve_index))
        .with_state(app_state)
        .layer(cors);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    println!("Veldra-7 World Sim server running on http://0.0.0.0:8080");
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn get_state(State(app): State<AppState>) -> Json<WorldState> {
    let sim = app.sim.read().await;
    Json(sim.get_state().await)
}

async fn export_state(State(app): State<AppState>) -> impl IntoResponse {
    let sim = app.sim.read().await;
    let json = sim.export_json().await;
    ([("Content-Type", "application/json")], json)
}

async fn get_config(State(app): State<AppState>) -> Json<SimConfig> {
    let sim = app.sim.read().await;
    Json(sim.config.clone())
}

#[derive(serde::Deserialize)]
struct LedgerEditRequest {
    edit_type: String, // "CrossOut", "Rewrite", "Append", "Deletion"
    target_key: String,
    new_value: Option<serde_json::Value>,
    injector_name: String, // "Varel" or "Merrow"
}

async fn ledger_edit(
    State(app): State<AppState>,
    Json(req): Json<LedgerEditRequest>,
) -> Result<Json<LedgerEdit>, (StatusCode, String)> {
    let mut sim = app.sim.write().await;
    
    let injector_id = {
        let state = sim.get_state().await;
        state.characters.values()
            .find(|c| c.name == req.injector_name)
            .map(|c| c.id)
            .ok_or_else(|| (StatusCode::BAD_REQUEST, "Invalid injector".to_string()))?
    };

    let edit_type = match req.edit_type.as_str() {
        "CrossOut" => LedgerEditType::CrossOut,
        "Rewrite" => LedgerEditType::Rewrite,
        "Append" => LedgerEditType::Append,
        "Deletion" => LedgerEditType::Deletion,
        _ => return Err((StatusCode::BAD_REQUEST, "Invalid edit type".to_string())),
    };

    let new_value = req.new_value.and_then(|v| {
        serde_json::from_value(v).ok()
    });

    match sim.perform_ledger_edit(edit_type, req.target_key, new_value, injector_id).await {
        Ok(edit) => Ok(Json(edit)),
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, e.to_string())),
    }
}

async fn inject_conjugate(
    State(app): State<AppState>,
    Json(req): Json<serde_json::Value>,
) -> Result<Json<LedgerEdit>, (StatusCode, String)> {
    let mut sim = app.sim.write().await;
    
    let injector_name = req.get("injector_name").and_then(|v| v.as_str()).unwrap_or("Merrow");
    let injector_id = {
        let state = sim.get_state().await;
        state.characters.values()
            .find(|c| c.name == injector_name)
            .map(|c| c.id)
            .ok_or_else(|| (StatusCode::BAD_REQUEST, "Invalid injector".to_string()))?
    };

    match sim.inject_conjugate_constant(injector_id).await {
        Ok(edit) => Ok(Json(edit)),
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, e.to_string())),
    }
}

async fn websocket_handler(
    ws: WebSocketUpgrade,
    State(app): State<AppState>,
) -> Response {
    ws.on_upgrade(move |socket| handle_socket(socket, app))
}

async fn handle_socket(mut socket: WebSocket, app: AppState) {
    let mut rx = app.tx.subscribe();
    
    // Send initial state
    let initial = app.sim.read().await.get_state().await;
    if let Ok(json) = serde_json::to_string(&initial) {
        let _ = socket.send(Message::Text(json.into())).await;
    }
    
    // Forward simulation updates
    while let Ok(msg) = rx.recv().await {
        if socket.send(Message::Text(msg.into())).await.is_err() {
            break;
        }
    }
}

async fn serve_index() -> Html<&'static str> {
    Html(r#"
<!DOCTYPE html>
<html>
<head>
    <title>Veldra-7 World Engine</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Monospace', monospace; background: #0a0a0f; color: #e0e0e0; margin: 0; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: #ffd700; text-shadow: 0 0 10px #ffd700; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .panel { background: #111; border: 1px solid #333; border-radius: 8px; padding: 16px; }
        .panel h2 { color: #00ffff; margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 8px; }
        .metric { display: flex; justify-content: space-between; margin: 8px 0; }
        .metric .label { color: #888; }
        .metric .value { color: #fff; font-weight: bold; }
        .critical .value { color: #ff4444; animation: pulse 1s infinite; }
        .warning .value { color: #ffaa00; }
        .good .value { color: #44ff44; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .event-log { max-height: 300px; overflow-y: auto; font-size: 12px; }
        .event { padding: 4px 0; border-bottom: 1px solid #222; }
        .event .time { color: #666; }
        .event .desc { color: #ccc; }
        .event.existential .desc { color: #ff4444; }
        .event.critical .desc { color: #ffaa00; }
        button { background: #1a1a2e; border: 1px solid #00ffff; color: #00ffff; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin: 4px; }
        button:hover { background: #00ffff; color: #000; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .phi { color: #ffd700; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🟣 Veldra-7 Living World Engine</h1>
        <div class="grid" id="panels">
            <!-- Panels populated by JS -->
        </div>
    </div>
    <script>
        const ws = new WebSocket('ws://' + location.host + '/ws');
        const panels = document.getElementById('panels');
        
        ws.onmessage = (event) => {
            const state = JSON.parse(event.data);
            render(state);
        };
        
        function render(s) {
            panels.innerHTML = `
                <div class="panel">
                    <h2>📜 Theorem Artifact</h2>
                    <div class="metric"><span class="label">Anchor Constant (φ)</span><span class="value phi">${s.theorem_artifact.anchor_constant.toFixed(12)}</span></div>
                    <div class="metric"><span class="label">Conjugate (1/φ)</span><span class="value phi">${s.theorem_artifact.conjugate_constant.toFixed(12)}</span></div>
                    <div class="metric ${s.theorem_artifact.countdown_days < 2 ? 'critical' : s.theorem_artifact.countdown_days < 5 ? 'warning' : 'good'}">
                        <span class="label">Countdown</span><span class="value">${s.theorem_artifact.countdown_days.toFixed(2)} days</span>
                    </div>
                    <div class="metric"><span class="label">Burn Rate</span><span class="value">${(s.theorem_artifact.countdown_acceleration * 100).toFixed(1)}%</span></div>
                    <div class="metric"><span class="label">Emission Lines</span><span class="value">${s.theorem_artifact.emission_lines.map(x => x.toFixed(3) + ' MeV').join(', ')}</span></div>
                    <div class="metric"><span class="label">Flare Intensity</span><span class="value">${(s.theorem_artifact.flare_intensity * 100).toFixed(1)}%</span></div>
                    <button onclick="injectConjugate()">Inject Conjugate (1/φ)</button>
                </div>
                <div class="panel">
                    <h2>🌪️ Dust Storm</h2>
                    <div class="metric"><span class="label">Phase</span><span class="value">${s.dust_storm.phase}</span></div>
                    <div class="metric"><span class="label">Optical Depth (τ)</span><span class="value">${s.dust_storm.optical_depth.toFixed(2)}</span></div>
                    <div class="metric"><span class="label">Electrostatic Field</span><span class="value">${(s.dust_storm.electrostatic_field / 1e6).toFixed(2)} × 10⁶ V/km</span></div>
                    <div class="metric"><span class="label">Days Elapsed</span><span class="value">${s.dust_storm.days_elapsed.toFixed(1)} / ${s.dust_storm.duration_days}</span></div>
                    <div class="metric"><span class="label">Triboelectric Charge</span><span class="value">${s.dust_storm.triboelectric_charge_kv} kV</span></div>
                </div>
                <div class="panel">
                    <h2>🏭 Colony Infrastructure</h2>
                    <div class="metric"><span class="label">Population</span><span class="value">${s.colony.population}</span></div>
                    <div class="metric"><span class="label">Solar Output</span><span class="value">${s.colony.solar_array.current_kw.toFixed(0)} / ${s.colony.solar_array.peak_kw} kW</span></div>
                    <div class="metric ${s.colony.battery_bank.current_pct < 0.2 ? 'critical' : 'warning'}">
                        <span class="label">Battery</span><span class="value">${(s.colony.battery_bank.current_pct * 100).toFixed(1)}%</span>
                    </div>
                    <div class="metric"><span class="label">Water Efficiency</span><span class="value">${(s.colony.water_reclamation.efficiency * 100).toFixed(1)}%</span></div>
                    <div class="metric"><span class="label">O₂ Efficiency</span><span class="value">${(s.colony.oxygen_generation.efficiency * 100).toFixed(1)}%</span></div>
                    <div class="metric"><span class="label">Comms Range</span><span class="value">${s.colony.comms_mesh.range_km.toFixed(1)} km</span></div>
                    <div class="metric"><span class="label">Packet Loss</span><span class="value">${s.colony.comms_mesh.packet_loss_pct.toFixed(1)}%</span></div>
                </div>
                <div class="panel">
                    <h2>📦 Supplies</h2>
                    <div class="metric ${s.colony.supply_days.food_days < 3 ? 'critical' : s.colony.supply_days.food_days < 7 ? 'warning' : 'good'}">
                        <span class="label">Food</span><span class="value">${s.colony.supply_days.food_days.toFixed(1)} days</span>
                    </div>
                    <div class="metric ${s.colony.supply_days.water_days < 3 ? 'critical' : 'warning'}">
                        <span class="label">Water</span><span class="value">${s.colony.supply_days.water_days.toFixed(1)} days</span>
                    </div>
                    <div class="metric ${s.colony.supply_days.oxygen_days < 2 ? 'critical' : 'warning'}">
                        <span class="label">Oxygen</span><span class="value">${s.colony.supply_days.oxygen_days.toFixed(1)} days</span>
                    </div>
                </div>
                <div class="panel">
                    <h2>🔬 Geophysics Lab (GL-7)</h2>
                    <div class="metric"><span class="label">Power</span><span class="value">${s.geophysics_lab.power_watts.toFixed(1)} / 45 W</span></div>
                    <div class="metric"><span class="label">Detector 1</span><span class="value">${s.geophysics_lab.detector1_active ? 'ACTIVE (Peltier)' : 'OFFLINE'}</span></div>
                    <div class="metric"><span class="label">Detector 2/3</span><span class="value">${s.geophysics_lab.detector2_active ? 'ACTIVE' : 'OFFLINE (RTG 3 cold)'}</span></div>
                    <div class="metric"><span class="label">Neutron Source</span><span class="value">${(s.geophysics_lab.neutron_source_output / 1e3).toFixed(1)}k n/s</span></div>
                    <div class="metric"><span class="label">RTG Units</span><span class="value">${s.geophysics_lab.rtg_units.filter(r => r.operational).length} / 3 operational</span></div>
                    <div class="metric"><span class="label">Radiation</span><span class="value">${s.geophysics_lab.atmospheric.radiation_background_usv_hr.toFixed(2)} μSv/hr</span></div>
                </div>
                <div class="panel">
                    <h2>👥 Characters</h2>
                    ${Object.values(s.characters).map(c => `
                        <div class="metric"><span class="label">${c.name} (${c.role})</span><span class="value">Health: ${(c.health*100).toFixed(0)}% | Stress: ${(c.stress*100).toFixed(0)}%</span></div>
                        ${c.neural_link ? `<div class="metric critical"><span class="label">Neural Link Countdown</span><span class="value">${c.neural_link.countdown_display_days.toFixed(2)} days</span></div>` : ''}
                        ${c.neural_link ? `<div class="metric"><span class="label">Data Corruption</span><span class="value">${(c.neural_link.data_corruption*100).toFixed(1)}%</span></div>` : ''}
                    `).join('')}
                </div>
                <div class="panel" style="grid-column: 1 / -1;">
                    <h2>📋 Event Log</h2>
                    <div class="event-log">
                        ${s.event_log.slice(-20).reverse().map(e => `
                            <div class="event ${e.severity.toLowerCase()}">
                                <span class="time">[Tick ${s.tick} | ${e.timestamp.0.toFixed(2)} V-yr]</span>
                                <span class="desc"> ${e.description}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        function injectConjugate() {
            fetch('/api/ledger/conjugate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ injector_name: 'Elara Merrow' })
            }).then(r => r.json()).then(d => console.log('Injected:', d));
        }
    </script>
</body>
</html>
"#)
}