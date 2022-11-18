from abc import ABC, abstractmethod
from typing import Optional

from transactions.adapters.repositories import (
    TransactionAbstractRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work"""

    def __init__(self):
        self.transactions: Optional["TransactionAbstractRepository"] = None
        self.engine = None

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        """Commit changes to the database."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        """Rollback changes to the database."""
        raise NotImplementedError
