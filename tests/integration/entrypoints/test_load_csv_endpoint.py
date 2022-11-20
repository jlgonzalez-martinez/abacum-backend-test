import os
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from config import TEST_RESOURCES, settings
from transactions.bootstrap import bootstrap
from transactions.domain.models import Transaction
from transactions.entrypoints.fastapi_application import app
from transactions.services.unit_of_work.unit_of_work_factory import UnitOfWorkFactory


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("clean_pandas_file")
@pytest.mark.integration
class TestLoadCsvEndpoint:
    """Test the load_csv endpoint."""

    @pytest.fixture(scope="class")
    def client(self) -> TestClient:
        return TestClient(app)

    @pytest.fixture(scope="class")
    def csv_path(self) -> str:
        return os.path.join(TEST_RESOURCES, "data.csv")

    @pytest.mark.parametrize("backend", ["sqlalchemy", "pandas"])
    def test_load_csv_endpoint(self, client, csv_path, backend):
        """Test the load_csv endpoint load correctly a CSV file."""
        settings.backend = backend
        app.bus = bootstrap()

        response = client.post(
            "/transactions/load-csv", files={"file": open(csv_path, "rb")}
        )
        expected = [
            Transaction(
                date=datetime(2020, 8, 15), account="68100000", amount=-60512.99
            ),
            Transaction(
                date=datetime(2020, 10, 26), account="52000012", amount=176450.62
            ),
        ]
        assert response.status_code == 200
        with UnitOfWorkFactory.from_config() as uow:
            assert all(
                transaction in expected for transaction in uow.transactions.all()
            )
