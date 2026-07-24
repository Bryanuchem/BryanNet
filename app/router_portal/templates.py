from pathlib import Path

from fastapi.templating import (
    Jinja2Templates,
)


# ==========================================================
# Template Directory
# ==========================================================

TEMPLATE_DIRECTORY = (
    Path(__file__)
    .resolve()
    .parent
    / "templates"
)


# ==========================================================
# Jinja Environment
# ==========================================================

templates = Jinja2Templates(
    directory=str(
        TEMPLATE_DIRECTORY
    ),
)


# ==========================================================
# Globals
# ==========================================================

templates.env.globals.update(

    zip=zip,

    enumerate=enumerate,

    len=len,

    min=min,

    max=max,

)


# ==========================================================
# Filters
# ==========================================================

def yes_no(
    value: bool,
) -> str:

    return (
        "Yes"
        if value
        else "No"
    )


templates.env.filters[
    "yes_no"
] = yes_no