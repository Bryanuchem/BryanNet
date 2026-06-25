import requests
from datetime import datetime

from bot.config import API_BASE_URL

from bot.keyboards import (
    get_main_keyboard,
    get_inline_menu
)

from bot.services.helpers import (
    get_customer_by_telegram_id
)

from bot.handler_modules.registration import (
    REGISTER_NAME,
    REGISTER_PHONE,
    register_start,
    register_name,
    register_phone,
    register_cancel
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


REMOVE_DEVICE = 3
CONFIRM_REMOVE_DEVICE = 4

BUY_PLAN = 5
CONFIRM_PURCHASE = 6


from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)

from bot.config import API_BASE_URL


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "📡 Welcome to BryanNet!\n\n"
        "Your personal internet self-service assistant.\n\n"
        "Whether you want to buy a plan, check your "
        "subscription, or manage your devices, "
        "I'm here to help.\n\n"
        "Type /menu to get started."
    )

    await update.message.reply_text(
        message,
        reply_markup=get_main_keyboard()
    )
        
async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "📡 BryanNet Assistant\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "👤 Account\n"
        "• /register\n"
        "  Create your BryanNet account.\n\n"

        "• /status\n"
        "  View your current subscription.\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "🌐 Internet\n"
        "• /plans\n"
        "  View available internet plans.\n\n"

        "• /buy\n"
        "  Purchase an internet plan.\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "💻 Devices\n"
        "• /devices\n"
        "  View your registered devices.\n\n"

        "• /remove_device\n"
        "  Remove one of your devices.\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "Need help?\n"
        "Reply to any message or contact BryanNet support."
    )

    await update.message.reply_text(
        message,
        reply_markup=get_inline_menu()
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
        
async def plans(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_plans(
    update.message
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
        
async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_status(
        update.message,
        update.effective_user.id
    )

async def send_devices(
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

    customer = customer_response.json()

    devices_response = requests.get(
        f"{API_BASE_URL}/devices/"
        f"{customer['customer_id']}"
    )

    if devices_response.status_code != 200:

        await message.reply_text(
            "Unable to retrieve devices."
        )

        return

    device_list = devices_response.json()

    if not device_list:

        await message.reply_text(
            "No registered devices found.\n\n"
            "Connect to BryanNet WiFi and your first device "
            "will be registered automatically."
        )

        return

    text = "💻 Registered Devices\n\n"

    for index, device in enumerate(
        device_list,
        start=1
    ):

        status = (
            device["device_status"]
            .title()
        )

        text += (
            f"{index}. {device['device_name']}\n"
            f"   Status: {status}\n\n"
        )

    await message.reply_text(
        text
    )
   
async def devices(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_devices(
        update.message,
        update.effective_user.id
    ) 

async def remove_device_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_user_id = (
        update.effective_user.id
    )

    customer_response = requests.get(
        f"{API_BASE_URL}/customers/telegram/{telegram_user_id}"
    )

    if customer_response.status_code != 200:

        await update.message.reply_text(
            "You are not registered. Use /register first."
        )

        return ConversationHandler.END

    customer = customer_response.json()

    devices_response = requests.get(
        f"{API_BASE_URL}/devices/"
        f"{customer['customer_id']}"
    )

    devices = devices_response.json()

    if not devices:

        await update.message.reply_text(
            "No registered devices found."
        )

        return ConversationHandler.END

    context.user_data["devices"] = devices

    message = (
        "Which device would you like to remove?\n\n"
    )

    for index, device in enumerate(
        devices,
        start=1
    ):

        message += (
            f"{index}. "
            f"{device['device_name']}\n"
        )

    message += (
        "\nReply with the device number."
    )

    await update.message.reply_text(
        message
    )

    return REMOVE_DEVICE

async def remove_device_selection(
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
            "Please enter a valid number."
        )

        return REMOVE_DEVICE

    devices = context.user_data.get(
        "devices",
        []
    )

    if (
        selected_index < 0
        or
        selected_index >= len(devices)
    ):

        await update.message.reply_text(
            "Invalid device number."
        )

        return REMOVE_DEVICE

    selected_device = (
        devices[selected_index]
    )

    context.user_data[
        "selected_device"
    ] = selected_device

    if len(devices) == 1:

        await update.message.reply_text(
            "You currently have 1 registered device.\n\n"
            "Removing this device will leave you "
            "with no registered devices and may "
            "interrupt your internet access.\n\n"
            "Reply YES to continue or NO to cancel."
        )

        return CONFIRM_REMOVE_DEVICE

    response = requests.delete(
        f"{API_BASE_URL}/devices/"
        f"{selected_device['device_id']}"
    )

    if response.status_code == 200:

        await update.message.reply_text(
            f"Device removed successfully.\n\n"
            f"{selected_device['device_name']} "
            f"has been removed."
        )

    else:

        await update.message.reply_text(
            "Unable to remove device."
        )

    return ConversationHandler.END
  
async def confirm_remove_device(
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
            "Device removal cancelled."
        )

        return ConversationHandler.END

    if answer != "YES":

        await update.message.reply_text(
            "Reply YES or NO."
        )

        return CONFIRM_REMOVE_DEVICE

    selected_device = (
        context.user_data[
            "selected_device"
        ]
    )

    response = requests.delete(
        f"{API_BASE_URL}/devices/"
        f"{selected_device['device_id']}"
    )

    if response.status_code == 200:

        await update.message.reply_text(
            f"Device removed successfully.\n\n"
            f"{selected_device['device_name']} "
            f"has been removed."
        )

    else:

        await update.message.reply_text(
            "Unable to remove device."
        )

    return ConversationHandler.END

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

                    callback_data="menu"

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
                        callback_data="menu"
                    )
                ]
            ]
        )

        await query.edit_message_text(
            message,
            reply_markup=keyboard
        )        

    elif query.data == "menu":

        await query.edit_message_text(
            "📡 BryanNet Assistant\n\n"
            "Choose an option below.",
            reply_markup=get_inline_menu()
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
                    callback_data="menu"
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
                        callback_data="menu"
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
  
async def keyboard_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "📊 My Status":
        await send_status(
            update.message,
            update.effective_user.id
        )

    elif text == "📋 View Plans":
        await send_plans(
            update.message
        )

    elif text == "💻 My Devices":
        await send_devices(
            update.message,
            update.effective_user.id
        )

    elif text == "🌐 Buy Internet":

        response = requests.get(
            f"{API_BASE_URL}/plans"
        )

        if response.status_code != 200:

            await update.message.reply_text(
                "Unable to retrieve plans."
            )

            return

        plans = response.json()

        keyboard = []

        for plan in plans:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{plan['plan_name']} - ₦{plan['price']}",
                        callback_data=f"buy_{plan['plan_id']}"
                    )
                ]
            )

        await update.message.reply_text(
            "🌐 Choose a Plan",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    elif text == "❌ Remove Device":

        customer_response = requests.get(
            f"{API_BASE_URL}/customers/telegram/"
            f"{update.effective_user.id}"
        )

        if customer_response.status_code != 200:

            await update.message.reply_text(
                "You are not registered."
            )

            return

        customer = customer_response.json()

        devices_response = requests.get(
            f"{API_BASE_URL}/devices/"
            f"{customer['customer_id']}"
        )

        if devices_response.status_code != 200:

            await update.message.reply_text(
                "Unable to retrieve devices."
            )

            return

        devices = devices_response.json()

        if not devices:

            await update.message.reply_text(
                "No registered devices found."
            )

            return

        keyboard = []

        for device in devices:

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
                    callback_data="menu"
                )
            ]
        )

        await update.message.reply_text(
            "💻 Select a device to remove:",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )
    elif text == "📡 Menu":
        await menu(
            update,
            context
        )
        


