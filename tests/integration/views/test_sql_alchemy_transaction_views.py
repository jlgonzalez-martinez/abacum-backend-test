from datetime import datetime

import pytest

from transactions.domain.models import Transaction
from transactions.views.sqlalchemy_transaction_views import SqlAlchemyTransactionViews


@pytest.mark.integration
class TestSqlAlchemyTransactionViews:
    """Test the SqlAlchemyTransactionViews."""

    @pytest.fixture(autouse=True)
    def add_test_transactions(self, db_session, mappers):
        """"""
        db_session.begin()

        db_session.add(
            Transaction(date=datetime(2020, 8, 15), account="68100000", amount=10)
        )
        db_session.add(
            Transaction(date=datetime(2020, 9, 20), account="68100000", amount=-5)
        )
        db_session.add(
            Transaction(date=datetime(2020, 9, 10), account="68100000", amount=20)
        )
        db_session.add(
            Transaction(date=datetime(2020, 10, 26), account="52000012", amount=10)
        )
        db_session.add(
            Transaction(date=datetime(2020, 9, 5), account="52000012", amount=6)
        )
        db_session.commit()
        yield
        db_session.query(Transaction).delete()
        db_session.commit()

    @pytest.fixture(scope="class")
    def transaction_views(self) -> SqlAlchemyTransactionViews:
        """Return a SqlAlchemyTransactionViews instance."""
        return SqlAlchemyTransactionViews()

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
            ("52000012", "2020-9", 6.0),
            ("52000012", "2020-10", 10.0),
            ("68100000", "2020-8", 10.0),
            ("68100000", "2020-9", 15.0),
        ]

    def test_group_by_account_and_month_specific_account(self, transaction_views):
        """Test the monthly_balance endpoint."""
        result = transaction_views.group_by_account_and_month(account="68100000")

        assert result == [
            ("68100000", "2020-8", 10.0),
            ("68100000", "2020-9", 15.0),
        ]

    def test_monthly_balance_specific_account_and_month(self, transaction_views):
        result = transaction_views.group_by_account_and_month(
            account="68100000", month=9
        )

        assert result == [
            ("68100000", "2020-9", 15.0),
        ]

    def test_monthly_balance_specific_month(self, transaction_views):

        result = transaction_views.group_by_account_and_month(month=9)

        assert result == [
            ("52000012", "2020-9", 6.0),
            ("68100000", "2020-9", 15.0),
        ]
