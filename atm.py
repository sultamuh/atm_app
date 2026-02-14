"""
ATM Application Entry Point

Initializes core components (console, file manager, account manager, session manager, controller)
and provides the main command loop for user interaction.
"""

from controllers.transaction_controller import TransactionController
from models.session_manager import SessionManager
from models.account_manager import AccountManager
from utilities.file_manager import FileManager
from io_layer.console_io import ConsoleIO


def main():
    """
    Main function to start the ATM application.
    Sets up all managers and runs the interactive command loop.
    """

    # Initialize I/O handler for console input/output
    console = ConsoleIO()

    # Initialize file manager to handle reading/writing accounts and transactions
    file_manager = FileManager()

    # Initialize account manager with an empty dictionary of accounts
    account_manager = AccountManager(accounts={})

    # Initialize session manager with the account manager
    session = SessionManager(account_manager)

    # Initialize transaction controller with session manager, file manager, and console I/O
    controller = TransactionController(session, file_manager, console)

    console.writeLine("===== ATM Application Started =====")

    # Main application loop
    while True:
        # Display available commands based on login state
        if not session.isLoggedIn:
            console.writeLine("Available command: LOGIN")
        else:
            # Show all commands except LOGIN when user is already logged in
            commands = [cmd for cmd in controller.commands.keys() if cmd != "LOGIN"]
            console.writeLine(f"Available commands: {', '.join(commands)}")

        console.writeLine("Type EXIT to quit the application.")

        # Read user input
        user_input = console.readLine("Enter command: ").strip()

        # Exit application if user types EXIT
        if user_input.upper() == "EXIT":
            console.writeLine("Exiting ATM application. Goodbye!")
            break

        # Pass input to controller for processing
        controller.processInput(user_input)


# Entry point for script execution
if __name__ == "__main__":
    main()
