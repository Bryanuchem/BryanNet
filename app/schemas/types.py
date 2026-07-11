from typing import Annotated

from decimal import Decimal

from pydantic import (
    Field,
)


# ==========================================================
# Common String Types
# ==========================================================

Username = Annotated[
    str,
    Field(
        min_length=3,
        max_length=50,
    ),
]

Password = Annotated[
    str,
    Field(
        min_length=8,
        max_length=255,
    ),
]

FullName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=100,
    ),
]

PhoneNumber = Annotated[
    str,
    Field(
        min_length=11,
        max_length=20,
        pattern=r"^[0-9+\-\s()]+$",
    ),
]

PlanName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
    ),
]

RouterName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
    ),
]

LocationName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
    ),
]

MacAddress = Annotated[
    str,
    Field(
        pattern=(
            r"^([0-9A-Fa-f]{2}:){5}"
            r"[0-9A-Fa-f]{2}$"
        ),
    ),
]

IPv4Address = Annotated[
    str,
    Field(
        pattern=(
            r"^((25[0-5]|2[0-4][0-9]|"
            r"[01]?[0-9][0-9]?)\.){3}"
            r"(25[0-5]|2[0-4][0-9]|"
            r"[01]?[0-9][0-9]?)$"
        ),
    ),
]


# ==========================================================
# Common Numeric Types
# ==========================================================

PositiveInt = Annotated[
    int,
    Field(gt=0),
]

PositiveFloat = Annotated[
    float,
    Field(gt=0),
]

DeviceName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
    ),
]

PaymentMethod = Annotated[
    str,
    Field(
        min_length=2,
        max_length=50,
    ),
]

ApiUsername = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
    ),
]

ApiPassword = Annotated[
    str,
    Field(
        min_length=1,
        max_length=255,
    ),
]

PortNumber = Annotated[
    int,
    Field(
        ge=1,
        le=65535,
    ),
]

Money = Annotated[
    Decimal,
    Field(
        gt=0,
    ),
]