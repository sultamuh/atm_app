"""
Account Manager

Handles account lookup and validation logic.
"""

from models.account import Account
from enums.account_status import AccountStatus


class AccountManager:
    def __init__(self, accounts: dict[int, Account]):
        """
        Initializes the AccountManager.

        Parameters:
        accounts (dict[int, Account]):
            Dictionary mapping account numbers to Account objects.

        Purpose:
        - Provides centralized access and validation logic for accounts.
        - Acts as abstraction layer between controllers and raw account storage.
        """
        self.accounts = accounts

    def getAccount(self, accountNumber: int) -> Account:
        """
        Retrieves an Account object by account number.

        Parameters:
        accountNumber (int):
            Unique account identifier.

        Returns:
        Account | None:
            Returns the Account object if found, otherwise None.
        """
        return self.accounts.get(accountNumber)

    def accountExists(self, accountNumber: int) -> bool:
        """
        Checks if an account exists in the system.

        Parameters:
        accountNumber (int):
            Account number to check.

        Returns:
        bool:
            True if account exists, False otherwise.
        """
        return accountNumber in self.accounts

    def validateOwnership(self, accountNumber: int, holderName: str) -> bool:
        """
        Validates that an account exists and belongs to the specified holder.

        Parameters:
        accountNumber (int):
            Account number being validated.

        holderName (str):
            Expected account holder name.

        Returns:
        bool:
            True if account exists and holder name matches, False otherwise.
        """
        account = self.getAccount(accountNumber)
        return account and account.getHolderName() == holderName

    def isAccountActive(self, accountNumber: int) -> bool:
        """
        Checks if an account exists and is currently ACTIVE.

        Parameters:
        accountNumber (int):
            Account number to check.

        Returns:
        bool:
            True if account exists and status is ACTIVE.
        """
        account = self.getAccount(accountNumber)
        return account and account.getStatus() == AccountStatus.ACTIVE

    def isAccountUsable(self, accountNumber: int) -> bool:
        """
        Checks if an account exists and is usable for transactions.

        Usable means:
        - Account exists
        - Account is ACTIVE

        Parameters:
        accountNumber (int):
            Account number to validate.

        Returns:
        bool:
            True if account is usable.
        """
        return self.accountExists(accountNumber) and self.isAccountActive(accountNumber)

    def addAccount(self, account: Account):
        """
        Adds a new account to the system.

        Parameters:
        account (Account):
            Account object to add to storage.

        Behavior:
        - Inserts or overwrites account entry using account number as key.
        """
        self.accounts[account.getAccountNumber()] = account

    def removeAccount(self, accountNumber: int):
        """
        Removes an account from the system.

        Parameters:
        accountNumber (int):
            Account number to remove.

        Behavior:
        - Safely deletes account if it exists.
        - Does nothing if account does not exist.
        """
        if accountNumber in self.accounts:
            del self.accounts[accountNumber]
