"""
Session Mode Enumeration

Defines login privilege level.
"""

from enum import Enum


class SessionMode(Enum):
    STANDARD = 1
    ADMIN = 2
