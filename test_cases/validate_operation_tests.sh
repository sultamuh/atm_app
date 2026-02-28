#!/bin/bash

################################################################################
# Validate Operation-Based Tests
#
# Validates tests from individual operation directories.
# Compares actual outputs with expected outputs for each operation.
#
# Usage:
#   bash validate_operation_tests.sh [operation_name]
#
# Examples:
#   bash validate_operation_tests.sh           # Validate all operations
#   bash validate_operation_tests.sh login     # Validate only login tests
################################################################################

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUTS_DIR="$SCRIPT_DIR/outputs"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================"
echo "Validation for Operation-Based Tests"
echo "========================================"
echo "Outputs Directory: $OUTPUTS_DIR"
echo ""

# Array of operations
operations=("login" "logout" "create" "delete" "deposit" "withdrawal" "transfer" "paybill" "disable" "changeplan")

# If a specific operation is provided
if [ -n "$1" ]; then
    operations=("$1")
fi

# Counters
pass_count=0
fail_count=0
total_count=0

# Validate each operation
for operation in "${operations[@]}"; do
    expected_dir="$SCRIPT_DIR/$operation/expected_out"
    
    if [ ! -d "$expected_dir" ]; then
        echo -e "${YELLOW}⚠ Expected output directory not found for '$operation'${NC}"
        continue
    fi
    
    echo -e "${BLUE}Validating: $operation${NC}"
    echo "--------------------------------"
    
    found_any=false
    
    # Check each expected file
    for expected_file in "$expected_dir"/*; do
        if [ -f "$expected_file" ]; then
            found_any=true
            filename=$(basename "$expected_file")
            test_name="${filename%.*}"
            extension="${filename##*.}"
            
            # Find matching actual output file
            actual_file="$OUTPUTS_DIR/${operation}_${test_name}.${extension}"
            
            ((++total_count))
            echo -n "  ${test_name}: "
            
            if [ ! -f "$actual_file" ]; then
                echo -e "${RED}MISSING${NC} (expected: $actual_file)"
                ((++fail_count))
            elif diff -q "$expected_file" "$actual_file" > /dev/null 2>&1; then
                echo -e "${GREEN}PASS${NC}"
                ((++pass_count))
            else
                echo -e "${RED}FAIL${NC}"
                echo "    Expected: $expected_file"
                echo "    Actual:   $actual_file"
                # Show first difference
                echo "    Diff:"
                diff -u "$expected_file" "$actual_file" 2>&1 | head -20 | sed 's/^/      /'
                ((++fail_count))
            fi
        fi
    done
    
    if [ "$found_any" = false ]; then
        echo -e "  ${YELLOW}No expected output files found${NC}"
    fi
    echo ""
done

echo "========================================"
echo "Validation Summary"
echo "========================================"
echo "Total: $total_count"
echo -e "Passed: ${GREEN}$pass_count${NC}"
echo -e "Failed: ${RED}$fail_count${NC}"

if [ "$fail_count" -eq 0 ] && [ "$total_count" -gt 0 ]; then
    echo -e "${GREEN}All tests validated successfully!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed validation.${NC}"
    exit 1
fi
