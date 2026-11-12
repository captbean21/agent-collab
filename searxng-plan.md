# SearXNG Deployment Plan — Proofed & Ready

**Status:** Awaiting Bean's go (pin verification first, then agent registration)
**Proofed by:** FrancisCuée (2026-10-28 04:19 UTC) + Rook (2026-10-28 05:09 UTC)
**Discord refs:** #rook channel, messages 1564855997 (Francis draft) → 1564868749406900326 (Rook proof)

---

## Plan Summary

| Step | Action | Status |
|------|--------|--------|
| 0 | **Reachability check** — `nc -zv <container-ip> 8888` from gateway host | Pending (Bean) |
| 1 | **Install deps** — `sudo apt install python3-venv python3-pip redis-server uwsgi uwsgi-plugin-python3` | Ready |
| 2 | **Create venv + install** — `/opt/searxng` venv, `pip install searxng` | Ready |
| 3 | **Config** — `settings.yml` at `/opt/searxng/searxng/settings.yml`, bind `0.0.0.0:8888`, `SEARXNG_BASE_URL=http://<container-eth0-ip>:8888` | Ready |
| 4 | **systemd/uwsgi** — service files at `/etc/uwsgi/apps-available/searxng.ini`, enable + start | Ready |
| 5 | **Firewall** — ufw/iptables restrict port 8888 to gateway host IP only | Ready |
| 6 | **Verify** — `curl http://<container-ip>:8888` from gateway | Ready |
| 7 | **Rollback** — documented clean removal | Ready |

---

## Critical Notes (from proofing)

- **Bind address:** `0.0.0.0:8888` inside container (not `127.0.0.1`) — LXD proxy/routing won't hit container loopback. Restrict via ufw/iptables to gateway host IP.
- **Base URL:** `SEARXNG_BASE_URL=http://<container-eth0-ip>:8888` — get container IP via `lxc config get <container> volatile.eth0.hwaddr` / `ip -4 addr show eth0`.
- **RAM:** 150–300 MB (uwsgi workers + Redis) — 15.3 GB free, no issue.
- **Security:** HTTP on container LAN only. No public exposure.
- **Rollback:** `systemctl stop searxng && systemctl disable searxng && rm -rf /opt/searxng /etc/uwsgi/apps-available/searxng.ini /etc/uwsgi/apps-enabled/searxng.ini && sudo apt purge --auto-remove python3-venv python3-pip redis-server uwsgi uwsgi-plugin-python3`

---

## Execution Dependencies (Bean's side)

1. **Pin verification** (30s) — confirm gateway pin matches model window: `openclaw config get pin` / `openclaw status`. If pin is wrong, compaction breaks everything.
2. **Agent registration** — register `rook` on gateway so Francis can `sessions_send` directly (cross-gateway mention-ping is fallback).

---

## Next Steps

1. Bean runs pin verification
2. Bean runs reachability check (step 0)
3. Bean executes steps 1–6
4. Francis registers Rook agent on gateway
5. Rook builds search skill against `http://<container-ip>:8888/search`

---

## Extra Engines Patch (for broader research coverage)

Add to the `engines:` list in `settings.yml` template (step 3) before execution:

```yaml
engines:
  # Default engines (proven, reliable)
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
  - name: bing
    engine: bing
    shortcut: b
  - name: wikipedia
    engine: wikipedia
    shortcut: w
  - name: github
    engine: github
    shortcut: gh

  # Research-focused additions
  - name: huggingface
    engine: huggingface
    shortcut: hf
  - name: arxiv
    engine: arxiv
    shortcut: arxiv
  - name: reddit
    engine: reddit
    shortcut: rddt
  - name: searxng-news
    engine: searxng-news
    shortcut: news
  - name: scholar
    engine: scholar
    shortcut: gs

  # Niche / specialized
  - name: ahmia
    engine: ahmia
    shortcut: ahmia
  - name: piratebay
    engine: piratebay
    shortcut: tpb
  - name: wikidata
    engine: wikidata
    shortcut: wd
```

**Rationale:**
- **huggingface, arxiv, scholar** — direct research paper/model search
- **reddit** — community discussions, real-world feedback
- **searxng-news** — recent articles, breaking changes
- **ahmia** — tor hidden services (if needed for obscure tech)
- **wikidata** — structured knowledge graph queries

**Note:** Each engine adds ~1-2s latency per search. Start with the 8 engines above (4 default + 4 research). Add niche ones only if needed.

---

**Workspace anchor:** This file lives at `/home/rook/.openclaw/workspace/searxng-plan.md` — survives context resets. Read it in any new session.