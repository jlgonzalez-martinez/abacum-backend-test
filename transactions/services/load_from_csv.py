import csv
from datetime import datetime
from logging import Logger
from typing import TYPE_CHECKING

from transactions.domain.models import Transaction
from transactions.services.unit_of_work import AbstractUnitOfWork

if TYPE_CHECKING:
    from transactions.domain.commands import LoadTransactionsFromCSV


class CsvTransactionsLoaderService:
    """Load transactions from a CSV file."""

    def __init__(self, logger: Logger, uow: AbstractUnitOfWork):
        self._logger = logger
        self._uow = uow

    def __call__(self, cmd: "LoadTransactionsFromCSV"):
        with self._uow:
            csv_reader = csv.reader(cmd.csv_content, delimiter=",")
            _ = next(csv_reader)  # skip header
            for date, account, amount in csv_reader:
                date = datetime.strptime(date, "%Y-%m-%d")
                amount = float(amount)
                transaction = Transaction(date=date, account=account, amount=amount)
                self._uow.transactions.add(transaction)
            self._uow.commit()
