import unittest
import os
import tempfile
from account import Account
from read import read_old_bank_accounts


class TestWithdrawStatementCoverage(unittest.TestCase):

    def setUp(self):
        self.account = Account("1234", "Test User", "A", 100.00, 0, "NP")

    def test_SC1_negative_amount_returns_false(self):
        """SC1: amount < 0 — covers S1 (True) and S2."""
        result = self.account.withdraw(-10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.00)
        self.assertEqual(self.account.total_transactions, 0)

    def test_SC2_insufficient_funds_returns_false(self):
        """SC2: amount > balance — covers S1 (False), S3 (True), S4."""
        result = self.account.withdraw(200)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.00)
        self.assertEqual(self.account.total_transactions, 0)

    def test_SC3_valid_withdrawal_succeeds(self):
        """SC3: 0 <= amount <= balance — covers S1 (False), S3 (False), S5, S6, S7."""
        result = self.account.withdraw(50)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 50.00)
        self.assertEqual(self.account.total_transactions, 1)

    def test_SC4_withdraw_exact_balance_boundary(self):
        """SC4 (boundary): amount == balance — not greater, so succeeds."""
        result = self.account.withdraw(100.00)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 0.00)
        self.assertEqual(self.account.total_transactions, 1)

    def test_SC5_withdraw_zero(self):
        """SC5 (edge): amount == 0 — valid (not negative, not > balance)."""
        result = self.account.withdraw(0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 100.00)
        self.assertEqual(self.account.total_transactions, 1)



# Verified 45-character test lines (matching old_accounts.txt format):
VALID_SP  = "1234  Sean Smith           A 00100.00 0005 SP"
VALID_NP  = "9012  Mia Johnson          D 00075.25 0001 NP"
VALID_2   = "5678  Alex Brown           A 00200.00 0010 NP"
BAD_ACCT  = "ABCD  Sean Smith           A 00100.00 0005 SP"
BAD_STAT  = "1234  Sean Smith           X 00100.00 0005 SP"
BAD_NEG   = "1234  Sean Smith           A -0100.00 0005 SP"
BAD_FMT   = "1234  Sean Smith           A 0012345X 0005 SP"
BAD_TRANS = "1234  Sean Smith           A 00100.00 00XX SP"
BAD_PLAN  = "1234  Sean Smith           A 00100.00 0005 XX"


def make_temp_file(content):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    f.write(content)
    f.close()
    return f.name


class TestReadOldBankAccountsDecisionLoop(unittest.TestCase):

    def _run(self, content):
        path = make_temp_file(content)
        try:
            return read_old_bank_accounts(path)
        finally:
            os.unlink(path)

    def test_verify_line_lengths(self):
        """Meta-test: all static test lines must be exactly 45 chars."""
        for name, line in [
            ("VALID_SP", VALID_SP), ("VALID_NP", VALID_NP), ("VALID_2", VALID_2),
            ("BAD_ACCT", BAD_ACCT), ("BAD_STAT", BAD_STAT), ("BAD_NEG", BAD_NEG),
            ("BAD_FMT",  BAD_FMT),  ("BAD_TRANS", BAD_TRANS), ("BAD_PLAN", BAD_PLAN),
        ]:
            self.assertEqual(len(line), 45, f"{name} is {len(line)} chars, expected 45")

    # ---- Loop coverage ----

    def test_DL1_empty_file_loop_not_entered(self):
        """DL1: Empty file — for loop body is never entered."""
        result = self._run("")
        self.assertEqual(result, [])

    def test_DL2_single_valid_line_loop_once(self):
        """DL2: 1 valid line — loop runs once; all decisions take False branch."""
        result = self._run(VALID_SP + "\n")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Sean Smith')
        self.assertEqual(result[0]['status'], 'A')
        self.assertAlmostEqual(result[0]['balance'], 100.00)
        self.assertEqual(result[0]['total_transactions'], 5)
        self.assertEqual(result[0]['plan'], 'SP')

    def test_DL3_multiple_valid_lines_loop_many(self):
        """DL3: 3 valid lines — loop runs multiple times."""
        content = "\n".join([VALID_SP, VALID_2, VALID_NP]) + "\n"
        result = self._run(content)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], 'Sean Smith')
        self.assertEqual(result[1]['name'], 'Alex Brown')
        self.assertEqual(result[2]['status'], 'D')

    # ---- Decision coverage: True branch of each decision ----

    def test_DL4_wrong_line_length_D1_true(self):
        """DL4: Short line — D1 = True (line length != 45), line skipped."""
        result = self._run("1234 short\n")
        self.assertEqual(result, [])

    def test_DL5_non_digit_account_number_D2_true(self):
        """DL5: Account number 'ABCD' — D2 = True, line skipped."""
        result = self._run(BAD_ACCT + "\n")
        self.assertEqual(result, [])

    def test_DL6_invalid_status_D3_true(self):
        """DL6: Status 'X' — D3 = True, line skipped."""
        result = self._run(BAD_STAT + "\n")
        self.assertEqual(result, [])

    def test_DL7_negative_balance_D4_true(self):
        """DL7: Balance starts with '-' — D4 = True, line skipped."""
        result = self._run(BAD_NEG + "\n")
        self.assertEqual(result, [])

    def test_DL8_malformed_balance_D5_true(self):
        """DL8: Balance format invalid — D5 = True, line skipped."""
        result = self._run(BAD_FMT + "\n")
        self.assertEqual(result, [])

    def test_DL9_non_digit_transactions_D6_true(self):
        """DL9: Transaction count 'XX' — D6 = True, line skipped."""
        result = self._run(BAD_TRANS + "\n")
        self.assertEqual(result, [])

    def test_DL10_invalid_plan_type_D7_true(self):
        """DL10: Plan type 'XX' — D7 = True, line skipped."""
        result = self._run(BAD_PLAN + "\n")
        self.assertEqual(result, [])

    # ---- Decision coverage: False branch (valid lines parsed correctly) ----

    def test_DL11_mixed_valid_and_invalid_lines(self):
        """DL11: Loop runs multiple times; line 2 triggers D2=True, others pass."""
        content = "\n".join([VALID_SP, BAD_ACCT, VALID_2]) + "\n"
        result = self._run(content)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Sean Smith')
        self.assertEqual(result[1]['name'], 'Alex Brown')

    def test_DL12_all_decisions_false_NP_disabled(self):
        """DL12: Valid NP/disabled account — all decisions False, parsed correctly."""
        result = self._run(VALID_NP + "\n")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['plan'], 'NP')
        self.assertEqual(result[0]['status'], 'D')
        self.assertAlmostEqual(result[0]['balance'], 75.25)
        self.assertEqual(result[0]['total_transactions'], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
