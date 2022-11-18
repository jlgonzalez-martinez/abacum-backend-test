from unittest.mock import MagicMock

import pytest

from transactions.services.command_bus import CommandBus
from tests.unit.fakes.fake_command import TestCommand


@pytest.mark.unit
class TestCommandBus:
    """Unit tests for the CommandBus class."""

    @pytest.fixture(scope="class")
    def service(self):
        """Fixture for a service mock."""
        return MagicMock()

    @pytest.fixture(scope="class")
    def handlers(self, service) -> dict:
        return {TestCommand: service}

    def test_handle_command(self, service, handlers):
        command = TestCommand(test_attribute=1)
        command_bus = CommandBus(handlers)

        command_bus.handle_command(command)

        service.assert_called_once_with(command)

    def test_handle_command_without_handler(self, service):
        command = TestCommand(test_attribute=1)
        command_bus = CommandBus({})

        with pytest.raises(KeyError):
            command_bus.handle_command(command)
