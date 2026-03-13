"""
Transaction Record Model

Represents one transaction entry for logging and file output.
"""

from enums.transaction_code import TransactionCode


class TransactionRecord:
    def __init__(
        self,
        code: TransactionCode,
        holderName: str,
        accountNumber: int,
        amount: float,
        miscInfo: str,
    ):
        """
        Initializes a transaction record.

        Parameters:
        code (TransactionCode): Type of transaction.
        holderName (str): Account holder name associated with transaction.
        accountNumber (int): Account number involved in transaction.
        amount (float): Transaction amount.
        miscInfo (str): Additional information (e.g., target account for transfer, company for paybill).
        """

        self.code = code
        self.holderName = holderName
        self.accountNumber = accountNumber
        self.amount = amount
        self.miscInfo = miscInfo

    def getFileTransactionCode(self) -> str:
        """
        Converts enum transaction code into required two-digit file code.

        Mapping follows:
        01 - Withdrawal
        02 - Transfer
        03 - Paybill
        04 - Deposit
        05 - Create
        06 - Delete
        07 - Disable
        08 - ChangePlan
        00 - End of session

        Returns:
        str: Two-digit code corresponding to the transaction.
        """
        mapping = {
            TransactionCode.WITHDRAWAL: "01",
            TransactionCode.TRANSFER: "02",
            TransactionCode.PAYBILL: "03",
            TransactionCode.DEPOSIT: "04",
            TransactionCode.CREATE: "05",
            TransactionCode.DELETE: "06",
            TransactionCode.DISABLE: "07",
            TransactionCode.CHANGEPLAN: "08",
            TransactionCode.END_OF_SESSION: "00",
        }

        return mapping.get(self.code, "00")

    def toFileString(self) -> str:
        """
        Formats the transaction record as a line suitable for writing to a file.

        Format:
        CC ACCOUNT_NUMBER HOLDER_NAME(20 chars left-justified) AMOUNT(10 chars right-justified, 2 decimals) MISC_INFO

        Returns:
        str: Formatted string for file output.
        """
        return f"{self.getFileTransactionCode()} {self.accountNumber} {self.holderName:<20} {self.amount:>10.2f} {self.miscInfo}"
