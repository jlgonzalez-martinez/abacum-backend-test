from datetime import datetime

import pytest
from pandas import DataFrame
from transactions.adapters.repositories.transaction_repository import (
    TransactionPandasRepository,
)
from transactions.domain.models import Transaction


class TestTransactionPandasRepository:
    """Test the TransactionPandasRepository."""

    @pytest.fixture
    def dataframe(self):
        """Return a dataframe."""
        return DataFrame()

    @pytest.fixture
    def transactions_repository(self, dataframe):
        """Return a PandasTransactionsRepository instance."""
        return TransactionPandasRepository(dataframe)

    def test_add(self, transactions_repository):
        """Test add method add a new transaction."""
        transaction = Transaction(
            amount=4.0, account="68100000", date=datetime(2020, 8, 15)
        )

        transactions_repository.add(transaction)
        records, columns = transactions_repository.dataframe.shape

        assert records == 1
        assert columns == 3
        assert transactions_repository.dataframe.iloc[0].to_dict() == dict(
            account=transaction.account,
            amount=transaction.amount,
            date=transaction.date,
        )

    def test_all(self, transactions_repository):
        """Test all method return all the transactions."""
        transaction = Transaction(
            amount=4.0, account="68100000", date=datetime(2020, 8, 15)
        )
        other_transaction = Transaction(
            amount=8.0, account="100000", date=datetime(2020, 1, 15)
        )
        transactions_repository.add(transaction)
        transactions_repository.add(other_transaction)

        transactions = transactions_repository.all()

        assert transactions == [transaction, other_transaction]
