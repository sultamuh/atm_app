from print_error import log_constraint_error


class TransactionProcessor:
    """
    Reads transaction commands from a file and applies them
    to the banking system.
    """

    def __init__(self, bank_system):
        """
        Initializes the transaction processor.

        Args:
            bank_system (BankSystem): The banking system object.
        """
        self.bank_system = bank_system

    def process_transactions(self, file_path):
        """
        Reads and processes each transaction line from a file.

        Args:
            file_path (str): Path to the transaction file.

        Returns:
            None
        """
        with open(file_path, "r") as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.strip()

                if not clean_line:
                    continue

                self.process_transaction_line(clean_line, line_num)

    def process_transaction_line(self, line, line_num):
        """
        Processes one transaction line.

        Expected simple formats:
            DEPOSIT account_number amount
            WITHDRAW account_number amount
            TRANSFER from_account to_account amount
            CREATE account_number name status balance plan
            DELETE account_number
            CHANGEPLAN account_number new_plan

        Args:
            line (str): The transaction line.
            line_num (int): Line number in the transaction file.

        Returns:
            None
        """
        parts = line.split()

        if len(parts) == 0:
            return

        command = parts[0].upper()

        try:
            if command == "DEPOSIT":
                account_number = parts[1]
                amount = float(parts[2])
                self.bank_system.deposit_to_account(account_number, amount)

            elif command == "WITHDRAW":
                account_number = parts[1]
                amount = float(parts[2])
                self.bank_system.withdraw_from_account(account_number, amount)

            elif command == "TRANSFER":
                from_account = parts[1]
                to_account = parts[2]
                amount = float(parts[3])
                self.bank_system.transfer(from_account, to_account, amount)

            elif command == "CREATE":
                account_number = parts[1]

                # CREATE format allows multi-word account names:
                # CREATE account_number <name...> status balance plan
                if len(parts) < 6:
                    raise ValueError("Invalid CREATE format")

                status = parts[-3]
                balance = float(parts[-2])
                plan = parts[-1]
                name = " ".join(parts[2:-3]).strip()

                if not name:
                    raise ValueError("CREATE requires a holder name")

                self.bank_system.create_account(account_number, name, status, balance, plan)

            elif command == "DELETE":
                account_number = parts[1]
                self.bank_system.delete_account(account_number)

            elif command == "DISABLE":
                account_number = parts[1]
                self.bank_system.disable_account(account_number)

            elif command == "CHANGEPLAN":
                account_number = parts[1]
                new_plan = parts[2]
                self.bank_system.change_account_plan(account_number, new_plan)

            else:
                log_constraint_error(
                    f"Unknown transaction type on line {line_num}",
                    "Transaction Processor"
                )

        except (IndexError, ValueError):
            log_constraint_error(
                f"Invalid transaction format on line {line_num}: {line}",
                "Transaction Processor"
            )