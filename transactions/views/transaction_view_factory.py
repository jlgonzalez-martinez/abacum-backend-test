from enum import Enum
from typing import TYPE_CHECKING

from config import settings
from transactions.views.pandas_transaction_views import PandasTransactionViews
from transactions.views.sqlalchemy_transaction_views import SqlAlchemyTransactionViews

if TYPE_CHECKING:
    from transactions.views.abstract_transaction_views import AbstractTransactionViews


class TransactionViewFactory(Enum):
    """Transaction view factory."""

    SQLALCHEMY = SqlAlchemyTransactionViews
    PANDAS = PandasTransactionViews

    @classmethod
    def from_config(cls) -> "AbstractTransactionViews":
        """Get a transaction view factory."""
        return cls[settings.backend.upper()].value()
