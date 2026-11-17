# Joint Research: Mini Self-Hosted Space (not trycloudflare)

**Date:** 2026-11-17 · **Participants:** Rook, Castle · **Judged/reviewed by:** FrancisCuée (audit standard), Bean (constraint owner)
**Bean's ask:** find a mini self-hosted space/server not reliant on trycloudflare-style dynamic tunnels; research only, parked as joint research; minimal Bean input preferred.

## Context

`agent-collab` ships a live high-score board (`board.html`) whose backing service runs on Rook's cage behind an anonymous Cloudflare quick tunnel. It works but Bean called it: done many times before, temporary by contract (no uptime SLA, hostname rotates, public URL reachable by anyone, ~200 in-flight request ceiling, no SSE). FrancisCuée's audit stands as the gate for calling anything "deployed": server source must live in the public tree, atomic writes + body limits + rate limiting, CORS ≠ auth, bounded score-sync to git, true static fallback (not last-tunnel URL), name validation in game.js, and lock + bounded fetch/rebase/push retries in the supervisor.

## Ground truth measured on Rook's cage (2026-11-17)

- No global IPv6 (link-local only); external `curl -6` probes fail.
- NAT IPv4: 192.168.1.201 behind 192.168.1.1; public egress 121.200.4.35.
- No cloud credentials of any kind on the box (no gh, wrangler/CF token, Supabase keys, Tailscale auth). Only GitHub identity = git deploy key on `agent-collab`.
- Inbound reachability impossible without router access; Bean cannot touch the router.
- Anonymous JSON-storage services (kvdb.io) now require an email login link; bucket creation returns 422 without one. Not viable anonymously.
- Local ports free ≥ 8899; 8899 currently serves the spike score_server.
- Existing outbound: HTTPS to api.cloudflare.com OK; GitHub SSH OK.

## Candidate matrix

| Option | Bean input | Inbound exposure | Stable name | Ops burden | Verdict |
|---|---|---|---|---|---|
| trycloudflare quick tunnel | none | open via URL | **no** (rotates, no SLA) | low | **Rejected** for production; fine as demo/spike only |
| GitHub-as-DB (Actions + repo JSON) | none | n/a (no public server) | n/a | low | **Fallback**: true zero-input path; eventual consistency only |
| Router port-forward + Caddy + DuckDNS | **router access required** | open port | yes | medium | **Rejected** (Bean: cannot touch router) |
| Tailscale Funnel | **1 tailscale auth click** | none (Funnel-mediated HTTPS) | yes (*.ts.net) | low | **Recommended** |
| Named Cloudflare Tunnel | CF account + token | none | yes | low-medium | Sound, Bean decision, Francis already flagged SLA/ops trade-offs |
| ngrok free static domain | authtoken | open via URL | yes | low | Weak free tier (bandwidth/session caps); third choice |
| Free VPS (Oracle Always Free ARM) | account + verification | open port | yes (static IP) | **high** (TLS, updates, fail2ban, SSH hardening) | Not minimal-Bean; price before recommending |
| VPS + Nginx + SQLite | account/$5/mo | open port | yes | high | Honest but overkill; Castle's proposal, still good for full ownership |

## Findings

1. **Zero-Bean public persistent server is impossible from this cage.** Without router access (ruled out), global IPv6 (absent), or an outbound-mediated tunnel (account-gated), there is no third path. Any claim otherwise is marketing, not measurement.
2. **Tailscale Funnel is the minimal real option:** one `tailscale up` click by Bean, stable `*.ts.net` HTTPS name, no inbound ports opened, no router change, restart-resilient, ops close to the quick-tunnel spike we already proved works. Falls back naturally: swap `data/endpoint.json` contents; frontend unchanged.
3. **GitHub-as-DB remains the zero-input fallback:** issue-intake Action (already sketched in `update-metrics.yml` pattern) or `workflow_dispatch` sync. Not real-time, but auditable, durable, zero accounts, and rides existing Pages + SSH key.
4. **Named CF Tunnel** is the best security posture (edge WAF, access policies) if Bean prefers Cloudflare over Tailscale; Francis's prior SLA/terms points apply to named tunnels too, not just quick ones.
5. **VPS is the "real server" answer** only when Bean wants ownership and is willing to carry the ops blast radius; free tier is a capacity lottery (Oracle ARM, AArch64 constraints) and ToS risk if idle.

## Joint recommendation (parked, pending Bean)

1. Park as joint research; no live migration until Bean picks a path.
2. If Bean clicks once: **Tailscale Funnel**; if not: **GitHub-as-DB fallback**; if Bean wants max security: named CF Tunnel.
3. Whichever path is chosen, first action is finishing FrancisCuée's audit list on the spike (sanitise + commit `score_server.py`, rate-limit + body cap, static `data/scores.json` fallback, `game.js` name regex, score-sync job, atomic pushes with rebase retry) — a stable name on an insecure service is worse than a rotating one.

## Not claiming

No Bean-account object exists; no live Funnel/named tunnel/VPS was provisioned; router SSH/HTTP port-forward untested and unavailable; IPv6 inbound unproven by design (no global v6 address).
