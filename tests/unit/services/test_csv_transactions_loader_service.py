import os
from datetime import datetime
from typing import List
from unittest.mock import MagicMock

import pytest

from config import TEST_RESOURCES
from tests.unit.fakes.fake_unit_of_work import FakeUnitOfWork
from transactions.domain.commands import LoadTransactionsFromCSV
from transactions.domain.models import Transaction
from transactions.services.load_from_csv import CsvTransactionsLoaderService


@pytest.mark.unit
class TestCsvTransactionsLoaderService:
    @pytest.fixture
    def logger(self):
        return MagicMock()

    @pytest.fixture
    def unit_of_work(self) -> FakeUnitOfWork:
        return FakeUnitOfWork()

    @pytest.fixture
    def service(self, logger, unit_of_work) -> CsvTransactionsLoaderService:
        return CsvTransactionsLoaderService(logger, unit_of_work)

    @pytest.fixture(scope="class")
    def csv_content(self) -> List[str]:
        with open(os.path.join(TEST_RESOURCES, "data.csv"), "r") as f:
            return f.readlines()

    def test_load_transactions_from_csv(self, csv_content, service, unit_of_work):
        """Test that loading transactions from a csv file persists the transactions."""
        service(LoadTransactionsFromCSV(csv_content=csv_content))

        expected = [
            Transaction(
                date=datetime(2020, 8, 15), account="68100000", amount=-60512.99
            ),
            Transaction(
                date=datetime(2020, 10, 26), account="52000012", amount=176450.62
            ),
        ]
        assert unit_of_work.committed
        assert all(
            transaction in expected for transaction in unit_of_work.transactions.all()
        )
