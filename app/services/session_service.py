from app.enums.keyboard import (
    KeyboardType,
)

from app.enums.next_action import (
    NextAction,
)

from app.enums.subscription_status import (
    SubscriptionStatus,
)

from app.models.customer import (
    Customer,
)

class SessionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_customer(
        db,
        telegram_user_id,
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id,
            )
            .first()
        )

    @staticmethod
    def _has_active_subscription(
        customer,
    ):

        if customer is None:

            return False

        return any(

            subscription.status
            == SubscriptionStatus.ACTIVE

            for subscription in customer.subscriptions

        )

    @staticmethod
    def _build_session(
        next_action,
        message,
        keyboard,
        customer=None,
        has_active_subscription=False,
    ):

        return {

            "next_action": next_action,

            "has_active_subscription":
                has_active_subscription,

            "message": message,

            "keyboard": keyboard,

            "customer": customer,

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_session(
        db,
        telegram_user_id,
        first_login=False,
    ):

        customer = (
            SessionService._find_customer(
                db,
                telegram_user_id,
            )
        )
        
        has_active_subscription = (
            SessionService
            ._has_active_subscription(
                customer,
            )
        )

        # ======================================================
        # Brand New Customer
        # ======================================================

        if customer is None:

            return (
                SessionService._build_session(

                    next_action=NextAction.START_ONBOARDING,

                    message="",

                    keyboard=KeyboardType.REMOVE,

                    customer=None,

                    has_active_subscription=False,

                )
            )

        # ======================================================
        # Enter Name
        # ======================================================

        if (
            customer.registration_step
            == NextAction.ENTER_NAME
        ):

            return (
                SessionService._build_session(

                    next_action=NextAction.ENTER_NAME,

                    message=(

                        "👋 Welcome to BryanNet!\n\n"

                        "Let's create your BryanNet account.\n"

                        "This will only take a minute.\n\n"

                        "Step 1 of 3\n\n"

                        "What is your full name?"

                    ),

                    keyboard=KeyboardType.REMOVE,

                    customer=customer,

                    has_active_subscription=(
                        has_active_subscription
                    ),

                )
            )

        # ======================================================
        # Enter Phone Number
        # ======================================================

        if (
            customer.registration_step
            == NextAction.ENTER_PHONE_NUMBER
        ):

            return (
                SessionService._build_session(

                    next_action=NextAction.ENTER_PHONE_NUMBER,

                    message=(
                        "📱 Step 2 of 3\n\n"
                        "Please share your phone number."
                    ),

                    keyboard=KeyboardType.REQUEST_PHONE,

                    customer=customer,

                    has_active_subscription=(
                        has_active_subscription
                    ),

                )
            )

        # ======================================================
        # Enter Email
        # ======================================================

        if (
            customer.registration_step
            == NextAction.ENTER_EMAIL
        ):

            return (
                SessionService._build_session(

                    next_action=NextAction.ENTER_EMAIL,

                    message=(

                        "📧 Step 3 of 3\n\n"

                        "Almost done!\n\n"

                        "Please enter your email address."

                    ),

                    keyboard=KeyboardType.REMOVE,

                    customer=customer,

                    has_active_subscription=(
                        has_active_subscription
                    ),

                )
            )

        # ======================================================
        # Registration Complete
        # ======================================================

        if (
            customer.registration_step
            == NextAction.COMPLETE
        ):

            if first_login:

                message = (
                    f"🎉 Registration complete!\n\n"
                    f"Welcome to BryanNet, "
                    f"{customer.full_name}!"
                )

            else:

                message = (
                    f"👋 Welcome back, "
                    f"{customer.full_name}!"
                )

            return (
                SessionService._build_session(

                    next_action=NextAction.SHOW_MAIN_MENU,

                    message=message,

                    keyboard=KeyboardType.MAIN_MENU,

                    customer=customer,

                    has_active_subscription=(
                        has_active_subscription
                    ),

                )
            )

        # ======================================================
        # Fallback
        # ======================================================

        return (
            SessionService._build_session(

                next_action=NextAction.START_ONBOARDING,

                message="",

                keyboard=KeyboardType.REMOVE,

                customer=customer,

                has_active_subscription=(
                    has_active_subscription
                ),

            )
        )