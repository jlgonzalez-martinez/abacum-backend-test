from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, List

from transactions.domain.models import Transaction

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class TransactionAbstractRepository(ABC):
    """Transaction Abstract Repository"""

    def __init__(self):
        self.seen = set()  # type: Set["Transaction"]

    @abstractmethod
    def add(self, transaction: "Transaction"):
        """Add a transaction to the repository"""
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List["Transaction"]:
        """Get all transactions."""
        raise NotImplementedError


class TransactionSqlAlchemyRepository(TransactionAbstractRepository):
    """Transaction SQLAlchemy Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def add(self, transaction: "Transaction"):
        """Add a transaction to the repository"""
        self._session.add(transaction)

    def all(self) -> List["Transaction"]:
        """Get all transactions."""
        return self._session.query(Transaction).all()
