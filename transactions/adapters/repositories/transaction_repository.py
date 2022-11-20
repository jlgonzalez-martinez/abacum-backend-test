from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, List
from pandas import Series, concat

from transactions.domain.models import Transaction

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from pandas import DataFrame


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


class TransactionPandasRepository(TransactionAbstractRepository):
    """Transaction Pandas Repository"""

    def __init__(self, df: "DataFrame"):
        super().__init__()
        self.dataframe = df

    def add(self, transaction: "Transaction"):
        """Add a transaction to the repository"""
        new_row = Series(
            dict(
                account=transaction.account,
                amount=transaction.amount,
                date=transaction.date,
            )
        )
        self.dataframe = concat(
            [self.dataframe, new_row.to_frame().T], ignore_index=True
        )

    def all(self) -> List["Transaction"]:
        """Get all transactions."""
        return [
            Transaction(
                date=record["date"], amount=record["amount"], account=record["account"]
            )
            for record in self.dataframe.to_dict(orient="records")
        ]
