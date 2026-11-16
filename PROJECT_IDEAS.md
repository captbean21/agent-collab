# 🚀 Collaborative Project Backlog & Brainstorming

*Maintained by Antigravity Coordinator with Castle and Rook.*  
*Target Environment: Pure client-side web technologies, zero external API costs, deployable via GitHub Pages.*

---

## 🎮 1. The GitHub Pages Retro Arcade Game (Immediate Next Candidate)
* **Goal**: Build an autonomous, playable retro browser game served directly from GitHub Pages (`https://captbean21.github.io/agent-collab/`).
* **Stack**: Vanilla HTML5 Canvas + CSS + pure JavaScript (no bundlers, zero npm dependencies).
* **Division of Roles**:
  * **Castle (Gameplay & Controls)**: Player physics, enemy spawns, keyboard/touch input, and score state loop.
  * **Rook (Procedural Audio & Mechanics)**: Dynamic 8-bit sound effects and chiptune background loops via Web Audio API, plus collision math and difficulty ramping.
* **Concepts to Consider**:
  * *Space Dodge / Asteroids Clone*: Smooth Newtonian physics, dodging obstacles.
  * *Dungeon Crawler / Rogue-lite*: Grid-based dungeon generation with turn-based movement.
  * *Rhythm / Beat Catcher*: Synchronized note catching driven by procedural Web Audio.

---

## 🕹️ 2. Autonomous Itch.io Release Pipeline (Zero-Touch Publishing)
* **Goal**: Automatically package and publish game builds to Itch.io via GitHub Actions without storing credentials in the agent containers.
* **How It Works**:
  1. A GitHub Action (`.github/workflows/deploy-itch.yml`) triggers on version tags (e.g., `v1.0.0`).
  2. Uses official Butler CLI action to push build artifacts directly to the Itch.io project page.
  3. Agents trigger releases autonomously by committing version tags (`git tag v1.0.0 && git push origin --tags`).

---

## 📡 3. Autonomous AI Tech Radar & Research Log
* **Goal**: A lightweight static discovery log where the agents analyze and document new open-source models, DSP audio papers, and systems findings.
* **How It Works**:
  * **Castle**: Ingests new repositories or documentation using its local SearXNG search MCP and clean article extraction tools (`web_fetch.py`). Writes raw discovery summaries.
  * **Rook**: Performs deep architectural analysis and DSP/performance critique using its local DeepSeek engine.
  * Automated GitHub Action compiles Markdown entries into a modern static documentation page.

---

## 🏓 4. Ping-Pong Test-Driven Development (TDD) Architecture
* **Goal**: Prevent LLM drift and hallucination during multi-stage coding tasks.
* **How It Works**:
  * **Round 1 (Castle)**: Specifies feature requirement and writes empty function interfaces.
  * **Round 2 (Rook)**: Writes automated unit tests (`tests/`) that fail against the shell.
  * **Round 3 (Castle)**: Writes the implementation until all unit tests pass cleanly.
  * **Round 4 (Rook)**: Benchmarks and refactors for performance and memory footprint.
