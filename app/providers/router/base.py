from abc import ABC
from abc import abstractmethod

from app.domain import (
    RouterContext,
    RouterHealth,
)

from app.models.router import Router


class RouterProvider(ABC):

    # ==========================================================
    # Customer Synchronization
    # ==========================================================

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