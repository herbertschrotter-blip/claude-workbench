#!/bin/sh
# Eigenes Fenster „Tickets“ (tmux-Sitzung „{{slug}}“) im Claude Terminal: Claude Code im Projekt {{slug}} für Tickets
# aus dem Melden-Knopf. Legt das Fenster beim ersten Aufruf an (Claude-Sitzung „{{slug}}-tickets“, bleibt offen, solange
# das Add-on läuft) und wechselt sonst nur dorthin. Aufruf im Projekt: sh tools/tickets-fenster.sh
set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
SITZUNG=${TMUX_SITZUNG:-{{slug}}}
FENSTER=Tickets

if ! tmux has-session -t "$SITZUNG" 2>/dev/null; then
  tmux new-session -d -s "$SITZUNG" -c "$REPO"
fi
if ! tmux list-windows -t "$SITZUNG" -F '#{window_name}' | grep -qx "$FENSTER"; then
  tmux new-window -t "$SITZUNG" -n "$FENSTER" -c "$REPO" "claude -n {{slug}}-tickets"
fi
if [ -n "${TMUX:-}" ]; then
  tmux switch-client -t "$SITZUNG:$FENSTER"  # auch aus einer anderen Sitzung heraus
else
  tmux attach -t "$SITZUNG:$FENSTER"
fi
