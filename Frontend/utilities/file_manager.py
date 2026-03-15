"""
File Manager Utility

Responsible for:
- Reading account data from files
- Writing transaction logs to files
- Formatting helpers for file output
"""

from models.account import Account
from models.transaction_record import TransactionRecord
from typing import List, Dict


class FileManager:
    """
    Handles all file read/write operations for accounts and transactions.
    """

    def readAccountsFile(self, filePath: str) -> Dict[int, Account]:
        """
        Reads account file and returns dictionary of Account objects.

        Each line in the file should be in the format:
        accountNumber,name,balance

        Returns:
            dict[int, Account]: Keyed by account number.
        """
        accounts = {}

        try:
            with open(filePath, "r") as f:
                for line in f:
                    if line.strip():  # skip empty lines
                        acc = self.parseAccountLine(line)
                        accounts[acc.getAccountNumber()] = acc
        except FileNotFoundError:
            # If file doesn't exist, return empty dictionary
            pass

        return accounts

    def writeTransactionFile(
        self, filePath: str, transactions: List[TransactionRecord]
    ) -> None:
        """
        Writes transaction records to output file.

        Parameters:
            filePath (str): Path to output file.
            transactions (List[TransactionRecord]): Transactions to write.
        """
        with open(filePath, "w") as f:
            for t in transactions:
                f.write(t.toFileString() + "\n")

    def parseAccountLine(self, line: str) -> Account:
        """
        Converts one line from account file into Account object.

        Expected file line format:
            accountNumber,name,balance

        Parameters:
            line (str): Line from file.

        Returns:
            Account: Account object parsed from line.
        """
        parts = line.strip().split(",")

        acc_num = int(parts[0])
        name = parts[1]
        balance = float(parts[2])

        return Account(acc_num, name, balance)

    def formatTransactionLine(self, t: TransactionRecord) -> str:
        """
        Converts TransactionRecord into a formatted string for file output.

        Parameters:
            t (TransactionRecord): Transaction to format.

        Returns:
            str: Formatted string.
        """
        return t.toFileString()

    def padLeftZeros(self, value: str, length: int) -> str:
        """
        Pads string with leading zeros to reach specified length.

        Parameters:
            value (str): Original string.
            length (int): Desired total length.

        Returns:
            str: Padded string.
        """
        return value.zfill(length)

    def padRightSpaces(self, value: str, length: int) -> str:
        """
        Pads string with trailing spaces to reach specified length.

        Parameters:
            value (str): Original string.
            length (int): Desired total length.

        Returns:
            str: Padded string.
        """
        return value.ljust(length)

    def formatMoney(self, value: float) -> str:
        """
        Formats float value as money string with 2 decimals.

        Parameters:
            value (float): Amount to format.

        Returns:
            str: Formatted monetary value, e.g., "123.45"
        """
        return f"{value:0.2f}"

    def isEndOfFileAccount(self, line: str) -> bool:
        """
        Checks if the line indicates end of account file.

        Parameters:
            line (str): Line to check.

        Returns:
            bool: True if line is 'END', else False.
        """
        return line.strip() == "END"
