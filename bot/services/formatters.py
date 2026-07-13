from datetime import (
    datetime,
)


def format_duration(
    duration,
):

    duration = float(
        duration,
    )

    if duration < 1:

        return "1 Hour"

    if duration == 1:

        return "1 Day"

    if duration.is_integer():

        duration = int(
            duration,
        )

    return f"{duration} Days"

def format_currency(
    amount,
):

    return (
        f"₦{float(amount):,.2f}"
        .replace(
            ".00",
            "",
        )
    )

def format_expiry_date(
    expiry_date,
):

    if not expiry_date:

        return "N/A"

    return (

        datetime
        .fromisoformat(
            expiry_date,
        )
        .strftime(
            "%d %b %Y %H:%M",
        )

    )
    
# ==========================================================
# Payments
# ==========================================================

def format_payment_initialization(
    payment,
):

    return f"""💳 Payment Initialized

📦 Plan
{payment["plan_name"]}

💰 Amount
{format_currency(payment["amount"])}

🧾 Payment Reference
{payment["payment_reference"]}

Tap the button below to complete your payment securely.

Your subscription will be activated automatically once payment has been confirmed.
"""