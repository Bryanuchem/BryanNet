from .script_builder import (
    build_daily_cleanup_script,
    build_login_error_script,
    build_login_script,
    build_logout_script,
)

# ==========================================================
# IMPORTANT
# ==========================================================
#
# The placeholders below are replaced during router
# bootstrap.
#
# ROUTER-001        -> router.router_identifier
# GENERATED_SECRET  -> router.router_secret
# __BN_API_URL__    -> Router Events endpoint
#
# Do not replace them manually.
#

LOGIN_SCRIPT = build_login_script()

LOGOUT_SCRIPT = build_logout_script()

LOGIN_ERROR_SCRIPT = build_login_error_script()

DAILY_CLEANUP_SCRIPT = build_daily_cleanup_script()

__all__ = [
    "LOGIN_SCRIPT",
    "LOGOUT_SCRIPT",
    "LOGIN_ERROR_SCRIPT",
    "DAILY_CLEANUP_SCRIPT",
]