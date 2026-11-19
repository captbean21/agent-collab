#!/usr/bin/env bash
# =====================================================================
# SSH Reverse Tunnel Setup — HPE NAS → T340 (Boundary Pipe)
# Run THIS SCRIPT on the HPE NAS (192.168.1.199) as the castle user.
# =====================================================================
# Creates persistent reverse tunnels from HPE to T340:
#   - Qdrant:      HPE localhost:6333  → T340 localhost:6333
#   - Survival:    HPE localhost:8080  → T340 localhost:8080
#   - SearXNG:     HPE localhost:8888  → T340 localhost:8888
# =====================================================================

set -euo pipefail

T340_HOST="192.168.1.201"      # Rook's T340 container IP
T340_USER="rook"                # SSH user on T340
SSH_KEY="$HOME/.ssh/id_ed25519_castle_to_rook"  # Dedicated key (generate if needed)

# Tunnel mappings: LOCAL_PORT:REMOTE_HOST:REMOTE_PORT
TUNNELS=(
    "6333:localhost:6333"      # Qdrant
    "8080:localhost:8080"      # Survival backend API
    "8888:localhost:8888"      # SearXNG
)

AUTOSsh_PID_FILE="/tmp/castle_rook_tunnels.pid"
LOG_FILE="/tmp/castle_rook_tunnels.log"

log() { echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "$LOG_FILE"; }

# Check prerequisites
check_prereqs() {
    if ! command -v autossh &>/dev/null; then
        log "Installing autossh..."
        sudo apt-get update && sudo apt-get install -y autossh
    fi
    
    if [[ ! -f "$SSH_KEY" ]]; then
        log "Generating dedicated SSH key for Castle→Rook tunnel..."
        ssh-keygen -t ed25519 -f "$SSH_KEY" -N "" -C "castle-rook-boundary-pipe"
        log "Public key (add to T340 ~/.ssh/authorized_keys):"
        cat "${SSH_KEY}.pub"
        return 1
    fi
    return 0
}

# Build autossh command
build_autossh_cmd() {
    local local_port="$1"
    local remote_port="$2"
    
    autossh -M 0 \
        -o "ServerAliveInterval=30" \
        -o "ServerAliveCountMax=3" \
        -o "ExitOnForwardFailure=yes" \
        -o "StrictHostKeyChecking=accept-new" \
        -o "UserKnownHostsFile=$HOME/.ssh/known_hosts" \
        -i "$SSH_KEY" \
        -N -R "${local_port}:${remote_host}:${remote_port}" \
        "${T340_USER}@${T340_HOST}"
}

# Start all tunnels
start_tunnels() {
    log "Starting reverse tunnels to T340 ($T340_HOST)..."
    
    # Kill any existing autossh processes for these tunnels
    pkill -f "autossh.*${T340_USER}@${T340_HOST}" 2>/dev/null || true
    sleep 1
    
    for tunnel in "${TUNNELS[@]}"; do
        IFS=':' read -r local_port remote_host remote_port <<< "$tunnel"
        
        log "Starting tunnel: HPE localhost:$local_port → T340 $remote_host:$remote_port"
        
        autossh -M 0 \
            -o "ServerAliveInterval=30" \
            -o "ServerAliveCountMax=3" \
            -o "ExitOnForwardFailure=yes" \
            -o "StrictHostKeyChecking=accept-new" \
            -o "UserKnownHostsFile=$HOME/.ssh/known_hosts" \
            -i "$SSH_KEY" \
            -N -R "${local_port}:${remote_host}:${remote_port}" \
            "${T340_USER}@${T340_HOST}" >> "$LOG_FILE" 2>&1 &
        
        echo $! >> "$AUTOSsh_PID_FILE"
        sleep 1
    done
    
    log "All tunnels started. PIDs saved to $AUTOSsh_PID_FILE"
    log "Log file: $LOG_FILE"
}

# Stop all tunnels
stop_tunnels() {
    log "Stopping tunnels..."
    if [[ -f "$AUTOSsh_PID_FILE" ]]; then
        while read -r pid; do
            kill "$pid" 2>/dev/null && log "Stopped PID $pid"
        done < "$AUTOSsh_PID_FILE"
        rm -f "$AUTOSsh_PID_FILE"
    fi
    pkill -f "autossh.*${T340_USER}@${T340_HOST}" 2>/dev/null || true
    log "All tunnels stopped."
}

# Check tunnel status
check_tunnels() {
    log "Checking tunnel status..."
    for tunnel in "${TUNNELS[@]}"; do
        IFS=':' read -r local_port remote_host remote_port <<< "$tunnel"
        if timeout 3 nc -zv localhost "$local_port" 2>&1 | grep -q "succeeded"; then
            log "✓ Tunnel localhost:$local_port → T340 $remote_host:$remote_port: CONNECTED"
        else
            log "✗ Tunnel localhost:$local_port → T340 $remote_host:$remote_port: FAILED"
        fi
    done
}

# Main
case "${1:-start}" in
    start)
        check_prereqs || { log "Add the public key above to T340's ~/.ssh/authorized_keys and re-run"; exit 1; }
        start_tunnels
        sleep 3
        check_tunnels
        ;;
    stop)
        stop_tunnels
        ;;
    restart)
        stop_tunnels
        sleep 2
        start_tunnels
        sleep 3
        check_tunnels
        ;;
    status)
        check_tunnels
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac