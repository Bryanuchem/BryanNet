from io import (
    BytesIO,
)

import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
)

from bot.services.payment_service import (
    PaymentService,
)

from bot.services.formatters import (
    format_currency,
)

from bot.keyboards import (
    get_payment_checkout_keyboard,
)

async def payment_return(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    payment_reference: str,
):

    payment = None

    for _ in range(5):
        
        payment = (
            
            
            PaymentService.get_payment(

                telegram_user_id=(
                    update.effective_user.id
                ),

                payment_reference=(
                    payment_reference
                ),

            )

        )

        if (

            payment is not None

            and

            payment["status"] == "successful"

        ):

            break

        await asyncio.sleep(
            1,
        )

    if payment is None:

        await update.message.reply_text(

            "Unable to locate that payment.",

        )

        return

    if payment["status"] == "pending":

        payment = (

            PaymentService.verify_payment(
                payment_reference,
            )

        )

    status = payment["status"]

    if status == "successful":

        pass

    elif status == "pending":

        await update.message.reply_text(

            "⏳ Your payment is still being processed.\n\n"

            "Please check again in a few moments.",

        )

        return

    elif status == "failed":

        await update.message.reply_text(

            "❌ Payment failed.\n\n"

            "No money was deducted.\n"

            "Please try again.",

        )

        return

    elif status == "cancelled":

        await update.message.reply_text(

            "🚫 This payment was cancelled.",

        )

        return

    elif status == "expired":

        await update.message.reply_text(

            "⌛ This payment has expired.\n\n"

            "Please purchase a new subscription.",

        )

        return

    elif status == "refunded":

        await update.message.reply_text(

            "💸 This payment has already been refunded.",

        )

        return

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "🧾 Receipt",

                    callback_data=(
                        f"payment_receipt_"
                        f"{payment_reference}"
                    ),

                ),

            ],

            [

                InlineKeyboardButton(

                    "📊 My Subscription",

                    callback_data=(
                        "payment_status"
                    ),

                ),

                InlineKeyboardButton(

                    "🏠 Main Menu",

                    callback_data=(
                        "payment_menu"
                    ),

                ),

            ],

        ],

    )

    if payment.get(
        "subscription_queued",
        False,
    ):

        message = (

            "🎉 Payment Successful!\n\n"

            "Thank you for choosing BryanNet.\n\n"

            "📦 Plan\n"

            f"{payment['plan_name']}\n\n"

            "💰 Amount\n"

            f"{format_currency(payment['amount'])}\n\n"

            "📄 Reference\n"

            f"{payment_reference}\n\n"

            "Your payment has been received successfully.\n\n"

            "You already have an active subscription, "

            "so this plan has been queued and "

            "will activate automatically when "

            "your current subscription expires."

        )

    else:

        message = (

            "🎉 Payment Successful!\n\n"

            "Thank you for choosing BryanNet.\n\n"

            "📦 Plan\n"

            f"{payment['plan_name']}\n\n"

            "💰 Amount\n"

            f"{format_currency(payment['amount'])}\n\n"

            "📄 Reference\n"

            f"{payment_reference}\n\n"

            "Your subscription has been "

            "activated successfully."

        )

    await update.message.reply_text(

        message,

        reply_markup=keyboard,

    )

async def payment_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "payment_history":

        await show_payments(
            update,
            context,
        )

        return


    if data.startswith(
        "payment_detail_",
    ):

        payment_reference = (

            data.removeprefix(

                "payment_detail_",

            )

        )

        await show_payment_details(

            query,

            payment_reference,

        )

        return

    if data.startswith(
        "payment_retry_",
    ):

        payment_reference = (

            data.removeprefix(
                "payment_retry_",
            )

        )

        payment = (

            PaymentService.retry_payment(

                update.effective_user.id,

                payment_reference,

            )

        )

        if payment is None:

            await query.answer(

                "Unable to retry payment.",

                show_alert=True,

            )

            return

        await query.edit_message_text(

            "💳 Payment Ready\n\n"

            "A new payment has been created for this plan.\n\n"

            "Tap the button below to continue.",

            reply_markup=(

                get_payment_checkout_keyboard(

                    payment["checkout_url"],

                )

            ),

        )

        return

    if data.startswith(
        "payment_receipt_",
    ):

        payment_reference = (
            data.removeprefix(
                "payment_receipt_",
            )
        )

        receipt = (

            PaymentService.get_receipt(

                telegram_user_id=(
                    update.effective_user.id
                ),

                payment_reference=(
                    payment_reference
                ),

            )

        )

        if receipt is None:

            await query.answer(

                "Unable to retrieve receipt.",

                show_alert=True,

            )

            return

        await query.message.reply_document(

            document=BytesIO(
                receipt,
            ),

            filename=(
                f"BryanNet Receipt - "
                f"{payment_reference}.pdf"
            ),

            caption=(

                "🧾 BryanNet Payment Receipt"

            ),

        )

        return

    if data == "payment_status":

        from bot.handler_modules.subscriptions import (
            send_status,
        )

        await send_status(

            query.message,

            update.effective_user.id,

        )

        return

    if data == "payment_menu":

        from bot.handler_modules.menu import (
            menu,
        )

        await menu(
            update,
            context,
        )

        return
    
async def show_payments(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    payments = (

        PaymentService.get_payments(

            update.effective_user.id,

        )

    )

    if not payments:

        await update.effective_message.reply_text(

            "You have not made any payments yet.",

        )

        return

    keyboard = []

    text = (

        "💳 Recent Payments\n\n"

        "Select a payment to view details.\n\n"

    )

    for payment in payments[:10]:

        created = (

            payment["created_at"][:10]

        )

        text += (

            f"{payment['status'].replace('_', ' ').title()}"

            f" • {payment['plan_name']}\n"

            f"{format_currency(payment['amount'])}"

            f" • {created}\n\n"

        )

        keyboard.append(

            [

                InlineKeyboardButton(

                    text=(

                        f"{payment['plan_name']}"

                        "\n"

                        f"{format_currency(payment['amount'])}"

                    ),

                    callback_data=(

                        "payment_detail_"

                        f"{payment['payment_reference']}"

                    ),

                )

            ]

        )

    keyboard.append(

        [

            InlineKeyboardButton(

                "🏠 Main Menu",

                callback_data="payment_menu",

            ),

        ],

    )

    await update.effective_message.reply_text(

        text,

        reply_markup=InlineKeyboardMarkup(

            keyboard,

        ),

    )
    
async def show_payment_details(
    query,
    payment_reference,
):

    payment = (

        PaymentService.get_payment_details(

            payment_reference,

        )

    )

    if payment is None:

        await query.answer(

            "Unable to load payment.",

            show_alert=True,

        )

        return

    rows = [

        [

            InlineKeyboardButton(

                "🧾 Receipt",

                callback_data=(

                    "payment_receipt_"

                    f"{payment_reference}"

                ),

            ),

        ],

    ]

    if payment["status"] in (

        "failed",

        "expired",

        "cancelled",

    ):

        rows.append(

            [

                InlineKeyboardButton(

                    "🔄 Retry Payment",

                    callback_data=(

                        "payment_retry_"

                        f"{payment_reference}"

                    ),

                ),

            ]

        )

    rows.append(

        [

            InlineKeyboardButton(

                "📊 My Subscription",

                callback_data="payment_status",

            ),

            InlineKeyboardButton(

                "◀ Back",

                callback_data="payment_history",

            ),

        ]

    )

    rows.append(

        [

            InlineKeyboardButton(

                "🏠 Main Menu",

                callback_data="payment_menu",

            ),

        ]

    )

    keyboard = InlineKeyboardMarkup(

        rows,

    )

    created = (

        payment["created_at"][:10]

    )

    paid = (

        payment["payment_date"][:10]

        if payment["payment_date"]

        else "Not yet paid"

    )

    await query.edit_message_text(

        "💳 Payment Details\n\n"

        "📦 Plan\n"

        f"{payment['plan_name']}\n\n"

        "💰 Amount\n"

        f"{format_currency(payment['amount'])}\n\n"

        "📌 Status\n"

        f"{payment['status'].replace('_', ' ').title()}\n\n"

        "🏦 Provider\n"

        f"{payment['payment_provider'].title()}\n\n"

        "💳 Channel\n"

        f"{payment['payment_channel'].replace('_', ' ').title()}\n\n"

        "🔑 Authorization\n"

        f"{payment['authorization_code'] or 'N/A'}\n\n"

        "📅 Created\n"

        f"{created}\n\n"

        "💵 Paid\n"

        f"{paid}\n\n"

        "📄 Reference\n"

        f"{payment['payment_reference']}\n\n"

        "🌐 Gateway Status\n"

        f"{(payment["gateway_status"] or "N/A").replace("_", " ")}",

        reply_markup=keyboard,

    )