import logging

from app.core.settings import settings


# ==========================================================
# Logging Configuration
# ==========================================================

logging.basicConfig(

    level=(
        logging.DEBUG
        if settings.debug
        else logging.INFO
    ),

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

)


logger = logging.getLogger(
    "bryannet",
)


# ==========================================================
# Helper
# ==========================================================

def get_logger(
    name: str,
):

    return logger.getChild(
        name,
    )