from os.path import join, exists
from typing import Optional, List

from pandas import read_pickle, DataFrame

from config import settings, RESOURCES
from transactions.views.abstract_transaction_views import AbstractTransactionViews


class PandasTransactionViews(AbstractTransactionViews):
    """Pandas Unit of Work"""

    def __init__(self, base_path: str = RESOURCES):
        super().__init__()
        path = join(base_path, settings.pandas.file)
        self.dataframe = read_pickle(path) if exists(path) else DataFrame()

    def group_by_account(
        self,
        account: Optional[str] = None,
    ) -> List[tuple]:
        """Group transactions by account"""
        if account:
            self.dataframe = self.dataframe[self.dataframe["account"] == account]

        grouped_df = self.dataframe.groupby("account", group_keys=False).agg(
            dict(amount=sum)
        )
        return [(account, amount) for account, amount in grouped_df.to_records()]

    def group_by_account_and_month(
        self, account: Optional[str] = None, month: Optional[int] = None
    ) -> List[tuple]:
        """Group transactions by account and month"""
        if account:
            self.dataframe = self.dataframe[self.dataframe["account"] == account]
        if month:
            self.dataframe = self.dataframe[self.dataframe["date"].dt.month == month]

        grouped_df = self.dataframe.groupby(
            ["account", self.dataframe.date.dt.month, self.dataframe.date.dt.year],
            group_keys=False,
            as_index=False,
        ).agg(dict(date=max, amount=sum))
        grouped_df["date"] = grouped_df["date"].dt.strftime("%Y-%m")
        grouped_df["amount"] = grouped_df["amount"].astype(float)
        return [
            (account, date, amount)
            for account, date, amount in grouped_df.to_records(index=False)
        ]
