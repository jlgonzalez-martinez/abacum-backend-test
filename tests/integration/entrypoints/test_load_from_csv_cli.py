import os
from datetime import datetime

import pytest
from click.testing import CliRunner

from config import TEST_RESOURCES, settings
from transactions.domain.models import Transaction
from transactions.entrypoints.cli_application import load_transactions_from_csv
from transactions.services.unit_of_work.unit_of_work_factory import UnitOfWorkFactory


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("clean_pandas_file")
@pytest.mark.integration
class TestLoadFromCSVCLI:
    """Test the load_from_csv CLI command."""

    @pytest.fixture(scope="class")
    def csv_path(self):
        return os.path.join(TEST_RESOURCES, "data.csv")

    @pytest.fixture(scope="class")
    def runner(self):
        return CliRunner()

    @pytest.mark.parametrize("backend", ["sqlalchemy", "pandas"])
    def test_load_from_csv_cli(self, csv_path, runner, backend):
        """Test the load_from_csv CLI command load correctly a CSV file."""
        settings.backend = backend

        result = runner.invoke(load_transactions_from_csv, [csv_path])
        expected = [
            Transaction(
                date=datetime(2020, 8, 15), account="68100000", amount=-60512.99
            ),
            Transaction(
                date=datetime(2020, 10, 26), account="52000012", amount=176450.62
            ),
        ]
        with UnitOfWorkFactory.from_config() as uow:
            assert all(
                transaction in expected for transaction in uow.transactions.all()
            )
        assert result.exit_code == 0
