"""Commands module, this module contains all the transaction commands."""
from dataclasses import dataclass
from typing import List


class Command:
    """Command base class"""

    pass


@dataclass
class LoadTransactionsFromCSV(Command):
    """Load command"""

    csv_content: List[str]
