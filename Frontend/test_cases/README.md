# ATM Application Test Framework

A comprehensive, organized testing framework for the ATM application with automated test execution and validation.

## Directory Structure

```
test_cases/
├── inputs/                      # Centralized test input files
├── expected/                    # Expected outputs for centralized tests
├── outputs/                     # Actual test outputs (generated)
├── login/
│   ├── input/                   # Login test inputs
│   └── expected_out/            # Login expected outputs
├── logout/
│   ├── input/
│   └── expected_out/
├── create/
│   ├── input/
│   └── expected_out/
├── delete/
│   ├── input/
│   └── expected_out/
├── deposit/
│   ├── input/
│   └── expected_out/
├── withdrawal/
│   ├── input/
│   └── expected_out/
├── transfer/
│   ├── input/
│   └── expected_out/
├── paybill/
│   ├── input/
│   └── expected_out/
├── disable/
│   ├── input/
│   └── expected_out/
├── changeplan/
│   ├── input/
│   └── expected_out/
├── run_tests.sh                 # Run tests from inputs/ directory
├── validate_tests.sh            # Validate centralized tests
├── run_operation_tests.sh       # Run operation-specific tests
├── validate_operation_tests.sh  # Validate operation-specific tests
└── README.md                    # This file
```

## Two Testing Approaches

### Approach 1: Centralized (Using inputs/ and expected/ directories)

Best for flat test organization where you manage all test files in one location.

**Input files:** `test_cases/inputs/`
**Expected outputs:** `test_cases/expected/`
**Script:** `run_tests.sh` and `validate_tests.sh`

### Approach 2: Operation-Organized (Using {operation}/input/ and {operation}/expected_out/)

Best for organizing tests by operation type, making it easy to find and manage related tests.

**Input files:** `test_cases/{operation}/input/` (e.g., `login/input/`)
**Expected outputs:** `test_cases/{operation}/expected_out/` (e.g., `login/expected_out/`)
**Script:** `run_operation_tests.sh` and `validate_operation_tests.sh`

## Running Tests

### Method 1: With Operation-Based Organization (Recommended)

Run all operation tests:
```bash
cd test_cases
bash run_operation_tests.sh
```

Run tests for a specific operation:
```bash
bash run_operation_tests.sh login
bash run_operation_tests.sh deposit
bash run_operation_tests.sh withdrawal
```

### Method 2: With Centralized Organization

Run all centralized tests:
```bash
cd test_cases
bash run_tests.sh
```

## Validating Tests

After running tests, validate the outputs match expectations.

### Validate Operation-Based Tests:
```bash
bash validate_operation_tests.sh           # All operations
bash validate_operation_tests.sh login     # Specific operation
```

### Validate Centralized Tests:
```bash
bash validate_tests.sh
```

## Understanding Test Files

### Input Files

Files defining the commands and responses the ATM will receive.

**Example:** `login/input/valid_login.txt`
```
LOGIN
1001
1234
EXIT
```

Each line is a response to an input prompt.

### Expected Output Files

Files containing the expected output for a test case.

**Terminal output:** `login/expected_out/valid_login_terminal.txt`
- Contains expected console messages

**Transaction output:** `deposit/expected_out/deposit_valid_transactions.txt`
- Contains expected transaction records (if applicable)

## Creating New Tests

### To add a test to an existing operation:

1. Create an input file: `test_cases/{operation}/input/test_name.txt`
```bash
cd test_cases/{operation}/input
nano test_name.txt
```

2. Create expected terminal output: `test_cases/{operation}/expected_out/test_name_terminal.txt`

3. Create expected transaction output (if needed): `test_cases/{operation}/expected_out/test_name_transactions.txt`

4. Run the test:
```bash
bash run_operation_tests.sh {operation}
bash validate_operation_tests.sh {operation}
```

### Example: Adding a "valid_deposit" test to deposit operations

Input file (`deposit/input/valid_deposit.txt`):
```
LOGIN
1001
1234
DEPOSIT
500
EXIT
```

Expected terminal output (`deposit/expected_out/valid_deposit_terminal.txt`):
```
===== ATM Application Started =====
Available command: LOGIN
Type EXIT to quit the application.
Enter command: Account Number: PIN:
Login successful. Welcome back!
Available commands: CREATE, DELETE, DEPOSIT, WITHDRAWAL, TRANSFER, PAYBILL, DISABLE, CHANGEPLAN, LOGOUT
Type EXIT to quit the application.
Enter command: Amount: Deposit successful. New balance: 2500.00
Available commands: CREATE, DELETE, DEPOSIT, WITHDRAWAL, TRANSFER, PAYBILL, DISABLE, CHANGEPLAN, LOGOUT
Type EXIT to quit the application.
Enter command: Exiting ATM application. Goodbye!
```

