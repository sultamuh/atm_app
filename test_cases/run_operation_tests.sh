#!/bin/bash

################################################################################
# Comprehensive Test Runner
#
# This script runs tests from either:
# 1. Individual operation directories (login/input/, deposit/input/, etc.)
# 2. Centralized inputs/ directory
#
# Usage:
#   bash run_operation_tests.sh [operation_name]
#
# Examples:
#   bash run_operation_tests.sh           # Run all operations
#   bash run_operation_tests.sh login     # Run only login tests
#   bash run_operation_tests.sh deposit   # Run only deposit tests
################################################################################

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUTS_DIR="$SCRIPT_DIR/outputs"
ATM_SCRIPT="$PROJECT_ROOT/atm.py"
ACCOUNTS_FILE="$PROJECT_ROOT/accounts.txt"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create outputs directory
mkdir -p "$OUTPUTS_DIR"

echo "========================================"
echo "ATM Comprehensive Test Runner"
echo "========================================"

# Array of operations
operations=("login" "logout" "create" "delete" "deposit" "withdrawal" "transfer" "paybill" "disable" "changeplan")

# If a specific operation is provided as argument
if [ -n "$1" ]; then
    operations=("$1")
fi

# Counter
test_count=0
pass_count=0
fail_count=0

# Loop through each operation
for operation in "${operations[@]}"; do
    operation_dir="$SCRIPT_DIR/$operation"
    input_dir="$operation_dir/input"
    expected_dir="$operation_dir/expected_out"
    
    if [ ! -d "$input_dir" ]; then
        echo -e "${YELLOW}⚠ Operation '$operation' directory not found${NC}"
        continue
    fi
    
    echo ""
    echo -e "${BLUE}Operation: $operation${NC}"
    echo "================================"
    
    # Loop through input files in this operation
    input_count=0
    for input_file in "$input_dir"/*; do
        if [ -f "$input_file" ]; then
            ((input_count++))
            ((test_count++))
            
            filename=$(basename "$input_file")
            test_name="${filename%.*}"
            
            echo -n "  Test: $test_name ... "
            
            # Generate output filenames
            terminal_output="$OUTPUTS_DIR/${operation}_${test_name}_terminal.txt"
            transaction_output="$OUTPUTS_DIR/${operation}_${test_name}_transactions.txt"
            temp_accounts="$OUTPUTS_DIR/${operation}_${test_name}_accounts.txt"
            
            # Copy accounts file
            if [ -f "$ACCOUNTS_FILE" ]; then
                cp "$ACCOUNTS_FILE" "$temp_accounts"
            else
                touch "$temp_accounts"
            fi
            
            # Run test
            if python3 "$ATM_SCRIPT" < "$input_file" > "$terminal_output" 2>&1; then
                echo -e "${GREEN}✓${NC}"
                ((pass_count++))
            else
                echo -e "${RED}✗${NC}"
                ((fail_count++))
            fi
            
            # Capture transaction output
            if [ -f "$PROJECT_ROOT/transactions.txt" ]; then
                cp "$PROJECT_ROOT/transactions.txt" "$transaction_output"
            else
                touch "$transaction_output"
            fi
        fi
    done
    
    if [ "$input_count" -eq 0 ]; then
        echo -e "  ${YELLOW}No input files found${NC}"
    fi
done

echo ""
echo "========================================"
echo "Test Run Summary"
echo "========================================"
echo "Total Tests: $test_count"
echo -e "Passed: ${GREEN}$pass_count${NC}"
echo -e "Failed: ${RED}$fail_count${NC}"
echo ""
echo "Output files saved to: $OUTPUTS_DIR"
echo ""
echo "Next: Run 'bash validate_operation_tests.sh' to validate outputs"
