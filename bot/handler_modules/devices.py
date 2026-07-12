from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from bot.services.device_service import (
    DeviceService,
)


RENAME_DEVICE = 1


# ==========================================================
# Private Helpers
# ==========================================================

STATUS_ORDER = {

    "active": 0,

    "inactive": 1,

    "blocked": 2,

}


def _sort_devices(
    devices,
):

    devices["devices"] = sorted(

        devices["devices"],

        key=lambda device: (

            STATUS_ORDER.get(
                device["device_status"].lower(),
                99,
            ),

            device["device_name"].lower(),

        ),

    )

    return devices


def _build_devices_text(
    devices,
):

    used_slots = (

        devices["allowed_devices"]

        - devices["available_slots"]

    )

    text = (

        "💻 Manage Devices\n\n"

        f"Slots: {used_slots} / "

        f"{devices['allowed_devices']}\n\n"

    )

    if not devices["devices"]:

        return (

            text

            + "No registered devices found.\n\n"

            "Connect to BryanNet WiFi and your "

            "first device will be registered "

            "automatically."

        )

    status_icons = {

        "active": "🟢",

        "inactive": "⚪",

        "blocked": "🔴",

    }

    for device in devices["devices"]:

        status = (
            device["device_status"]
            .lower()
        )

        icon = status_icons.get(
            status,
            "⚫",
        )

        text += (

            f"{icon} "

            f"{device['device_name']}\n"

            f"   {status.title()}\n\n"

        )

    return text


def _build_devices_keyboard(
    devices,
):

    keyboard = []

    for device in devices["devices"]:

        keyboard.append(

            [

                InlineKeyboardButton(

                    device["device_name"],

                    callback_data=(
                        f"device_{device['device_id']}"
                    ),

                )

            ]

        )

    return InlineKeyboardMarkup(
        keyboard,
    )


def _build_actions_keyboard(
    device,
):

    device_id = device["device_id"]

    status = (
        device["device_status"]
        .lower()
    )

    keyboard = [

        [

            InlineKeyboardButton(

                "✏ Rename",

                callback_data=(
                    f"rename_{device_id}"
                ),

            )

        ]

    ]

    if status == "active":

        keyboard.append(

            [

                InlineKeyboardButton(

                    "⚪ Deactivate",

                    callback_data=(
                        f"deactivate_{device_id}"
                    ),

                )

            ]

        )

        keyboard.append(

            [

                InlineKeyboardButton(

                    "🚫 Block",

                    callback_data=(
                        f"block_{device_id}"
                    ),

                )

            ]

        )

    elif status == "inactive":

        keyboard.append(

            [

                InlineKeyboardButton(

                    "🟢 Activate",

                    callback_data=(
                        f"activate_{device_id}"
                    ),

                )

            ]

        )

        keyboard.append(

            [

                InlineKeyboardButton(

                    "🚫 Block",

                    callback_data=(
                        f"block_{device_id}"
                    ),

                )

            ]

        )

    elif status == "blocked":

        keyboard.append(

            [

                InlineKeyboardButton(

                    "✅ Unblock",

                    callback_data=(
                        f"unblock_{device_id}"
                    ),

                )

            ]

        )

    keyboard.append(

        [

            InlineKeyboardButton(

                "⬅ Back",

                callback_data="devices",

            )

        ]

    )

    return InlineKeyboardMarkup(
        keyboard,
    )


async def _refresh_devices(
    message,
    telegram_user_id,
):

    devices = DeviceService.get_devices(
        telegram_user_id,
    )

    if devices is None:

        await message.reply_text(
            "Unable to retrieve devices.",
        )

        return

    devices = _sort_devices(
        devices,
    )

    await message.reply_text(

        _build_devices_text(
            devices,
        ),

        reply_markup=_build_devices_keyboard(
            devices,
        ),

    )


async def _refresh_device_details(
    message,
    telegram_user_id,
    device_id,
    context,
):

    devices = DeviceService.get_devices(
        telegram_user_id,
    )

    if devices is None:

        await message.reply_text(
            "Unable to retrieve devices.",
        )

        return

    selected_device = next(

        (

            device

            for device

            in devices["devices"]

            if device["device_id"] == device_id

        ),

        None,

    )

    if selected_device is None:

        await message.reply_text(
            "Device not found.",
        )

        return

    context.user_data[
        "selected_device"
    ] = selected_device

    status_icons = {

        "active": "🟢",

        "inactive": "⚪",

        "blocked": "🔴",

    }

    status = (
        selected_device["device_status"]
        .lower()
    )

    icon = status_icons.get(
        status,
        "⚫",
    )

    await message.reply_text(

        "💻 Device\n\n"

        "Name\n"

        f"{selected_device['device_name']}\n\n"

        "Status\n"

        f"{icon} {status.title()}",

        reply_markup=_build_actions_keyboard(
            selected_device,
        ),

    )


