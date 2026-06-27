from app.models.customer import Customer

from app.enums.session import NextAction

from app.enums.keyboard import KeyboardType

class SessionService:

    @staticmethod
    def get_session(
        db,
        telegram_user_id,
        first_login=False
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        # Brand new customer

        if customer is None:

            return {
                "next_action": NextAction.START_ONBOARDING,
                "message": "",
                "keyboard": KeyboardType.REMOVE,
                "customer": None
            }

        if customer.registration_step == "START":

            return {
                "next_action": NextAction.ENTER_NAME,
                "message": (
                    "👋 Welcome to BryanNet!\n\n"
                    "Let's get your account set up.\n\n"
                    "Step 1 of 2\n\n"
                    "What is your full name?"
                ),
                "keyboard": KeyboardType.REMOVE,
                "customer": customer
            }
    
        # Existing customer still entering phone

        if customer.registration_step == "PHONE":

            return {
                "next_action": NextAction.ENTER_PHONE,
                "message": (
                    "📱 Step 2 of 2\n\n"
                    "Please share your phone number."
                ),
                "keyboard": "REQUEST_PHONE",
                "customer": customer
            }

        # Registration complete
        if customer.registration_step == "COMPLETE":

            if first_login:

                message = (
                    f"🎉 Registration complete!\n\n"
                    f"Welcome to BryanNet, {customer.full_name}!"
                )

            else:

                message = (
                    f"👋 Welcome back, {customer.full_name}!"
                )

            return {
                "next_action": NextAction.SHOW_MAIN_MENU,
                "message": message,
                "keyboard": "MAIN_MENU",
                "customer": customer
            }