Expected transaction output (`deposit/expected_out/valid_deposit_transactions.txt`):
```
1001,DEPOSIT,500.00
```

## Output Files

Test outputs are saved in `test_cases/outputs/`:

- `{operation}_{test_name}_terminal.txt` - Console/terminal output
- `{operation}_{test_name}_transactions.txt` - Transaction file output

Example outputs from running `bash run_operation_tests.sh login`:
```
outputs/
├── login_valid_login_terminal.txt
├── login_valid_login_transactions.txt
├── login_invalid_account_terminal.txt
├── login_invalid_account_transactions.txt
└── ...
```

## Troubleshooting

### "No input files found"
- Ensure you've created `.txt` files in the `{operation}/input/` directories
- Check file permissions

### "No expected output files found"
- Create corresponding expected output files in `{operation}/expected_out/`
- Files must be named to match input files

### Test output differs from expected
- Review the diff output shown by validation script
- Update expected output files or fix test input as needed
- Run validation again to confirm

## Script Details

### run_operation_tests.sh

Runs tests from individual operation directories.

**What it does:**
1. Loops through each operation's `input/` directory
2. Executes the ATM application with each input file
3. Captures terminal output to `terminal.txt`
4. Captures transaction output to `transactions.txt`
5. Saves all outputs to `outputs/` directory

**Options:**
- No arguments: Runs all operations
- With operation name: `bash run_operation_tests.sh login`

### validate_operation_tests.sh

Compares generated outputs with expected outputs.

**What it does:**
1. Finds all expected output files in each operation's `expected_out/` directory
2. Locates corresponding actual output files in `outputs/`
3. Uses `diff` command to compare files
4. Reports pass/fail status for each test
5. Shows differences for failed tests

**Features:**
- Color-coded output (green=pass, red=fail, yellow=missing)
- Shows diffs for failed tests
- Handles missing files gracefully

### run_tests.sh

Runs tests from the centralized `inputs/` directory.

**What it does:**
1. Loops through each file in `inputs/`
2. Runs the ATM application with that input
3. Captures both terminal and transaction output
4. Saves outputs to `outputs/`

### validate_tests.sh

Validates centralized tests against expected outputs.

**What it does:**
1. Finds all expected output files in `expected/`
2. Locates corresponding actual output in `outputs/`
3. Uses `diff` to compare
4. Reports results and differences

## Best Practices

1. **Use Operation-Based Organization** - Easier to manage and find tests
2. **Clear Test Names** - Use descriptive names that indicate what's being tested
   - `valid_login.txt` - Test successful login
   - `invalid_account.txt` - Test login with invalid account
   - `insufficient_funds.txt` - Test withdrawal with insufficient balance

3. **Input File Format**
   - One response per line
   - Match the exact order of prompts the application expects
   - Use `EXIT` to gracefully exit the application

4. **Expected Output Files**
   - Should exactly match what the application prints
   - Include all prompts and messages
   - Pay attention to spacing and formatting

5. **Commit Test Files**
   - Mark `outputs/` as ignored in `.gitignore`
   - Commit `input/` and `expected_out/` files
   - Never commit generated test outputs

## Automation Integration

These scripts can be integrated into CI/CD pipelines:

```bash
#!/bin/bash
cd test_cases
bash run_operation_tests.sh
bash validate_operation_tests.sh
```

Or in a GitHub Actions workflow:
```yaml
- name: Run ATM Tests
  run: |
    cd test_cases
    bash run_operation_tests.sh
    bash validate_operation_tests.sh
```

## Common Test Patterns

### Valid Operation Test
1. Login with valid credentials
2. Perform operation
3. Exit

### Invalid Input Test
1. Login with valid credentials
2. Attempt operation with invalid input
3. System should handle gracefully
4. Exit

### Edge Case Test
1. Login with valid credentials
2. Perform operation at boundary (e.g., exact balance, minimum/maximum amount)
3. Verify correct behavior
4. Exit

## Further Customization

To modify the test scripts:

1. **Change output directory:**
   - Edit `OUTPUTS_DIR` variable in scripts

2. **Add more operations:**
   - Create new directories: `test_cases/{new_operation}/{input,expected_out}`
   - Scripts automatically discover and test them

3. **Add pre/post processing:**
   - Edit scripts to add setup/cleanup steps before/after tests

4. **Custom diff format:**
   - Modify `diff` command in validation scripts to use different flags

5. **Generate JUnit reports:**
   - Parse validation output and create JUnit XML for CI integration
