"""CLI application entrypoint."""
import logging

import click

from transactions.bootstrap import bootstrap
from transactions.domain.commands import LoadTransactionsFromCSV

logger = logging.getLogger(__name__)

bus = bootstrap()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def load_transactions_from_csv(filename):
    """Load transactions from a CSV file."""
    bus.handle(LoadTransactionsFromCSV(filename))


if __name__ == "__main__":
    load_transactions_from_csv()
