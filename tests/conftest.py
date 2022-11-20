import pytest

from config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing", ENVVAR_FOR_DYNACONF="ABACUM")
