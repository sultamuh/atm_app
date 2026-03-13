from account import Account
from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error


class BankSystem:
    """
    Manages all bank accounts and provides methods to perform
    banking operations on them.
    """

    def __init__(self):
        """
        Initializes the banking system with an empty collection of accounts.
        """
        self.accounts = {}

    def load_accounts(self, file_path):
        """
        Loads accounts from the old current bank accounts file.

        Args:
            file_path (str): Path to the input accounts file.

        Returns:
            None
        """
        account_dicts = read_old_bank_accounts(file_path)

        for acc in account_dicts:
            account = Account(
                acc["account_number"],
                acc["name"],
                acc["status"],
                acc["balance"],
                acc["total_transactions"],
                acc["plan"]
            )
            self.accounts[account.account_number] = account

    def save_accounts(self, file_path):
        """
        Saves all current accounts to the output file.

        Args:
            file_path (str): Path to the output accounts file.

        Returns:
            None
        """
        account_list = []

        for account in self.accounts.values():
            account_list.append(account.to_dict())

        write_new_current_accounts(account_list, file_path)

    def get_account(self, account_number):
        """
        Finds and returns an account by account number.

        Args:
            account_number (str): The account number to search for.

        Returns:
            Account or None: The matching account if found, otherwise None.
        """
        return self.accounts.get(str(account_number))

    def create_account(self, account_number, name, status="A", balance=0.0, plan="NP"):
        """
        Creates a new account if the account number does not already exist.

        Args:
            account_number (str): New account number.
            name (str): Account holder name.
            status (str): Account status.
            balance (float): Starting balance.
            plan (str): Account plan type.

        Returns:
            bool: True if successful, False otherwise.
        """
        account_number = str(account_number)

        if account_number in self.accounts:
            log_constraint_error("Account already exists", "Create Account")
            return False

        self.accounts[account_number] = Account(
            account_number,
            name,
            status,
            balance,
            0,
            plan
        )
        return True

    def delete_account(self, account_number):
        """
        Disables an account instead of permanently deleting it.

        Args:
            account_number (str): Account number to disable.

        Returns:
            bool: True if successful, False otherwise.
        """
        account = self.get_account(account_number)

        if account is None:
            log_constraint_error("Account not found", "Delete Account")
            return False

        account.disable()
        return True

    def deposit_to_account(self, account_number, amount):
        """
        Deposits money into an account.

        Args:
            account_number (str): Account number.
            amount (float): Amount to deposit.

        Returns:
            bool: True if successful, False otherwise.
        """
        account = self.get_account(account_number)

        if account is None:
            log_constraint_error("Account not found", "Deposit")
            return False

        if not account.deposit(amount):
            log_constraint_error("Invalid deposit amount", "Deposit")
            return False

        return True

    def withdraw_from_account(self, account_number, amount):
        """
        Withdraws money from an account.

        Args:
            account_number (str): Account number.
            amount (float): Amount to withdraw.

        Returns:
            bool: True if successful, False otherwise.
        """
        account = self.get_account(account_number)

        if account is None:
            log_constraint_error("Account not found", "Withdraw")
            return False

        if not account.withdraw(amount):
            log_constraint_error("Invalid withdrawal or insufficient funds", "Withdraw")
            return False

        return True

    def transfer(self, from_account_number, to_account_number, amount):
        """
        Transfers money from one account to another.

        Args:
            from_account_number (str): Source account number.
            to_account_number (str): Destination account number.
            amount (float): Amount to transfer.

        Returns:
            bool: True if successful, False otherwise.
        """
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)

        if from_account is None or to_account is None:
            log_constraint_error("One or both accounts not found", "Transfer")
            return False

        if not from_account.withdraw(amount):
            log_constraint_error("Transfer failed due to insufficient funds or invalid amount", "Transfer")
            return False

        if not to_account.deposit(amount):
            log_constraint_error("Transfer deposit failed", "Transfer")
            return False

        return True

    def change_account_plan(self, account_number, new_plan):
        """
        Changes the plan type of an account.

        Args:
            account_number (str): Account number.
            new_plan (str): New plan type.

        Returns:
            bool: True if successful, False otherwise.
        """
        account = self.get_account(account_number)

        if account is None:
            log_constraint_error("Account not found", "Change Plan")
            return False

        if not account.change_plan(new_plan):
            log_constraint_error("Invalid plan type", "Change Plan")
            return False

        return True