#!/usr/bin/env bash
# =====================================================================
# Castle Cron Setup — Install periodic sync for Boundary Pipe
# Run on HPE NAS as castle user: ./castle_cron_setup.sh install
# =====================================================================

set -euo pipefail

CRON_JOBS=(
    # Every 15 minutes: sync git + Qdrat + health check
    "*/15 * * * * /home/castle/tools/castle_sync.sh >> /tmp/castle_sync_cron.log 2>&1"
    
    # Every hour: verify tunnels are up, restart if needed
    "0 * * * * /home/castle/tools/setup_reverse_tunnel.sh status >> /tmp/castle_tunnel_status.log 2>&1"
    
    # Daily at 3 AM: full Qdrant vector sync (when implemented)
    "0 3 * * * /home/castle/tools/castle_sync.sh full >> /tmp/castle_full_sync.log 2>&1"
)

SYSTEMD_TIMER="
[Unit]
Description=Castle-Rook Boundary Pipe Sync Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
"

install_cron() {
    echo "Installing cron jobs..."
    # Remove any existing castle sync jobs
    crontab -l 2>/dev/null | grep -v "castle_sync\|setup_reverse_tunnel" | crontab -
    
    # Add new jobs
    for job in "${CRON_JOBS[@]}"; do
        (crontab -l 2>/dev/null; echo "$job") | crontab -
        echo "Added: $job"
    done
    echo "Cron jobs installed."
    crontab -l | grep castle
}

install_systemd_timer() {
    echo "Installing systemd timer (alternative to cron)..."
    sudo tee /etc/systemd/system/castle-rook-sync.timer > /dev/null << 'TIMER_EOF'
[Unit]
Description=Castle-Rook Boundary Pipe Sync Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
TIMER_EOF

    sudo tee /etc/systemd/system/castle-rook-sync.service > /dev/null << 'SERVICE_EOF'
[Unit]
Description=Castle-Rook Boundary Pipe Sync
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=castle
WorkingDirectory=/home/castle
ExecStart=/home/castle/tools/castle_sync.sh
StandardOutput=journal
StandardError=journal
SERVICE_EOF

    sudo systemctl daemon-reload
    sudo systemctl enable --now castle-rook-sync.timer
    sudo systemctl enable castle-rook-tunnel.service
    echo "Systemd timer installed and started."
}

uninstall() {
    echo "Removing cron jobs..."
    crontab -l 2>/dev/null | grep -v "castle_sync\|setup_reverse_tunnel" | crontab -
    echo "Cron jobs removed."
    
    echo "Removing systemd timer..."
    sudo systemctl disable --now castle-rook-sync.timer 2>/dev/null || true
    sudo systemctl disable castle-rook-tunnel.service 2>/dev/null || true
    sudo rm -f /etc/systemd/system/castle-rook-sync.timer /etc/systemd/system/castle-rook-sync.service
    sudo systemctl daemon-reload
    echo "Systemd timer removed."
}

case "${1:-install}" in
    install)
        install_cron
        install_systemd_timer
        ;;
    cron-only)
        install_cron
        ;;
    systemd-only)
        install_systemd_timer
        ;;
    uninstall)
        uninstall
        ;;
    *)
        echo "Usage: $0 {install|cron-only|systemd-only|uninstall}"
        exit 1
        ;;
esac