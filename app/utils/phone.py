import re


NIGERIA_COUNTRY_CODE = "234"


def normalize_nigerian_phone_number(
    phone_number: str,
) -> str:
    """
    Normalize Nigerian phone numbers into the format:
        234XXXXXXXXX

    Examples
    --------
    0XXXXXXXXXX
        -> 234XXXXXXXXX

    8XXXXXXXXXX
        -> 234XXXXXXXXX

    +234XXXXXXXXXX
        -> 234XXXXXXXXX

    234XXXXXXXXXX
        -> 234XXXXXXXXX

    +234 XXX XXX XXX
        -> 234XXXXXXXXX
    """

    phone_number = re.sub(
        r"\D",
        "",
        phone_number,
    )

    if phone_number.startswith(
        NIGERIA_COUNTRY_CODE,
    ):
        return phone_number

    if phone_number.startswith("0"):
        return (
            NIGERIA_COUNTRY_CODE
            + phone_number[1:]
        )

    return (
        NIGERIA_COUNTRY_CODE
        + phone_number
    )