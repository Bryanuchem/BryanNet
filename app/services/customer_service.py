from app.models.customer import Customer


class CustomerService:

    @staticmethod
    def create_customer(
        db,
        phone_number,
        full_name,
        telegram_user_id=None
    ):

        customer = Customer(
            phone_number=phone_number,
            full_name=full_name,
            telegram_user_id=telegram_user_id
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer
    
    @staticmethod
    def start_onboarding(
        db,
        telegram_user_id
    ):
        """
        Starts onboarding for a Telegram user.

        If the user already exists, return the existing record.
        Otherwise create a new incomplete customer.
        """

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if customer:
            return customer

        customer = Customer(
            telegram_user_id=telegram_user_id,
            is_registered=False,
            registration_step="NAME"
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer    

    @staticmethod
    def update_name(
        db,
        telegram_user_id,
        full_name
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:
            return None

        customer.full_name = full_name
        customer.registration_step = "PHONE"

        db.commit()
        db.refresh(customer)

        return customer
    
    @staticmethod
    def update_phone(
        db,
        telegram_user_id,
        phone_number
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:
            return None

        customer.phone_number = phone_number
        customer.is_registered = True
        customer.registration_step = "COMPLETE"

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def get_customer_by_phone(
        db,
        phone_number
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number
            )
            .first()
        )
        
    @staticmethod
    def get_customer_by_telegram_id(
        db,
        telegram_user_id
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id
                == telegram_user_id
            )
            .first()
        )