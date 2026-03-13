from bank_system import BankSystem
from transaction_processor import TransactionProcessor


def main():
    """
    Main driver program for the banking system backend.

    Purpose:
        Loads the current bank accounts file, processes transactions,
        and writes the updated current accounts file.

    Input Files:
        - old_accounts.txt
        - transactions.txt

    Output File:
        - new_accounts.txt

    How to Run:
        Run this file in PyCharm using the green Run button,
        or right-click main.py and select Run.
    """
    old_accounts_file = "old_accounts.txt"
    transactions_file = "transactions.txt"
    new_accounts_file = "new_accounts.txt"

    bank_system = BankSystem()

    print("Loading accounts...")
    bank_system.load_accounts(old_accounts_file)

    print("Processing transactions...")
    processor = TransactionProcessor(bank_system)
    processor.process_transactions(transactions_file)

    print("Saving updated accounts...")
    bank_system.save_accounts(new_accounts_file)

    print("Done.")


if __name__ == "__main__":
    main()