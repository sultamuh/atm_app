"""
Transaction Code Enumeration

Defines all valid transaction types.
"""

from enum import Enum


class TransactionCode(Enum):
    LOGIN = 1
    LOGOUT = 2
    WITHDRAWAL = 3
    TRANSFER = 4
    PAYBILL = 5
    DEPOSIT = 6
    CREATE = 7
    DELETE = 8
    DISABLE = 9
    CHANGEPLAN = 10
    END_OF_SESSION = 11
