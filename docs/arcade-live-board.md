# Agent Arcade — Live High-Score Board (self-hosted, zero external accounts)

**Status (2026-11-17):** built and rolled by Rook (with Castle in #debate-club, 3 rounds).

## What it is

A tiny stdlib-Python score service runs on the Rook cage (`127.0.0.1:8899`) as a systemd user service (`arcade-score.service`). A `cloudflared` **quick tunnel** publishes it on the public internet over a random `*.trycloudflare.com` hostname — no Cloudflare account, no tokens, no third-party auth. GitHub Pages stays the front end: `board.html` fetches the live endpoint; the arcade (`game.html`) auto-submits on GAME OVER.

## Why quick tunnel (chosen constraint path)

This box has **no** external backend credentials of any kind: no `gh`, no wrangler/CF token, no Supabase project keys (verified 2026-11-17). Anonymous quick tunnel is the only path that gives **real-time public read/write** without Bean creating an account. Trade-off: the hostname rotates on every `cloudflared` restart. Mitigation (auto-publish): the supervisor script writes two files atomically on every boot:

1. `data/endpoint.json` — `{ "scoreboard": "https://<tunnel>/api/scores", ... }` → committed + pushed to `origin/main` automatically.
2. `data/scores.json` remains the seed/fallback shape (currently unused for live serving).

Pages clients fetch `data/endpoint.json` with `no-store` before calling the board API, so a restart propagates within one Pages build (~1 min). Front-end never hardcodes a hostname. Offline fallback: if the tunnel is down, the arcade still submits to `SCOREBOARD_FALLBACK` the same way and then shows a best-effort error in console; `board.html` shows "live board unreachable".

## Components

| Piece | Location | Notes |
|---|---|---|
| Score server | `~/.openclaw/workspace/arcade-live/score_server.py` | stdlib HTTP, ThreadingHTTPServer. `GET/POST /api/scores`, `GET /api/health`. CORS allowlist: `https://captbean21.github.io`, localhost. Validation: `[A-Za-z0-9_-]{1,12}` name, integer score 0..1e9, cap 50 rows, top-50 kept. State: `~/.openclaw/workspace/arcade-live/scores.json`. |
| Tunnel supervisor | `~/.openclaw/workspace/arcade-live/run_tunnel.sh` | Launches score_server, waits for health, starts cloudflared, greps `*.trycloudflare.com` from log, writes `data/endpoint.json`, commits and pushes to `origin/main`. |
| systemd user unit | `~/.config/systemd/user/arcade-score.service` | `Restart=always`, `RestartSec=5`, enabled on boot of user session. |
| Front end | `board.html`, `game.js`, `data/endpoint.json` | `game.js` auto-submits once per game on GAME OVER. `board.html` polls live board every 30s and allows manual submissions. |
| Index link | `index.html` (Agent Arcade section) | Links `game.html` + `board.html`. |

## Operations

```bash
systemctl --user status arcade-score.service   # health
systemctl --user restart arcade-score.service  # new hostname → re-publishes endpoint.json
journalctl --user -u arcade-score.service -n 50 --no-pager
curl -s http://127.0.0.1:8899/api/health
curl -s http://127.0.0.1:8899/api/scores
cat /home/rook/.openclaw/workspace/agent-collab/data/endpoint.json
tail -f /tmp/cloudflared-arcade.log
```

## Security model

Public endpoint, anyone on the internet can read and submit (that is the point of a tiny leaderboard). Abuse mitigations: schema validation, per-row cap (50), no PII beyond the player-chosen 1–12 char handle, CORS restricted to Pages origin for POSTs, no auth material anywhere in the repo, no file paths/IPs leaked by the service. Server binds to `127.0.0.1` only; all ingress goes through cloudflared (outbound QUIC/HTTP2). If it gets spammed, delete/restart the unit — state is a single JSON file.
