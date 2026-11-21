#!/usr/bin/env python3
"""
Integration module: Connects narrative engine to world-sim REST API.
Polls world state, generates narratives for events, maintains canon timeline.
"""

import asyncio
import httpx
import json
from pathlib import Path
from datetime import datetime
from narrative_engine import NarrativeEngine, NarrativeConfig, NarrativeOutput


class WorldSimClient:
    """Client for world-sim REST/WebSocket API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
        self.last_tick = 0
        self.last_event_count = 0
    
    async def get_state(self) -> dict:
        """Fetch current world state."""
        response = await self.client.get(f"{self.base_url}/api/state")
        response.raise_for_status()
        return response.json()
    
    async def get_events_since(self, tick: int) -> list:
        """Get events since a given tick (approximate via full state)."""
        state = await self.get_state()
        events = state.get("event_log", [])
        return [e for e in events if e.get("timestamp", {}).get("0", 0) > tick / 3600.0]  # Rough conversion
    
    async def close(self):
        await self.client.aclose()


class NarrativeIntegrator:
    """Orchestrates narrative generation from world simulation."""
    
    def __init__(self, world_sim_url: str = "http://localhost:8080", 
                 output_dir: str = "narrative_output"):
        self.world_sim = WorldSimClient(world_sim_url)
        self.engine = NarrativeEngine(NarrativeConfig())
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.event_log_path = self.output_dir / "event_narratives.jsonl"
        self.chapter_log_path = self.output_dir / "chapters.jsonl"
        self.running = False
    
    async def run_once(self) -> dict:
        """Single integration cycle: fetch state, generate narratives for new events."""
        state = await self.world_sim.get_state()
        current_tick = state.get("tick", 0)
        
        results = {
            "tick": current_tick,
            "new_events": [],
            "chapter": None,
        }
        
        # Check for new events
        events = state.get("event_log", [])
        new_events = events[self.last_event_count:]
        
        for event in new_events:
            # Generate narrative for significant events
            if event.get("severity") in ["Warning", "Critical", "Existential"]:
                narrative = await self.engine.generate_event_narrative(state, event)
                self._save_event_narrative(narrative, event)
                results["new_events"].append({
                    "event_type": event.get("event_type"),
                    "severity": event.get("severity"),
                    "narrative_title": narrative.chapter_title,
                })
        
        self.last_event_count = len(events)
        self.last_tick = current_tick
        
        # Check for chapter milestones
        if self._should_generate_chapter(state):
            chapter = await self._generate_milestone_chapter(state)
            if chapter:
                results["chapter"] = chapter.chapter_title
        
        return results
    
    def _should_generate_chapter(self, state: dict) -> bool:
        """Determine if a chapter milestone has been reached."""
        artifact = state.get("theorem_artifact", {})
        countdown = artifact.get("countdown_days", 8.0)
        storm = state.get("dust_storm", {})
        storm_phase = storm.get("phase", "Dormant")
        
        # Chapter triggers
        triggers = []
        
        # First injection milestone (countdown drops below 8 days)
        if countdown < 8.0 and countdown > 7.9:
            triggers.append("first_injection")
        
        # Storm protocols (storm active + countdown critical)
        if storm_phase == "Active" and countdown < 6.0:
            triggers.append("storm_protocols")
        
        # Contraction day / anchor critical
        if countdown < 1.0:
            triggers.append("contraction_day")
        
        # Post-storm expedition
        if storm_phase == "Settling" and countdown > 0.5:
            triggers.append("outside_bubble")
        
        if triggers:
            self._next_chapter_trigger = triggers[0]
            return True
        return False
    
    async def _generate_milestone_chapter(self, state: dict) -> NarrativeOutput:
        """Generate chapter for milestone."""
        trigger = getattr(self, '_next_chapter_trigger', "storm_protocols")
        chapter = await self.engine.generate_chapter(state, trigger)
        self._save_chapter(chapter)
        return chapter
    
    def _save_event_narrative(self, narrative: NarrativeOutput, event: dict):
        """Save event narrative to JSONL."""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "narrative": {
                "title": narrative.chapter_title,
                "pov": narrative.pov_character,
                "content": narrative.content,
                "word_count": narrative.word_count,
            }
        }
        with open(self.event_log_path, "a") as f:
            f.write(json.dumps(record) + "\n")
    
    def _save_chapter(self, chapter: NarrativeOutput):
        """Save chapter to JSONL."""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "chapter": {
                "title": chapter.chapter_title,
                "pov": chapter.pov_character,
                "content": chapter.content,
                "word_count": chapter.word_count,
                "world_state_ref": chapter.world_state_ref,
            }
        }
        with open(self.chapter_log_path, "a") as f:
            f.write(json.dumps(record) + "\n")
    
    async def run_continuous(self, interval: float = 5.0):
        """Run continuous integration loop."""
        self.running = True
        print(f"Starting narrative integrator (polling every {interval}s)...")
        
        while self.running:
            try:
                results = await self.run_once()
                if results["new_events"] or results["chapter"]:
                    print(f"Tick {results['tick']}: {len(results['new_events'])} event narratives"
                          f"{', chapter: ' + results['chapter'] if results['chapter'] else ''}")
            except Exception as e:
                print(f"Integration error: {e}")
            
            await asyncio.sleep(interval)
    
    def stop(self):
        self.running = False
    
    async def close(self):
        await self.world_sim.close()
        await self.engine.close()


async def main():
    """Demo: Run single integration cycle against local world-sim."""
    integrator = NarrativeIntegrator()
    
    try:
        print("Fetching world state...")
        results = await integrator.run_once()
        print(f"Results: {json.dumps(results, indent=2)}")
    finally:
        await integrator.close()


if __name__ == "__main__":
    asyncio.run(main())