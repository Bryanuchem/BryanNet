from app.models.customer import Customer

from app.enums.session import NextAction


class SessionService:

    @staticmethod
    def get_session(
        db,
        telegram_user_id
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
                "message": (
                    "👋 Welcome to BryanNet!\n\n"
                    "Let's get your account set up.\n\n"
                    "Step 1 of 2\n\n"
                    "What is your full name?"
                ),
                "keyboard": "REMOVE",
                "customer": None
            }


        # Existing customer still entering name

        if customer.registration_step == "NAME":

            return {
                "next_action": NextAction.ENTER_NAME,
                "customer": customer
            }

        # Existing customer still entering phone

        if customer.registration_step == "PHONE":

            return {
                "next_action": NextAction.ENTER_NAME,
                "message": (
                    "Let's continue your onboarding.\n\n"
                    "What is your full name?"
                ),
                "keyboard": "REMOVE",
                "customer": customer
            }

        # Registration complete
        if customer.registration_step == "COMPLETE":
            
            return {
                "next_action": NextAction.ENTER_PHONE,
                "message": (
                    "📱 Step 2 of 2\n\n"
                    "Please share your phone number."
                ),
                "keyboard": "REQUEST_PHONE",
                "customer": customer
            }
