import os
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from pandas import DataFrame, read_pickle

from config import settings
from transactions.domain.models import Transaction
from transactions.services.unit_of_work.pandas_unit_of_work import PandasUnitOfWork


@pytest.mark.unit
class TestPandasUnitOfWork:
    """Unit tests for the SqlAlchemyUnitOfWork class."""

    @pytest.fixture
    def temp_path(self):
        temp_path = mkdtemp()
        yield temp_path
        rmtree(temp_path)

    def test_committed_unit_of_work(self, temp_path):
        """Unit of work should be committed, close the session and rollback the not commit changes."""

        with PandasUnitOfWork(base_path=temp_path) as uow:
            uow.transactions.add(
                Transaction(account="68100000", amount=10, date=datetime(2020, 8, 15))
            )
            uow.commit()

        assert os.path.exists(os.path.join(temp_path, settings.pandas.file))

    def test_not_committed_unit_of_work(self, temp_path):
        """Unit of work should be rollback, close the session and rollback when no commit executed."""
        with PandasUnitOfWork(base_path=temp_path) as uow:
            uow.transactions.add(
                Transaction(account="68100000", amount=10, date=datetime(2020, 8, 15))
            )

        assert not os.path.exists(os.path.join(temp_path, settings.pandas.file))

    def test_load_existing_transactions_dataframe(self, temp_path):
        """Unit of work should load existing transactions dataframe."""
        transactions_file = os.path.join(temp_path, settings.pandas.file)
        transaction_dataframe = DataFrame.from_dict(
            dict(account=["68100000"], amount=[10.0], date=[datetime(2020, 8, 15)])
        )
        transaction_dataframe.to_pickle(transactions_file)

        with PandasUnitOfWork(base_path=temp_path) as uow:
            uow.transactions.add(
                Transaction(
                    account="100000000", amount=20.0, date=datetime(2020, 9, 15)
                )
            )
            uow.commit()

        edited_transaction_dataframe = read_pickle(transactions_file)
        assert edited_transaction_dataframe.shape == (2, 3)
