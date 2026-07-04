from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

from fastapi.exceptions import (
    RequestValidationError,
)

from fastapi.responses import (
    JSONResponse,
)

from app.core.logging import (
    get_logger,
)


logger = get_logger(
    __name__,
)


def register_exception_handlers(
    app: FastAPI,
):

    # ==========================================================
    # HTTP Exceptions
    # ==========================================================

    @app.exception_handler(
        HTTPException,
    )
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):

        logger.warning(
            "%s %s -> %s: %s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.detail,
        )

        return JSONResponse(

            status_code=exc.status_code,

            content={

                "success": False,

                "message": exc.detail,

            },

        )

    # ==========================================================
    # Validation Exceptions
    # ==========================================================

    @app.exception_handler(
        RequestValidationError,
    )
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):

        logger.warning(
            "%s %s -> Validation failed: %s",
            request.method,
            request.url.path,
            exc.errors(),
        )

        return JSONResponse(

            status_code=422,

            content={

                "success": False,

                "message": "Validation failed.",

                "errors": exc.errors(),

            },

        )

    # ==========================================================
    # Unhandled Exceptions
    # ==========================================================

    @app.exception_handler(
        Exception,
    )
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):

        logger.exception(
            "%s %s -> Unexpected exception.",
            request.method,
            request.url.path,
        )

        return JSONResponse(

            status_code=500,

            content={

                "success": False,

                "message": (
                    "An unexpected error occurred."
                ),

            },

        )