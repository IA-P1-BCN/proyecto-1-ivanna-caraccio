import logging

from application.validate_access import ValidateAccess
from domain.password import hash_password
from infrastructure.logging_config import SensitiveDataFilter, register_sensitive_value

PASSWORD = "taxi123-test"


def build_validate_access(password=PASSWORD):
    return ValidateAccess(hash_password(password))


def test_valid_password_grants_access():
    validate = build_validate_access()

    assert validate.execute(PASSWORD) is True


def test_wrong_password_denies_access():
    validate = build_validate_access()

    assert validate.execute("otra-clave") is False


def test_registered_password_is_masked_in_logs(caplog):
    register_sensitive_value(PASSWORD)
    caplog.handler.addFilter(SensitiveDataFilter())

    logging.getLogger("test.auth").warning("Password tried: %s", PASSWORD)

    assert PASSWORD not in caplog.text
    assert "***" in caplog.text