def register_handlers(app):

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )
    
    app.add_handler(
        CommandHandler(
            "menu",
            menu
        )
    )
        
    app.add_handler(
        CommandHandler(
            "plans",
            plans
        )
    )
    
    registration_handler = (
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    "register",
                    register_start
                )
            ],
            states={
                REGISTER_NAME: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        register_name
                    )
                ],
                REGISTER_PHONE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        register_phone
                    )
                ]
            },
            fallbacks=[
                CommandHandler(
                    "cancel",
                    register_cancel
                )
            ]
        )
    )

    app.add_handler(
        registration_handler
    )   
    
    app.add_handler(
    CommandHandler(
        "status",
        status
    )
)
    
    app.add_handler(
    CommandHandler(
        "devices",
        devices
    )
)
    
    remove_device_handler = (
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    "remove_device",
                    remove_device_start
                )
            ],
            states={
                REMOVE_DEVICE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        remove_device_selection
                    )
                ],
                CONFIRM_REMOVE_DEVICE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        confirm_remove_device
                    )
                ]
            },
            fallbacks=[
                CommandHandler(
                    "cancel",
                    register_cancel
                )
            ]
        )
    )

    app.add_handler(
        remove_device_handler
    )
    
    buy_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "buy",
                buy_start
            )
        ],
        states={
            BUY_PLAN: [
                MessageHandler(
                    filters.TEXT
                    & ~filters.COMMAND,
                    buy_plan_selection
                )
            ],
            CONFIRM_PURCHASE: [
                MessageHandler(
                    filters.TEXT
                    & ~filters.COMMAND,
                    confirm_purchase
                )
            ]            
        },
        fallbacks=[
            CommandHandler(
                "cancel",
                register_cancel
            )
        ]
    )

    app.add_handler(
        buy_handler
    )
    
    app.add_handler(
        CallbackQueryHandler(
            menu_callback
        )
    )
    
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            keyboard_handler
        )
    )