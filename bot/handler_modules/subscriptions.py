from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
)

from bot.services.plan_service import (
    PlanService,
)

from bot.services.subscription_service import (
    SubscriptionService,
)

from bot.services.payment_service import (
    PaymentService,
)

from bot.services.formatters import (
    format_currency,
    format_duration,
    format_expiry_date,
)


# ==========================================================
# Plans
# ==========================================================

async def plans(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await send_plans(
        update.message,
    )


async def send_plans(
    message,
):

    plans = (
        PlanService.get_all_plans()
    )

    if plans is None:

        await message.reply_text(
            "Unable to retrieve plans.",
        )

        return

    text = (
        "🌐 Available Plans\n\n"
    )

    for index, plan in enumerate(
        plans,
        start=1,
    ):

        text += (

            f"{index}. "
            f"{plan['plan_name']}\n"

            f"💰 "
            f"{format_currency(plan['price'])}\n"

            f"⚡ "
            f"{plan['speed_limit_mbps']} Mbps\n"

            f"💻 "
            f"{plan['max_devices']} Devices "
            f"({plan['concurrent_devices']} Concurrent)\n"

            f"⏱ "
            f"{format_duration(plan['duration_days'])}"

            "\n\n"

        )

    await message.reply_text(
        text,
    )


# ==========================================================
# Subscription Status
# ==========================================================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await send_status(

        update.message,

        update.effective_user.id,

    )


async def send_status(
    message,
    telegram_user_id,
):

    status_data = (

        SubscriptionService
        .get_subscription_status(
            telegram_user_id,
        )

    )

    if status_data is None:

        await message.reply_text(

            "📡 BryanNet Subscription\n\n"

            "You do not currently have "
            "an active subscription.",

        )

        return

    text = (

        "🛰 BryanNet Subscription\n\n"

        f"🟢 "
        f"{status_data['status'].title()}\n\n"

        "📦 Plan\n"

        f"{status_data['plan_name']}\n\n"

        "⚡ Speed\n"

        f"{status_data['speed_limit_mbps']} Mbps\n\n"

        "💻 Devices\n"

        f"{status_data['max_devices']} Registered\n"

        f"{status_data['concurrent_devices']} Concurrent\n\n"

        "⏳ Remaining\n"

        f"{status_data['remaining_days']} Days\n\n"

        "📅 Expires\n"

        f"{format_expiry_date(status_data['expiry_date'])}\n\n"

        "📚 Queued Plans\n"

        f"{status_data['queued_subscriptions']}"

    )

    await message.reply_text(
        text,
    )


# ==========================================================
# Purchase Helpers
# ==========================================================

def _build_purchase_keyboard():

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "✅ Continue",

                    callback_data=(
                        "confirm_purchase"
                    ),

                ),

                InlineKeyboardButton(

                    "❌ Cancel",

                    callback_data=(
                        "cancel_purchase"
                    ),

                ),

            ],

        ],

    )


# ==========================================================
# Buy Internet
# ==========================================================

async def buy_keyboard(
    update: Update,
):

    plans = (
        PlanService.get_all_plans()
    )

    if plans is None:

        await update.message.reply_text(
            "Unable to retrieve plans.",
        )

        return

    keyboard = []

    for plan in plans:

        keyboard.append(

            [

                InlineKeyboardButton(

                    (
                        f"{plan['plan_name']} "
                        f"- {format_currency(plan['price'])}"
                    ),

                    callback_data=(
                        f"buy_{plan['plan_id']}"
                    ),

                ),

            ]

        )

    await update.message.reply_text(

        "🌐 Choose Your Internet Plan",

        reply_markup=(
            InlineKeyboardMarkup(
                keyboard,
            )
        ),

    )


async def buy_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    plan_id = int(
        query.data.split("_")[1]
    )

    plans = (
        PlanService.get_all_plans()
    )

    if plans is None:

        await query.edit_message_text(
            "Unable to retrieve plans.",
        )

        return

    selected_plan = next(

        (

            plan

            for plan

            in plans

            if plan["plan_id"] == plan_id

        ),

        None,

    )

    if selected_plan is None:

        await query.edit_message_text(
            "Plan not found.",
        )

        return

    context.user_data[
        "selected_plan"
    ] = selected_plan

    await query.edit_message_text(

        "✳ Confirm Purchase\n\n"

        "📦 Plan\n"

        f"{selected_plan['plan_name']}\n\n"

        "💰 Price\n"

        f"{format_currency(selected_plan['price'])}\n\n"

        "⚡ Speed\n"

        f"{selected_plan['speed_limit_mbps']} Mbps\n\n"

        "💻 Devices\n"

        f"{selected_plan['max_devices']} Registered\n"
        f"{selected_plan['concurrent_devices']} Concurrent\n\n"

        "⏱ Duration\n"

        f"{format_duration(selected_plan['duration_days'])}",

        reply_markup=(
            _build_purchase_keyboard()
        ),

    )
    
# ==========================================================
# Purchase Actions
# ==========================================================

async def confirm_purchase_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    selected_plan = context.user_data.get(
        "selected_plan",
    )

    if selected_plan is None:

        await query.edit_message_text(
            "No plan selected.",
        )

        return

    payment = (
        PaymentService.initialize_payment(
            telegram_user_id=(
                update.effective_user.id
            ),
            plan_id=(
                selected_plan["plan_id"]
            ),
        )
    )

    if payment is None:

        await query.edit_message_text(
            "Unable to initialize payment.",
        )

        return

    await query.edit_message_text(

        "💳 Payment Initialized\n\n"

        "📦 Plan\n"

        f"{selected_plan['plan_name']}\n\n"

        "💰 Price\n"

        f"{format_currency(selected_plan['price'])}\n\n"

        "📄 Payment Reference\n"

        f"`{payment['payment_reference']}`\n\n"

        "Complete your payment using "
        "this reference.\n\n"

        "Your subscription will be "
        "activated automatically once "
        "payment is confirmed.",

        parse_mode="Markdown",

    )

    context.user_data.pop(
        "selected_plan",
        None,
    )


async def cancel_purchase_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    context.user_data.pop(
        "selected_plan",
        None,
    )

    await query.edit_message_text(

        "❌ Purchase cancelled.",

    )