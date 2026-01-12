#!/usr/bin/env bash

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/validate.log"
CONFIG_FILE="config.json"
SRC_DIR="src"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

error_exit() {
  log "ERROR: $1"
  echo "$1"
  exit 1
}

log "Validation started"


if [ ! -d "$SRC_DIR" ]; then
  error_exit "src/ directory does not exist"
else
  log "src/ directory exists"
fi


if [ ! -f "$CONFIG_FILE" ]; then
  error_exit "config.json not found"
fi


if ! jq empty "$CONFIG_FILE" >/dev/null 2>&1; then
  error_exit "config.json is invalid JSON"
else
  log "config.json is valid"
fi

log "Validation completed successfully"
echo "Validation passed"
exit 0

