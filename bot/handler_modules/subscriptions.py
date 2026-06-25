import requests

from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from bot.config import API_BASE_URL

from bot.keyboards import (
    get_inline_menu
)

from bot.services.helpers import (
    format_duration,
    format_expiry_date,
    get_customer_by_telegram_id,
    get_all_plans
)

BUY_PLAN = 5
CONFIRM_PURCHASE = 6

async def plans(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_plans(
    update.message
)
    
async def send_plans(
    message
):

    response = requests.get(
        f"{API_BASE_URL}/plans"
    )

    if response.status_code != 200:

        await message.reply_text(
            "Unable to retrieve plans."
        )

        return

    plans = response.json()

    text = "🌐 Available Plans\n\n"

    for index, plan in enumerate(
        plans,
        start=1
    ):

        duration = plan["duration_days"]

        if duration == 0:
            duration_text = "1 Hour"
        elif duration == 1:
            duration_text = "1 Day"
        else:
            duration_text = f"{duration} Days"

        text += (
            f"{index}. {plan['plan_name']}\n"
            f"💰 ₦{plan['price']}\n"
            f"⚡ {plan['speed_limit_mbps']} Mbps\n"
            f"⏱ {duration_text}\n\n"
        )

    await message.reply_text(
        text
    )
       
async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_status(
        update.message,
        update.effective_user.id
    )


async def send_status(
    message,
    telegram_user_id
):

    customer_response = requests.get(
        f"{API_BASE_URL}/customers/telegram/{telegram_user_id}"
    )

    if customer_response.status_code != 200:

        await message.reply_text(
            "You are not registered. Use /register first."
        )

        return

    customer = get_customer_by_telegram_id(
        telegram_user_id
    )

    if not customer:

        await message.reply_text(
            "You are not registered."
        )

        return
    
    status_response = requests.get(
        f"{API_BASE_URL}/subscriptions/status/"
        f"{customer['customer_id']}"
    )

    if status_response.status_code != 200:

        await message.reply_text(
            "Unable to retrieve subscription status."
        )

        return

    status_data = status_response.json()

    plan_name = status_data.get(
        "plan_name"
    )

    status_value = status_data.get(
        "status"
    )

    expiry_date = status_data.get(
        "expiry_date"
    )

    if expiry_date:

        expiry_date = (
            datetime.fromisoformat(
                expiry_date
            ).strftime(
                "%d %b %Y %H:%M"
            )
        )

    queued_count = status_data.get(
        "queued_subscriptions",
        0
    )

    if not status_value:

        text = (
            "No active subscription found.\n"
            f"Queued Plans: {queued_count}"
        )

    else:

        text = (
            "📡 BryanNet Subscription\n\n"
            f"Plan: {plan_name}\n"
            f"Status: {status_value.title()}\n"
            f"Expires: {expiry_date}\n\n"
            f"Queued Plans: {queued_count}"
        )

    await message.reply_text(
        text
    )
        
        
async def buy_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    response = requests.get(
        f"{API_BASE_URL}/plans"
    )

    if response.status_code != 200:

        await update.message.reply_text(
            "Unable to retrieve plans."
        )

        return ConversationHandler.END

    plans = response.json()

    context.user_data["plans"] = plans

    message = "Available Plans\n\n"

    for index, plan in enumerate(
        plans,
        start=1
    ):

        message += (
            f"{index}. {plan['plan_name']}\n"
            f"   ₦{plan['price']}\n"
            f"   {plan['speed_limit_mbps']} Mbps\n"
            f"   {plan['duration_days']} Days\n\n"
        )

    message += (
        "Reply with the plan number."
    )

    await update.message.reply_text(
        message
    )

    return BUY_PLAN
 

async def buy_plan_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        selected_index = (
            int(update.message.text)
            - 1
        )

    except ValueError:

        await update.message.reply_text(
            "Please enter a valid plan number."
        )

        return BUY_PLAN

    plans = context.user_data.get(
        "plans",
        []
    )

    if (
        selected_index < 0
        or
        selected_index >= len(plans)
    ):

        await update.message.reply_text(
            "Invalid plan number."
        )

        return BUY_PLAN

    selected_plan = plans[selected_index]

    context.user_data["selected_plan"] = selected_plan

    duration_days = selected_plan["duration_days"]

    if duration_days == 0:
        duration_text = "1 Hour"
    elif duration_days == 1:
        duration_text = "1 Day"
    else:
        duration_text = f"{duration_days} Days"

    message = (
        "Confirm Purchase\n\n"
        f"Plan: {selected_plan['plan_name']}\n"
        f"Price: ₦{selected_plan['price']}\n"
        f"Speed: {selected_plan['speed_limit_mbps']} Mbps\n"
        f"Duration: {duration_text}\n\n"
        "Reply YES to confirm or NO to cancel."
    )

    await update.message.reply_text(
        message
    )

    return CONFIRM_PURCHASE


async def confirm_purchase(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    answer = (
        update.message.text
        .strip()
        .upper()
    )

    if answer == "NO":

        await update.message.reply_text(
            "Purchase cancelled."
        )

        return ConversationHandler.END

    if answer != "YES":

        await update.message.reply_text(
            "Reply YES or NO."
        )

        return CONFIRM_PURCHASE

    telegram_user_id = (
        update.effective_user.id
    )

    customer_response = requests.get(
        f"{API_BASE_URL}/customers/telegram/{telegram_user_id}"
    )

    if customer_response.status_code != 200:

        await update.message.reply_text(
            "Unable to locate your account."
        )

        return ConversationHandler.END

    customer = customer_response.json()

    selected_plan = context.user_data[
        "selected_plan"
    ]

    purchase_response = requests.post(
        f"{API_BASE_URL}/subscriptions/purchase",
        json={
            "customer_id": customer["customer_id"],
            "plan_id": selected_plan["plan_id"]
        }
    )

    if purchase_response.status_code != 200:

        await update.message.reply_text(
            "Purchase failed."
        )

        return ConversationHandler.END

    subscription = purchase_response.json()

    status = subscription["status"].title()

    if status == "Active":

        message = (
            "✅ Purchase Successful\n\n"
            f"Plan: {selected_plan['plan_name']}\n"
            f"Price: ₦{selected_plan['price']}\n"
            f"Status: {status}\n\n"
            "Your internet service is now active.\n\n"
            "Thank you for choosing BryanNet!"
        )

    else:

        message = (
            "✅ Purchase Successful\n\n"
            f"Plan: {selected_plan['plan_name']}\n"
            f"Price: ₦{selected_plan['price']}\n"
            f"Status: {status}\n\n"
            "Your current plan is still active.\n"
            "The new plan will activate automatically "
            "when it expires."
        )

    await update.message.reply_text(
        message
    )

    return ConversationHandler.END
            