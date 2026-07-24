from abc import ABC
from abc import abstractmethod

from app.domain import (
    RouterContext,
    RouterHealth,
)

from app.models.router import Router

from typing import Any



class RouterProvider(ABC):

    # ==========================================================
    # Customer Synchronization
    # ==========================================================

    connection: Any

    hotspot: Any

    sessions: Any

    @abstractmethod
    def synchronize_customer(
        self,
        db,
        context: RouterContext,
    ):
        """
        Synchronize the router so that the customer's
        access matches the supplied RouterContext.
        """
        pass

    @abstractmethod
    def disconnect_customer(
        self,
        db,
        context: RouterContext,
    ):
        """
        Immediately disconnect the customer's active
        session without modifying their subscription.
        """
        pass

    # ==========================================================
    # Bootstrap
    # ==========================================================

    def ensure_router_bootstrap(
        self,
        db,
        router,
    ):

        raise NotImplementedError(
            "Router bootstrap "
            "not implemented."
        )

    # ==========================================================
    # Router Health
    # ==========================================================

    @abstractmethod
    def health_check(
        self,
        router: Router,
    ) -> RouterHealth:
        """
        Check the health of a router.
        """
        pass