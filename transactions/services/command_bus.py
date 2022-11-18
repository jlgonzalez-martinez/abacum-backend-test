import logging
from typing import Callable, Dict, Type

from ..domain.commands import Command

logger = logging.getLogger(__name__)


class CommandBus:
    """Bus for handling commands."""

    def __init__(
        self,
        command_handlers: Dict[Type[Command], Callable],
    ):
        self.command_handlers = command_handlers

    def handle(self, command: Command):
        """Handle message in the bus."""
        self.handle_command(command)

    def handle_command(self, command: Command):
        """Handle a command by passing it to the appropriate handler."""
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
        except Exception:
            logger.exception(f"Exception handling command {command}", exc_info=True)
            raise
