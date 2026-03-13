class Account:
    """
    Represents a single bank account in the banking system.
    Stores account information and provides basic account operations.
    """

    def __init__(self, account_number, name, status, balance, total_transactions=0, plan="NP"):
        """
        Initializes an Account object.

        Args:
            account_number (str): The account number.
            name (str): The account holder's name.
            status (str): Account status ('A' for active, 'D' for disabled).
            balance (float): Current account balance.
            total_transactions (int): Number of transactions completed.
            plan (str): Account plan type ('SP' or 'NP').
        """
        self.account_number = str(account_number)
        self.name = name
        self.status = status
        self.balance = float(balance)
        self.total_transactions = int(total_transactions)
        self.plan = plan

    def deposit(self, amount):
        """
        Adds money to the account balance.

        Args:
            amount (float): Amount to deposit.

        Returns:
            bool: True if successful, False otherwise.
        """
        if amount < 0:
            return False

        self.balance += amount
        self.total_transactions += 1
        return True

    def withdraw(self, amount):
        """
        Removes money from the account balance if enough funds exist.

        Args:
            amount (float): Amount to withdraw.

        Returns:
            bool: True if successful, False otherwise.
        """
        if amount < 0:
            return False

        if amount > self.balance:
            return False

        self.balance -= amount
        self.total_transactions += 1
        return True

    def disable(self):
        """
        Disables the account.

        Returns:
            None
        """
        self.status = "D"

    def change_plan(self, new_plan):
        """
        Changes the account plan type.

        Args:
            new_plan (str): New account plan ('SP' or 'NP').

        Returns:
            bool: True if successful, False otherwise.
        """
        if new_plan not in ("SP", "NP"):
            return False

        self.plan = new_plan
        return True

    def to_dict(self):
        """
        Converts the Account object into a dictionary format.

        Returns:
            dict: Dictionary containing account data.
        """
        return {
            "account_number": self.account_number,
            "name": self.name,
            "status": self.status,
            "balance": self.balance,
            "total_transactions": self.total_transactions,
            "plan": self.plan
        }