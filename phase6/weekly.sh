#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DAILY_SCRIPT="$SCRIPT_DIR/daily.sh"

usage() {
    cat <<'EOF'
Usage:
  bash phase6/weekly.sh <week_id> <day_sessions_root> <initial_current_accounts>

Expected day_sessions_root layout:
  <day_sessions_root>/day1/*.txt
  <day_sessions_root>/day2/*.txt
  ...
  <day_sessions_root>/day7/*.txt

Example:
  bash phase6/weekly.sh week1 phase6/sessions/week1 Backend/old_accounts.txt

What it does:
  - Runs daily.sh for 7 days.
  - Uses each day's output account file as the next day's input.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ "$#" -ne 3 ]]; then
    usage
    exit 1
fi

WEEK_ID="$1"
DAY_SESSIONS_ROOT="$2"
INITIAL_CURRENT_ACCOUNTS="$3"

if [[ ! -x "$DAILY_SCRIPT" ]]; then
    echo "ERROR: daily.sh is missing or not executable: $DAILY_SCRIPT" >&2
    exit 1
fi

if [[ ! -d "$DAY_SESSIONS_ROOT" ]]; then
    echo "ERROR: Day sessions root not found: $DAY_SESSIONS_ROOT" >&2
    exit 1
fi

if [[ ! -f "$INITIAL_CURRENT_ACCOUNTS" ]]; then
    echo "ERROR: Initial current accounts file not found: $INITIAL_CURRENT_ACCOUNTS" >&2
    exit 1
fi

WEEK_OUT_DIR="$SCRIPT_DIR/outputs/$WEEK_ID"
mkdir -p "$WEEK_OUT_DIR"

current_accounts="$INITIAL_CURRENT_ACCOUNTS"

for day in 1 2 3 4 5 6 7; do
    day_dir="$DAY_SESSIONS_ROOT/day$day"
    if [[ ! -d "$day_dir" ]]; then
        echo "ERROR: Missing directory for day$day: $day_dir" >&2
        exit 1
    fi

    day_sessions=()
    while IFS= read -r session_path; do
        day_sessions+=("$session_path")
    done < <(find "$day_dir" -maxdepth 1 -type f -name '*.txt' | sort)
    if [[ "${#day_sessions[@]}" -eq 0 ]]; then
        echo "ERROR: No session input files for day$day in $day_dir" >&2
        exit 1
    fi

    day_id="${WEEK_ID}_day${day}"
    echo "[weekly:$WEEK_ID] Running $day_id"

    bash "$DAILY_SCRIPT" "$day_id" "$current_accounts" "${day_sessions[@]}"

    current_accounts="$SCRIPT_DIR/outputs/$day_id/new_accounts.txt"
    cp "$current_accounts" "$WEEK_OUT_DIR/day${day}_new_accounts.txt"
done

cp "$current_accounts" "$WEEK_OUT_DIR/final_new_accounts.txt"

echo "[weekly:$WEEK_ID] Complete"
echo "  Final output: $WEEK_OUT_DIR/final_new_accounts.txt"