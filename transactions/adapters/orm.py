"""Transaction orm for SqlAlchemy."""
import logging

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import mapper, class_mapper
from sqlalchemy.orm.exc import UnmappedError

from transactions.domain.models import Transaction

logger = logging.getLogger(__name__)

metadata = MetaData()


transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", DateTime, nullable=False),
    Column("account", String, nullable=False),
    Column("amount", Float, nullable=False),
)


def start_mappers():
    """Start ORM mappers with the domain model classes."""
    logger.info("Starting ORM mappers")
    if not exist_mapper(Transaction):
        mapper(Transaction, transactions)


def exist_mapper(klass) -> bool:
    """Check if the ORM mappers have been started."""
    try:
        class_mapper(klass)
        return True
    except UnmappedError:
        return False
