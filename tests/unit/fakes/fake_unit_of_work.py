from typing import TYPE_CHECKING, List

from transactions.adapters.repositories import TransactionAbstractRepository
from transactions.services.unit_of_work import AbstractUnitOfWork

if TYPE_CHECKING:
    from transactions.domain.models import Transaction


class FakeTransactionRepository(TransactionAbstractRepository):
    """In memory Transaction Repository"""

    def __init__(self, transactions):
        super().__init__()
        self._transactions = set(transactions)

    def add(self, transaction: "Transaction"):
        self._transactions.add(transaction)

    def all(self) -> List["Transaction"]:
        return list(self._transactions)


class FakeUnitOfWork(AbstractUnitOfWork):
    """In memory Unit of Work"""

    def __init__(self):
        super().__init__()
        self.transactions = FakeTransactionRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
