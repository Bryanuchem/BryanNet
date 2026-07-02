from datetime import datetime

from fastapi import HTTPException

from app.domain import RouterContext

from app.models.virtual_router_account import (
    VirtualRouterAccount,
)

from app.enums import SubscriptionStatus

class VirtualRouterAccountService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_virtual_account(
        db,
        virtual_router_account_id,
    ):

        virtual_account = (
            db.query(VirtualRouterAccount)
            .filter(
                VirtualRouterAccount.virtual_router_account_id
                == virtual_router_account_id
            )
            .first()
        )

        if not virtual_account:

            raise HTTPException(
                status_code=404,
                detail="Virtual router account not found.",
            )

        return virtual_account

    @staticmethod
    def _find_by_router_account(
        db,
        router_account_id,
    ):

        return (
            db.query(VirtualRouterAccount)
            .filter(
                VirtualRouterAccount.router_account_id
                == router_account_id
            )
            .first()
        )

    @staticmethod
    def _approved_device_count(
        context: RouterContext,
    ):

        return len(

            [

                device

                for device in context.devices

                if device.device_status.value
                == "approved"

            ]

        )

    @staticmethod
    def _apply_context(
        virtual_account,
        context: RouterContext,
    ):

        virtual_account.router_id = (
            context.router.router_id
        )

        virtual_account.router_account_id = (
            context.router_account.router_account_id
        )

        virtual_account.username = (
            context.router_account.username
        )

        virtual_account.enabled = (
            context.subscription.status
            == SubscriptionStatus.ACTIVE
        )

        virtual_account.speed_limit_mbps = (
            context.plan.speed_limit_mbps
        )

        virtual_account.max_devices = (
            context.plan.max_devices
        )

        virtual_account.concurrent_devices = (
            context.plan.concurrent_devices
        )

        virtual_account.approved_device_count = (

            VirtualRouterAccountService
            ._approved_device_count(
                context,
            )

        )

        virtual_account.last_synchronized_at = (
            datetime.utcnow()
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_virtual_account(
        db,
        context: RouterContext,
    ):

        virtual_account = VirtualRouterAccount(

            connected=False,

        )

        VirtualRouterAccountService._apply_context(

            virtual_account,

            context,

        )

        db.add(
            virtual_account,
        )

        db.commit()

        db.refresh(
            virtual_account,
        )

        return virtual_account

    @staticmethod
    def synchronize_virtual_account(
        db,
        context: RouterContext,
    ):

        virtual_account = (

            VirtualRouterAccountService
            ._find_by_router_account(

                db,

                context.router_account.router_account_id,

            )

        )

        if not virtual_account:

            return (

                VirtualRouterAccountService
                .create_virtual_account(

                    db,

                    context,

                )

            )

        VirtualRouterAccountService._apply_context(

            virtual_account,

            context,

        )

        db.commit()

        db.refresh(
            virtual_account,
        )

        return virtual_account

    @staticmethod
    def set_connection_status(
        db,
        router_account_id,
        connected,
    ):

        virtual_account = (

            VirtualRouterAccountService
            ._find_by_router_account(

                db,

                router_account_id,

            )

        )

        if not virtual_account:

            raise HTTPException(
                status_code=404,
                detail="Virtual router account not found.",
            )

        virtual_account.connected = connected

        db.commit()

        db.refresh(
            virtual_account,
        )

        return virtual_account

    @staticmethod
    def delete_virtual_account(
        db,
        router_account_id,
    ):

        virtual_account = (

            VirtualRouterAccountService
            ._find_by_router_account(

                db,

                router_account_id,

            )

        )

        if not virtual_account:

            raise HTTPException(
                status_code=404,
                detail="Virtual router account not found.",
            )

        db.delete(
            virtual_account,
        )

        db.commit()

        return {

            "message":
                "Virtual router account deleted successfully."

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_virtual_account(
        db,
        virtual_router_account_id,
    ):

        return (

            VirtualRouterAccountService
            ._find_virtual_account(

                db,

                virtual_router_account_id,

            )

        )

    @staticmethod
    def get_virtual_account_by_router_account(
        db,
        router_account_id,
    ):

        virtual_account = (

            VirtualRouterAccountService
            ._find_by_router_account(

                db,

                router_account_id,

            )

        )

        if not virtual_account:

            raise HTTPException(
                status_code=404,
                detail="Virtual router account not found.",
            )

        return virtual_account

    @staticmethod
    def get_all_virtual_accounts(
        db,
    ):

        return (

            db.query(
                VirtualRouterAccount,
            )

            .order_by(
                VirtualRouterAccount.updated_at.desc(),
            )

            .all()

        )