# ==========================================================
# Device Management
# ==========================================================

async def devices(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await send_devices(

        update.message,

        update.effective_user.id,

    )


async def send_devices(
    message,
    telegram_user_id,
):

    await _refresh_devices(

        message,

        telegram_user_id,

    )


async def device_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    device_id = int(
        query.data.split("_")[1]
    )

    await query.delete_message()

    await _refresh_device_details(

        query.message,

        update.effective_user.id,

        device_id,

        context,

    )


# ==========================================================
# Navigation
# ==========================================================

async def back_to_devices(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.delete_message()

    await _refresh_devices(

        query.message,

        update.effective_user.id,

    )
    
# ==========================================================
# Rename Device
# ==========================================================

async def rename_device_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    selected_device = context.user_data.get(
        "selected_device",
    )

    if selected_device is None:

        await query.answer(
            "Device not found.",
            show_alert=True,
        )

        return

    context.user_data[
        "awaiting_device_name"
    ] = True

    context.user_data[
        "rename_device_id"
    ] = selected_device["device_id"]

    await query.edit_message_text(

        "✏ Rename Device\n\n"

        "Current Name\n"

        f"{selected_device['device_name']}\n\n"

        "Send the new device name.",

    )

async def rename_device_finish(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not context.user_data.get(
        "awaiting_device_name",
    ):

        return

    device_id = context.user_data.get(
        "rename_device_id",
    )

    telegram_user_id = (
        update.effective_user.id
    )

    device = DeviceService.rename_device(

        telegram_user_id,

        device_id,

        update.message.text.strip(),

    )

    context.user_data.pop(
        "awaiting_device_name",
        None,
    )

    context.user_data.pop(
        "rename_device_id",
        None,
    )

    if device is None:

        await update.message.reply_text(
            "Unable to rename device.",
        )

        return

    await update.message.reply_text(
        "✅ Device renamed.",
    )

    await _refresh_device_details(

        update.message,

        telegram_user_id,

        device_id,

        context,

    )

# ==========================================================
# Device Actions
# ==========================================================

async def activate_device(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    device_id = int(
        query.data.split("_")[1]
    )

    telegram_user_id = (
        update.effective_user.id
    )

    device = DeviceService.activate_device(

        telegram_user_id,

        device_id,

    )

    if device is None:

        await query.answer(
            "Unable to activate device.",
            show_alert=True,
        )

        return

    await query.delete_message()

    await _refresh_device_details(

        query.message,

        telegram_user_id,

        device_id,

        context,

    )


async def deactivate_device(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    device_id = int(
        query.data.split("_")[1]
    )

    telegram_user_id = (
        update.effective_user.id
    )

    device = DeviceService.deactivate_device(

        telegram_user_id,

        device_id,

    )

    if device is None:

        await query.answer(
            "Unable to deactivate device.",
            show_alert=True,
        )

        return

    await query.delete_message()

    await _refresh_device_details(

        query.message,

        telegram_user_id,

        device_id,

        context,

    )


async def block_device(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    device_id = int(
        query.data.split("_")[1]
    )

    telegram_user_id = (
        update.effective_user.id
    )

    device = DeviceService.block_device(

        telegram_user_id,

        device_id,

    )

    if device is None:

        await query.answer(
            "Unable to block device.",
            show_alert=True,
        )

        return

    await query.delete_message()

    await _refresh_device_details(

        query.message,

        telegram_user_id,

        device_id,

        context,

    )


async def unblock_device(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    device_id = int(
        query.data.split("_")[1]
    )

    telegram_user_id = (
        update.effective_user.id
    )

    device = DeviceService.unblock_device(

        telegram_user_id,

        device_id,

    )

    if device is None:

        await query.answer(
            "Unable to unblock device.",
            show_alert=True,
        )

        return

    await query.delete_message()

    await _refresh_device_details(

        query.message,

        telegram_user_id,

        device_id,

        context,

    )