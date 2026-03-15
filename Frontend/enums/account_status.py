"""
Account Status Enumeration

Defines whether an account is usable.
"""

from enum import Enum


class AccountStatus(Enum):
    ACTIVE = 1
    DISABLED = 2
