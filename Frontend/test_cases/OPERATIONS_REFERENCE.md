# Test Operations Reference

Quick reference for all ATM operations and their test cases.

## Operations Tested

### 1. LOGIN
Tests account authentication and session initialization.

**Test cases included:**
- `valid_login.txt` - Successful login with correct credentials
- `invalid_account.txt` - Login attempt with non-existent account
- `wrong_pin_then_correct.txt` - Multiple login attempts

**Run:** `bash run_operation_tests.sh login`

---

### 2. LOGOUT
Tests session termination and state reset.

**Test cases included:**
- `logout_after_login.txt` - Proper logout after login

**Run:** `bash run_operation_tests.sh logout`

---

### 3. CREATE
Tests creating new accounts in the system.

**Test cases included:**
- `create_new_account.txt` - Create account with valid parameters

**Run:** `bash run_operation_tests.sh create`

---

### 4. DELETE
Tests deleting accounts from the system.

**Test cases included:**
- `delete_account.txt` - Delete existing account

**Run:** `bash run_operation_tests.sh delete`

---

### 5. DEPOSIT
Tests depositing money into accounts.

**Test cases included:**
- `deposit_valid.txt` - Valid deposit transaction

**Run:** `bash run_operation_tests.sh deposit`

---

### 6. WITHDRAWAL
Tests withdrawing money from accounts.

**Test cases included:**
- `withdrawal_valid.txt` - Valid withdrawal transaction
- `withdrawal_insufficient_funds.txt` - Withdrawal exceeding balance

**Run:** `bash run_operation_tests.sh withdrawal`

---

### 7. TRANSFER
Tests transferring money between accounts.

**Test cases included:**
- `transfer_valid.txt` - Valid transfer between two accounts

**Run:** `bash run_operation_tests.sh transfer`

---

### 8. PAYBILL
Tests paying bills from account.

**Test cases included:**
- `paybill_hydro.txt` - Pay HYDRO bill

**Run:** `bash run_operation_tests.sh paybill`

---

### 9. DISABLE
Tests disabling accounts.

**Test cases included:**
- `disable_account.txt` - Disable an account

**Run:** `bash run_operation_tests.sh disable`

---

### 10. CHANGEPLAN
Tests changing transaction plans.

**Test cases included:**
- `changeplan_monthly.txt` - Change to MONTHLY plan

**Run:** `bash run_operation_tests.sh changeplan`

---

## Test File Naming Convention

### Input Files
Format: `{operation}/input/{test_description}.txt`

Examples:
- `login/input/valid_login.txt`
- `deposit/input/deposit_valid.txt`
- `withdrawal/input/withdrawal_insufficient_funds.txt`

### Expected Output Files
Format: `{operation}/expected_out/{test_description}_{type}.txt`

Where `{type}` is:
- `terminal.txt` - Console/screen output
- `transactions.txt` - Transaction log file output

Examples:
- `login/expected_out/valid_login_terminal.txt`
- `deposit/expected_out/deposit_valid_terminal.txt`
- `deposit/expected_out/deposit_valid_transactions.txt`

---

## File Organization Example

For the `deposit` operation:

```
deposit/
├── input/
│   └── deposit_valid.txt              # Input commands/responses
├── expected_out/
│   ├── deposit_valid_terminal.txt     # Expected screen output
│   └── deposit_valid_transactions.txt # Expected transaction log
```

---

## Running All Tests

```bash
# Run all operation tests
bash run_operation_tests.sh

# Validate all results
bash validate_operation_tests.sh
```

---

## Running Tests by Category

```bash
# Financial Operations
bash run_operation_tests.sh deposit
bash run_operation_tests.sh withdrawal
bash run_operation_tests.sh transfer
bash run_operation_tests.sh paybill

# Account Management
bash run_operation_tests.sh create
bash run_operation_tests.sh delete
bash run_operation_tests.sh login
bash run_operation_tests.sh logout

# Settings
bash run_operation_tests.sh disable
bash run_operation_tests.sh changeplan
```

---

## Adding Test Cases

### Template for New Test Case

To add a new test case for an operation:

1. **Create input file:**
```bash
cat > {operation}/input/{new_test_name}.txt << 'EOF'
# Commands and responses here
EOF
```

2. **Create expected terminal output:**
```bash
cat > {operation}/expected_out/{new_test_name}_terminal.txt << 'EOF'
# Expected console output
EOF
```

3. **Create expected transaction output (if applicable):**
```bash
cat > {operation}/expected_out/{new_test_name}_transactions.txt << 'EOF'
# Expected transaction record format
EOF
```

4. **Run and validate:**
```bash
bash run_operation_tests.sh {operation}
bash validate_operation_tests.sh {operation}
```

---

## Input File Format

Each line in an input file corresponds to a response to a prompt.

**Example:** Login test
```
LOGIN          # Response to "Enter command: "
1001           # Response to "Account Number: "
1234           # Response to "PIN: "
EXIT           # Response to "Enter command: "
```

**Example:** Deposit test
```
LOGIN          # Login first
1001
1234
DEPOSIT        # Then deposit
500            # Amount to deposit
EXIT
```

---

## Expected Output Format

### Terminal Output
Should match exactly what the application prints, including:
- Prompts
- Messages
- Spacing and formatting
- Error messages (if testing error cases)

### Transaction Output
Format depends on the application's transaction record format.

**Example Transaction Line:**
```
accountNumber,operationType,amount
1001,DEPOSIT,500.00
```

---

## Best Practices for Test Cases

### Test Naming
Use descriptive names that indicate what's being tested:
- ✅ `valid_login.txt` - Clearly shows successful login test
- ✅ `invalid_account.txt` - Clearly shows invalid account test
- ✅ `insufficient_funds.txt` - Clearly shows insufficient balance test
- ❌ `test1.txt` - Not descriptive
- ❌ `fail.txt` - Ambiguous

### Input File Format
- One line per prompt response
- Include `EXIT` to cleanly end the session
- Order responses to match prompt sequence exactly

### Expected Output Files
- Match exact application output (including whitespace)
- Include all prompts and response messages
- Update when application output changes intentionally

---

## Troubleshooting Tests

### Test not found
```bash
# List all tests in an operation
ls {operation}/input/
ls {operation}/expected_out/
```

### Output mismatch
```bash
# View differences
diff {operation}/expected_out/{test}_terminal.txt outputs/{operation}_{test}_terminal.txt
```

### Re-running a test
```bash
# Run and validate specific operation
bash run_operation_tests.sh {operation}
bash validate_operation_tests.sh {operation}
```

---

## Integration with CI/CD

Add this to your CI/CD pipeline:

```bash
#!/bin/bash
cd test_cases
bash run_operation_tests.sh
if ! bash validate_operation_tests.sh; then
    echo "Tests failed!"
    exit 1
fi
echo "All tests passed!"
```
