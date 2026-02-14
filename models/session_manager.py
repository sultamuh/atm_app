"""
Session Manager

Controls login state, session limits, and transaction logging.
"""

from enums.session_mode import SessionMode
from enums.transaction_code import TransactionCode
from models.transaction_record import TransactionRecord


class SessionManager:
    def __init__(self, accountManager):
        """
        Initializes the SessionManager.

        Parameters:
        accountManager:
            Reference to AccountManager used for account-related operations.

        Responsibilities:
        - Tracks session login state
        - Tracks current session user and mode
        - Maintains session transaction logs
        - Tracks session transaction limits (withdrawal, transfer, paybill)
        - Tracks session-level account modifications
        """

        self.accountManager = accountManager
        self.transactionLog = []
        self.currentMode: SessionMode | None = None
        self.currentUser: str = ""
        self.isLoggedIn: bool = False

        # Session limit trackers
        self.sessionWithdrawalTotal = 0.0
        self.sessionTransferTotal = 0.0
        self.sessionPaybillTotal = 0.0

        # Session state tracking
        self.pendingDeposits = {}
        self.sessionCreatedAccounts = set()
        self.sessionDeletedAccounts = set()
        self.sessionDisabledAccounts = set()

    def login(self, mode: SessionMode, username: str) -> bool:
        """
        Logs a user into the system.

        Parameters:
        mode (SessionMode):
            Session mode (STANDARD or ADMIN).

        username (str):
            Username or account holder name for session tracking.

        Returns:
        bool:
            True if login successful.
            False if already logged in.
        """

        if self.isLoggedIn:
            return False

        self.currentMode = mode
        self.currentUser = username
        self.isLoggedIn = True
        return True

    def logout(self):
        """
        Logs the user out of the system.

        Responsibilities:
        - Generates END_OF_SESSION transaction record
        - Appends record to transaction log
        - Clears login state
        - Returns session transaction log

        Returns:
        list[TransactionRecord]:
            List of all transactions performed during session.
        """

        if not self.isLoggedIn:
            return []

        end_record = TransactionRecord(
            TransactionCode.END_OF_SESSION, self.currentUser, 0, 0, ""
        )

        self.transactionLog.append(end_record)

        self.isLoggedIn = False
        self.currentUser = ""

        return self.transactionLog

    def validateTransactionPrivilege(self, code: TransactionCode) -> bool:
        """
        Validates whether current session is allowed to execute a transaction.

        Parameters:
        code (TransactionCode):
            Transaction type being requested.

        Returns:
        bool:
            True if transaction is allowed for current session state and mode.
        """

        if not self.isLoggedIn:
            # Only LOGIN allowed when not logged in
            return code == TransactionCode.LOGIN

        # Restrict admin-only operations in STANDARD mode
        if self.currentMode == SessionMode.STANDARD:
            if code in [
                TransactionCode.CREATE,
                TransactionCode.DELETE,
                TransactionCode.DISABLE,
                TransactionCode.CHANGEPLAN,
            ]:
                return False

        return True

    def checkSessionLimits(self, code: TransactionCode, amount: float) -> bool:
        """
        Checks whether a transaction exceeds session limits.

        Parameters:
        code (TransactionCode):
            Transaction type being executed.

        amount (float):
            Transaction amount.

        Returns:
        bool:
            True if transaction stays within allowed session limits.
        """

        if self.currentMode == SessionMode.STANDARD:
            if code == TransactionCode.WITHDRAWAL:
                return self.sessionWithdrawalTotal + amount <= 500.0

            elif code == TransactionCode.TRANSFER:
                return self.sessionTransferTotal + amount <= 1000.0

            elif code == TransactionCode.PAYBILL:
                return self.sessionPaybillTotal + amount <= 2000.0

        return True

    def logTransaction(self, record: TransactionRecord):
        """
        Logs a transaction into session history.

        Parameters:
        record (TransactionRecord):
            Transaction record object to append to session log.

        Behavior:
        - Appends record to transaction log list
        - Updates session transaction totals if applicable
        """

        self.transactionLog.append(record)
        self.updateSessionTotals(record.code, record.amount)

    def updateSessionTotals(self, code: TransactionCode, amount: float):
        """
        Updates session transaction totals based on transaction type.

        Parameters:
        code (TransactionCode):
            Transaction type.

        amount (float):
            Transaction amount to accumulate.
        """

        if code == TransactionCode.WITHDRAWAL:
            self.sessionWithdrawalTotal += amount

        elif code == TransactionCode.TRANSFER:
            self.sessionTransferTotal += amount

        elif code == TransactionCode.PAYBILL:
            self.sessionPaybillTotal += amount

    def generateEndSessionRecord(self):
        """
        Generates an END_OF_SESSION transaction record.

        Returns:
        TransactionRecord:
            End session transaction record object.
        """

        return TransactionRecord(
            TransactionCode.END_OF_SESSION, self.currentUser, 0, 0, ""
        )

    def getCurrentMode(self):
        """
        Returns current session mode.

        Returns:
        SessionMode | None:
            Current session mode if logged in, otherwise None.
        """
        return self.currentMode
