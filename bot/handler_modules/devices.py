import requests

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)


from bot.services.helpers import (
    get_customer_by_telegram_id
)

from bot.config import API_BASE_URL

REMOVE_DEVICE = 3
CONFIRM_REMOVE_DEVICE = 4


async def devices(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await send_devices(
        update.message,
        update.effective_user.id
    ) 

async def send_devices(
    message,
    telegram_user_id
):

    customer = get_customer_by_telegram_id(
        telegram_user_id
    )

    if not customer:

        await message.reply_text(
            "You are not registered. Use /register first."
        )

        return

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
   
async def remove_device_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_user_id = (
        update.effective_user.id
    )

    customer = get_customer_by_telegram_id(
        telegram_user_id
    )

    if not customer:

        await update.message.reply_text(
            "You are not registered. Use /register first."
        )

        return ConversationHandler.END

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

async def remove_device_keyboard(
    update: Update
):

    customer = get_customer_by_telegram_id(
        update.effective_user.id
    )

    if not customer:

        await update.message.reply_text(
            "You are not registered."
        )

        return

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
