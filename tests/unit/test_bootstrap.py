from unittest.mock import patch, MagicMock

import pytest

from tests.unit.fakes.fake_unit_of_work import FakeUnitOfWork
from transactions.bootstrap import bootstrap
from transactions.domain.commands import LoadTransactionsFromCSV
from transactions.services.command_bus import CommandBus
from transactions.services.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.unit
@patch("transactions.bootstrap.orm")
class TestBootstrap:
    """Unit tests for the application initialization."""

    @pytest.fixture(scope="class")
    def uow(self):
        return FakeUnitOfWork()

    def test_bootstrap_with_orm_and_sqlalchemy_uow(self, orm_mock):
        """Application should be initialized with the ORM."""
        sqlalchemy_uow = MagicMock(spec=SqlAlchemyUnitOfWork, engine=MagicMock())

        command_bus = bootstrap(start_orm=True, uow=sqlalchemy_uow)
        csv_loader_service = command_bus.command_handlers.get(
            LoadTransactionsFromCSV, None
        )

        assert isinstance(command_bus, CommandBus)
        assert csv_loader_service is not None
        assert csv_loader_service._uow == sqlalchemy_uow
        orm_mock.start_mappers.assert_called_once()
        orm_mock.metadata.create_all.assert_called_once_with(sqlalchemy_uow.engine)

    def test_bootstrap_with_orm_and_not_sqlalchemy_uow(self, orm_mock, uow):
        """Application should be initialized with the ORM."""
        command_bus = bootstrap(start_orm=True, uow=uow)
        csv_loader_service = command_bus.command_handlers.get(
            LoadTransactionsFromCSV, None
        )

        assert isinstance(command_bus, CommandBus)
        assert csv_loader_service is not None
        assert csv_loader_service._uow == uow
        assert not orm_mock.start_mappers.called
        assert not orm_mock.metadata.create_all.called

    def test_bootstrap_without_orm(self, orm_mock, uow):
        """Application should be initialized without the ORM."""

        command_bus = bootstrap(start_orm=False, uow=uow)
        csv_loader_service = command_bus.command_handlers.get(
            LoadTransactionsFromCSV, None
        )

        assert isinstance(command_bus, CommandBus)
        assert csv_loader_service is not None
        assert csv_loader_service._uow == uow
        assert not orm_mock.start_mappers.called
        assert not orm_mock.metadata.create_all.called
