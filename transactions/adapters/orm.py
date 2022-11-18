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
from sqlalchemy.orm import mapper

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
    mapper(Transaction, transactions)
