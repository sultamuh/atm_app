#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/Frontend"
BACKEND_DIR="$ROOT_DIR/Backend"
AWK_CONVERTER="$SCRIPT_DIR/convert_frontend_transactions.awk"

usage() {
    cat <<'EOF'
Usage:
  bash phase6/daily.sh <day_id> <current_accounts_file> <session_input_1> [session_input_2 ...]

Example:
  bash phase6/daily.sh day1 Backend/old_accounts.txt phase6/sessions/day1/session1.txt phase6/sessions/day1/session2.txt

What it does:
  1) Runs Frontend once per session input file.
  2) Extracts each session's transaction records into separate files.
  3) Concatenates them into one merged frontend transaction file.
  4) Converts merged frontend records into backend command format.
  5) Runs Backend with that merged transaction file.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ "$#" -lt 3 ]]; then
    usage
    exit 1
fi

DAY_ID="$1"
CURRENT_ACCOUNTS_INPUT="$2"
shift 2
SESSION_INPUTS=("$@")

to_abs_path() {
    local p="$1"
    echo "$(cd "$(dirname "$p")" && pwd)/$(basename "$p")"
}

if [[ ! -f "$AWK_CONVERTER" ]]; then
    echo "ERROR: Converter not found: $AWK_CONVERTER" >&2
    exit 1
fi

if [[ ! -f "$CURRENT_ACCOUNTS_INPUT" ]]; then
    echo "ERROR: Current accounts input file not found: $CURRENT_ACCOUNTS_INPUT" >&2
    exit 1
fi

CURRENT_ACCOUNTS_INPUT="$(to_abs_path "$CURRENT_ACCOUNTS_INPUT")"

ABS_SESSION_INPUTS=()
for session_file in "${SESSION_INPUTS[@]}"; do
    if [[ ! -f "$session_file" ]]; then
        echo "ERROR: Session input not found: $session_file" >&2
        exit 1
    fi
    ABS_SESSION_INPUTS+=("$(to_abs_path "$session_file")")
done

OUT_DAY_DIR="$SCRIPT_DIR/outputs/$DAY_ID"
SESSION_TXN_DIR="$OUT_DAY_DIR/session_transactions"
SESSION_TERMINAL_DIR="$OUT_DAY_DIR/session_terminal"
mkdir -p "$SESSION_TXN_DIR" "$SESSION_TERMINAL_DIR"

MERGED_FRONTEND_TXN="$OUT_DAY_DIR/merged_frontend_transactions.txt"
MERGED_BACKEND_TXN="$OUT_DAY_DIR/merged_backend_transactions.txt"
DAY_NEW_ACCOUNTS="$OUT_DAY_DIR/new_accounts.txt"

rm -f "$MERGED_FRONTEND_TXN" "$MERGED_BACKEND_TXN"

backend_old_accounts="$BACKEND_DIR/old_accounts.txt"
backend_transactions="$BACKEND_DIR/transactions.txt"
backend_new_accounts="$BACKEND_DIR/new_accounts.txt"

backup_old="$OUT_DAY_DIR/.backup_old_accounts.txt"
backup_txn="$OUT_DAY_DIR/.backup_transactions.txt"
backup_new="$OUT_DAY_DIR/.backup_new_accounts.txt"

if [[ -f "$backend_old_accounts" ]]; then
    cp "$backend_old_accounts" "$backup_old"
fi
if [[ -f "$backend_transactions" ]]; then
    cp "$backend_transactions" "$backup_txn"
fi
if [[ -f "$backend_new_accounts" ]]; then
    cp "$backend_new_accounts" "$backup_new"
fi

restore_backend_files() {
    if [[ -f "$backup_old" ]]; then
        cp "$backup_old" "$backend_old_accounts"
    else
        rm -f "$backend_old_accounts"
    fi

    if [[ -f "$backup_txn" ]]; then
        cp "$backup_txn" "$backend_transactions"
    else
        rm -f "$backend_transactions"
    fi

    if [[ -f "$backup_new" ]]; then
        cp "$backup_new" "$backend_new_accounts"
    else
        rm -f "$backend_new_accounts"
    fi
}

trap restore_backend_files EXIT

if [[ "$(cd "$(dirname "$CURRENT_ACCOUNTS_INPUT")" && pwd)/$(basename "$CURRENT_ACCOUNTS_INPUT")" != "$(cd "$(dirname "$backend_old_accounts")" && pwd)/$(basename "$backend_old_accounts")" ]]; then
    cp "$CURRENT_ACCOUNTS_INPUT" "$backend_old_accounts"
fi

echo "[daily:$DAY_ID] Running ${#ABS_SESSION_INPUTS[@]} frontend session(s)..."

session_index=1
for session_file in "${ABS_SESSION_INPUTS[@]}"; do
    terminal_out="$SESSION_TERMINAL_DIR/session_${session_index}.txt"
    txn_out="$SESSION_TXN_DIR/session_${session_index}.txt"

    (
        cd "$FRONTEND_DIR"
        python3 atm.py < "$session_file" > "$terminal_out" 2>&1
    )

    # Extract transaction lines that match frontend fixed record prefix "CC "
    # (e.g., "01 ...", "04 ...", "00 ...").
    awk '/^[0-9][0-9][[:space:]]/ {print $0}' "$terminal_out" > "$txn_out"
    cat "$txn_out" >> "$MERGED_FRONTEND_TXN"

    session_index=$((session_index + 1))
done

awk -f "$AWK_CONVERTER" "$MERGED_FRONTEND_TXN" > "$MERGED_BACKEND_TXN"
cp "$MERGED_BACKEND_TXN" "$backend_transactions"

echo "[daily:$DAY_ID] Running backend batch..."
(
    cd "$BACKEND_DIR"
    python3 main.py
)

cp "$backend_new_accounts" "$DAY_NEW_ACCOUNTS"

echo "[daily:$DAY_ID] Complete"
echo "  Merged frontend transactions: $MERGED_FRONTEND_TXN"
echo "  Merged backend transactions : $MERGED_BACKEND_TXN"
echo "  New accounts output         : $DAY_NEW_ACCOUNTS"