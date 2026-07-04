from app.enums import RouterProviderType

from app.models.router import Router

from app.providers.router.base import RouterProvider

from app.providers.router.simulated import (
    SimulatedRouterProvider,
)

from app.providers.router.mikrotik_chr import (
    MikroTikCHRProvider,
)

from app.providers.router.mikrotik_physical import (
    MikroTikPhysicalProvider,
)


class ProviderFactory:

    @staticmethod
    def get(
        router: Router,
    ) -> RouterProvider:

        match router.router_type:

            case RouterProviderType.SIMULATED:

                return SimulatedRouterProvider()

            case RouterProviderType.MIKROTIK_CHR:

                return MikroTikCHRProvider()

            case RouterProviderType.MIKROTIK_PHYSICAL:

                return MikroTikPhysicalProvider()

            case _:

                raise ValueError(

                    f"Unsupported router type: "
                    f"{router.router_type}"

                )