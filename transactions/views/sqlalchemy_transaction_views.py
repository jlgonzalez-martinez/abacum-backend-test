from typing import Optional, List

from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import sessionmaker

from config import settings
from transactions.domain.models import Transaction
from transactions.views.abstract_transaction_views import AbstractTransactionViews


class SqlAlchemyTransactionViews(AbstractTransactionViews):
    def __init__(self):
        self._engine = create_engine(
            f"postgresql://{settings.database.user}:{settings.database.password}"
            f"@{settings.database.host}:{settings.database.port}/{settings.database.database}",
            isolation_level="REPEATABLE READ",
        )
        self._session = sessionmaker(bind=self._engine)()

    def group_by_account(
        self,
        account: Optional[str] = None,
    ) -> List[tuple]:
        """Group transactions by account"""
        queryset = (
            self._session.query(Transaction.account, func.sum(Transaction.amount))
            .group_by(Transaction.account)
            .order_by(Transaction.account)
        )
        if account:
            queryset = queryset.filter(Transaction.account == account)
        return queryset.all()

    def group_by_account_and_month(
        self, account: Optional[str] = None, month: Optional[int] = None
    ) -> List[tuple]:
        """Group transactions by account and month"""
        queryset = (
            self._session.query(
                Transaction.account,
                func.concat(
                    extract("year", func.max(Transaction.date)),
                    "-",
                    extract("month", func.max(Transaction.date)),
                ).label("month_date"),
                func.sum(Transaction.amount),
            )
            .group_by(
                Transaction.account,
                extract("month", Transaction.date),
            )
            .order_by(
                Transaction.account,
                extract("month", Transaction.date),
            )
        )
        if account:
            queryset = queryset.filter(Transaction.account == account)
        if month:
            queryset = queryset.filter(extract("month", Transaction.date) == month)
        return queryset.all()
