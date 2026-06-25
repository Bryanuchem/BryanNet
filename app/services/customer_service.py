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