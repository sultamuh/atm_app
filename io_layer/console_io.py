"""
Console IO Layer

Handles all user input/output and validation.
"""


class ConsoleIO:
    """Handles console input/output with validation helpers."""

    def readLine(self, prompt: str = "") -> str:
        """
        Reads a line of input from the user.

        Parameters:
            prompt (str): Message displayed to the user.

        Returns:
            str: The input string entered by the user.
        """
        return input(prompt)

    def writeLine(self, message: str):
        """
        Prints a message to the console.

        Parameters:
            message (str): Message to display.
        """
        print(message)

    def writeError(self, message: str):
        """
        Prints an error message to the console, prefixed with 'Error:'.

        Parameters:
            message (str): Error message to display.
        """
        print(f"Error: {message}")

    def readChoice(
        self, prompt: str, valid_choices: list[str], case_sensitive=False
    ) -> str:
        """
        Repeatedly prompts user until a valid choice is entered.

        Parameters:
            prompt (str): Prompt message to show.
            valid_choices (list[str]): List of allowed choices.
            case_sensitive (bool): Whether comparison is case-sensitive.

        Returns:
            str: The choice entered by the user.
        """
        while True:
            choice = input(prompt).strip()

            cmp_choice = choice if case_sensitive else choice.upper()
            valid_cmp = (
                valid_choices if case_sensitive else [c.upper() for c in valid_choices]
            )

            if cmp_choice in valid_cmp:
                return choice

            self.writeError(
                f"Invalid choice. Valid options: {', '.join(valid_choices)}"
            )

    def readFloat(
        self, prompt: str, min_value: float = None, max_value: float = None
    ) -> float:
        """
        Reads a floating-point number from the user with optional bounds.

        Parameters:
            prompt (str): Prompt message to display.
            min_value (float): Minimum allowed value (inclusive).
            max_value (float): Maximum allowed value (inclusive).

        Returns:
            float: The validated float input.
        """
        while True:
            try:
                value = float(input(prompt).strip())

                if (min_value is not None and value < min_value) or (
                    max_value is not None and value > max_value
                ):
                    self.writeError(
                        f"Value must be between {min_value} and {max_value}."
                    )
                    continue

                return value

            except ValueError:
                self.writeError("Invalid number. Please enter a valid numeric value.")

    def readInt(self, prompt: str, min_value: int = None, max_value: int = None) -> int:
        """
        Reads an integer from the user with optional bounds.

        Parameters:
            prompt (str): Prompt message to display.
            min_value (int): Minimum allowed value (inclusive).
            max_value (int): Maximum allowed value (inclusive).

        Returns:
            int: The validated integer input.
        """
        while True:
            try:
                value = int(input(prompt).strip())

                if (min_value is not None and value < min_value) or (
                    max_value is not None and value > max_value
                ):
                    self.writeError(
                        f"Value must be between {min_value} and {max_value}."
                    )
                    continue

                return value

            except ValueError:
                self.writeError("Invalid number. Please enter a valid integer.")
