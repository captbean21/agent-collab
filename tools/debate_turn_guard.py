#!/usr/bin/env python3
"""
tools/debate_turn_guard.py — Anti-Ping-Pong Circuit Breaker
Tracks consecutive autonomous bot-to-bot turns between Rook and Castle in #debate-club.
Trips after 3 consecutive turns without human intervention to prevent 500 RPD quota drain.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

STATE_DIR = Path("/home/rook/.openclaw/workspace/.state")
STATE_FILE = STATE_DIR / "debate_turns.json"
MAX_CONSECUTIVE_BOT_TURNS = 3
RESET_TTL_SECONDS = 900  # 15 minutes idle resets counter

def load_state():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        return {"consecutive_bot_turns": 0, "last_updated": 0, "last_speaker": None}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if now - data.get("last_updated", 0) > RESET_TTL_SECONDS:
            return {"consecutive_bot_turns": 0, "last_updated": now, "last_speaker": None}
        return data
    except Exception:
        return {"consecutive_bot_turns": 0, "last_updated": 0, "last_speaker": None}

def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.datetime.now(datetime.timezone.utc).timestamp()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def check_or_record_turn(target_mention, is_human_reply=False):
    state = load_state()
    
    if is_human_reply:
        state["consecutive_bot_turns"] = 0
        state["last_speaker"] = "human"
        save_state(state)
        print("Human turn detected: Circuit breaker reset to 0 turns.")
        return 0, False
        
    current_count = state.get("consecutive_bot_turns", 0) + 1
    state["consecutive_bot_turns"] = current_count
    state["last_speaker"] = "bot"
    save_state(state)
    
    tripped = current_count >= MAX_CONSECUTIVE_BOT_TURNS
    
    if tripped:
        handoff_msg = (
            f"\n\n🛑 [Circuit Breaker Tripped]: Exchanged {current_count} consecutive turns with {target_mention}. "
            f"Halting autonomous ping-pong to protect daily free-tier quota. "
            f"Standing by for operator (@Bean) direction before proceeding."
        )
        print(f"TRIPPED: {handoff_msg}")
        return current_count, True
    else:
        print(f"OK: Turn {current_count}/{MAX_CONSECUTIVE_BOT_TURNS} with {target_mention}. Remaining autonomous turns: {MAX_CONSECUTIVE_BOT_TURNS - current_count}")
        return current_count, False

def main():
    parser = argparse.ArgumentParser(description="Anti-Ping-Pong Circuit Breaker")
    parser.add_argument("--target", default="@Rook", help="Peer mention to track (default: @Rook)")
    parser.add_argument("--human", action="store_true", help="Record that a human just spoke (resets counter)")
    parser.add_argument("--status", action="store_true", help="View current counter status without incrementing")
    args = parser.parse_args()
    
    if args.status:
        st = load_state()
        print(f"Current consecutive bot turns: {st.get('consecutive_bot_turns', 0)}/{MAX_CONSECUTIVE_BOT_TURNS} (Last speaker: {st.get('last_speaker')})")
        return
        
    check_or_record_turn(args.target, is_human_reply=args.human)

if __name__ == "__main__":
    main()
