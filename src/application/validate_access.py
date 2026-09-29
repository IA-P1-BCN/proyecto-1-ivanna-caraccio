import hmac

from domain.password import hash_password
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)


class ValidateAccess:
    def __init__(self, password_hash):
        self.password_hash = password_hash

    def execute(self, password):
        if not password:
            logger.warning("Access denied: empty password")
            return False

        granted = hmac.compare_digest(
            hash_password(password), self.password_hash
        )

        if granted:
            logger.info("Access granted")
        else:
            logger.warning("Access denied: wrong password")

        return granted
