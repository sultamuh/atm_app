#!/usr/bin/awk -f

# Convert frontend transaction records into backend command lines.
# Input line format is based on Frontend TransactionRecord.toFileString().

/^[0-9][0-9][[:space:]]+/ {
    code = $1
    acc = $2

    # Ignore session terminator records.
    if (code == "00") {
        next
    }

    if (code == "01") {
        # WITHDRAWAL
        amount = $NF
        printf "WITHDRAW %s %s\n", acc, amount
    } else if (code == "02") {
        # TRANSFER (destination account stored in trailing misc field)
        amount = $(NF - 1)
        dest = $NF
        printf "TRANSFER %s %s %s\n", acc, dest, amount
    } else if (code == "03") {
        # PAYBILL maps to a withdrawal from the paying account in backend model.
        amount = $(NF - 1)
        printf "WITHDRAW %s %s\n", acc, amount
    } else if (code == "04") {
        # DEPOSIT
        amount = $NF
        printf "DEPOSIT %s %s\n", acc, amount
    } else if (code == "05") {
        # CREATE account_number holder_name status balance plan
        amount = $NF
        name = ""
        for (i = 3; i <= NF - 1; i++) {
            if (name == "") {
                name = $i
            } else {
                name = name " " $i
            }
        }
        if (name == "") {
            name = "New Account"
        }
        printf "CREATE %s %s A %s NP\n", acc, name, amount
    } else if (code == "06") {
        # DELETE
        printf "DELETE %s\n", acc
    } else if (code == "07") {
        # DISABLE
        printf "DISABLE %s\n", acc
    } else if (code == "08") {
        # CHANGEPLAN (frontend only supports SP -> NP)
        printf "CHANGEPLAN %s NP\n", acc
    }
}