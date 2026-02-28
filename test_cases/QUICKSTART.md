# Quick Start Guide - ATM Test Framework

## 5-Minute Setup

### Step 1: Navigate to test_cases directory
```bash
cd test_cases
```

### Step 2: Run tests for a specific operation
```bash
# Test login functionality
bash run_operation_tests.sh login

# Test deposit functionality
bash run_operation_tests.sh deposit

# Test withdrawal functionality
bash run_operation_tests.sh withdrawal
```

### Step 3: Validate results
```bash
# Validate login tests
bash validate_operation_tests.sh login

# Validate deposit tests
bash validate_operation_tests.sh deposit
```

---

## Common Commands

### Run all tests
```bash
bash run_operation_tests.sh
```

### Run tests for one operation
```bash
bash run_operation_tests.sh login
bash run_operation_tests.sh create
bash run_operation_tests.sh delete
bash run_operation_tests.sh deposit
bash run_operation_tests.sh withdrawal
bash run_operation_tests.sh transfer
bash run_operation_tests.sh paybill
bash run_operation_tests.sh disable
bash run_operation_tests.sh changeplan
bash run_operation_tests.sh logout
```

### Validate all tests
```bash
bash validate_operation_tests.sh
```

### Validate one operation
```bash
bash validate_operation_tests.sh login
```

### View generated outputs
```bash
# List all generated outputs
ls -la outputs/

# View terminal output from a test
cat outputs/login_valid_login_terminal.txt

# View transaction output from a test
cat outputs/deposit_valid_deposit_transactions.txt
```

---

## Adding Your First Test

### Example: Add a "high_balance" test to withdrawal

1. **Create input file:**
```bash
cat > withdrawal/input/high_balance.txt << 'EOF'
LOGIN
1001
1234
WITHDRAWAL
100
EXIT
EOF
```

2. **Create expected output files:**

Terminal output:
```bash
cat > withdrawal/expected_out/high_balance_terminal.txt << 'EOF'
===== ATM Application Started =====
Available command: LOGIN
Type EXIT to quit the application.
Enter command: Account Number: PIN:
Login successful. Welcome back!
Available commands: CREATE, DELETE, DEPOSIT, WITHDRAWAL, TRANSFER, PAYBILL, DISABLE, CHANGEPLAN, LOGOUT
Type EXIT to quit the application.
Enter command: Amount: Withdrawal successful. New balance: 2100.00
Available commands: CREATE, DELETE, DEPOSIT, WITHDRAWAL, TRANSFER, PAYBILL, DISABLE, CHANGEPLAN, LOGOUT
Type EXIT to quit the application.
Enter command: Exiting ATM application. Goodbye!
EOF
```

Transaction output:
```bash
cat > withdrawal/expected_out/high_balance_transactions.txt << 'EOF'
1001,WITHDRAWAL,100.00
EOF
```

3. **Run the new test:**
```bash
bash run_operation_tests.sh withdrawal
bash validate_operation_tests.sh withdrawal
```

---

## Directory Reference

| Directory | Purpose |
|-----------|---------|
| `inputs/` | Centralized test inputs (alternative to operation dirs) |
| `expected/` | Expected outputs for centralized tests |
| `outputs/` | **Auto-generated** - actual test outputs |
| `{operation}/input/` | Input files for that operation |
| `{operation}/expected_out/` | Expected outputs for that operation |

---

## Troubleshooting

### Tests show as "FAIL"
1. Check the diff output shown by validation script
2. View the actual output: `cat outputs/{test_name}_terminal.txt`
3. Compare with expected: `cat {operation}/expected_out/{test_name}_terminal.txt`
4. Update expected outputs if application behavior changed

### No input files found
```bash
# Check if input files exist
ls login/input/
ls deposit/input/

# Create a test input file if needed
echo "LOGIN" > login/input/my_test.txt
echo "1001" >> login/input/my_test.txt
echo "1234" >> login/input/my_test.txt
echo "EXIT" >> login/input/my_test.txt
```

### Permission denied when running scripts
```bash
# Make scripts executable
chmod +x *.sh
```

---

## Test Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✓ (Green) | Test passed |
| ✗ (Red) | Test failed or missing |
| ⚠ (Yellow) | Warning - no files found |

---

## Example Workflow

```bash
# 1. Run login tests
bash run_operation_tests.sh login

# 2. Check results
bash validate_operation_tests.sh login

# 3. If tests failed, review differences
diff login/expected_out/valid_login_terminal.txt outputs/login_valid_login_terminal.txt

# 4. Update expected output or input as needed
# 5. Re-validate
bash validate_operation_tests.sh login
```

---

## Next Steps

- Read [README.md](README.md) for complete documentation
- Add more test cases for edge cases and error conditions
- Integrate tests into your CI/CD pipeline
- Share test cases with team members
