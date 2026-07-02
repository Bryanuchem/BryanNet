from enum import Enum


class PaymentProvider(str, Enum):

    PAYSTACK = "paystack"

    FLUTTERWAVE = "flutterwave"

    MONNIFY = "monnify"

    MANUAL = "manual"