import logging
from typing import TYPE_CHECKING

from transactions.adapters import orm
from transactions.domain.commands import LoadTransactionsFromCSV
from transactions.services.command_bus import CommandBus
from transactions.services.load_from_csv import CsvTransactionsLoaderService
from transactions.services.unit_of_work.unit_of_work_factory import UnitOfWorkFactory
from transactions.services.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

if TYPE_CHECKING:
    from logging import Logger
    from transactions.services.unit_of_work import (
        AbstractUnitOfWork,
    )


def bootstrap(
    start_orm: bool = True,
    uow: "AbstractUnitOfWork" = None,
    logger: "Logger" = logging.getLogger(__name__),
) -> CommandBus:
    """Initialize the application dependencies."""
    if uow is None:
        uow = UnitOfWorkFactory.from_config()
    if start_orm and isinstance(uow, SqlAlchemyUnitOfWork):
        orm.start_mappers()
        orm.metadata.create_all(uow.engine)

    injected_command_handlers = {
        LoadTransactionsFromCSV: CsvTransactionsLoaderService(logger, uow)
    }
    return CommandBus(injected_command_handlers)
