import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    clear_mappers,
    scoped_session,
    close_all_sessions,
)
from sqlalchemy_utils import database_exists, create_database, drop_database
from tenacity import retry, stop_after_delay

from config import settings
from transactions.adapters.orm import metadata, start_mappers


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@pytest.fixture(scope="session")
def postgres_db():

    postgres_url = (
        f"postgresql://{settings.database.user}:{settings.database.password}"
        f"@{settings.database.host}:{settings.database.port}/{settings.database.database}"
    )
    if not database_exists(postgres_url):
        create_database(postgres_url)
    engine = create_engine(postgres_url, isolation_level="SERIALIZABLE")
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    yield engine
    close_all_sessions()
    metadata.drop_all(engine)
    drop_database(postgres_url)


@pytest.fixture
def db_session(postgres_db):
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=postgres_db)
    )
    session.execute("DELETE FROM transactions")
    session.commit()
    yield session
    session.close()
