from fastapi import HTTPException

from app.enums.next_action import NextAction

from app.models.customer import Customer


class CustomerService:

    @staticmethod
    def register_customer(
        db,
        phone_number,
        full_name,
        telegram_user_id=None,
    ):

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        customer = Customer(
            phone_number=phone_number,
            full_name=full_name,
            telegram_user_id=telegram_user_id,
            is_registered=True,
            registration_step=NextAction.COMPLETE,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def start_onboarding(
        db,
        telegram_user_id,
    ):

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
            registration_step=NextAction.START_ONBOARDING,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def update_full_name(
        db,
        telegram_user_id,
        full_name,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.full_name = full_name

        customer.registration_step = (
            NextAction.ENTER_PHONE_NUMBER
        )

        db.commit()

        db.refresh(
            customer,
        )

        return customer

    @staticmethod
    def update_phone_number(
        db,
        telegram_user_id,
        phone_number,
    ):

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number,
                Customer.telegram_user_id != telegram_user_id,
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.phone_number = phone_number

        customer.is_registered = True

        customer.registration_step = (
            NextAction.COMPLETE
        )

        db.commit()

        db.refresh(
            customer,
        )

        return customer

    @staticmethod
    def update_customer(
        db,
        customer_id,
        customer_data,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == customer_data.phone_number,
                Customer.customer_id != customer_id,
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        customer.full_name = customer_data.full_name
        customer.phone_number = customer_data.phone_number

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def activate_customer(
        db,
        customer_id,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.status = "active"

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def deactivate_customer(
        db,
        customer_id,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.status = "inactive"

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def get_customer(
        db,
        customer_id,
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

    @staticmethod
    def get_customer_by_phone(
        db,
        phone_number,
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
        telegram_user_id,
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

    @staticmethod
    def get_all_customers(db):

        return (
            db.query(Customer)
            .order_by(Customer.customer_id)
            .all()
        )