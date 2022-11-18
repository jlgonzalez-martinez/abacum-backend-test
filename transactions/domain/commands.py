"""Commands module, this module contains all the transaction commands."""
from dataclasses import dataclass
from typing import Union


class Command:
    """Command base class"""

    pass


@dataclass
class LoadTransactionsFromCSV(Command):
    """Load command"""

    csv_file: Union[str, bytearray]
