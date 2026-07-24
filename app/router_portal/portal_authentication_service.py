from typing import cast

from sqlalchemy.orm import (
    Session,
)

from app.router_portal.schemas import (
    LoginRequestSchema,
    PortalAuthenticationResultSchema,
)

from app.services.router_credential_manager import (
    RouterCredentialManager,
)

from app.models.router_account import (
    RouterAccount,
)

from app.models.subscription import (
    Subscription,
)

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.enums import (
    SubscriptionStatus,
    CustomerStatus,
    PortalAuthenticationError,
)

from app.services.device_service import (
    DeviceService,
)

from app.enums import (
    DeviceStatus,
)

class PortalAuthenticationService:
    """
    Handles portal authentication business logic.

    Responsibilities:
    - Customer validation
    - Subscription validation
    - Plan validation
    - Router account validation
    - Device validation

    This service deliberately does NOT:
    - Render HTML
    - Return HTTP responses
    - Know about RouterOS
    - Interact with templates
    """

    # ==========================================================
    # Public API
    # ==========================================================

    @staticmethod
    def authenticate(
        db: Session,
        request: LoginRequestSchema,
    ) -> PortalAuthenticationResultSchema:
        """
        Authenticate a portal login request.

        Returns a structured authentication result only.
        """

        result = (

            PortalAuthenticationService

            ._validate_router_account(

                db,

                request.username,

            )

        )
        
        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_customer(

                result.router_account,

            )

        )
       
        
        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_password(

                request.password,

                result.router_account,

            )

        )

        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_subscription(

                db,

                result,

            )

        )


        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_plan(

                result,

            )

        )

        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_device(

                db,

                result,

                request.mac_address,

            )

        )

        if not result.success:

            return result

        result = (

            PortalAuthenticationService

            ._validate_concurrent_device_limit(

                db,

                result,

            )

        )

        if not result.success:

            return result
        
        return (

            PortalAuthenticationService

            ._validate_registered_device_limit(

                db,

                result,

            )

        )
        
    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _validate_concurrent_device_limit(
        db: Session,
        result: PortalAuthenticationResultSchema,
    ) -> PortalAuthenticationResultSchema:

        online_devices = (

            DeviceService

            .count_online_devices(

                db,

                result.customer.customer_id,

            )

        )

        if (

            online_devices

            >=

            result.plan.concurrent_devices

        ):

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError

                    .CONCURRENT_DEVICE_LIMIT_REACHED,

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=result.subscription,

                    plan=result.plan,

                    device=result.device,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=result.router_account,

                customer=result.customer,

                subscription=result.subscription,

                plan=result.plan,

                device=result.device,

            )

        )

    @staticmethod
    def _validate_registered_device_limit(
        db: Session,
        result: PortalAuthenticationResultSchema,
    ) -> PortalAuthenticationResultSchema:

        registered_devices = (

            DeviceService

            .count_registered_devices(

                db,

                result.customer.customer_id,

            )

        )

        if (

            registered_devices

            >

            result.plan.max_devices

        ):

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError

                    .REGISTERED_DEVICE_LIMIT_REACHED,

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=result.subscription,

                    plan=result.plan,

                    device=result.device,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=result.router_account,

                customer=result.customer,

                subscription=result.subscription,

                plan=result.plan,

                device=result.device,

            )

        )

    @staticmethod
    def _success(
        **kwargs,
    ) -> PortalAuthenticationResultSchema:

        return PortalAuthenticationResultSchema(

            success=True,

            **kwargs,

        )

    @staticmethod
    def _failure(
        error: PortalAuthenticationError,
        **kwargs,
    ) -> PortalAuthenticationResultSchema:

        return PortalAuthenticationResultSchema(

            success=False,

            error=error,

            **kwargs,

        )

    # ==========================================================
    # Validation
    # ==========================================================

    @staticmethod
    def _validate_router_account(
        db: Session,
        username: str,
    ) -> PortalAuthenticationResultSchema:

        # ==========================================================
        # Router Username
        # ==========================================================
        
        router_username = (

            RouterUsernameService

            .to_router_username(

                username,

            )

        )
        
        # ==========================================================
        # Router Account
        # ==========================================================

        router_account = (

            db.query(

                RouterAccount,

            )

            .filter(

                RouterAccount.username
                == router_username,

            )

            .first()

        )

        if router_account is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .ROUTER_ACCOUNT_NOT_FOUND,

                )

            )

        if not cast(

            bool,

            router_account.is_enabled,

        ):

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .ROUTER_ACCOUNT_DISABLED,

                    router_account=router_account,

                )

            )

        customer = (

            router_account.customer

        )

        if customer is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .CUSTOMER_NOT_FOUND,

                    router_account=router_account,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                customer=customer,

                router_account=router_account,

            )

        )

    @staticmethod
    def _validate_customer(
        router_account: RouterAccount,
    ) -> PortalAuthenticationResultSchema:

        customer = router_account.customer

        if customer is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .CUSTOMER_NOT_FOUND,

                    router_account=router_account,

                )

            )

        if customer.status != CustomerStatus.ACTIVE:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .CUSTOMER_DISABLED,

                    router_account=router_account,

                    customer=customer,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=router_account,

                customer=customer,

            )

        )

    @staticmethod
    def _validate_password(
        password: str,
        router_account: RouterAccount,
    ) -> PortalAuthenticationResultSchema:

        stored_password = (

            RouterCredentialManager

            .decrypt(
                
                cast(
                    
                    str,

                router_account.encrypted_password,
                ),
                
            )

        )

        if password != stored_password:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError.INVALID_PASSWORD,

                    router_account=router_account,

                    customer=router_account.customer,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=router_account,

                customer=router_account.customer,

            )

        )

    @staticmethod
    def _validate_subscription(
        db: Session,
        result: PortalAuthenticationResultSchema,
    ) -> PortalAuthenticationResultSchema:

        customer = result.customer

        if customer is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .CUSTOMER_NOT_FOUND,

                    router_account=result.router_account,

                )

            )

        subscription = (

            db.query(
                Subscription,
            )

            .filter(

                Subscription.customer_id
                == customer.customer_id,

                Subscription.status
                == SubscriptionStatus.ACTIVE,

            )

            .first()

        )

        if subscription is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .NO_ACTIVE_SUBSCRIPTION,

                    router_account=result.router_account,

                    customer=result.customer,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=result.router_account,

                customer=result.customer,

                subscription=subscription,

            )

        )

    @staticmethod
    def _validate_plan(
        result: PortalAuthenticationResultSchema,
    ) -> PortalAuthenticationResultSchema:

        subscription = result.subscription

        if subscription is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .NO_ACTIVE_SUBSCRIPTION,

                    router_account=result.router_account,

                    customer=result.customer,

                )

            )

        plan = subscription.plan

        if plan is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .PLAN_INACTIVE,

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=subscription,

                    plan=plan,

                )

            )

        if plan.is_active is False:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .PLAN_INACTIVE,

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=subscription,
                    
                    plan=plan,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=result.router_account,

                customer=result.customer,

                subscription=subscription,

                plan=plan,

            )

        )

    @staticmethod
    def _validate_device(
        db: Session,
        result: PortalAuthenticationResultSchema,
        mac_address: str | None,
    ) -> PortalAuthenticationResultSchema:

        if mac_address is None:

            return (

                PortalAuthenticationService

                ._success(

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=result.subscription,

                    plan=result.plan,

                )

            )

        device = (

            DeviceService

            .find_by_mac_address(

                db,

                mac_address,

            )

        )

        if device is None:

            return (

                PortalAuthenticationService

                ._success(

                    router_account=result.router_account,

                    customer=result.customer,

                    subscription=result.subscription,

                    plan=result.plan,

                )

            )

        customer = result.customer

        if customer is None:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .CUSTOMER_NOT_FOUND,

                )

            )

        if device.customer_id != customer.customer_id:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .DEVICE_OWNERSHIP_MISMATCH,

                    router_account=result.router_account,

                    customer=customer,

                    subscription=result.subscription,

                    plan=result.plan,

                    device=device,

                )

            )

        status = device.device_status

        if status == DeviceStatus.BLOCKED:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .DEVICE_BLOCKED,

                    router_account=result.router_account,

                    customer=customer,

                    subscription=result.subscription,

                    plan=result.plan,

                    device=device,

                )

            )

        if status == DeviceStatus.INACTIVE:

            return (

                PortalAuthenticationService

                ._failure(

                    PortalAuthenticationError
                    .DEVICE_INACTIVE,

                    router_account=result.router_account,

                    customer=customer,

                    subscription=result.subscription,

                    plan=result.plan,

                    device=device,

                )

            )

        return (

            PortalAuthenticationService

            ._success(

                router_account=result.router_account,

                customer=customer,

                subscription=result.subscription,

                plan=result.plan,

                device=device,

            )

        )