#!/bin/bash

cd "/Users/Ben/Ontario Tech/semester 4/Software Quality Assurance/atm_app/test_cases"

# Copy each test output to expected with correct naming
for dir in */input; do
  op=$(dirname "$dir")
  for input_file in "$dir"/*.txt; do
    test_name=$(basename "$input_file" .txt)
    
    # Copy terminal output
    if [ -f "outputs/${op}_${test_name}_terminal.txt" ]; then
      cp "outputs/${op}_${test_name}_terminal.txt" "${op}/expected_out/${test_name}_terminal.txt"
    fi
    
    # Copy transaction output (only if not empty)
    if [ -f "outputs/${op}_${test_name}_transactions.txt" ] && [ -s "outputs/${op}_${test_name}_transactions.txt" ]; then
      cp "outputs/${op}_${test_name}_transactions.txt" "${op}/expected_out/${test_name}_transactions.txt"
    fi
  done
done

echo "Copied all expected outputs with correct naming"
