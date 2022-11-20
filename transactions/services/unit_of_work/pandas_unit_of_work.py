from os import path
from os.path import join

from pandas import read_pickle, DataFrame

from config import settings, RESOURCES
from .abstract_unit_of_work import AbstractUnitOfWork
from ...adapters.repositories.transaction_repository import TransactionPandasRepository


class PandasUnitOfWork(AbstractUnitOfWork):
    """SqlAlchemy Unit of Work"""

    def __init__(self, base_path: str = RESOURCES):
        super().__init__()
        self.path = join(base_path, settings.pandas.file)

    def __enter__(self):
        dataframe = read_pickle(self.path) if path.exists(self.path) else DataFrame()
        self.transactions = TransactionPandasRepository(dataframe)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit(self):
        """Commit SQL transaction."""
        self.transactions.dataframe.to_pickle(self.path)

    def rollback(self):
        """Rollback SQL transaction."""
        pass
