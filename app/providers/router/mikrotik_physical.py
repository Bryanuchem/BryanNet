from app.providers.router.mikrotik_chr import (
    MikroTikCHRProvider,
)


class MikroTikPhysicalProvider(
    MikroTikCHRProvider,
):
    """
    Physical MikroTik routers currently share the
    exact same RouterOS implementation as CHR.

    This class exists so that physical routers can
    introduce hardware-specific behavior in the
    future without affecting the CHR provider.
    """

    pass