import requests

# Telegram
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

# Local
from bot.config import API_BASE_URL
from bot.session import render_session
from bot.services.customer_service import CustomerService
from bot.services.session_service import SessionService

from bot.handler_modules.subscriptions import (
    send_status,
    send_plans
)

from bot.handler_modules.devices import (
    send_devices
)

from bot.keyboards import get_main_keyboard

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_user_id = update.effective_user.id

    session = SessionService.get_session(
        telegram_user_id
    )

    if session is None:

        await update.message.reply_text(
            "Unable to retrieve your session."
        )

        return

    if session["next_action"] == "START_ONBOARDING":

        success = CustomerService.start_onboarding(
            telegram_user_id
        )

        if not success:

            await update.message.reply_text(
                "Unable to start onboarding."
            )

            return

        await render_session(
            update.message,
            telegram_user_id
        )

        return

    if session["next_action"] == "ENTER_PHONE":

        session["message"] = (
            "Let's continue your onboarding.\n\n"
            + session["message"]
        )

    await render_session(
        update.message,
        telegram_user_id,
        session=session
    )
       
async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "🛰️ *BryanNet Assistant*\n\n"
        "Choose an option below to get started.\n\n"

        "📊 *My Status*\n"
        "View your active subscription and connection.\n\n"

        "📋 *View Plans*\n"
        "Browse all available internet plans.\n\n"

        "🌐 *Buy Internet*\n"
        "Purchase a new internet plan.\n\n"

        "💻 *My Devices*\n"
        "View and manage your registered devices.\n\n"

        "❌ *Remove Device*\n"
        "Remove one of your registered devices.\n\n"

        "💬 *Need help?*\n"
        "Reply to any message to contact BryanNet support."
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "status":

        await send_status(
            query.message,
            query.from_user.id
        )
    elif query.data == "plans":

        await send_plans(
            query.message
        )    
    elif query.data == "devices":

        await send_devices(
            query.message,
            query.from_user.id
        )        
    elif query.data == "buy":

        response = requests.get(
            f"{API_BASE_URL}/plans"
        )

        plans = response.json()

        keyboard = []

        for plan in plans:

            keyboard.append([
                InlineKeyboardButton(
                    f"{plan['plan_name']} - ₦{plan['price']}",
                    callback_data=f"buy_{plan['plan_id']}"
                )
            ])

        await query.edit_message_text(
            "🌐 Choose a Plan",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )      

    elif query.data.startswith(
        "buy_"
    ):

        plan_id = int(
            query.data.split("_")[1]
        )

        response = requests.get(
            f"{API_BASE_URL}/plans"
        )

        if response.status_code != 200:

            await query.edit_message_text(
                "Unable to retrieve plans."
            )

            return

        plans = response.json()

        selected_plan = next(

            (
                plan
                for plan in plans
                if plan["plan_id"] == plan_id
            ),

            None

        )

        if not selected_plan:

            await query.edit_message_text(
                "Plan not found."
            )

            return

        duration = selected_plan[
            "duration_days"
        ]

        if duration == 0:

            duration_text = "1 Hour"

        elif duration == 1:

            duration_text = "1 Day"

        else:

            duration_text = (
                f"{duration} Days"
            )

        keyboard = [

            [

                InlineKeyboardButton(

                    "✅ Confirm",

                    callback_data=
                    f"confirm_buy_{plan_id}"

                )

            ],

            [

                InlineKeyboardButton(

                    "❌ Cancel",

                    callback_data="close"

                )

            ]

        ]

        await query.edit_message_text(

            "🛒 Confirm Purchase\n\n"

            f"Plan: "
            f"{selected_plan['plan_name']}\n"

            f"Price: "
            f"₦{selected_plan['price']}\n"

            f"Speed: "
            f"{selected_plan['speed_limit_mbps']} Mbps\n"

            f"Duration: "
            f"{duration_text}",

            reply_markup=InlineKeyboardMarkup(
                keyboard
            )

        )
        
    elif query.data.startswith(
        "confirm_buy_"
    ):

        plan_id = int(
            query.data.split("_")[2]
        )

        customer_response = requests.get(
            f"{API_BASE_URL}/customers/telegram/"
            f"{query.from_user.id}"
        )

        if customer_response.status_code != 200:

            await query.edit_message_text(
                "You are not registered.\n\n"
                "Use /register first."
            )

            return

        customer = customer_response.json()

        purchase_response = requests.post(
            f"{API_BASE_URL}/subscriptions/purchase",
            json={
                "customer_id": customer["customer_id"],
                "plan_id": plan_id
            }
        )

        if purchase_response.status_code != 200:

            await query.edit_message_text(
                "Purchase failed."
            )

            return

        subscription = purchase_response.json()

        response = requests.get(
            f"{API_BASE_URL}/plans"
        )

        plans = response.json()

        selected_plan = next(

            (
                plan
                for plan in plans
                if plan["plan_id"] == plan_id
            ),

            None

        )

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

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="close"
                    )
                ]
            ]
        )

        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )        
        
    elif query.data == "close":

        await query.edit_message_reply_markup(
            reply_markup=None
        )
    
    elif query.data == "remove_device":

            customer_response = requests.get(
                f"{API_BASE_URL}/customers/telegram/"
                f"{query.from_user.id}"
            )

            if customer_response.status_code != 200:

                await query.edit_message_text(
                    "You are not registered."
                )

                return

            customer = customer_response.json()

            devices_response = requests.get(
                f"{API_BASE_URL}/devices/"
                f"{customer['customer_id']}"
            )

            if devices_response.status_code != 200:

                await query.edit_message_text(
                    "Unable to retrieve devices."
                )

                return

            device_list = devices_response.json()

            if not device_list:

                await query.edit_message_text(
                    "No registered devices found."
                )

                return

            keyboard = []

            for device in device_list:

                keyboard.append(
                    [
                        InlineKeyboardButton(
                            device["device_name"],
                            callback_data=f"remove_{device['device_id']}"
                        )
                    ]
                )

            keyboard.append(
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="close"
                    )
                ]
            )

            await query.edit_message_text(
                "💻 Select a device to remove:",
                reply_markup=InlineKeyboardMarkup(
                    keyboard
                )
            )
    elif query.data.startswith(
        "remove_"
    ):

        device_id = int(
            query.data.split("_")[1]
        )

        customer_response = requests.get(
            f"{API_BASE_URL}/customers/telegram/"
            f"{query.from_user.id}"
        )

        if customer_response.status_code != 200:

            await query.edit_message_text(
                "You are not registered."
            )

            return

        customer = customer_response.json()

        devices_response = requests.get(
            f"{API_BASE_URL}/devices/"
            f"{customer['customer_id']}"
        )

        if devices_response.status_code != 200:

            await query.edit_message_text(
                "Unable to retrieve devices."
            )

            return

        device_list = devices_response.json()

        selected_device = next(

            (
                device
                for device in device_list
                if device["device_id"] == device_id
            ),

            None

        )

        if not selected_device:

            await query.edit_message_text(
                "Device not found."
            )

            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes",
                        callback_data=f"confirm_remove_{device_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ No",
                        callback_data="remove_device"
                    )
                ]
            ]
        )

        await query.edit_message_text(
            "⚠ Confirm Device Removal\n\n"
            f"Device: {selected_device['device_name']}\n\n"
            "Are you sure you want to remove this device?",
            reply_markup=keyboard
        )
    elif query.data.startswith(
        "confirm_remove_"
    ):

        device_id = int(
            query.data.split("_")[2]
        )

        response = requests.delete(
            f"{API_BASE_URL}/devices/{device_id}"
        )

        if response.status_code != 200:

            await query.edit_message_text(
                "Unable to remove device."
            )

            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="close"
                    )
                ]
            ]
        )

        await query.edit_message_text(
            "✅ Device removed successfully.\n\n"
            "The selected device has been removed "
            "from your BryanNet account.",
            reply_markup=keyboard
        )

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Operation cancelled.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END