from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from transactions.adapters.repositories import (
    TransactionSqlAlchemyRepository,
)
from config import settings
from .abstract_unit_of_work import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SqlAlchemy Unit of Work"""

    def __init__(self):
        super().__init__()
        self.engine = create_engine(
            f"postgresql://{settings.database.user}:{settings.database.password}"
            f"@{settings.database.host}:{settings.database.port}/{settings.database.database}",
            isolation_level="REPEATABLE READ",
        )
        self.session_factory = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.transactions = TransactionSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        """Commit SQL transaction."""
        self.session.commit()

    def rollback(self):
        """Rollback SQL transaction."""
        self.session.rollback()
