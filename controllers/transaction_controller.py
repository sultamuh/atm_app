"""
Transaction Controller

Handles command routing and transaction execution.
"""

from models.session_manager import SessionManager
from utilities.file_manager import FileManager
from io_layer.console_io import ConsoleIO
from enums.session_mode import SessionMode
from enums.transaction_code import TransactionCode
from enums.bill_company import BillCompany
from enums.account_status import AccountStatus
from enums.transaction_plan import TransactionPlan
from models.account import Account


class TransactionController:
    def __init__(
        self, session: SessionManager, fileManager: FileManager, console: ConsoleIO
    ):
        """
        Initializes the TransactionController.

        Parameters:
        session (SessionManager):
            Handles login state, session transactions, and account manager access.

        fileManager (FileManager):
            Handles file read/write operations for system persistence.

        console (ConsoleIO):
            Handles user input and output display operations.

        Initializes:
        - Internal references to session, file manager, and console
        - Command routing dictionary mapping command strings to handler functions
        """

        self.session = session
        self.fileManager = fileManager
        self.console = console

        # Command routing map - maps user input commands to execution methods
        self.commands = {
            "LOGIN": self.executeLogin,
            "LOGOUT": self.executeLogout,
            "WITHDRAWAL": self.executeWithdrawal,
            "TRANSFER": self.executeTransfer,
            "PAYBILL": self.executePaybill,
            "DEPOSIT": self.executeDeposit,
            "CREATE": self.executeCreateAcct,
            "DELETE": self.executeDeleteAcct,
            "DISABLE": self.executeDisableAcct,
            "CHANGEPLAN": self.executeChangePlan,
        }

    def processInput(self, input_str: str):
        """
        Processes raw user command input and routes it to the correct transaction handler.

        Parameters:
        input_str (str):
            Raw command string entered by the user.

        Responsibilities:
        - Normalize input (strip + uppercase)
        - Validate command exists
        - Enforce login rules
        - Route execution to mapped command handler
        """

        cmd = input_str.strip().upper()

        # Validate command exists in command dictionary
        if cmd not in self.commands:
            self.console.writeError(
                f"Invalid command. Valid commands: {', '.join(self.commands.keys())}"
            )
            return

        # Prevent non-login commands when not logged in
        if cmd != "LOGIN" and not self.session.isLoggedIn:
            self.console.writeError("You must login first.")
            return

        # Prevent logging in again when already logged in
        if cmd == "LOGIN" and self.session.isLoggedIn:
            self.console.writeError(
                "You are already logged in. Logout first to login again."
            )
            return

        # Execute routed command
        self.commands[cmd]()

    def executeLogin(self):
        """
        Handles user login process.

        Responsibilities:
        - Prompts user for session mode (STANDARD or ADMIN)
        - Prompts for username if STANDARD mode
        - Calls session manager login
        - Displays login confirmation message
        """

        mode_str = self.console.readChoice(
            "Enter session mode (STANDARD / ADMIN): ",
            [mode.name for mode in SessionMode],
        )

        # Convert string selection to SessionMode enum
        mode = SessionMode[mode_str.upper()]

        username = ""
        # Only STANDARD mode requires username input
        if mode == SessionMode.STANDARD:
            username = self.console.readLine("Enter account holder name: ").strip()

        # Perform session login
        self.session.login(mode, username)

        self.console.writeLine(f"Logged in as {mode.name} mode. Welcome {username}!")

    def executeLogout(self):
        """
        Handles logout process.

        Responsibilities:
        - Ends session via SessionManager
        - Retrieves logged transactions
        - Displays transaction output records to console
        """

        transactions = self.session.logout()

        self.console.writeLine("Session ended. Transactions written:")
        for t in transactions:
            self.console.writeLine(t.toFileString())

    def executeWithdrawal(self):
        """
        Handles withdrawal transaction.

        Responsibilities:
        - Collect account + amount input
        - Validate session transaction limits
        - Validate sufficient balance
        - Deduct balance
        - Log transaction record
        """

        holder_name, account_number, amount = self._getAccountTransactionInput()

        # Check session limit rules
        if not self.session.checkSessionLimits(TransactionCode.WITHDRAWAL, amount):
            self.console.writeError("Withdrawal exceeds session limit.")
            return

        account = self.session.accountManager.getAccount(account_number)

        # Check if account exists
        if not account:
            self.console.writeError(f"Account {account_number} does not exist.")
            return

        # Validate sufficient funds
        if account.getBalance() - amount < 0:
            self.console.writeError("Insufficient funds.")
            return

        # Apply balance change
        account.setBalance(account.getBalance() - amount)

        # Create transaction record
        record = self._createTransactionRecord(
            TransactionCode.WITHDRAWAL, holder_name, account_number, amount
        )

        self.session.logTransaction(record)
        self.console.writeLine("Withdrawal successful.")

    def executeTransfer(self):
        """
        Handles transfer transaction.

        Responsibilities:
        - Collect source/destination account input
        - Validate session limits
        - Validate sufficient source balance
        - Apply debit and credit operations
        - Log transaction record
        """

        holder_name, from_acc, to_acc, amount = self._getTransferInput()

        if not self.session.checkSessionLimits(TransactionCode.TRANSFER, amount):
            self.console.writeError("Transfer exceeds session limit.")
            return

        from_account = self.session.accountManager.getAccount(from_acc)
        to_account = self.session.accountManager.getAccount(to_acc)

        # Check if accounts exist
        if not from_account:
            self.console.writeError(f"Source account {from_acc} does not exist.")
            return
        if not to_account:
            self.console.writeError(f"Destination account {to_acc} does not exist.")
            return

        if from_account.getBalance() - amount < 0:
            self.console.writeError("Insufficient funds in source account.")
            return

        # Apply transfer balance changes
        from_account.setBalance(from_account.getBalance() - amount)
        to_account.setBalance(to_account.getBalance() + amount)

        record = self._createTransactionRecord(
            TransactionCode.TRANSFER,
            holder_name,
            from_acc,
            amount,
            miscInfo=str(to_acc),
        )

        self.session.logTransaction(record)
        self.console.writeLine("Transfer successful.")

    def executePaybill(self):
        """
        Handles bill payment transaction.

        Responsibilities:
        - Collect account + company + amount input
        - Validate session limits
        - Validate sufficient funds
        - Deduct balance
        - Log transaction record with company info
        """

        holder_name, account_number, amount, company = self._getPaybillInput()

        if not self.session.checkSessionLimits(TransactionCode.PAYBILL, amount):
            self.console.writeError("Payment exceeds session limit.")
            return

        account = self.session.accountManager.getAccount(account_number)

        # Check if account exists
        if not account:
            self.console.writeError(f"Account {account_number} does not exist.")
            return

        if account.getBalance() - amount < 0:
            self.console.writeError("Insufficient funds.")
            return

        account.setBalance(account.getBalance() - amount)

        record = self._createTransactionRecord(
            TransactionCode.PAYBILL,
            holder_name,
            account_number,
            amount,
            miscInfo=company.name,
        )

        self.session.logTransaction(record)
        self.console.writeLine("Bill payment successful.")

    def executeDeposit(self):
        """
        Handles deposit transaction.

        Responsibilities:
        - Collect account + amount input
        - Create deposit transaction record
        - Log transaction (no balance update here by design)
        """

        holder_name, account_number, amount = self._getAccountTransactionInput(
            deposit=True
        )

        record = self._createTransactionRecord(
            TransactionCode.DEPOSIT, holder_name, account_number, amount
        )

        self.session.logTransaction(record)
        self.console.writeLine("Deposit recorded.")

    def executeCreateAcct(self):
        """
        Handles account creation transaction (ADMIN only).

        Responsibilities:
        - Validate ADMIN mode access
        - Collect account holder name
        - Collect initial balance
        - Generate new account number
        - Create Account object
        - Register account in AccountManager
        - Log transaction record
        """

        if self.session.getCurrentMode() != SessionMode.ADMIN:
            self.console.writeError("Create account allowed only in ADMIN mode.")
            return

        name = self.console.readLine("Enter new account holder name: ").strip()[:20]

        balance = self.console.readFloat(
            "Enter initial balance: ", min_value=0, max_value=99999.99
        )

        # Generate next account number
        account_number = max(self.session.accountManager.accounts.keys(), default=0) + 1

        account = Account(account_number, name, balance)

        self.session.accountManager.addAccount(account)

        record = self._createTransactionRecord(
            TransactionCode.CREATE, name, account_number, balance
        )

        self.session.logTransaction(record)
        self.console.writeLine("Account created successfully.")

    def executeDeleteAcct(self):
        """
        Wrapper for DELETE admin account action.
        """
        self._adminAccountAction(TransactionCode.DELETE, "delete")

    def executeDisableAcct(self):
        """
        Wrapper for DISABLE admin account action.
        """
        self._adminAccountAction(TransactionCode.DISABLE, "disable")

    def executeChangePlan(self):
        """
        Wrapper for CHANGE PLAN admin account action.
        """
        self._adminAccountAction(TransactionCode.CHANGEPLAN, "change plan")

    # Helpers

    def _getAccountTransactionInput(self, deposit=False):
        """
        Collects account transaction input for withdrawal or deposit.

        Parameters:
        deposit (bool):
            Indicates if input is for deposit transaction (currently unused logically).

        Returns:
        tuple: (holder_name, account_number, amount)
        """

        if self.session.getCurrentMode() == SessionMode.ADMIN:
            holder_name = self.console.readLine("Enter account holder name: ").strip()
        else:
            holder_name = self.session.currentUser

        account_number = self.console.readInt("Enter account number: ")
        amount = self.console.readFloat("Enter amount: ", min_value=0)

        return holder_name, account_number, amount

    def _getTransferInput(self):
        """
        Collects transfer transaction input.

        Returns:
        tuple: (holder_name, source_account, destination_account, amount)
        """

        if self.session.getCurrentMode() == SessionMode.ADMIN:
            holder_name = self.console.readLine("Enter account holder name: ").strip()
        else:
            holder_name = self.session.currentUser

        from_acc = self.console.readInt("Enter source account number: ")
        to_acc = self.console.readInt("Enter destination account number: ")
        amount = self.console.readFloat("Enter transfer amount: ", min_value=0)

        return holder_name, from_acc, to_acc, amount

    def _getPaybillInput(self):
        """
        Collects bill payment input.

        Returns:
        tuple: (holder_name, account_number, amount, company_enum)
        """

        if self.session.getCurrentMode() == SessionMode.ADMIN:
            holder_name = self.console.readLine("Enter account holder name: ").strip()
        else:
            holder_name = self.session.currentUser

        account_number = self.console.readInt("Enter account number: ")

        company_choice = self.console.readChoice(
            "Enter bill company (EC / CQ / FI): ", [c.name for c in BillCompany]
        )

        company = BillCompany[company_choice.upper()]

        amount = self.console.readFloat("Enter amount to pay: ", min_value=0)

        return holder_name, account_number, amount, company

    def _createTransactionRecord(
        self, code: TransactionCode, holder_name, account_number, amount, miscInfo=""
    ):
        """
        Creates a TransactionRecord object.

        Parameters:
        code (TransactionCode): Transaction enum code
        holder_name (str): Account holder name
        account_number (int): Account number
        amount (float): Transaction amount
        miscInfo (str): Additional transaction info (e.g., destination account, company)

        Returns:
        TransactionRecord
        """

        from models.transaction_record import TransactionRecord

        return TransactionRecord(code, holder_name, account_number, amount, miscInfo)

    def _adminAccountAction(self, code: TransactionCode, action_name: str):
        """
        Generic handler for admin account modification actions.

        Supports:
        - DELETE account
        - DISABLE account
        - CHANGE PLAN

        Parameters:
        code (TransactionCode):
            Enum representing transaction action.

        action_name (str):
            Human-readable action name for messaging.
        """

        if self.session.getCurrentMode() != SessionMode.ADMIN:
            self.console.writeError(
                f"{action_name.capitalize()} allowed only in ADMIN mode."
            )
            return

        holder_name = self.console.readLine("Enter account holder name: ").strip()

        account_number = self.console.readInt(
            f"Enter account number to {action_name}: "
        )

        account = self.session.accountManager.getAccount(account_number)

        if not account or account.getHolderName() != holder_name:
            self.console.writeError("Invalid account or holder name.")
            return

        # Perform specific admin action based on transaction code
        if code == TransactionCode.DISABLE:
            account.setStatus(AccountStatus.DISABLED)

        elif code == TransactionCode.CHANGEPLAN:
            if account.getPlan() == TransactionPlan.STUDENT_PLAN:
                account.setPlan(TransactionPlan.NON_STUDENT_PLAN)

        elif code == TransactionCode.DELETE:
            self.session.accountManager.removeAccount(account_number)

        record = self._createTransactionRecord(code, holder_name, account_number, 0)

        self.session.logTransaction(record)

        self.console.writeLine(f"{action_name.capitalize()} successful.")
