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
                "next_action": NextAction.ENTER_PHONE,
                "customer": customer
            }

        # Registration complete

        return {
            "next_action": NextAction.SHOW_MAIN_MENU,
            "customer": customer
        }