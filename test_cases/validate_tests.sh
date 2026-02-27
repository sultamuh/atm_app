#!/bin/bash

################################################################################
# Test Validation Script
#
# Compares actual test outputs with expected outputs.
#
# Uses 'diff' to detect mismatches between:
# - Actual terminal output and expected terminal output
# - Actual transaction output and expected transaction output
#
# Reports detailed differences for each failing test.
################################################################################

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths
OUTPUTS_DIR="$SCRIPT_DIR/outputs"
EXPECTED_DIR="$SCRIPT_DIR/expected"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "ATM Test Validation"
echo "========================================"
echo "Outputs Directory: $OUTPUTS_DIR"
echo "Expected Directory: $EXPECTED_DIR"
echo ""

# Check if directories exist
if [ ! -d "$OUTPUTS_DIR" ]; then
    echo -e "${RED}Error: Outputs directory not found at $OUTPUTS_DIR${NC}"
    echo "Run 'bash run_tests.sh' first to generate test outputs"
    exit 1
fi

if [ ! -d "$EXPECTED_DIR" ]; then
    echo -e "${RED}Error: Expected directory not found at $EXPECTED_DIR${NC}"
    echo "Please populate the expected/ directory with expected output files"
    exit 1
fi

# Check if there are any expected files
expected_count=$(find "$EXPECTED_DIR" -type f 2>/dev/null | wc -l)

if [ "$expected_count" -eq 0 ]; then
    echo -e "${YELLOW}Warning: No expected output files found in $EXPECTED_DIR${NC}"
    echo "Please add expected output files with matching names to outputs/"
    exit 0
fi

echo "Validating against $expected_count expected output file(s)"
echo ""

# Counters
passed=0
failed=0
missing=0

# Loop through all expected files
for expected_file in "$EXPECTED_DIR"/*; do
    if [ -f "$expected_file" ]; then
        filename=$(basename "$expected_file")
        actual_file="$OUTPUTS_DIR/$filename"
        
        echo -e "${BLUE}Checking: $filename${NC}"
        
        if [ ! -f "$actual_file" ]; then
            echo -e "  ${RED}✗ MISSING${NC}: Actual output file not found"
            echo "    Expected: $expected_file"
            echo "    Actual:   $actual_file"
            ((missing++))
        else
            # Use diff to compare files
            if diff -q "$expected_file" "$actual_file" > /dev/null 2>&1; then
                echo -e "  ${GREEN}✓ PASS${NC}: Output matches expected"
                ((passed++))
            else
                echo -e "  ${RED}✗ FAIL${NC}: Output differs from expected"
                echo ""
                echo "  Differences:"
                echo "  ============"
                # Show unified diff format (max 20 lines)
                diff -u "$expected_file" "$actual_file" | head -40 | sed 's/^/  /'
                if [ "$(diff "$expected_file" "$actual_file" | wc -l)" -gt 40 ]; then
                    echo "  ... (more differences - see full diff with: diff -u $expected_file $actual_file)"
                fi
                echo ""
                ((failed++))
            fi
        fi
    fi
done

echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Passed:  ${GREEN}$passed${NC}"
echo -e "Failed:  ${RED}$failed${NC}"
echo -e "Missing: ${YELLOW}$missing${NC}"
echo ""

# Exit with appropriate code
if [ "$failed" -eq 0 ] && [ "$missing" -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed or files were missing.${NC}"
    echo ""
    echo "To fix failing tests:"
    echo "1. Review the differences shown above"
    echo "2. Update expected/ files if needed"
    echo "3. Re-run this script to validate"
    exit 1
fi
