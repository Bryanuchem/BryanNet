from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
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

        return None

    next_action = session[
        "next_action"
    ]

    # ======================================================
    # Enter Name
    # ======================================================

    if next_action == NextAction.ENTER_NAME.value:

        await message_obj.reply_text(

            "👋 Welcome to BryanNet!\n\n"

            "Let's create your BryanNet account.\n"

            "This will only take a minute.\n\n"

            "Step 1 of 3\n\n"

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
    # Enter Email
    # ======================================================

    # ======================================================
    # Enter Email
    # ======================================================

    if next_action == NextAction.ENTER_EMAIL.value:

        await message_obj.reply_text(

            "📧 Step 3 of 3\n\n"
            "Almost done!\n\n"
            "Please enter your email address.\n\n"
            "Example:\n"
            "name@example.com",

            reply_markup=ReplyKeyboardRemove(),

        )

        return session

    # ======================================================
    # Main Menu
    # ======================================================

    if next_action == NextAction.SHOW_MAIN_MENU.value:

        await message_obj.reply_text(

            f"👋 Welcome, "
            f"{session['full_name']}!",

            reply_markup=get_main_keyboard(

                session[
                    "has_active_subscription"
                ],

            ),

        )

        return session

    # ======================================================
    # Fallback
    # ======================================================

    await message_obj.reply_text(

        "Something went wrong. "
        "Please try again later.",

        reply_markup=ReplyKeyboardRemove(),

    )

    return session