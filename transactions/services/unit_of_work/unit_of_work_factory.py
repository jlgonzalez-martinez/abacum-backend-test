from enum import Enum
from typing import TYPE_CHECKING

from config import settings
from transactions.services.unit_of_work import SqlAlchemyUnitOfWork
from transactions.services.unit_of_work.pandas_unit_of_work import PandasUnitOfWork

if TYPE_CHECKING:
    from transactions.services.unit_of_work import AbstractUnitOfWork


class UnitOfWorkFactory(Enum):
    """Transaction view factory."""

    SQLALCHEMY = SqlAlchemyUnitOfWork
    PANDAS = PandasUnitOfWork

    @classmethod
    def from_config(cls) -> "AbstractUnitOfWork":
        """Get a transaction view factory."""
        return cls[settings.backend.upper()].value()
