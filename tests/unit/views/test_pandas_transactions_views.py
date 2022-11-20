from datetime import datetime
from os.path import join
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from pandas import DataFrame

from config import settings
from transactions.views.pandas_transaction_views import PandasTransactionViews


@pytest.mark.unit
class TestPandasTransactionsViews:
    """Unit tests for the PandasTransactionViews class."""

    @pytest.fixture
    def temp_path(self):
        temp_path = mkdtemp()
        yield temp_path
        rmtree(temp_path)

    @pytest.fixture(autouse=True)
    def transaction_df(self, temp_path):
        dataframe = DataFrame(
            data=dict(
                account=["68100000", "68100000", "68100000", "52000012", "52000012"],
                amount=[10, -5, 20, 10, 6],
                date=[
                    datetime(2020, 8, 15),
                    datetime(2020, 9, 20),
                    datetime(2020, 9, 10),
                    datetime(2020, 10, 26),
                    datetime(2020, 9, 5),
                ],
            )
        )
        dataframe.to_pickle(join(temp_path, settings.pandas.file))

    @pytest.fixture
    def transaction_views(self, temp_path, transaction_df):
        return PandasTransactionViews(base_path=temp_path)

    def test_group_by_account(self, transaction_views):
        result = transaction_views.group_by_account()

        assert result == [
            ("52000012", 16.0),
            ("68100000", 25.0),
        ]

    def test_group_by_account_for_specific_account(self, transaction_views):
        result = transaction_views.group_by_account(account="68100000")

        assert result == [("68100000", 25.0)]

    def test_group_by_account_and_month(self, transaction_views):

        result = transaction_views.group_by_account_and_month()

        assert result == [
            ("52000012", "2020-09", 6.0),
            ("52000012", "2020-10", 10.0),
            ("68100000", "2020-08", 10.0),
            ("68100000", "2020-09", 15.0),
        ]

    def test_group_by_account_and_month_specific_account(self, transaction_views):
        """Test the monthly_balance endpoint."""
        result = transaction_views.group_by_account_and_month(account="68100000")

        assert result == [
            ("68100000", "2020-08", 10.0),
            ("68100000", "2020-09", 15.0),
        ]

    def test_monthly_balance_specific_account_and_month(self, transaction_views):
        result = transaction_views.group_by_account_and_month(
            account="68100000", month=9
        )

        assert result == [
            ("68100000", "2020-09", 15.0),
        ]

    def test_monthly_balance_specific_month(self, transaction_views):

        result = transaction_views.group_by_account_and_month(month=9)

        assert result == [
            ("52000012", "2020-09", 6.0),
            ("68100000", "2020-09", 15.0),
        ]
