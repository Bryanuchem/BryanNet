from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)

from app.enums.next_action import (
    NextAction,
)

from bot.keyboards import (
    get_main_keyboard,
)

from bot.services.session_service import (
    SessionService,
)


async def render_session(
    message_obj,
    telegram_user_id,
    session=None,
):

    if session is None:

        session = (
            SessionService.get_session(
                telegram_user_id,
            )
        )

    if session is None:

        await message_obj.reply_text(
            "Unable to communicate with BryanNet."
        )

        return None

    next_action = session[
        "next_action"
    ]

    # ======================================================
    # Start Onboarding
    # ======================================================

    if next_action == NextAction.START_ONBOARDING.value:

        await message_obj.reply_text(

            "👋 Welcome to BryanNet!\n\n"
            "Let's get your account set up.",

            reply_markup=ReplyKeyboardRemove(),

        )

        return session

    # ======================================================
    # Enter Name
    # ======================================================

    if next_action == NextAction.ENTER_NAME.value:

        await message_obj.reply_text(

            "👋 Welcome to BryanNet!\n\n"
            "Step 1 of 2\n\n"
            "What is your full name?",

            reply_markup=ReplyKeyboardRemove(),

        )

        return session

    # ======================================================
    # Enter Phone Number
    # ======================================================

    if next_action == NextAction.ENTER_PHONE_NUMBER.value:

        keyboard = ReplyKeyboardMarkup(

            [

                [

                    KeyboardButton(

                        "📱 Share Phone Number",

                        request_contact=True,

                    )

                ]

            ],

            resize_keyboard=True,

            one_time_keyboard=True,

        )

        await message_obj.reply_text(

            "📱 Step 2 of 2\n\n"
            "Please share your phone number.",

            reply_markup=keyboard,

        )

        return session

    # ======================================================
    # Main Menu
    # ======================================================

    if next_action == NextAction.SHOW_MAIN_MENU.value:

        first_name = (
            session.get(
                "full_name",
            )
            or
            "there" 
        )

        await message_obj.reply_text(

            f"👋 Welcome, {first_name}!",

            reply_markup=get_main_keyboard(),

        )

        return session

    # ======================================================
    # Fallback
    # ======================================================

    await message_obj.reply_text(

        "Something went wrong. Please try again later.",

        reply_markup=ReplyKeyboardRemove(),

    )

    return session