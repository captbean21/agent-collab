#!/usr/bin/env bash
# =====================================================================
# Castle Sync — Periodic sync from Castle (HPE) to Rook (T340)
# Runs on HPE NAS via cron. Uses SSH reverse tunnels established by
# setup_reverse_tunnel.sh to push/pull Qdrant vectors and git repo.
# =====================================================================

set -euo pipefail

# Configuration
REPO_ROOT="/home/castle/agent-collab"          # Castle's local agent-collab clone
QDRANT_LOCAL="http://localhost:6333"           # Via reverse tunnel
SURVIVAL_LOCAL="http://localhost:8080/api"     # Via reverse tunnel
GIT_REMOTE="origin"
SYNC_LOG="/tmp/castle_sync.log"

log() { echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "$SYNC_LOG"; }

# Check tunnels are up
check_tunnels() {
    for port in 6333 8080 8888; do
        if ! timeout 3 nc -zv localhost "$port" 2>&1 | grep -q "succeeded"; then
            log "ERROR: Tunnel on port $port is down"
            return 1
        fi
    done
    log "All tunnels verified"
    return 0
}

# Git sync: pull latest, push any local commits
git_sync() {
    log "Syncing git repo..."
    cd "$REPO_ROOT" || { log "ERROR: Repo not found at $REPO_ROOT"; return 1; }
    
    # Pull with rebase
    if git pull --rebase "$GIT_REMOTE" main >> "$SYNC_LOG" 2>&1; then
        log "Git pull OK"
    else
        log "Git pull failed (may be clean)"
    fi
    
    # Push if we have local commits
    if git log --oneline "@{u}..HEAD" 2>/dev/null | grep -q .; then
        if git push "$GIT_REMOTE" main >> "$SYNC_LOG" 2>&1; then
            log "Git push OK"
        else
            log "Git push failed"
            return 1
        fi
    else
        log "No local commits to push"
    fi
}

# Qdrant vector sync: push local vectors, pull remote vectors
qdrant_sync() {
    log "Syncing Qdrant vectors..."
    
    # For now: just verify connection and count points
    local count=$(curl -sf "$QDRANT_LOCAL/collections/memory_bus" 2>/dev/null | \
        python3 -c "import sys,json; print(json.load(sys.stdin)['result']['points_count'])" 2>/dev/null)
    
    if [[ -n "$count" ]]; then
        log "Qdrant memory_bus: $count points (connected via tunnel)"
    else
        log "WARNING: Could not query Qdrant via tunnel"
        return 1
    fi
    
    # TODO: Implement actual vector push/pull logic here
    # - Pull new vectors from Rook's Qdrant
    # - Push Castle's new vectors to Rook's Qdrant
    # - Use collection 'memory_bus' as shared space
}

# Survival backend health check
survival_check() {
    local health=$(curl -sf "$SURVIVAL_LOCAL/health" 2>/dev/null)
    if [[ "$health" == *"ok"* ]]; then
        log "Survival backend: HEALTHY"
    else
        log "WARNING: Survival backend unreachable"
        return 1
    fi
}

# Main
main() {
    log "=== Castle Sync Started ==="
    
    if ! check_tunnels; then
        log "Tunnel check failed, attempting restart..."
        /home/castle/tools/setup_reverse_tunnel.sh restart
        sleep 5
        if ! check_tunnels; then
            log "ERROR: Tunnels still down after restart"
            exit 1
        fi
    fi
    
    git_sync
    qdrant_sync
    survival_check
    
    log "=== Castle Sync Complete ==="
}

main "$@"