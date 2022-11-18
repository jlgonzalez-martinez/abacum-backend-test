from unittest.mock import patch, MagicMock

import pytest

from transactions.services.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.unit
@patch("transactions.services.unit_of_work.sqlalchemy_unit_of_work.create_engine")
@patch("transactions.services.unit_of_work.sqlalchemy_unit_of_work.sessionmaker")
class TestSqlAlchemyUnitOfWork:
    """Unit tests for the SqlAlchemyUnitOfWork class."""

    @pytest.fixture
    def session_mock(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def engine_mock(self) -> MagicMock:
        return MagicMock()

    def test_commited_unit_of_work(
        self, sessionmaker_mock, create_engine_mock, session_mock, engine_mock
    ):
        """Unit of work should be committed, close the session and rollback the not commit changes."""
        sessionmaker_mock.return_value = MagicMock(return_value=session_mock)
        create_engine_mock.return_value = engine_mock

        with SqlAlchemyUnitOfWork() as uow:
            uow.commit()

        session_mock.commit.assert_called_once()
        session_mock.close.assert_called_once()
        session_mock.rollback.assert_called_once()

    def test_rollbacked_unit_of_work(
        self, sessionmaker_mock, create_engine_mock, session_mock, engine_mock
    ):
        """Unit of work should be rollback, close the session and rollback when no commit executed."""
        sessionmaker_mock.return_value = MagicMock(return_value=session_mock)
        create_engine_mock.return_value = engine_mock

        with SqlAlchemyUnitOfWork():
            pass

        assert not session_mock.commit.called
        session_mock.close.assert_called_once()
        session_mock.rollback.assert_called_once()
