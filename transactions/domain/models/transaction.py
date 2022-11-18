from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Transaction class model."""

    date: datetime
    account: str
    amount: float

    def __hash__(self):
        return id(self)

    def __eq__(self, other: "Transaction"):
        return (
            self.date == other.date
            and self.account == other.account
            and self.amount == other.amount
        )
