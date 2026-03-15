## How to Run the Banking System Backend

### 1. Prepare the Project Files

The **Backend** folder should contain all Python source files, and the input text files should be accessible to the program.

**Required Python files:**

- account.py
- bank_system.py
- main.py
- print_error.py
- read.py
- transaction_processor.py
- write.py

**Required input files:**

- old_accounts.txt
- transactions.txt

The program will automatically create the output file:

- new_accounts.txt

Ensure that the input files are in the same directory where the program is executed, or update the file paths in `main.py` if they are located elsewhere.

---

### 2. Run the Program

Open a terminal, navigate to the Backend folder, and run:

```bash
python main.py
```

or

```bash
python3 main.py
```

---

### 3. Program Execution

When the program runs, it performs the following steps:

1. The system loads account information from `old_accounts.txt`.
2. The accounts are stored as **Account** objects in the `BankSystem`.
3. The transaction file `transactions.txt` is read line by line.
4. Each transaction is processed and applied to the corresponding account.
5. After all transactions are processed, transaction fees are applied based on the account plan type.
6. The updated account information is written to `new_accounts.txt`.

During execution, the console will display progress messages indicating when accounts are loaded, transactions are processed, and the updated accounts file is saved.

---

### 4. Output

After the program finishes running, the updated account information will be stored in `new_accounts.txt`.

This file contains the final account balances and account information after all transactions have been applied. The file will also include an **END_OF_FILE** record to mark the end of the data.

---

### 5. Error Messages

If an error occurs during processing, an error message will be displayed in the console. These messages indicate issues such as:

- Invalid transactions
- Missing accounts
- Formatting errors in the input files
