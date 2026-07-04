from enum import Enum


class PaymentChannel(str, Enum):

    CASH = "cash"

    BANK_TRANSFER = "bank_transfer"

    CARD = "card"

    USSD = "ussd"

    WALLET = "wallet"

    SYSTEM = "system"