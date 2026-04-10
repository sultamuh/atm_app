# Phase 6 Integration Scripts

This folder provides the two required Unix shell scripts for Phase 6:

- `daily.sh`
- `weekly.sh`

It also includes a small converter script used by `daily.sh`:

- `convert_frontend_transactions.awk`

## Daily Script

Run one business day of operation by:

1. Executing multiple frontend sessions from input files.
2. Saving each session transaction output separately.
3. Concatenating all session outputs into one merged transaction file.
4. Converting merged frontend transaction lines into backend input commands.
5. Running backend processing.

Usage:

```bash
bash phase6/daily.sh <day_id> <current_accounts_file> <session_input_1> [session_input_2 ...]
```

Example:

```bash
bash phase6/daily.sh day1 Backend/old_accounts.txt phase6/sessions/day1/session1.txt phase6/sessions/day1/session2.txt
```

## Weekly Script

Run seven consecutive days using day-specific session sets. The previous day's
output accounts file is used as the next day's input accounts file.

Expected directory structure:

```text
phase6/sessions/week1/
  day1/*.txt
  day2/*.txt
  day3/*.txt
  day4/*.txt
  day5/*.txt
  day6/*.txt
  day7/*.txt
```

Usage:

```bash
bash phase6/weekly.sh <week_id> <day_sessions_root> <initial_current_accounts>
```

Example:

```bash
bash phase6/weekly.sh week1 phase6/sessions/week1 Backend/old_accounts.txt
```

## Output Layout

`daily.sh` writes outputs under:

```text
phase6/outputs/<day_id>/
  session_terminal/
  session_transactions/
  merged_frontend_transactions.txt
  merged_backend_transactions.txt
  new_accounts.txt
```

`weekly.sh` writes week-level snapshots under:

```text
phase6/outputs/<week_id>/
  day1_new_accounts.txt
  ...
  day7_new_accounts.txt
  final_new_accounts.txt
```