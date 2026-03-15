#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Update login
cp outputs/login_invalid_account_terminal.txt login/expected_out/invalid_account_terminal.txt
cp outputs/login_valid_login_terminal.txt login/expected_out/valid_login_terminal.txt
cp outputs/login_wrong_pin_then_correct_terminal.txt login/expected_out/wrong_pin_then_correct_terminal.txt

# Update logout
cp outputs/logout_logout_after_login_terminal.txt logout/expected_out/logout_after_login_terminal.txt

# Update create
cp outputs/create_create_new_account_terminal.txt create/expected_out/create_new_account_terminal.txt
cp outputs/create_create_new_account_transactions.txt create/expected_out/create_new_account_transactions.txt

# Update delete
cp outputs/delete_delete_account_terminal.txt delete/expected_out/delete_account_terminal.txt

# Update deposit
cp outputs/deposit_deposit_valid_terminal.txt deposit/expected_out/deposit_valid_terminal.txt
cp outputs/deposit_deposit_valid_transactions.txt deposit/expected_out/deposit_valid_transactions.txt

# Update withdrawal
cp outputs/withdrawal_withdrawal_valid_terminal.txt withdrawal/expected_out/withdrawal_valid_terminal.txt
cp outputs/withdrawal_withdrawal_valid_transactions.txt withdrawal/expected_out/withdrawal_valid_transactions.txt
cp outputs/withdrawal_withdrawal_insufficient_funds_terminal.txt withdrawal/expected_out/withdrawal_insufficient_funds_terminal.txt

# Update transfer
cp outputs/transfer_transfer_valid_terminal.txt transfer/expected_out/transfer_valid_terminal.txt
cp outputs/transfer_transfer_valid_transactions.txt transfer/expected_out/transfer_valid_transactions.txt

# Update paybill
cp outputs/paybill_paybill_hydro_terminal.txt paybill/expected_out/paybill_hydro_terminal.txt
cp outputs/paybill_paybill_hydro_transactions.txt paybill/expected_out/paybill_hydro_transactions.txt

# Update disable
cp outputs/disable_disable_account_terminal.txt disable/expected_out/disable_account_terminal.txt

# Update changeplan
cp outputs/changeplan_changeplan_monthly_terminal.txt changeplan/expected_out/changeplan_monthly_terminal.txt

echo "Updated all expected outputs"
