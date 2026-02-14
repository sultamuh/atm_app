"""
Account Model

Represents a bank account entity.
"""

from enums.account_status import AccountStatus
from enums.transaction_plan import TransactionPlan


class Account:
    """
    Account domain object.

    Represents a single bank account within the system and stores:
    - Account identity information
    - Financial balance
    - Account operational status
    - Transaction plan type
    """

    def __init__(
        self,
        accountNumber: int,
        holderName: str,
        balance: float = 0.0,
        status: AccountStatus = AccountStatus.ACTIVE,
        plan: TransactionPlan = TransactionPlan.NON_STUDENT_PLAN,
    ):
        """
        Initializes an Account object.

        Parameters:
        accountNumber (int):
            Unique identifier for the account.

        holderName (str):
            Name of the account holder.

        balance (float):
            Starting account balance (default = 0.0).

        status (AccountStatus):
            Account operational status enum (default = ACTIVE).

        plan (TransactionPlan):
            Transaction plan enum indicating fee/limit structure (default = NON_STUDENT_PLAN).

        Notes:
        - Status and plan must always be stored as enum values (not strings).
        """
        self.accountNumber = accountNumber
        self.holderName = holderName
        self.balance = balance
        self.status = status
        self.plan = plan

    def getAccountNumber(self) -> int:
        """
        Returns the account number.

        Returns:
        int:
            Unique account identifier.
        """
        return self.accountNumber

    def getHolderName(self) -> str:
        """
        Returns the account holder name.

        Returns:
        str:
            Name of account owner.
        """
        return self.holderName

    def getBalance(self) -> float:
        """
        Returns current account balance.

        Returns:
        float:
            Current account balance value.
        """
        return self.balance

    def getStatus(self) -> AccountStatus:
        """
        Returns current account status enum.

        Returns:
        AccountStatus:
            ACTIVE or DISABLED status.
        """
        return self.status

    def getPlan(self) -> TransactionPlan:
        """
        Returns current transaction plan enum.

        Returns:
        TransactionPlan:
            STUDENT_PLAN or NON_STUDENT_PLAN.
        """
        return self.plan

    def setBalance(self, amount: float):
        """
        Updates account balance.

        Parameters:
        amount (float):
            New balance value to set.

        Notes:
        - Does not perform validation (handled at controller/service level).
        """
        self.balance = amount

    def setStatus(self, status: AccountStatus):
        """
        Updates account status.

        Parameters:
        status (AccountStatus):
            New status enum value.

        Notes:
        - Status must be enum, not string.
        """
        self.status = status

    def setPlan(self, plan: TransactionPlan):
        """
        Updates account transaction plan.

        Parameters:
        plan (TransactionPlan):
            New plan enum value.

        Notes:
        - Plan must be enum, not string.
        """
        self.plan = plan
