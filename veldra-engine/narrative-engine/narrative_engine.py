#!/usr/bin/env python3
"""
Veldra-7 Narrative Engine
Generates canon-compliant narrative content from world simulation state.
Uses local Qwen 2.5-Coder-14B-Instruct on port 5001 for generation.
"""

import json
import asyncio
import httpx
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import tiktoken


@dataclass
class NarrativeConfig:
    """Configuration for narrative generation."""
    llm_base_url: str = "http://127.0.0.1:5001/v1"
    model: str = "qwen2.5-coder-14b-instruct"
    max_context_tokens: int = 32000
    max_output_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    timeout_seconds: float = 60.0


@dataclass
class WorldStateSummary:
    """Condensed world state for LLM context."""
    simulation_time: float
    tick: int
    theorem_artifact: Dict[str, Any]
    dust_storm: Dict[str, Any]
    colony: Dict[str, Any]
    geophysics_lab: Dict[str, Any]
    characters: Dict[str, Any]
    recent_events: List[Dict[str, Any]]


@dataclass
class NarrativeOutput:
    """Generated narrative content."""
    chapter_title: str
    pov_character: str
    content: str
    word_count: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    world_state_ref: Dict[str, Any] = field(default_factory=dict)


class TokenCounter:
    """Token counting for context management."""
    
    def __init__(self, model: str = "cl100k_base"):
        try:
            self.encoding = tiktoken.get_encoding(model)
        except Exception:
            # Fallback to rough estimation
            self.encoding = None
    
    def count(self, text: str) -> int:
        if self.encoding:
            return len(self.encoding.encode(text))
        return len(text) // 4  # Rough estimate


class WorldStateCompressor:
    """Compresses world state into LLM-friendly summary."""
    
    def __init__(self, token_counter: TokenCounter, max_tokens: int = 8000):
        self.token_counter = token_counter
        self.max_tokens = max_tokens
    
    def compress(self, state: Dict[str, Any]) -> WorldStateSummary:
        """Extract key narrative-relevant information from full state."""
        
        # Theorem artifact summary
        artifact = state.get("theorem_artifact", {})
        artifact_summary = {
            "anchor_constant": artifact.get("anchor_constant"),
            "countdown_days": artifact.get("countdown_days"),
            "countdown_acceleration": artifact.get("countdown_acceleration"),
            "emission_lines": artifact.get("emission_lines"),
            "flare_intensity": artifact.get("flare_intensity"),
            "last_injection": artifact.get("last_injection"),
            "ledger_edit_count": len(artifact.get("ledger_state", {}).get("edit_history", [])),
        }
        
        # Dust storm summary
        storm = state.get("dust_storm", {})
        storm_summary = {
            "phase": storm.get("phase"),
            "optical_depth": storm.get("optical_depth"),
            "electrostatic_field_v_per_km": storm.get("electrostatic_field", 0) / 1000,
            "days_elapsed": storm.get("days_elapsed"),
            "duration_days": storm.get("duration_days"),
        }
        
        # Colony summary
        colony = state.get("colony", {})
        colony_summary = {
            "population": colony.get("population"),
            "solar_kw": colony.get("solar_array", {}).get("current_kw"),
            "battery_pct": colony.get("battery_bank", {}).get("current_pct"),
            "water_efficiency": colony.get("water_reclamation", {}).get("efficiency"),
            "oxygen_efficiency": colony.get("oxygen_generation", {}).get("efficiency"),
            "comms_range_km": colony.get("comms_mesh", {}).get("range_km"),
            "supplies": colony.get("supply_days"),
            "rtg_operational": sum(1 for r in colony.get("rtg_fleet", []) if r.get("operational")),
        }
        
        # Lab summary
        lab = state.get("geophysics_lab", {})
        lab_summary = {
            "power_watts": lab.get("power_watts"),
            "detector1_active": lab.get("detector1_active"),
            "detector2_active": lab.get("detector2_active"),
            "detector3_active": lab.get("detector3_active"),
            "neutron_source_n_per_s": lab.get("neutron_source_output"),
            "rtg_units_operational": sum(1 for r in lab.get("rtg_units", []) if r.get("operational")),
            "radiation_usv_hr": lab.get("atmospheric", {}).get("radiation_background_usv_hr"),
        }
        
        # Character summaries
        characters = {}
        for cid, char in state.get("characters", {}).items():
            characters[char.get("name", cid)] = {
                "role": char.get("role"),
                "location": char.get("location"),
                "health_pct": int(char.get("health", 1) * 100),
                "stress_pct": int(char.get("stress", 0) * 100),
                "skills": char.get("skills", []),
                "neural_link": char.get("neural_link") is not None,
                "countdown_display": char.get("neural_link", {}).get("countdown_display_days") if char.get("neural_link") else None,
                "data_corruption_pct": int(char.get("neural_link", {}).get("data_corruption", 0) * 100) if char.get("neural_link") else 0,
            }
        
        # Recent events (last 10)
        events = state.get("event_log", [])[-10:]
        recent_events = [
            {
                "tick": e.get("timestamp", {}).get("0", 0) if isinstance(e.get("timestamp"), dict) else 0,
                "type": e.get("event_type"),
                "description": e.get("description"),
                "severity": e.get("severity"),
            }
            for e in events
        ]
        
        return WorldStateSummary(
            simulation_time=state.get("simulation_time", {}).get("0", 200.0) if isinstance(state.get("simulation_time"), dict) else 200.0,
            tick=state.get("tick", 0),
            theorem_artifact=artifact_summary,
            dust_storm=storm_summary,
            colony=colony_summary,
            geophysics_lab=lab_summary,
            characters=characters,
            recent_events=recent_events,
        )


