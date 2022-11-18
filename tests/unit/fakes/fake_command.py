from dataclasses import dataclass

from transactions.domain.commands import Command


@dataclass
class TestCommand(Command):
    """Test command class"""

    test_attribute: int
