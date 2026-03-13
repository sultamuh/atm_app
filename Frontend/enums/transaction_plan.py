"""
Transaction Plan Enumeration

Defines account transaction fee plan.
"""

from enum import Enum


class TransactionPlan(Enum):
    STUDENT_PLAN = 1
    NON_STUDENT_PLAN = 2