class NarrativeEngine:
    """Main narrative generation engine."""
    
    # System prompt for Veldra-7 narrative generation
    SYSTEM_PROMPT = """You are the chronicler of Veldra-7, a hard-SF colony world 200 years post-landing.
Your task: Generate narrative content (character logs, chapter segments, event narratives) that is strictly consistent with the provided world state.

WORLD CONSTANTS (immutable):
- Theorem Artifact: Phase-conjugate topological anchor beneath Habitat Module 12
- Anchor constant C_p = φ (1.618033988749895...), conjugate C_p⁻¹ = 1/φ
- Emission lines: 1.3, 2.6, 4.1 MeV (Fibonacci-weighted: Eₙ = E₀·Fₙ)
- Countdown: Anchor half-life, accelerated by dust storm electrostatic coupling
- Ledger edits: CrossOut/Rewrite/Append/Deletion — each burns countdown time
- Dust Storm: Type-G, τ=8.4 peak, 10⁶ V/km electrostatic field, 4.3 Veldra-year cycle
- Colony: 17 survivors in H-12, solar 58/400 kW, battery 31%, supplies critical
- Characters: Kade Varel (robotics, GL-7), Elara Merrow (mathematician, neural link, GL-7)

NARRATIVE RULES:
1. NEVER contradict world state numbers — treat them as physical law
2. Elara's neural link shows the countdown; Kade maintains the lab
3. Storm electrostatics modulate the artifact; this is measurable physics
4. Ledger edits have physical consequences (countdown burn, emission shifts)
5. No magic, no handwaving — hard SF only
6. Character voices: Varel = practical/engineering, Merrow = theoretical/precise
7. Chapter hooks from spec: Year 3 Survey, Contraction Day, The Datapad, First Injection, Storm Protocols, Outside the Bubble

OUTPUT FORMAT: JSON with keys: chapter_title, pov_character, content"""
    
    def __init__(self, config: NarrativeConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=config.timeout_seconds)
        self.token_counter = TokenCounter()
        self.compressor = WorldStateCompressor(self.token_counter, max_tokens=8000)
        self.history: List[NarrativeOutput] = []
    
    async def generate(self, world_state: Dict[str, Any], 
                      prompt: str = "Generate next narrative segment",
                      pov: Optional[str] = None) -> NarrativeOutput:
        """Generate narrative from world state."""
        
        # Compress world state
        summary = self.compressor.compress(world_state)
        
        # Build user prompt
        state_json = json.dumps(summary.__dict__, indent=2)
        
        user_prompt = f"""WORLD STATE (Tick {summary.tick}, Year {summary.simulation_time:.2f} Post-Landing):
{state_json}

TASK: {prompt}
{f"POV: {pov}" if pov else "POV: Choose appropriate character (Varel or Merrow)"}

Generate narrative content as JSON with keys: chapter_title, pov_character, content"""
        
        # Count tokens
        system_tokens = self.token_counter.count(self.SYSTEM_PROMPT)
        user_tokens = self.token_counter.count(user_prompt)
        available_output = self.config.max_context_tokens - system_tokens - user_tokens - 500
        
        max_tokens = min(self.config.max_output_tokens, max(500, available_output))
        
        # Call LLM
        response = await self._call_llm(user_prompt, max_tokens)
        
        # Parse response
        try:
            parsed = json.loads(response)
            output = NarrativeOutput(
                chapter_title=parsed.get("chapter_title", "Untitled"),
                pov_character=parsed.get("pov_character", pov or "Unknown"),
                content=parsed.get("content", response),
                word_count=len(parsed.get("content", "").split()),
                world_state_ref={
                    "tick": summary.tick,
                    "simulation_time": summary.simulation_time,
                    "artifact_countdown": summary.theorem_artifact.get("countdown_days"),
                    "storm_phase": summary.dust_storm.get("phase"),
                }
            )
        except json.JSONDecodeError:
            # Fallback: wrap raw response
            output = NarrativeOutput(
                chapter_title="Raw Output",
                pov_character=pov or "Unknown",
                content=response,
                word_count=len(response.split()),
                world_state_ref={
                    "tick": summary.tick,
                    "simulation_time": summary.simulation_time,
                }
            )
        
        self.history.append(output)
        return output
    
    async def _call_llm(self, prompt: str, max_tokens: int) -> str:
        """Call local LLM API."""
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "stream": False
        }
        
        try:
            response = await self.client.post(
                f"{self.config.llm_base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM Error: {e}]"
    
    async def generate_chapter(self, world_state: Dict[str, Any], 
                              chapter_hook: str) -> NarrativeOutput:
        """Generate a full chapter from a narrative hook."""
        hooks = {
            "year3_survey": "Chapter 1: The Last Survey (Year 3) — Initial survey team discovers the artifact in bedrock. 'It's not ours. It's been waiting.'",
            "contraction_day": "Chapter 2: Contraction Day (Year 87) — Physics fails across the colony. The 5km bubble around H-12 holds. Everyone inside survives. Everyone outside... doesn't.",
            "the_datapad": "Chapter 3: The Datapad (Year 199-200) — Elara recovers Contraction-era archives. Finds φ in a theorist's suicide note: 'The universe counts in Fibonacci. The anchor holds at phi. Don't let them rewrite the ledger.'",
            "first_injection": "Chapter 4: First Injection (Year 200, Storm Season) — Kade and Elara jury-rig the DAC. Elara types φ. Equations bloom on her retinal implant — the entire ledger visible for 3.2 seconds. She sees her own death entry: 8 days, 14 hours, 7 minutes.",
            "storm_protocols": "Chapter 5: Storm Protocols (Current — Year 200, Day 3 of Type-G Storm) — Storm electrostatics accelerate the countdown. 11 days food, 8 days water, 6 days O₂ — but anchor half-life is now 5 days, 18 hours. Decision: run conjugate constant experiment (1/φ) to heal the anchor, knowing failure could zero the countdown instantly.",
            "outside_bubble": "Chapter 6: Outside the Bubble (Post-Storm) — Expedition to Hab-14 (2.3 km) through unpressurized tunnel. If anchor holds, tunnel physics are stable. If it fails, the tunnel ceases to exist — not blocked, gone."
        }
        
        prompt = f"Generate {hooks.get(chapter_hook, chapter_hook)} as a narrative chapter segment."
        return await self.generate(world_state, prompt)
    
    async def generate_event_narrative(self, world_state: Dict[str, Any], 
                                       event: Dict[str, Any]) -> NarrativeOutput:
        """Generate narrative for a specific world event."""
        prompt = f"Generate a character log entry for this event: {json.dumps(event, indent=2)}. Write from the perspective of the most relevant character."
        return await self.generate(world_state, prompt)
    
    def save_output(self, output: NarrativeOutput, path: Path):
        """Save narrative output to file."""
        data = {
            "chapter_title": output.chapter_title,
            "pov_character": output.pov_character,
            "content": output.content,
            "word_count": output.word_count,
            "timestamp": output.timestamp.isoformat(),
            "world_state_ref": output.world_state_ref,
        }
        path.write_text(json.dumps(data, indent=2))
    
    async def close(self):
        await self.client.aclose()


async def main():
    """Demo: Generate narrative from sample world state."""
    config = NarrativeConfig()
    engine = NarrativeEngine(config)
    
    # Sample world state (would come from world-sim API)
    sample_state = {
        "simulation_time": {"0": 200.0},
        "tick": 142,
        "theorem_artifact": {
            "anchor_constant": 1.618033988749895,
            "conjugate_constant": 0.6180339887498948,
            "countdown_days": 5.3,
            "countdown_acceleration": 1.35,
            "emission_lines": [1.3002, 2.6004, 4.1006],
            "flare_intensity": 0.72,
            "last_injection": {"edit_type": "Rewrite", "target_key": "anchor_constant", "countdown_delta": 0.34},
            "ledger_state": {"edit_history": [{"edit_type": "Rewrite"}, {"edit_type": "Append"}]}
        },
        "dust_storm": {
            "phase": "Active",
            "optical_depth": 7.2,
            "electrostatic_field": 890000,
            "days_elapsed": 3.4,
            "duration_days": 21.0
        },
        "colony": {
            "population": 17,
            "solar_array": {"current_kw": 58.0, "peak_kw": 400.0},
            "battery_bank": {"current_pct": 0.28, "capacity_mwh": 2.4},
            "water_reclamation": {"efficiency": 0.52},
            "oxygen_generation": {"efficiency": 0.41},
            "comms_mesh": {"range_km": 1.4, "nodes_operational": 9, "packet_loss_pct": 42.0},
            "supply_days": {"food_days": 9.2, "water_days": 7.1, "oxygen_days": 5.3},
            "rtg_fleet": [{"operational": True}] * 14
        },
        "geophysics_lab": {
            "power_watts": 38.0,
            "detector1_active": True,
            "detector2_active": False,
            "detector3_active": False,
            "neutron_source_output": 8500,
            "rtg_units": [{"operational": True}, {"operational": True}, {"operational": False}],
            "atmospheric": {"radiation_background_usv_hr": 8.7}
        },
        "characters": {
            "varel": {
                "name": "Kade Varel",
                "role": "RoboticsEngineer",
                "location": "GL-7",
                "health": 0.88,
                "stress": 0.65,
                "skills": ["robotics", "fabrication", "rtg-maintenance"],
                "neural_link": None
            },
            "merrow": {
                "name": "Elara Merrow",
                "role": "MathematicianTheorist",
                "location": "GL-7",
                "health": 0.82,
                "stress": 0.85,
                "skills": ["mathematics", "theorem-analysis", "archive-recovery"],
                "neural_link": {
                    "theorem_marked": True,
                    "countdown_display_days": 5.3,
                    "data_corruption": 0.12
                }
            }
        },
        "event_log": [
            {"timestamp": {"0": 200.0}, "event_type": "ArtifactFlare", "description": "Artifact flare: intensity 0.72", "severity": "Warning"},
            {"timestamp": {"0": 200.0}, "event_type": "LedgerEdit", "description": "Ledger edit: Rewrite on 'anchor_constant', countdown -0.340 days", "severity": "Warning"},
        ]
    }
    
    print("Generating Chapter 5: Storm Protocols...")
    output = await engine.generate_chapter(sample_state, "storm_protocols")
    
    print(f"\n=== {output.chapter_title} ===")
    print(f"POV: {output.pov_character}")
    print(f"Words: {output.word_count}")
    print(f"\n{output.content}\n")
    
    # Save
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    engine.save_output(output, output_dir / f"chapter_{output.chapter_title.lower().replace(' ', '_')}.json")
    print(f"Saved to {output_dir}")
    
    await engine.close()


if __name__ == "__main__":
    asyncio.run(main())