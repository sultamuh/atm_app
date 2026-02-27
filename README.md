# ATM Application Project

This is a Python-based ATM application that simulates basic banking transactions such as login, withdrawals, deposits, transfers, bill payments, and account management. The application supports **STANDARD** and **ADMIN** session modes.

---

## Features

- **Login / Logout** with session modes
- **Withdrawal**, **Deposit**, **Transfer**, **Paybill**
- **Account management** (Create, Delete, Disable, Change Plan) — Admin only
- Transaction logging
- Input validation for numbers and choices
- Session limits enforced for STANDARD users

---

## Prerequisites

- Python 3.10 or higher
- Terminal / Command Prompt for running the app

---

## How to Run

1. Open a terminal and navigate to the `atm_project` directory.
2. Run the main program:

```bash
python atm.py
```

---

## Running Tests

The application includes an automated test framework with bash scripts for test execution and validation.

### Quick Start

Navigate to the test_cases directory and run all tests:

```bash
cd test_cases
bash run_operation_tests.sh
bash validate_operation_tests.sh
```

### Available Test Scripts

**`run_operation_tests.sh`** — Executes all test cases
```bash
# Run all tests across all operations
bash run_operation_tests.sh

# Run tests for a specific operation
bash run_operation_tests.sh login
bash run_operation_tests.sh deposit
bash run_operation_tests.sh withdrawal
```

**`validate_operation_tests.sh`** — Validates test outputs against expected results
```bash
# Validate all tests
bash validate_operation_tests.sh

# Validate specific operation
bash validate_operation_tests.sh login
```

**`sync_expected_outputs.sh`** — Updates expected output files
```bash
# After verifying outputs are correct, sync them
bash sync_expected_outputs.sh
```

### Test Coverage

13 test cases covering all operations:
- **Login**: 3 tests (valid login, invalid account, wrong PIN)
- **Logout**: 1 test
- **Create**: 1 test
- **Delete**: 1 test
- **Deposit**: 1 test
- **Withdrawal**: 2 tests (valid, insufficient funds)
- **Transfer**: 1 test
- **Paybill**: 1 test
- **Disable**: 1 test
- **Changeplan**: 1 test

### Test Structure

Each operation has its own directory with:
- `input/` — Test input files with commands and responses
- `expected_out/` — Expected output files for comparison

Example test case layout:
```
test_cases/
├── login/
│   ├── input/
│   │   ├── valid_login.txt
│   │   ├── invalid_account.txt
│   │   └── wrong_pin_then_correct.txt
│   └── expected_out/
│       ├── valid_login_terminal.txt
│       ├── invalid_account_terminal.txt
│       └── wrong_pin_then_correct_terminal.txt
├── outputs/               (auto-generated during test runs)
└── [other operations...]
```

### Understanding Test Results

When you run `bash validate_operation_tests.sh`, you'll see:
```
Validating: login
  invalid_account_terminal: PASS
  valid_login_terminal: PASS
  wrong_pin_then_correct_terminal: PASS
```

- **PASS** — Actual output matches expected output
- **FAIL** — Output differs from expected (shows diff)
- **MISSING** — Expected file not found

### Adding New Tests

To add a test for an operation:

1. Create input file: `{operation}/input/test_name.txt`
2. Create expected output: `{operation}/expected_out/test_name_terminal.txt`
3. Run tests: `bash run_operation_tests.sh {operation}`
4. Validate: `bash validate_operation_tests.sh {operation}`

### Documentation

For detailed testing information, see:
- `test_cases/README.md` — Complete testing guide
- `test_cases/QUICKSTART.md` — Quick reference
- `test_cases/OPERATIONS_REFERENCE.md` — Operation details
