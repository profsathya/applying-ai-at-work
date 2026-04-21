#!/bin/bash
# ralph.sh - autonomous course build loop
#
# Runs claude code with the Ralph prompt repeatedly until the course is
# fully built in canvas (emits COURSE_COMPLETE) or a HALT condition fires.
#
# Usage:
#   ./ralph.sh                    # normal run
#   MAX_ITERATIONS=50 ./ralph.sh  # override iteration cap
#   ./ralph.sh --verbose          # tail iteration output live

set -euo pipefail

MAX_ITERATIONS="${MAX_ITERATIONS:-100}"
COMPLETION_SIGIL="COURSE_COMPLETE"
HALT_SIGIL="HALT:"
PROMPT_FILE="prompts/ralph-prompt.md"
LOG_DIR=".ralph"
LOG_FILE="$LOG_DIR/log.txt"
VERBOSE=0

for arg in "$@"; do
  case "$arg" in
    --verbose) VERBOSE=1 ;;
    --help)
      echo "Usage: ./ralph.sh [--verbose]"
      echo "  MAX_ITERATIONS env var caps iteration count (default 100)"
      echo "  TARGET_COURSE env var selects course1 or course2 (default from .env)"
      exit 0
      ;;
  esac
done

# Load .env so TARGET_COURSE and canvas creds are available to claude
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Expose target course to claude via an extra instruction line prepended to the prompt
TARGET_COURSE="${TARGET_COURSE:-course1}"

# Sanity checks
if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: $PROMPT_FILE not found. Run this from the repo root."
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "ERROR: .env not found. Copy .env.example and fill in your canvas credentials."
  exit 1
fi

if ! command -v claude &> /dev/null; then
  echo "ERROR: claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
  exit 1
fi

mkdir -p "$LOG_DIR"
echo "=== Ralph loop started $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

iteration=0
overload_retries=0
while [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
  iteration=$((iteration + 1))
  echo ""
  echo "=== Iteration $iteration/$MAX_ITERATIONS ==="
  echo "--- iteration $iteration $(date '+%H:%M:%S') ---" >> "$LOG_FILE"

  if [ "$VERBOSE" -eq 1 ]; then
    output=$(claude -p "TARGET COURSE: $TARGET_COURSE

$(cat $PROMPT_FILE)" --permission-mode bypassPermissions 2>&1 | tee -a "$LOG_FILE")
  else
    output=$(claude -p "TARGET COURSE: $TARGET_COURSE

$(cat $PROMPT_FILE)" --permission-mode bypassPermissions 2>&1)
    echo "$output" >> "$LOG_FILE"
    # Surface the last few lines so the operator sees progress
    echo "$output" | tail -5
  fi

  # Retry transient Anthropic API overloads without advancing the iteration counter.
  # Cap at 3 consecutive retries; after that, let the iteration count normally.
  if echo "$output" | grep -qE '"type":"overloaded_error"|"message":"Overloaded"'; then
    overload_retries=$((overload_retries + 1))
    if [ "$overload_retries" -le 3 ]; then
      echo "API overloaded (retry $overload_retries/3). Sleeping 30s and retrying iteration $iteration."
      echo "--- overload retry $overload_retries for iteration $iteration ---" >> "$LOG_FILE"
      iteration=$((iteration - 1))
      sleep 30
      continue
    fi
    echo "API overloaded after 3 retries; proceeding normally."
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
    halt_msg=$(echo "$output" | grep -oP '(?<=<promise>HALT: )[^<]+' | head -1)
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
