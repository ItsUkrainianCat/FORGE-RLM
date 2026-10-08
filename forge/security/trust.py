from __future__ import annotations

from enum import StrEnum


class TrustLevel(StrEnum):
    SYSTEM = "system"
    VERIFIED = "verified"
    USER = "user"
    RETRIEVED = "retrieved"
    TOOL_OUTPUT = "tool_output"
    UNTRUSTED = "untrusted"


def may_become_instruction(level: TrustLevel) -> bool:
    return level in {TrustLevel.SYSTEM, TrustLevel.VERIFIED, TrustLevel.USER}
