#!/bin/bash

################################################################################
# Test Runner Script
#
# Automatically runs all test cases in the test_cases directory structure.
#
# For each test case:
# 1. Reads input from inputs/ directory
# 2. Runs the ATM application with that input
# 3. Captures both terminal output and transaction output
# 4. Saves outputs to outputs/ directory
#
# Directory structure:
# - inputs/          - All test input files
# - expected/        - Expected transaction output files
# - outputs/         - Actual transaction and terminal output files
# - {operation}/     - Individual operation test directories
#   - input/         - Input files for that operation
#   - expected_out/  - Expected output files for that operation
################################################################################

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUTS_DIR="$SCRIPT_DIR/inputs"
OUTPUTS_DIR="$SCRIPT_DIR/outputs"
ATM_SCRIPT="$PROJECT_ROOT/atm.py"
ACCOUNTS_FILE="$PROJECT_ROOT/accounts.txt"

# Create outputs directory if it doesn't exist
mkdir -p "$OUTPUTS_DIR"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "ATM Test Runner"
echo "========================================"
echo "Project Root: $PROJECT_ROOT"
echo "Inputs Directory: $INPUTS_DIR"
echo "Outputs Directory: $OUTPUTS_DIR"
echo ""

# Check if inputs directory exists
if [ ! -d "$INPUTS_DIR" ]; then
    echo -e "${RED}Error: Inputs directory not found at $INPUTS_DIR${NC}"
    exit 1
fi

# Get count of input files
input_count=$(find "$INPUTS_DIR" -type f | wc -l)

if [ "$input_count" -eq 0 ]; then
    echo -e "${YELLOW}Warning: No input files found in $INPUTS_DIR${NC}"
    echo "Please add test input files to the inputs/ directory"
    exit 0
fi

echo "Found $input_count test case(s)"
echo ""

# Counter for passed/failed tests
passed=0
failed=0

# Loop through all input files in the inputs directory
for input_file in "$INPUTS_DIR"/*; do
    if [ -f "$input_file" ]; then
        filename=$(basename "$input_file")
        test_name="${filename%.*}"
        extension="${filename##*.}"
        
        echo "Running test: $test_name"
        
        # Create temporary files for this test
        terminal_output="$OUTPUTS_DIR/${test_name}_terminal.txt"
        transaction_output="$OUTPUTS_DIR/${test_name}_transactions.txt"
        temp_accounts="$OUTPUTS_DIR/${test_name}_accounts.txt"
        
        # Copy accounts file to temp location for this test
        if [ -f "$ACCOUNTS_FILE" ]; then
            cp "$ACCOUNTS_FILE" "$temp_accounts"
        else
            touch "$temp_accounts"
        fi
        
        # Run the ATM application with input from the test file
        # Capture both stdout and stderr
        if python3 "$ATM_SCRIPT" < "$input_file" > "$terminal_output" 2>&1; then
            echo -e "  ${GREEN}✓ Execution succeeded${NC}"
            ((++passed))
        else
            echo -e "  ${RED}✗ Execution failed${NC}"
            ((++failed))
        fi
        
        # Check if transaction output file was created
        if [ -f "$PROJECT_ROOT/transactions.txt" ]; then
            cp "$PROJECT_ROOT/transactions.txt" "$transaction_output"
            echo -e "  ${GREEN}✓ Transaction output captured${NC}"
        else
            echo -e "  ${YELLOW}⚠ No transaction output generated${NC}"
            touch "$transaction_output"
        fi
        
        echo "  Terminal Output: $terminal_output"
        echo "  Transaction Output: $transaction_output"
        echo ""
    fi
done

echo "========================================"
echo "Test Run Summary"
echo "========================================"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""
echo "Output files saved to: $OUTPUTS_DIR"
echo ""
echo "Next steps:"
echo "1. Review the generated output files in outputs/"
echo "2. Copy expected outputs to test_cases/expected/"
echo "3. Run 'bash validate_tests.sh' to compare actual vs expected"
