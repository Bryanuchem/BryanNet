from enum import Enum


class RouterProviderType(
    str,
    Enum,
):

    SIMULATED = "simulated"

    MIKROTIK_CHR = "mikrotik_chr"

    MIKROTIK_PHYSICAL = "mikrotik_physical"