import logging

logger = logging.getLogger(__name__)


def log_login_attempt(email, success):
    logger.info(
        "Login attempt",
        extra={
            "email": email,
            "success": success,
        },
    )