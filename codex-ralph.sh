#!/bin/bash
# codex-ralph.sh - Codex-backed autonomous course build loop
#
# Codex replacement for the legacy Ralph loop. It keeps the same file-backed
# PLAN/BUILD/VERIFY contract and sigils, and calls Codex non-interactively.
#
# Usage:
#   ./codex-ralph.sh
#   TARGET_COURSE=course2 ./codex-ralph.sh --verbose
#   CODEX_RALPH_ARGS="--full-auto" ./codex-ralph.sh
#
# Do not use dangerous approval bypass modes against production Canvas courses
# until the Codex pilot has passed on a sandbox course.

set -euo pipefail

MAX_ITERATIONS="${MAX_ITERATIONS:-100}"
COMPLETION_SIGIL="COURSE_COMPLETE"
HALT_SIGIL="HALT:"
PROMPT_FILE="prompts/codex/ralph-prompt.md"
LOG_DIR=".ralph"
LOG_FILE="$LOG_DIR/codex-log.txt"
VERBOSE=0

# Conservative default: full-auto is intended for unattended local execution,
# but still keeps Codex's sandbox/approval model in play. Override with
# CODEX_RALPH_ARGS only after reviewing Codex permissions for this repo.
CODEX_RALPH_ARGS="${CODEX_RALPH_ARGS:---full-auto}"

for arg in "$@"; do
  case "$arg" in
    --verbose) VERBOSE=1 ;;
    --help)
      echo "Usage: ./codex-ralph.sh [--verbose]"
      echo "  MAX_ITERATIONS env var caps iteration count (default 100)"
      echo "  TARGET_COURSE env var selects course1 or course2 (default from .env)"
      echo "  CODEX_RALPH_ARGS overrides Codex exec args (default: --full-auto)"
      exit 0
      ;;
  esac
done

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

TARGET_COURSE="${TARGET_COURSE:-course1}"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: $PROMPT_FILE not found. Run this from the repo root."
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "ERROR: .env not found. Copy .env.example and fill in your Canvas credentials."
  exit 1
fi

if ! command -v codex &> /dev/null; then
  echo "ERROR: codex CLI not found. Install with: npm i -g @openai/codex"
  exit 1
fi

mkdir -p "$LOG_DIR"
echo "=== Codex Ralph loop started $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

iteration=0
overload_retries=0
while [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
  iteration=$((iteration + 1))
  echo ""
  echo "=== Iteration $iteration/$MAX_ITERATIONS ==="
  echo "--- iteration $iteration $(date '+%H:%M:%S') ---" >> "$LOG_FILE"

  prompt="TARGET COURSE: $TARGET_COURSE

$(cat "$PROMPT_FILE")"

  if [ "$VERBOSE" -eq 1 ]; then
    output=$(codex exec $CODEX_RALPH_ARGS "$prompt" 2>&1 | tee -a "$LOG_FILE")
  else
    output=$(codex exec $CODEX_RALPH_ARGS "$prompt" 2>&1)
    echo "$output" >> "$LOG_FILE"
    echo "$output" | tail -5
  fi

  if echo "$output" | grep -qiE 'overloaded|rate.?limit|temporarily unavailable'; then
    overload_retries=$((overload_retries + 1))
    if [ "$overload_retries" -le 3 ]; then
      echo "Model service overloaded or rate-limited (retry $overload_retries/3). Sleeping 30s and retrying iteration $iteration."
      echo "--- overload retry $overload_retries for iteration $iteration ---" >> "$LOG_FILE"
      iteration=$((iteration - 1))
      sleep 30
      continue
    fi
    echo "Model service still unavailable after 3 retries; proceeding normally."
  fi
  overload_retries=0

  if echo "$output" | grep -q "<promise>$COMPLETION_SIGIL</promise>"; then
    echo ""
    echo "========================================"
    echo "  COURSE COMPLETE after $iteration iterations"
    echo "========================================"
    echo "See progress.md for the full build log."
    exit 0
  fi

  if echo "$output" | grep -q "<promise>$HALT_SIGIL"; then
    echo ""
    echo "========================================"
    echo "  HALTED after $iteration iterations"
    echo "========================================"
    halt_msg=$(echo "$output" | grep -oE '<promise>HALT: [^<]+' | sed 's/<promise>HALT: //' | head -1)
    echo "  $halt_msg"
    echo "See progress.md and $LOG_FILE for details."
    exit 1
  fi

  sleep 2
done

echo ""
echo "========================================"
echo "  MAX ITERATIONS ($MAX_ITERATIONS) REACHED"
echo "========================================"
echo "Course build did not complete. See progress.md and $LOG_FILE."
exit 2
